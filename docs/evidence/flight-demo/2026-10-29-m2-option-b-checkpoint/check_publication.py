"""Publication-only checks for the retained failed Option B experiment."""
import ast
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
BASE = '9570f0ab427121a4e8f042041a14c89aaaeff9e2'
BRANCH = 'codex/65aero-m2-option-b-lean-renderer'
EXPERIMENT = ROOT / 'docs/evidence/flight-demo/2026-10-29-m2-option-b'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root)


def verify_seal(root):
    seal = json.loads((root / 'seal.json').read_text())
    members = {str(p.relative_to(root)) for p in root.rglob('*')
               if p.is_file() and p != root / 'seal.json'}
    assert members == set(seal), root
    for name, item in seal.items():
        path = root / name
        assert path.stat().st_size == item['bytes'] and sha(path) == item['sha256'], path
    return len(seal)


def symbols(root):
    result = {}
    for line in (root / 'UNADMITTED.symbols').read_text().splitlines():
        fields = line.split()
        if len(fields) == 4 and int(fields[1], 16):
            result[fields[3]] = int(fields[1], 16)
    return result


def main():
    before = json.loads(gzip.decompress((HERE / 'reviewed-before.json.gz').read_bytes()))
    assert len(before) == 16135
    assert hashlib.sha256(json.dumps(before, sort_keys=True).encode()).hexdigest() == 'db06cd5d9e44eec09ff5717fc580877c7d30323f51ba95ec0929d13151d891c9'
    for name, item in before.items():
        path = HERE / 'WIP-before.md' if name == 'WORK_IN_PROGRESS.md' else ROOT / name
        assert path.stat().st_size == item['bytes'] and sha(path) == item['sha256'], name
    measured = json.loads((EXPERIMENT / 'result.json').read_text())
    for name, expected in measured['source_identities'].items():
        path = HERE / 'WIP-before.md' if name == 'WORK_IN_PROGRESS.md' else ROOT / name
        assert sha(path) == expected, name
    members = verify_seal(EXPERIMENT)
    assert members == 46 and sha(EXPERIMENT / 'seal.json') == '2a1959988ff324b5118a51b82aaa7cc4ed58b0bfdcbacf5fcb7c111d3b420b34'
    for tier in ['host-1793302504990999000','text-1793302574153355000','target-1793302615810967000']:
        verify_seal(EXPERIMENT / tier)
    target = json.loads((ROOT / measured['target_packet'] / 'result.json').read_text())
    baseline_path = ROOT / 'docs/evidence/flight-demo/2026-10-27-m2-min-rebuild-corrections/target-1793167696482111000'
    baseline = json.loads((baseline_path / 'result.json').read_text())
    a, b = symbols(baseline_path), symbols(ROOT / measured['target_packet'])
    delta = lambda name: b.get(name, 0) - a.get(name, 0)
    assert sum(delta(n) for n in ['prepare','copy_tile','background','m2_ground_prepared']) == 778
    assert sum(delta(n) for n in ['m2rb_text_row','field','hex','decimal','label']) == -271
    assert target['resident_bytes'] == 33395 and target['resident_limit'] == 24575
    assert target['resident_bytes'] - baseline['resident_bytes'] == 556
    assert target['resident_fit'] == 'FAIL' and target['deficit'] == 8820
    assert target['failure'] == 'incomplete target composition'
    assert [n for n,v in target['retained_implementation'].items() if not v] == ['m2_ground_prepared']
    assert measured['target_invocations'] == 1 and measured['reserve'] == 0
    assert json.loads((EXPERIMENT / 'relink-claim.json').read_text())['authorized_relinks'] == 1
    for name, expected in target['inputs'].items(): assert sha(ROOT / name) == expected, name
    assert target['toolchain']['flags'] == baseline['toolchain']['flags']
    assert target['toolchain']['compiler_sha256'] == baseline['toolchain']['compiler_sha256']
    assert git(ROOT,'branch','--show-current').decode().strip() == BRANCH
    subprocess.run(['git','merge-base','--is-ancestor',BASE,'HEAD'],cwd=ROOT,check=True)
    # Include both unstaged files and the committed/staged experiment range.
    paths = {n.decode() for n in git(ROOT,'ls-files','--others','--exclude-standard','-z').split(b'\0') if n}
    paths.update(git(ROOT,'diff','--name-only',BASE).decode().splitlines())
    exact = set(measured['source_identities']) | {'docs/reports/M2_OPTION_B_FAILED_EXPERIMENT_CHECKPOINT.md'}
    prefixes = ('docs/evidence/flight-demo/2026-10-29-m2-option-b/',
                'docs/evidence/flight-demo/2026-10-29-m2-option-b-checkpoint/')
    for name in paths:
        assert name in exact or name.startswith(prefixes), name
        path = ROOT / name
        assert path.is_file() and not path.is_symlink(), name
        assert not any(part in {'.aws','.codex','sessions','.env','credentials'} for part in path.relative_to(ROOT).parts), name
        if path.suffix == '.json': json.loads(path.read_text())
        if path.suffix == '.py': ast.parse(path.read_text(), filename=name)
        if path.suffix in {'.py','.c','.h','.md','.json','.txt'}:
            text = path.read_text()
            assert all(line == line.rstrip(' \t') for line in text.splitlines()), name
            if path.suffix == '.md':
                for href in re.findall(r'\]\(([^)]+)\)',text):
                    if '://' not in href and not href.startswith('#'):
                        # Archived WIP keeps its original repository-root link context.
                        parent = ROOT if path == HERE / 'WIP-before.md' else path.parent
                        destination = parent / href.split('#')[0]
                        assert destination.exists() or destination.resolve() == HERE / 'checks.json', (name,href)
    spec = importlib.util.spec_from_file_location('publication_policy',ROOT/'tools/ci/static_hygiene.py')
    policy = importlib.util.module_from_spec(spec);spec.loader.exec_module(policy)
    policy.guard_artifacts(paths, {})
    for name in ['.github/workflows/ci.yml','tools/ci/static_hygiene.py','tools/ci/retained_evidence_sha256.json','CURRENT_STATE.md']:
        assert (ROOT/name).read_bytes() == git(ROOT,'show',BASE+':'+name), name
    original = Path('/Users/slice/Developer/f65-megawing')
    old = json.loads((ROOT/'docs/evidence/flight-demo/2026-10-27-m2-min-rebuild/final-check-1793159584829644000/original-checkout-current-inventory.json').read_text())
    for name,item in old.items():
        path=original/name
        assert path.stat().st_size == item['bytes'] and sha(path) == item['sha256'], name
    historical = json.loads((ROOT/'docs/evidence/flight-demo/2026-10-27-m2-residency-feasibility/accounting.json').read_text())['original_checkout_before']
    for command,key in [(('status','--porcelain=v1'),'status_sha256'),(('diff','--binary'),'diff_sha256')]:
        assert hashlib.sha256(git(original,*command)).hexdigest() == historical[key]
    assert len(old) == 480
    for directory, head in [('f65-megawing-m2-banked-renderer-intent','28c8b722c35a276334906081842ec9f902226f24'),('f65-megawing-m2-source-baseline','a2f75a1c61287d29071b4b7448ea2cdc97258be3')]:
        checkout=ROOT.parent/directory
        assert git(checkout,'rev-parse','HEAD').decode().strip() == head
        assert not git(checkout,'status','--porcelain')
    print(json.dumps({'scope':'PASS','syntax':'PASS','whitespace':'PASS','artifact_guard':'PASS',
        'preservation':'PASS','reviewed_files':16135,'unchanged_live_files':16134,
        'WIP_preimage':'preserved; only prior file changed for publication','sealed_experiment_members':members,
        'unrelated_paths':480,'source_tests_handoff_measured_results':'UNCHANGED',
        'horizon_code_delta':778,'telemetry_code_delta':-271,'resident_delta':556,
        'resident_bytes':33395,'resident_limit':24575,'fit':'FAIL','runtime_benefit':'UNPROVEN',
        'xemu':'NOT RUN','physical_testing':'NOT RUN','candidate_path_count':len(paths)},indent=2))


if __name__ == '__main__':
    main()
