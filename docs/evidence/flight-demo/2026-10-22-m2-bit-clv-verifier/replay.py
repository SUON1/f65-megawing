"""Replay only hash-pinned retained disassemblies; never compile or link."""
import hashlib
import importlib.util
import json
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[4]
PACKET = Path(__file__).resolve().parent
PINS = {
    'previous': (
        'docs/evidence/flight-demo/2026-10-21-m2-projection-forward-guard/03-standalone/M2.disassembly',
        '4e547d315061d7445edab574b471814f08dd3373e1fb67a08ecb0f0e3fd2b0b2'),
    'interpolation': (
        'docs/evidence/flight-demo/2026-10-22-m2-interpolation-bitwalk/03-standalone/M2.disassembly',
        '446b837320606cfbd21a9619ed0cedbddea64c6711b1dbd71269a5cca4bb6fef'),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    reference_path = PACKET / 'reference_stack_check.py'
    assert sha(reference_path) == '4d344f815d246859b621caac01f2c9e27f1501ecec32c7f9491d7f2e427522ef'
    reference = runpy.run_path(str(reference_path))['check']
    current_path = ROOT / 'tools/flight_demo/m2/stack_check.py'
    spec = importlib.util.spec_from_file_location('bounded_stack_check', current_path)
    current = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(current)
    # Enforce the exact reviewed two-token delta plus its explanatory comment.
    expected = reference_path.read_text().replace(
        "    ordinary = set('adc and asl clc cli cmp",
        "    # BIT and CLV change flags, not stacks; both branch successors stay checked.\n"
        "    ordinary = set('adc and asl bit clc cli clv cmp", 1)
    assert current_path.read_text() == expected
    previous_report = ROOT / ('docs/evidence/flight-demo/'
        '2026-10-21-m2-projection-forward-guard/03-standalone/build.json')
    assert sha(previous_report) == '52686e6ce0007bde4612d8341d7dc7ba52a729904c59d998879d2aa58b820271'
    previous_stack = json.loads(previous_report.read_text())['stack']
    results = {}
    for name, (relative, digest) in PINS.items():
        path = ROOT / relative
        assert sha(path) == digest, relative
        text = path.read_text()
        try:
            before = dict(status='PASS', stack=reference(text))
        except ValueError as error:
            before = dict(status='FAIL', reason=str(error))
        if name == 'previous':
            assert before['status'] == 'PASS'
            assert all(previous_stack[k] == v for k, v in before['stack'].items())
        else:
            assert before == dict(status='FAIL', reason='unrecognized instruction: bit')
        after = current.check(text)
        if name == 'previous':
            assert after == before['stack'], 'previous passing bound drifted'
        assert sha(path) == digest
        results[name] = dict(path=relative, sha256=digest, before=before,
                             after=dict(status='PASS', stack=after))
    # Revalidate all original raw outputs, including corpora and binaries. No
    # target command is available in this replay program.
    identities = ROOT / ('docs/evidence/flight-demo/'
        '2026-10-22-m2-interpolation-bitwalk/artifact-identities.json')
    artifact_count = 0
    for directory, artifacts in json.loads(identities.read_text()).items():
        raw = Path(directory)
        assert {p.name for p in raw.iterdir() if p.is_file()} == set(artifacts)
        for name, identity in artifacts.items():
            path = raw / name
            assert path.stat().st_size == identity['bytes'] and sha(path) == identity['sha256']
            artifact_count += 1
    result = dict(status='PASS', reference_checker_sha256=sha(reference_path),
        checker_sha256=sha(current_path), replay=results,
        unchanged_raw_artifacts=artifact_count, relinks=0, target_execution='NOT RUN',
        scope='Pinned standalone direct-call probes; no IRQ/NMI, executed high-water, '
              'whole renderer, deadline or runtime/display admission')
    (PACKET / 'replay.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
