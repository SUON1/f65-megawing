"""Read-only final PC scope, syntax, link and preservation validation."""
import ast
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess

PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[3]
BASE = '5c78bf7d00aadda0e63ce800e27fe3e142c651c0'
ALLOW = {
    'WORK_IN_PROGRESS.md', 'src/platform/m1/m1_platform.c',
    'src/platform/m1/clock_private.h',
    'tests/flight_demo/m2_rebuild/clock_host.c',
    'tests/flight_demo/m2_rebuild/test_platform_clock.py',
    'docs/plans/65AERO_M2_PLATFORM_CLOCK_CONTINUITY_INTENT.md',
    'docs/reports/M2_PLATFORM_CLOCK_CONTINUITY.md',
}


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root)


def identity(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': sha256(raw).hexdigest()}


def verify(root, inventory):
    for name, expected in inventory.items():
        if identity(root / name) != expected:
            raise ValueError('Preservation mismatch: ' + str(root / name))


baseline = json.loads((PACKET / 'baseline-before.json').read_text())
published = Path('/private/tmp/f65-m2-fixed-kernel-cost-correction')
verify(published, baseline)
candidate = {p: value for p, value in baseline.items()
             if p not in ('WORK_IN_PROGRESS.md', 'src/platform/m1/m1_platform.c')}
verify(ROOT, candidate)
if git(ROOT, 'rev-parse', 'HEAD').decode().strip() != BASE:
    raise ValueError('Candidate ancestry changed')
if git(ROOT, 'branch', '--show-current').decode().strip() != 'codex/65aero-m2-platform-clock':
    raise ValueError('Candidate branch changed')
if git(ROOT, 'diff', '--cached', '--name-only'):
    raise ValueError('Unexpected staged changes')
if git(ROOT, 'rev-parse', 'origin/main').decode().strip() != '9570f0ab427121a4e8f042041a14c89aaaeff9e2':
    raise ValueError('Main reference changed')
changed = set(git(ROOT, 'ls-files', '--modified', '--others', '--exclude-standard', '-z')
              .decode().split('\0')) - {''}
prefix = str(PACKET.relative_to(ROOT)) + '/'
if any(p not in ALLOW and not p.startswith(prefix) for p in changed):
    raise ValueError('Unexpected changed-file scope')
counts = {'json': 0, 'python': 0, 'local_links': 0, 'text_whitespace': 0}
for name in sorted(changed):
    path = ROOT / name
    if path.suffix == '.gz':
        continue
    text = path.read_text()
    if any(line.rstrip(' \t') != line for line in text.splitlines()):
        raise ValueError('Trailing whitespace: ' + name)
    counts['text_whitespace'] += 1
    if path.suffix == '.json':
        json.loads(text)
        counts['json'] += 1
    if path.suffix == '.py':
        ast.parse(text, filename=name)
        counts['python'] += 1
    if path.suffix == '.md':
        for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
            if '://' not in link and not link.startswith('#'):
                if not (path.parent / link.split('#')[0]).exists():
                    raise ValueError('Broken local link: ' + link)
                counts['local_links'] += 1

related = json.loads((PACKET / 'related-before.json').read_text())
for name, expected in related.items():
    path = Path(name)
    current = {'head': git(path, 'rev-parse', 'HEAD').decode().strip(),
               'status': git(path, 'status', '--short').decode(),
               'diff_sha256': sha256(git(path, 'diff', '--binary')).hexdigest()}
    if current != {k: expected[k] for k in current}:
        raise ValueError('Related checkout changed: ' + name)
    verify(path, expected['dirty_files'])

host = json.loads((PACKET / 'host-result.json').read_text())
verify(ROOT, host['sources'])
if host['status'] != 'PASS' or any(c['exit_code'] != 0 for c in host['commands']):
    raise ValueError('Host check failure')
original = Path('/private/tmp/f65-m2-fixed-kernel-preflight/docs/evidence/flight-demo/2026-11-11-m2-fixed-kernel-preflight/check_scope.py')
retained = subprocess.run(['python3', '-B', str(original)], text=True, capture_output=True,
                          cwd=original.parents[4])
if retained.returncode:
    raise ValueError('Historical preservation checker failed: ' + retained.stderr)
subprocess.run(['git', 'diff', '--check'], cwd=ROOT, check=True)
seal = PACKET / 'seal.json'
if seal.exists():
    members = json.loads(seal.read_text())
    actual = {str(p.relative_to(PACKET)) for p in PACKET.rglob('*')
              if p.is_file() and p != seal}
    if actual != set(members):
        raise ValueError('Sealed packet membership changed')
    verify(PACKET, members)
print(json.dumps({'status': 'PASS for stated scope', 'published_files': len(baseline),
                  'unchanged_candidate_files': len(candidate), 'related_checkouts': len(related),
                  'checks': counts, 'changed_paths': sorted(changed),
                  'original_preservation': json.loads(retained.stdout),
                  'source_identity_match': True, 'target_links': 0, 'runtime_executions': 0,
                  'git_diff_check_exit': 0}, indent=2))
