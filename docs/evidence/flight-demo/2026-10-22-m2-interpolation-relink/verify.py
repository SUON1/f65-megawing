"""Seal resumed relink evidence without changing any earlier packet or output."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[4]
PACKET = Path(__file__).resolve().parent
PRIOR = ROOT / 'docs/evidence/flight-demo/2026-10-22-m2-interpolation-bitwalk'
REPORT = 'docs/reports/M2_PR2_INTERPOLATION_RELINK_RESULT.md'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *arguments):
    return subprocess.check_output(['git', '-C', str(root), *arguments])


def paths(root):
    result = set()
    for arguments in [('ls-files', '-z'), ('ls-files', '--others', '--exclude-standard', '-z')]:
        result.update(git(root, *arguments).decode().split('\0'))
    result.discard('')
    return result


def save(name, value):
    (PACKET / name).write_text(json.dumps(value, indent=2) + '\n')


def main():
    snapshot = json.loads((PACKET / 'checkout-before.json').read_text())
    current = paths(ROOT)
    assert set(snapshot) <= current
    changed = {p for p, h in snapshot.items() if sha(ROOT / p) != h}
    assert changed == {'WORK_IN_PROGRESS.md'}, changed
    added = current - set(snapshot)
    prefix = str(PACKET.relative_to(ROOT)) + '/'
    assert all(p == REPORT or p.startswith(prefix) for p in added), added
    assert sha(PACKET / 'wip-before.md') == snapshot['WORK_IN_PROGRESS.md']
    other_checkouts = {}
    for name, expected in json.loads((PRIOR / 'preservation-before.json').read_text()).items():
        checkout = Path(name)
        assert paths(checkout) == set(expected), name
        assert all(sha(checkout / p) == h for p, h in expected.items()), name
        other_checkouts[name] = len(expected)
    histories = {}
    for inventory in sorted((ROOT / 'docs/evidence/flight-demo').glob('*/inventory.json')):
        if inventory.parent == PACKET:
            continue
        entries = json.loads(inventory.read_text())
        assert all(sha(inventory.parent / p) == h for p, h in entries.items()), inventory
        histories[str(inventory.relative_to(ROOT))] = dict(sha256=sha(inventory), files=len(entries))
    assert len(histories) == 17
    unrelated = json.loads((PRIOR / 'preservation.json').read_text())['unrelated_entries']
    assert len(unrelated) == 20
    assert all((Path('/Users/slice/Developer/f65-megawing') / p).exists() for p in unrelated)
    raw_count = 0
    for directory, entries in json.loads((PRIOR / 'artifact-identities.json').read_text()).items():
        directory = Path(directory)
        assert {p.name for p in directory.iterdir() if p.is_file()} == set(entries)
        for p, identity in entries.items():
            assert sha(directory / p) == identity['sha256']
            assert (directory / p).stat().st_size == identity['bytes']
            raw_count += 1
    assert raw_count == 57
    preflight = json.loads((PACKET / 'preflight.json').read_text())
    out = Path(preflight['output'])
    actual = json.loads((out / 'build.json').read_text())
    reference = json.loads((PRIOR / '00-reference/build.json').read_text())
    reused_host = Path(preflight['reused_host']['output'])
    old_host = json.loads((reused_host / 'build.json').read_text())
    assert actual['commands'][:3] == old_host['commands']
    assert len(actual['commands']) == 7
    for command, recorded in zip(actual['commands'][3:], reference['commands'][3:]):
        assert command['exit'] == 0
        assert command['argv'] == [arg.replace(reference['output'], str(out)) for arg in recorded['argv']]
    assert all(sha(ROOT / p) == h for p, h in preflight['source_inputs'].items())
    assert actual['inputs'] == preflight['source_inputs']
    assert actual['tool_hashes'] == reference['tool_hashes'] == preflight['tool_hashes']
    for name, tool in dict(compiler='mos-mega65-clang', objdump='llvm-objdump', nm='llvm-nm').items():
        assert sha(ROOT / 'toolchain/runtime/llvm-mos/bin' / tool) == reference['tool_hashes'][name]
    assert sha(Path('/usr/bin/clang')) == reference['tool_hashes']['host_clang']
    assert actual['target_executed'] is False
    assert json.loads((PACKET / 'link-command.json').read_text())['exit'] == 1
    comparison = json.loads((PACKET / 'comparison.json').read_text())
    assert comparison['composed_candidate_relinks'] == 1
    assert comparison['savings'] == 385 and comparison['after']['excess'] == 9189
    assert set(comparison['all_symbol_size_kind_changes']) == {'interpolate_delta', '__ashldi3', '__set_v'}
    candidate_files = json.loads((PACKET / 'candidate-artifacts.json').read_text())
    assert set(candidate_files) == {str(p) for p in out.iterdir() if p.is_file()}
    assert all(sha(Path(p)) == h['sha256'] and Path(p).stat().st_size == h['bytes']
               for p, h in candidate_files.items())
    assert sha(out / 'RENDER.prg') == comparison['candidate_prg_sha256']
    assert sha(out / 'RENDER.prg.elf') == comparison['candidate_elf_sha256']
    for path in (PACKET / '01-candidate').iterdir():
        assert sha(path) == sha(out / path.name)
    assert (PACKET / 'source/src/graphics/m2_geometry.c').read_bytes() == (
        ROOT / 'src/graphics/m2_geometry.c').read_bytes()
    tracked = git(ROOT, 'ls-files', '-z').decode().split('\0')
    generated = [p for p in tracked if p.startswith(('interfaces/generated/', 'memory/'))]
    assert all((ROOT / p).read_bytes() == git(ROOT, 'show', 'HEAD:' + p) for p in generated)
    subprocess.run(['git', 'diff', '--check'], cwd=ROOT, check=True)
    documents = [ROOT / 'WORK_IN_PROGRESS.md', ROOT / REPORT, PACKET / 'README.md']
    links = 0
    for document in documents:
        for target in re.findall(r'\]\(([^)]+)\)', document.read_text()):
            if '://' not in target:
                assert (document.parent / target.split('#')[0]).exists(), (document, target)
                links += 1
    for path in documents + list(PACKET.glob('*.py')):
        assert all(line == line.rstrip() for line in path.read_text().splitlines()), path
    for path in PACKET.rglob('*.json'):
        json.loads(path.read_text())
    save('preservation.json', dict(status='PASS', resumed_checkout_existing_paths=len(snapshot),
        changed_existing_paths=sorted(changed), new_paths_within_report_and_packet='PASS',
        unchanged_other_checkouts=other_checkouts, historical_flight_inventories=histories,
        unrelated_entries=unrelated, old_raw_artifacts_unchanged=raw_count,
        generated_and_memory_files_unchanged=len(generated), source_and_verifier_frozen='PASS',
        exact_reference_target_recipe='PASS output path substitution only',
        candidate_raw_files=len(candidate_files), composed_candidate_relinks=1,
        local_links_checked=links, whitespace_and_json='PASS', report_sha256=sha(ROOT / REPORT),
        wip_sha256=sha(ROOT / 'WORK_IN_PROGRESS.md')))
    inventory = {str(p.relative_to(PACKET)):sha(p) for p in sorted(PACKET.rglob('*'))
                 if p.is_file() and p != PACKET / 'inventory.json'}
    save('inventory.json', inventory)
    assert all(sha(PACKET / p) == h for p, h in inventory.items())
    print(json.dumps(dict(status='PASS', changed=sorted(changed),
        historical_inventories=len(histories), old_raw_artifacts=raw_count,
        candidate_raw_files=len(candidate_files), generated=len(generated), unrelated=len(unrelated),
        original_checkouts=other_checkouts, packet_files=len(inventory), local_links=links), indent=2))


if __name__ == '__main__':
    main()
