"""Replay the exact reference recipe in two phases; never execute a target.

Host phase permits image comparison before the single candidate target relink.
Only fresh output-directory strings are substituted in the recorded commands.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[4]
PACKET = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(out, report):
    (out / 'build.json').write_text(json.dumps(report, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['host', 'link'])
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    reference = json.loads((PACKET / '00-reference/build.json').read_text())
    reference_output = reference['output']
    if args.phase == 'host':
        assert args.output is None
        out = ROOT / ('build/flight-demo/m2-interpolation-candidate-' + str(time.time_ns()))
        out.mkdir()
        inputs = {p: sha(ROOT / p) for p in reference['inputs']}
        differences = [p for p in inputs if inputs[p] != reference['inputs'][p]]
        assert differences == ['src/graphics/m2_geometry.c'], differences
        report = {'output': str(out), 'base': reference['base'], 'inputs': inputs,
                  'commands': [], 'target_executed': False,
                  'reference_build': reference_output, 'tool_hashes': reference['tool_hashes']}
        selected = reference['commands'][:3]
    else:
        assert args.output is not None
        out = args.output.resolve()
        report = json.loads((out / 'build.json').read_text())
        assert report['host'] == 'PASS' and report['image_comparison'] == 'PASS five byte-identical'
        assert len(report['commands']) == 3, 'candidate link already attempted'
        assert all(sha(ROOT / p) == h for p, h in report['inputs'].items())
        selected = reference['commands'][3:]
    save(out, report)
    for command in selected:
        argv = [p.replace(reference_output, str(out)) for p in command['argv']]
        started = time.monotonic()
        result = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True)
        (out / command['log']).write_text(result.stdout + result.stderr)
        report['commands'].append({'argv': argv, 'exit': result.returncode,
                                   'log': command['log'],
                                   'elapsed_seconds': time.monotonic() - started})
        save(out, report)
        if result.returncode:
            raise RuntimeError('check failed; retained log: ' + str(out / command['log']))
    if args.phase == 'host':
        for pose in range(5):
            name = 'pose-' + str(pose) + '.ppm'
            assert sha(out / name) == sha(PACKET / '00-reference' / name), name
        report.update(host='PASS', image_comparison='PASS five byte-identical')
        save(out, report)
        print(json.dumps({'output': str(out), 'host': report['host'],
                          'images': report['image_comparison']}), flush=True)
        return 0
    mapping = (out / 'RENDER.map').read_text()
    sections = {}
    for name in ['.text', '.rodata', '.data', '.bss', '.noinit']:
        match = re.search(r'^\s*([0-9a-f]+)\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+'
                          + re.escape(name) + '$', mapping, re.M)
        assert match, name
        start, size = [int(value, 16) for value in match.groups()]
        sections[name] = {'start': start, 'bytes': size}
    symbols = {}
    for line in (out / 'RENDER.symbols').read_text().splitlines():
        parts = line.split()
        if len(parts) == 4:
            symbols[parts[3]] = {'start': int(parts[0], 16),
                                  'bytes': int(parts[1], 16), 'kind': parts[2]}
    ledger = json.loads((ROOT / 'memory/m2-full-ledger.json').read_text())
    low, ceiling = ledger['resident']
    end = max(s['start'] + s['bytes'] for s in sections.values())
    fits = all(low <= s['start'] and s['start'] + s['bytes'] <= ceiling
               for s in sections.values())
    owners = {name: symbols[name] for name in reference['owners']}
    report.update(sections=sections, owners=owners, resident_end=end,
                  resident_bytes=end - low, ceiling=ceiling,
                  excess_bytes=max(0, end - ceiling),
                  early_renderer_fit='PASS intermediate only' if fits else 'FAIL',
                  target_sha256=sha(out / 'RENDER.prg'),
                  elf_sha256=sha(out / 'RENDER.prg.elf'), reserve_allocation=0,
                  interpolation=symbols['interpolate_delta'], shift_helper=symbols.get('__ashldi3'),
                  descriptor_tables={n: v for n, v in symbols.items()
                                     if n.startswith('m2_transform.')},
                  runtime_display_admission='NOT REACHED; no target execution')
    save(out, report)
    print(json.dumps({k: report[k] for k in ['output', 'interpolation', 'shift_helper', 'descriptor_tables',
                      'sections', 'resident_bytes', 'resident_end', 'excess_bytes',
                      'early_renderer_fit', 'target_sha256']}, indent=2), flush=True)
    return 0 if fits else 1


if __name__ == '__main__':
    raise SystemExit(main())
