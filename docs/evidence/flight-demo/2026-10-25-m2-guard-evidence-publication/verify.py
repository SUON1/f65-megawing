"""Read-only packaging verification; never extract, execute or regrade evidence."""
import ast
import difflib
import hashlib
import io
import json
from pathlib import Path
import tarfile

ROOT = Path(__file__).resolve().parent


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    record = json.loads((ROOT/'record.json').read_text())
    packet = record['accepted_packet']
    data = (ROOT/packet['archive']).read_bytes()
    assert sha(data) == packet['archive_sha256']
    assert len(data) == packet['archive_bytes']
    files = {}
    prefix = '65aero-m2-guard-test-isolation/'
    with tarfile.open(fileobj=io.BytesIO(data),mode='r:gz') as archive:
        for member in archive.getmembers():
            assert member.isfile() and member.name.startswith(prefix)
            name = member.name[len(prefix):]
            assert name in packet['member_hashes'] and name not in files
            files[name] = archive.extractfile(member).read()
    assert len(files) == packet['archive_regular_files'] == 11
    assert {name:sha(value) for name,value in files.items()} == packet['member_hashes']
    assert sha(files['inventory.json']) == packet['inventory_sha256']
    inventory = json.loads(files['inventory.json'])
    assert len(inventory) == packet['members'] == 10
    assert set(files) == set(inventory)|{'inventory.json'}
    assert all(sha(files[name]) == pin for name,pin in inventory.items())
    metadata = record['patch']
    patch_data = (ROOT/metadata['file']).read_bytes()
    assert sha(patch_data) == metadata['file_sha256']
    patch = json.loads(patch_data)
    decoded = ''.join(patch['lines'])
    assert sha(decoded.encode()) == patch['patch_sha256'] == metadata['decoded_sha256']
    name = patch['path']
    before,after = files['before/'+name],files['after/'+name]
    assert sha(before) == patch['before_sha256'] == metadata['before_sha256']
    assert sha(after) == patch['after_sha256'] == metadata['after_sha256']
    expected = ''.join(difflib.unified_diff(before.decode().splitlines(True),
                    after.decode().splitlines(True),fromfile='before/'+name,tofile='after/'+name))
    assert decoded == expected
    full = files['changes.diff'].decode()
    assert full[full.index('--- before/'+name+'\n'):] == decoded
    old = next(node for node in ast.walk(ast.parse(before))
               if isinstance(node,ast.FunctionDef) and node.name=='test_actual_guard_faults_limits_and_slack')
    new = next(node for node in ast.walk(ast.parse(after))
               if isinstance(node,ast.FunctionDef) and node.name=='_guard_source')
    old_source = next(node.value for node in old.body if isinstance(node,ast.Assign)
                     and any(isinstance(target,ast.Name) and target.id=='source' for target in node.targets))
    new_source = next(node.value for node in new.body if isinstance(node,ast.Return))
    assert ast.dump(old_source) == ast.dump(new_source)
    log = files['min-regressions.txt']
    assert sha(log) == record['accepted_host_tests']['log_sha256']
    assert b'Ran 13 tests' in log and log.rstrip().endswith(b'OK')
    assert json.loads(files['validation.json'])['status'] == 'PASS; READY FOR REVIEW'
    if (ROOT/'inventory.json').exists():
        seal = json.loads((ROOT/'inventory.json').read_text())
        assert all(sha((ROOT/name).read_bytes()) == pin for name,pin in seal.items())
    print(json.dumps(dict(status='PASS packaging and exact accepted identities only',
        archive_regular_files=11,sealed_host_members=10,exact_patch=True,
        positive_guard_fixture_unchanged=True,accepted_host_tests=13,host_test_reruns=0,
        active_m2_code_adopted=False,target_relinks=0,xemu_d81_sd_physical='NOT RUN'),indent=2))


if __name__ == '__main__':
    main()
