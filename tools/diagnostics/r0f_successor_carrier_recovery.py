#!/usr/bin/env python3
"""Fresh T05 carrier from retained T04 payloads; repeat all host/Xemu gates.

Read 00_D81_LOADABILITY_GATE.md before use. Canonical images are immutable;
Xemu SAVE changes only disposable copies. No SD operation in this command.
"""

import argparse
from pathlib import Path
import shutil

from d81_delivery import require_name
import r0f_successor_emulator as runtime

ROOT = runtime.ROOT
EVIDENCE = ROOT / 'docs/evidence/r0f/successor/2026-09-21'
SOURCE = '20b2aab382d0590037443b6a352fbc77fda7aa42'
PAYLOADS = {
    'autoboot.c65': ('AUTOBOOT.C65', 464, '9bdf352c44c411965229f68b2d92c358f08f0e6ef6486142115b53c9da246cc7'),
    'r0fsucc': ('r0fsucc', 21481, runtime.EXPECTED_PRG_SHA256),
    'token': ('TOKEN.prg', 34, '0e8d0ac2ce727ba51285be0173ea784b52b56fdc4729a1f7c0d2d7271005b572'),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('filename')
    parser.add_argument('--host-only', action='store_true')
    parser.add_argument('--resume-xemu', action='store_true')
    args = parser.parse_args()
    require_name(args.filename)  # Before creating any output or invoking tools.
    if args.filename not in ('R0FSUC10.D81', 'R0FHOST1.D81'):
        raise ValueError('only the two authorized recovery candidates are supported')
    output = ROOT / 'build/r0f/successor-t05-recovery' / args.filename[:-4]
    canonical = output / args.filename
    manifest_path = output / 'release.json'
    inputs = {}
    for name, (filename, length, digest) in PAYLOADS.items():
        path = EVIDENCE / filename
        if path.stat().st_size != length or runtime.sha256(path) != digest:
            raise ValueError('frozen T04 input drift: ' + filename)
        inputs[name] = path
    if args.resume_xemu:
        manifest = runtime.read_json(manifest_path)
        if runtime.sha256(canonical) != manifest['D81_SHA256']:
            raise ValueError('candidate drift')
    else:
        output.mkdir(parents=True, exist_ok=False)
        image = runtime.fresh_d81(output, canonical, runtime.CANONICAL_LABEL, inputs)
        if image['sha256'] != runtime.EXPECTED_CANONICAL_SHA256:
            raise ValueError('fresh construction does not reproduce frozen disk bytes')
        canonical.chmod(0o444)
        manifest = runtime.read_json(EVIDENCE / 'canonical-host-gate.json')
        manifest.update({
            'identity': 'R0F-T05-CARRIER-RECOVERY', 'D81_FILENAME': args.filename,
            'D81_STATE': 'HOST_CONTENT_VERIFIED', 'XEMU_RESULT': 'NOT RUN',
            'XEMU_EVIDENCE': [], 'image': image, 'TARGET_SOURCE_COMMIT': SOURCE,
            'SOURCE_COMMIT': runtime.source_commit(),
            'SOURCE_BRANCH': runtime.git_text('branch', '--show-current'),
            'SOURCE_STATE': 'working tree; exact recovery tooling hashes recorded',
            'RECOVERY_TOOL_SHA256': {str(p.relative_to(ROOT)): runtime.sha256(p) for p in (
                Path(__file__).resolve(), ROOT / 'tools/diagnostics/r0f_successor_emulator.py',
                ROOT / 'tools/diagnostics/d81_delivery.py',
                ROOT / 'tools/diagnostics/d81_foundation_compare.py',
                ROOT / runtime.ORACLE_SOURCE)},
            'retiredPhysicalIdentity': 'R0FSUCC10.D81; chooser ERROR CODE FF',
            'authorization': '2026-09-21 owner requested fresh construction and R0FSUC10 native-slot fill',
        })
        manifest['STRUCTURAL_VALIDATOR_IDENTITY']['sha256']['r0f_successor_emulator.py'] = runtime.sha256(ROOT / 'tools/diagnostics/r0f_successor_emulator.py')
        runtime.write_json(manifest_path, manifest)
        print(f'{args.filename}: fresh construction, structure, payloads PASS; {image["sha256"]}', flush=True)
    if args.host_only:
        return
    attempt = 1
    while (output / f'attempt-{attempt}').exists():
        attempt += 1
    runtime.OUT = output / f'attempt-{attempt}'
    runtime.OUT.mkdir()
    # Each runtime revalidation starts with an independently fresh build and
    # extraction, not just trust in a prior manifest. Keep prior evidence.
    reconstructed = runtime.OUT / 'fresh-host-check'
    reconstructed.mkdir()
    checked_image = runtime.fresh_d81(
        reconstructed, reconstructed / args.filename, runtime.CANONICAL_LABEL, inputs)
    if checked_image['sha256'] != runtime.sha256(canonical):
        raise ValueError('fresh reconstruction differs from immutable candidate')
    manifest.update(image=checked_image, HOST_STRUCTURAL_RESULT='PASS',
                    HOST_CONTENT_RESULT='PASS', D81_STATE='HOST_CONTENT_VERIFIED',
                    XEMU_RESULT='NOT RUN', XEMU_EVIDENCE=[])
    manifest['CURRENT_DELIVERY_TOOL_SHA256'] = {
        str(p.relative_to(ROOT)): runtime.sha256(p) for p in (
            ROOT / 'tools/diagnostics/d81_delivery.py',
            ROOT / 'tools/diagnostics/d81_sd_transfer.sh',
            ROOT / 'tools/diagnostics/d81_sd_contiguity.py',
            ROOT / 'tools/diagnostics/d81_fat32_audit.py',
        )}
    runtime.CANONICAL = canonical
    runtime.CANONICAL_NAME = args.filename
    runtime.SOURCE_BRANCH = runtime.git_text('branch', '--show-current')
    classes = runtime.OUT / 'classes'
    classes.mkdir(exist_ok=True)
    runtime.checked_run([runtime.platform_build.JAVA / 'javac', '-Xlint:all', '-Werror',
                         '-d', classes, ROOT / runtime.ORACLE_SOURCE])
    # Use the established T04 runtime and independent oracle, with truthful
    # new carrier name, working-tree provenance and immutable target identity.
    manifest['VALIDATION_TOOL_SHA256'] = {str(p.relative_to(ROOT)): runtime.sha256(p) for p in (
        Path(__file__).resolve(), ROOT / 'tools/diagnostics/r0f_successor_emulator.py',
        ROOT / runtime.ORACLE_SOURCE)}
    runtime.write_json(output / 'host-gate.json', manifest)
    runtime.carrier_tests()
    final = runtime.read_json(output / 'host-gate.json')
    final['TARGET_SOURCE_COMMIT'] = SOURCE
    final['SOURCE_STATE'] = manifest['SOURCE_STATE']
    runtime.write_json(manifest_path, final)
    retained = ROOT / 'docs/evidence/r0f/successor/2026-09-21-recovery' / args.filename[:-4]
    if retained.exists():
        retained = retained / f'attempt-{attempt}'
    retained.mkdir(parents=True, exist_ok=False)
    for name in ('release.json', 'construction.log'):
        shutil.copyfile(output / name, retained / name)
    shutil.copyfile(runtime.OUT / 'carrier-summary.json', retained / 'carrier-summary.json')
    shutil.copyfile(reconstructed / 'construction.log', retained / 'fresh-reconstruction.log')
    for run in (runtime.OUT / 'carrier-source-freeze').iterdir():
        target = retained / run.name
        target.mkdir()
        for name in ('evidence.json', 'result.bin', 'saved.prg', 'oracle.txt',
                     'screen.png', 'screen.txt', 'xemu.log', 'post-structure.json'):
            shutil.copyfile(run / name, target / name)
    print(f'{args.filename}: XEMU_BOOT_VERIFIED; canonical unchanged; physical NOT RUN', flush=True)


if __name__ == '__main__':
    main()
