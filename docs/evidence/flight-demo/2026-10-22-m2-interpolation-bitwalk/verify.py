"""Read-only scope, historical evidence and original-checkout preservation audit."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[4]
PACKET = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])


def save(name, data):
    (PACKET / name).write_text(json.dumps(data, indent=2) + '\n')


def main():
    preserved = {}
    snapshots = json.loads((PACKET / 'preservation-before.json').read_text())
    for name, original in snapshots.items():
        root = Path(name)
        paths = set(git(root, 'ls-files', '-z').decode().split('\0'))
        paths.update(git(root, 'ls-files', '--others', '--exclude-standard', '-z')
                     .decode().split('\0'))
        paths.discard('')
        assert paths == set(original), (name, paths ^ set(original))
        differences = [p for p in paths if sha(root / p) != original[p]]
        assert not differences, (name, differences)
        preserved[name] = len(paths)
    historical = {}
    tracked = git(ROOT, 'ls-files', '-z').decode().split('\0')
    for relative in tracked:
        if relative.startswith('docs/evidence/flight-demo/') and relative.endswith('/inventory.json'):
            path = ROOT / relative
            inventory = json.loads(path.read_text())
            assert all(sha(path.parent / p) == h for p, h in inventory.items()), relative
            historical[relative] = dict(sha256=sha(path), files=len(inventory))
    assert len(historical) == 15, len(historical)
    unrelated = json.loads((ROOT / 'docs/evidence/flight-demo/2026-10-21-m2-projection-sequence/preservation.json')
                           .read_text())['unrelated_entries']
    assert len(unrelated) == 20 and all((Path('/Users/slice/Developer/f65-megawing') / p).exists()
                                      for p in unrelated)
    generated = [p for p in tracked if p.startswith(('interfaces/generated/', 'memory/'))]
    assert all((ROOT / p).read_bytes() == git(ROOT, 'show', 'HEAD:' + p) for p in generated)
    changed = git(ROOT, 'diff', '--name-only').decode().splitlines()
    assert set(changed) == {'WORK_IN_PROGRESS.md', 'src/graphics/m2_geometry.c',
                            'src/graphics/m2_prepared_private.h'}, changed
    manifest = json.loads((PACKET / 'reconstruction.json').read_text())
    allowed = {r['destination'] for r in manifest['restorations']}
    allowed.update(['docs/plans/65AERO_M2_PR2_INTERPOLATION_BUILD_INTENT.md',
                    'docs/plans/65AERO_M2_PR2_INTERPOLATION_RECONSTRUCTION.json',
                    'tests/flight_demo/m2_full/interpolation_corpus.py',
                    'tests/flight_demo/m2_full/interpolation_equivalence.c',
                    'docs/reports/M2_PR2_INTERPOLATION_BITWALK_EXPERIMENT.md'])
    untracked = git(ROOT, 'ls-files', '--others', '--exclude-standard', '-z').decode().split('\0')
    assert all(not p or p in allowed or p.startswith(str(PACKET.relative_to(ROOT)) + '/')
               for p in untracked)
    subprocess.run(['git', 'diff', '--check'], cwd=ROOT, check=True)
    documents = [ROOT / 'WORK_IN_PROGRESS.md',
        ROOT / 'docs/reports/M2_PR2_INTERPOLATION_BITWALK_EXPERIMENT.md', PACKET / 'README.md']
    links = 0
    for document in documents:
        for target in re.findall(r'\]\(([^)]+)\)', document.read_text()):
            if '://' not in target:
                assert (document.parent / target.split('#')[0]).exists(), (document, target)
                links += 1
    json_count = 0
    for path in PACKET.rglob('*.json'):
        json.loads(path.read_text())
        json_count += 1
    # New authored sources only; retained source snapshots keep historical bytes.
    whitespace_paths = documents + [ROOT / 'tests/flight_demo/m2_full/interpolation_corpus.py',
        ROOT / 'tests/flight_demo/m2_full/interpolation_equivalence.c', PACKET/'collect.py',
        PACKET/'verify.py', PACKET/'run_recipe.py', PACKET/'bit-state-proof.md']
    for path in whitespace_paths:
        assert all(line == line.rstrip() for line in path.read_text().splitlines()), path
    save('preservation.json', dict(status='PASS', unchanged_checkout_path_counts=preserved,
        unrelated_entries=unrelated, historical_flight_inventories=historical,
        generated_and_memory_files_unchanged=len(generated),
        tracked_changed_paths=changed, new_paths_within_scope='PASS',
        diff_whitespace='PASS', authored_whitespace='PASS', local_links_checked=links,
        packet_json_checked=json_count))
    inventory = {str(p.relative_to(PACKET)):sha(p) for p in sorted(PACKET.rglob('*'))
                 if p.is_file() and p != PACKET/'inventory.json'}
    save('inventory.json', inventory)
    assert all(sha(PACKET/p) == h for p,h in inventory.items())
    print(json.dumps(dict(status='PASS', preserved=preserved, historical=len(historical),
        unrelated=len(unrelated), generated_unchanged=len(generated), links=links,
        packet_files=len(inventory)), indent=2))


if __name__ == '__main__':
    main()
