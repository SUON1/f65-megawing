"""Seal focused publication and preserve the original development worktrees."""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tokenize

ROOT = Path(__file__).resolve().parents[4]
PACKET = Path(__file__).resolve().parent
EXPERIMENT = Path('/private/tmp/f65-m2-interpolation-experiment')
REPORT = 'docs/reports/M2_PR2_INTERPOLATION_PUBLICATION.md'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])


def paths(root):
    result = set()
    for args in [('ls-files', '-z'), ('ls-files', '--others', '--exclude-standard', '-z')]:
        result.update(git(root, *args).decode().split('\0'))
    result.discard('')
    return result


def main():
    baseline = json.loads((PACKET / 'preservation-before.json').read_text())
    for name, expected in baseline.items():
        entries = paths(Path(name))
        digest = hashlib.sha256()
        for p in sorted(entries):
            digest.update(p.encode() + b'\0' + hashlib.sha256((Path(name) / p).read_bytes()).digest())
        assert len(entries) == expected['paths'] and digest.hexdigest() == expected['digest'], name
    pattern = r'static int64_t interpolate_delta\(.*?\n\}\n'
    reviewed = re.search(pattern, (EXPERIMENT / 'src/graphics/m2_geometry.c').read_text(), re.S)[0]
    original = git(ROOT, 'show', 'origin/main:src/graphics/m2_geometry.c').decode()
    expected_source = re.sub(pattern, lambda m: reviewed, original, count=1, flags=re.S)
    assert (ROOT / 'src/graphics/m2_geometry.c').read_text() == expected_source
    assert 'm2_registration_matches_prepared' not in expected_source
    for relative in ['tools/flight_demo/m2/stack_check.py', 'tests/flight_demo/m2/test_contract.py',
                     'tests/flight_demo/m2_full/interpolation_corpus.py',
                     'tests/flight_demo/m2_full/interpolation_equivalence.c',
                     'docs/plans/65AERO_M2_PR2_INTERPOLATION_BUILD_INTENT.md',
                     'docs/plans/65AERO_M2_PR2_INTERPOLATION_RECONSTRUCTION.json',
                     'docs/reports/M2_PR2_INTERPOLATION_BITWALK_EXPERIMENT.md',
                     'docs/reports/M2_BIT_CLV_VERIFIER_FIX.md',
                     'docs/reports/M2_PR2_INTERPOLATION_RELINK_RESULT.md']:
        assert (ROOT / relative).read_bytes() == (EXPERIMENT / relative).read_bytes(), relative
    previous_inventories = {}
    for inventory in (ROOT / 'docs/evidence/flight-demo').glob('*/inventory.json'):
        if inventory.parent == PACKET:
            continue
        assert all(sha(inventory.parent / p) == h for p, h in json.loads(inventory.read_text()).items())
        previous_inventories[str(inventory.relative_to(ROOT))] = sha(inventory)
    assert len(previous_inventories) == 18
    for name in ['2026-10-22-m2-interpolation-bitwalk', '2026-10-22-m2-bit-clv-verifier',
                 '2026-10-22-m2-interpolation-relink']:
        source = EXPERIMENT / 'docs/evidence/flight-demo' / name
        destination = ROOT / 'docs/evidence/flight-demo' / name
        source_files = {str(p.relative_to(source)):sha(p) for p in source.rglob('*') if p.is_file()}
        copied_files = {str(p.relative_to(destination)):sha(p) for p in destination.rglob('*') if p.is_file()}
        assert source_files == copied_files, name
    raw_count = 0
    identity = ROOT / 'docs/evidence/flight-demo/2026-10-22-m2-interpolation-bitwalk/artifact-identities.json'
    for directory, files in json.loads(identity.read_text()).items():
        directory = Path(directory)
        assert {p.name for p in directory.iterdir() if p.is_file()} == set(files)
        for p, value in files.items():
            assert sha(directory / p) == value['sha256'] and (directory / p).stat().st_size == value['bytes']
            raw_count += 1
    for p, value in json.loads((ROOT / 'docs/evidence/flight-demo/2026-10-22-m2-interpolation-relink/candidate-artifacts.json').read_text()).items():
        assert sha(Path(p)) == value['sha256'] and Path(p).stat().st_size == value['bytes']
        raw_count += 1
    assert raw_count == 75
    unrelated = json.loads((ROOT / 'docs/evidence/flight-demo/2026-10-22-m2-interpolation-relink/preservation.json').read_text())['unrelated_entries']
    assert len(unrelated) == 20 and all((Path('/Users/slice/Developer/f65-megawing') / p).exists() for p in unrelated)
    tracked = git(ROOT, 'ls-files', '-z').decode().split('\0')
    generated = [p for p in tracked if p.startswith(('interfaces/generated/', 'memory/'))]
    assert all((ROOT / p).read_bytes() == git(ROOT, 'show', 'origin/main:' + p) for p in generated)
    manifest_path = 'tools/ci/retained_evidence_sha256.json'
    manifest = json.loads((ROOT / manifest_path).read_text())
    previous_manifest = json.loads(git(ROOT, 'show', 'origin/main:' + manifest_path))
    assert manifest['d81'] == previous_manifest['d81']
    additions = set(manifest['whitespace']) - set(previous_manifest['whitespace'])
    assert additions == {'docs/evidence/flight-demo/2026-10-22-m2-interpolation-bitwalk/source/src/graphics/m2_font.c'}
    assert all(manifest['whitespace'][p] == h for p, h in previous_manifest['whitespace'].items())
    assert all(sha(ROOT / p) == manifest['whitespace'][p] for p in additions)
    validation = json.loads((PACKET / 'validation.json').read_text())
    assert validation['status'] == 'PASS' and validation['full_composition_relinks'] == 0
    assert validation['standalone_sha256'] == '622ff2318cdf7cee9cd3be721fabb118a56cf0929eb0fb58debcad6cd53fb88d'
    expected_tracked = {'CURRENT_STATE.md', 'WORK_IN_PROGRESS.md', 'src/graphics/m2_geometry.c',
        'tools/flight_demo/m2/stack_check.py', 'tests/flight_demo/m2/test_contract.py',
        'tools/ci/static_hygiene.py', 'tools/ci/test_static_hygiene.py', manifest_path}
    # Worktree diff is used before staging; staged changes may also be present.
    modified = set(git(ROOT, 'diff', 'origin/main', '--name-only').decode().splitlines())
    existing_modified = modified & set(p for p in tracked if p)
    assert existing_modified == expected_tracked, existing_modified
    exclusions = [':(exclude,literal)' + p for p in sorted(manifest['whitespace'])]
    subprocess.run(['git', 'diff', '--check', 'origin/main', '--', '.', *exclusions], cwd=ROOT, check=True)
    all_paths = paths(ROOT)
    json_count = python_count = shell_count = 0
    for relative in sorted(all_paths):
        path = ROOT / relative
        if path.suffix == '.json':
            json.loads(path.read_text())
            json_count += 1
        elif path.suffix == '.py':
            with tokenize.open(path) as stream:
                ast.parse(stream.read(), filename=relative)
            python_count += 1
        elif path.suffix == '.sh':
            subprocess.run(['sh', '-n', str(path)], check=True)
            shell_count += 1
    local_links = 0
    for path in [ROOT / 'CURRENT_STATE.md', ROOT / 'WORK_IN_PROGRESS.md', ROOT / REPORT, PACKET / 'README.md']:
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' not in target:
                assert (path.parent / target.split('#')[0]).exists(), (path, target)
                local_links += 1
    result = dict(status='PASS', original_checkouts_unchanged=baseline,
        historical_inventories=previous_inventories, copied_packets_byte_identical=True,
        retained_raw_artifacts=raw_count, unrelated_entries=unrelated,
        generated_files_unchanged=len(generated), exact_helper_and_verifier='PASS',
        active_target_scope='interpolate_delta only; no renderer/cache/owner scaffolding',
        existing_modified_paths=sorted(existing_modified), whitespace_exception_additions=sorted(additions),
        syntax=dict(json=json_count, python=python_count, shell=shell_count),
        local_links=local_links, full_composition_relinks=0)
    (PACKET / 'preservation.json').write_text(json.dumps(result, indent=2) + '\n')
    inventory = {str(p.relative_to(PACKET)):sha(p) for p in sorted(PACKET.rglob('*'))
                 if p.is_file() and p != PACKET / 'inventory.json'}
    (PACKET / 'inventory.json').write_text(json.dumps(inventory, indent=2) + '\n')
    assert all(sha(PACKET / p) == h for p, h in inventory.items())
    print(json.dumps(dict(status='PASS', preserved_checkouts=len(baseline), inventories=len(previous_inventories),
        old_raw=raw_count, unrelated=len(unrelated), generated=len(generated),
        syntax=result['syntax'], links=local_links, packet_files=len(inventory)), indent=2))


if __name__ == '__main__':
    main()
