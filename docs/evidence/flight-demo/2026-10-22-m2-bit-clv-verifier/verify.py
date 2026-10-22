"""Seal this packet while preserving every pre-existing unrelated path."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[4]
PACKET = Path(__file__).resolve().parent
PREVIOUS = ROOT / 'docs/evidence/flight-demo/2026-10-22-m2-interpolation-bitwalk'
CHANGES = {'WORK_IN_PROGRESS.md', 'tools/flight_demo/m2/stack_check.py',
           'tests/flight_demo/m2/test_contract.py'}
REPORT = 'docs/reports/M2_BIT_CLV_VERIFIER_FIX.md'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])


def paths(root):
    result = set()
    for arguments in [('ls-files', '-z'), ('ls-files', '--others', '--exclude-standard', '-z')]:
        result.update(git(root, *arguments).decode().split('\0'))
    result.discard('')
    return result


def save(name, value):
    (PACKET / name).write_text(json.dumps(value, indent=2) + '\n')


def main():
    before = json.loads((PACKET / 'checkout-before.json').read_text())
    current = paths(ROOT)
    assert set(before) <= current, set(before) - current
    changed = {p for p, h in before.items() if sha(ROOT / p) != h}
    assert changed == CHANGES, changed
    added = current - set(before)
    prefix = str(PACKET.relative_to(ROOT)) + '/'
    assert all(p == REPORT or p.startswith(prefix) for p in added), added
    assert sha(PACKET / 'reference_stack_check.py') == before['tools/flight_demo/m2/stack_check.py']
    assert sha(PACKET / 'reference_test_contract.py') == before['tests/flight_demo/m2/test_contract.py']
    assert sha(PACKET / 'wip-before.md') == before['WORK_IN_PROGRESS.md']
    other_checkouts = {}
    for name, expected in json.loads((PREVIOUS / 'preservation-before.json').read_text()).items():
        checkout = Path(name)
        assert paths(checkout) == set(expected), name
        assert all(sha(checkout / p) == h for p, h in expected.items()), name
        other_checkouts[name] = len(expected)
    inventories = {}
    for inventory in sorted((ROOT / 'docs/evidence/flight-demo').glob('*/inventory.json')):
        if inventory.parent == PACKET:
            continue
        entries = json.loads(inventory.read_text())
        assert all(sha(inventory.parent / p) == h for p, h in entries.items()), inventory
        inventories[str(inventory.relative_to(ROOT))] = dict(sha256=sha(inventory), files=len(entries))
    assert len(inventories) == 16
    unrelated = json.loads((PREVIOUS / 'preservation.json').read_text())['unrelated_entries']
    assert len(unrelated) == 20
    assert all((Path('/Users/slice/Developer/f65-megawing') / p).exists() for p in unrelated)
    tracked = git(ROOT, 'ls-files', '-z').decode().split('\0')
    generated = [p for p in tracked if p.startswith(('interfaces/generated/', 'memory/'))]
    assert all((ROOT / p).read_bytes() == git(ROOT, 'show', 'HEAD:' + p) for p in generated)
    replay = json.loads((PACKET / 'replay.json').read_text())
    assert replay['checker_sha256'] == sha(ROOT / 'tools/flight_demo/m2/stack_check.py')
    assert replay['status'] == 'PASS' and replay['relinks'] == 0
    raw_count = 0
    for directory, entries in json.loads((PREVIOUS / 'artifact-identities.json').read_text()).items():
        raw = Path(directory)
        assert {p.name for p in raw.iterdir() if p.is_file()} == set(entries)
        for name, identity in entries.items():
            assert sha(raw / name) == identity['sha256']
            assert (raw / name).stat().st_size == identity['bytes']
            raw_count += 1
    assert raw_count == replay['unchanged_raw_artifacts'] == 57
    for relative in sorted(CHANGES - {'WORK_IN_PROGRESS.md'}):
        destination = PACKET / 'source' / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, destination)
    subprocess.run(['git', 'diff', '--check'], cwd=ROOT, check=True)
    documents = [ROOT / 'WORK_IN_PROGRESS.md', ROOT / REPORT, PACKET / 'README.md']
    link_count = 0
    for document in documents:
        for target in re.findall(r'\]\(([^)]+)\)', document.read_text()):
            if '://' not in target:
                assert (document.parent / target.split('#')[0]).exists(), (document, target)
                link_count += 1
    for path in [ROOT / p for p in CHANGES] + documents + list(PACKET.glob('*.py')):
        assert all(line == line.rstrip() for line in path.read_text().splitlines()), path
    for path in PACKET.rglob('*.json'):
        json.loads(path.read_text())
    save('preservation.json', dict(status='PASS', experiment_existing_paths=len(before),
        changed_existing_paths=sorted(changed), new_paths_within_packet_and_report='PASS',
        unchanged_other_checkouts=other_checkouts, unrelated_entries=unrelated,
        historical_flight_inventories=inventories, raw_artifacts_unchanged=raw_count,
        generated_and_memory_files_unchanged=len(generated), local_links_checked=link_count,
        whitespace_and_json='PASS', report_sha256=sha(ROOT / REPORT),
        wip_sha256=sha(ROOT / 'WORK_IN_PROGRESS.md'), relinks=0))
    inventory = {str(p.relative_to(PACKET)):sha(p) for p in sorted(PACKET.rglob('*'))
                 if p.is_file() and p != PACKET / 'inventory.json'}
    save('inventory.json', inventory)
    assert all(sha(PACKET / p) == h for p, h in inventory.items())
    print(json.dumps(dict(status='PASS', changed=sorted(changed),
        original_checkouts=other_checkouts, historical_inventories=len(inventories),
        unrelated=len(unrelated), raw_artifacts=raw_count, generated=len(generated),
        packet_files=len(inventory), local_links=link_count), indent=2))


if __name__ == '__main__':
    main()
