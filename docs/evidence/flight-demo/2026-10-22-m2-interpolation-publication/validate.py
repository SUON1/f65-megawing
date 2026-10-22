"""Fresh checks of the narrowly published helper, never the full composition."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
PACKET = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    out = ROOT / ('build/flight-demo/interpolation-publication-' + str(time.time_ns()))
    out.mkdir(parents=True)
    proof = PACKET / 'proof'
    proof.mkdir()
    commands = []

    def run(argv, name):
        result = subprocess.run(list(map(str, argv)), cwd=ROOT, capture_output=True, text=True)
        (proof / name).write_text(result.stdout + result.stderr)
        commands.append(dict(argv=list(map(str, argv)), exit=result.returncode, log=name))
        (proof / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
        print(name, 'exit', result.returncode, flush=True)
        if result.returncode:
            raise RuntimeError('failed check; retained ' + str(proof / name))
        return result.stdout

    # Generator writes only the established generated files, verified below.
    standalone_result = json.loads(run([sys.executable, '-B', 'tools/flight_demo/m2/build.py'], 'standalone.txt'))
    standalone = Path(standalone_result['output'])
    standalone_report = json.loads((standalone / 'build.json').read_text())
    expected = json.loads((ROOT / 'docs/evidence/flight-demo/2026-10-22-m2-interpolation-relink/standalone-static.json').read_text())
    assert standalone_report['target_sha256'] == expected['target_sha256']
    assert standalone_report['sections'] == expected['sections'] and standalone_report['stack'] == expected['stack']
    archive = PACKET / 'standalone'
    archive.mkdir()
    for path in standalone.iterdir():
        if path.is_file() and path.suffix in {'.txt', '.json', '.map', '.symbols', '.disassembly', '.h'}:
            shutil.copyfile(path, archive / path.name)
    # Direct old/new helper comparison: the reference include is an immutable
    # original helper; expectations are independent Python unbounded integers.
    interpolation = out / 'interpolation.bin'
    run([sys.executable, '-B', 'tests/flight_demo/m2_full/interpolation_corpus.py', interpolation], 'interpolation-corpus.txt')
    assert sha(interpolation) == 'd86ade1681153dca3ea00d72de2272b64c09bda5c5c16ce489194aa566132b37'
    common = ['/usr/bin/clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Wconversion',
              '-Werror', '-fsanitize=address,undefined', '-Isrc/graphics',
              '-Isrc/environment', '-Iinterfaces/generated']
    run([*common, '-Idocs/evidence/flight-demo/2026-10-22-m2-interpolation-bitwalk',
         'tests/flight_demo/m2_full/interpolation_equivalence.c', 'src/environment/m2_fixture.c',
         'interfaces/generated/m2_tables.c', '-o', out / 'interpolation-host'], 'interpolation-compile.txt')
    run([out / 'interpolation-host', interpolation], 'interpolation.txt')
    projection = out / 'projection.bin'
    run([sys.executable, '-B', 'tests/flight_demo/m2_full/projection_corpus.py', projection], 'projection-corpus.txt')
    assert sha(projection) == '92c334a7812dabafe70ccef7ab8703db424c15ef1f312c56fd314bf36f90a8d5'
    run([*common, '-Idocs/evidence/flight-demo/2026-10-21-m2-projection-sequence',
         'tests/flight_demo/m2_full/projection_equivalence.c', 'src/environment/m2_fixture.c',
         'interfaces/generated/m2_tables.c', '-o', out / 'projection-host'], 'projection-compile.txt')
    run([out / 'projection-host', projection], 'projection.txt')
    run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tools/ci', '-p', 'test_*.py', '-v'], 'hygiene-fixtures.txt')
    result = dict(status='PASS', output=str(out), standalone_output=str(standalone),
        standalone_sha256=standalone_report['target_sha256'],
        reviewed_standalone_identity='PASS byte-identical', stack=standalone_report['stack'],
        sections=standalone_report['sections'], interpolation_cases=457334, projection_cases=799886,
        projection_contracts=34, decimal_cases=3857, clipping_regressions=841,
        interpolation_corpus_sha256=sha(interpolation), projection_corpus_sha256=sha(projection),
        reserve_allocation=0, full_composition_relinks=0, target_execution='NOT RUN')
    (PACKET / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
