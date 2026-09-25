#!/usr/bin/env python3
"""Build and run the T06 fault-0x58 physical diagnostic carrier.

MANDATORY D81 LOADABILITY GATE

Before creating, modifying, copying, renaming, packaging, mounting, testing, or releasing any D81, read and obey the repository-root file 00_D81_LOADABILITY_GATE.md.

The work must fail closed. A D81 may not be called final, test-ready, loadable, or delivered for physical testing until the exact artifact passes every applicable state in this order:

UNVERIFIED
-> HOST_STRUCTURALLY_VERIFIED
-> HOST_CONTENT_VERIFIED
-> XEMU_BOOT_VERIFIED
-> SD_COPY_VERIFIED
-> SD_CONTIGUITY_VERIFIED
-> PHYSICAL_CHOOSER_VERIFIED
-> TEST_ELIGIBLE

Never build a new test carrier by copying an existing D81 and reopening the copy in a second c1541 session to append files. Fresh-format the image and populate all files in one pinned-tool construction session.

ERROR CODE FF at the MEGA65 chooser is a hard chooser/attach-stage failure. Retire that tested copy and diagnose D81 construction, exact copied bytes, SD physical allocation, safe ejection, and platform identity before assigning a replacement. Do not patch, append to, rename, or re-test the failed copy and do not blame the program inside it.

A matching hash of the SD-card copy is necessary but not sufficient. The MEGA65 Freezer requires a disk-image file to occupy one contiguous FAT32 extent. A fragmented file can hash perfectly and still fail to mount with ERROR CODE FF. Do not submit a copied image to the physical chooser until an independent extent check reports exactly one extent.
"""

import argparse
import json
from pathlib import Path
import shutil
import sys

from d81_delivery import require_name
import r0f_platform_build as platform_build
import r0f_successor_emulator as runtime


ROOT = platform_build.ROOT
NAME = 'R0FDIAG2.D81'
LABEL = 'R0F DIAG T06'
OUT = ROOT / 'build/r0f/successor-t06-diagnostic'
CANONICAL_DIR = OUT / 'canonical'
CANONICAL = CANONICAL_DIR / NAME
RETAINED = (ROOT / 'docs/evidence/r0f/successor/'
            '2026-09-21-recovery/R0FDIAG2')
PRG = ROOT / 'build/r0f/successor-integration/R0F-SUCCESSOR-INTEGRATION.prg'
ACCOUNTING = ROOT / 'build/r0f/successor-integration/accounting.json'
SYMBOLS = (ROOT / 'build/r0f/successor-integration/'
           'R0F-SUCCESSOR-INTEGRATION.symbols')
PREDECESSOR = ROOT / 'docs/evidence/r0f/successor/2026-09-21'
EXPECTED_BOOT = (
    464, '9bdf352c44c411965229f68b2d92c358f08f0e6ef6486142115b53c9da246cc7')
EXPECTED_TOKEN = (
    34, '0e8d0ac2ce727ba51285be0173ea784b52b56fdc4729a1f7c0d2d7271005b572')


def require_file(path, expected):
    length, digest = expected
    if path.stat().st_size != length or runtime.sha256(path) != digest:
        raise ValueError('input identity drift: ' + str(path))


def configure(prg_bytes, prg_sha):
    runtime.OUT = OUT
    runtime.PRG = PRG
    runtime.ACCOUNTING = ACCOUNTING
    runtime.SYMBOLS = SYMBOLS
    runtime.EXPECTED_PRG_BYTES = prg_bytes
    runtime.EXPECTED_PRG_SHA256 = prg_sha
    runtime.CANONICAL_NAME = NAME
    runtime.CANONICAL_LABEL = LABEL
    runtime.CANONICAL = CANONICAL
    runtime.SOURCE_BRANCH = runtime.git_text('branch', '--show-current')
    runtime.EXPECTED_SCREEN_LINES = (
        'DEVELOPMENT EVIDENCE - NOT R0-F ACCEPTANCE',
        'SUCCESSOR HOST/STATIC IMAGE - RUNTIME UNVERIFIED',
        'FAULT   STATE   TICK    MASK  NMI',
        'RESERVE BEFORE   RESERVE AFTER',
        'RESULT CRC32',
    )


def retain():
    RETAINED.mkdir(parents=True, exist_ok=True)

    def copy_once(source, destination):
        if destination.exists():
            if runtime.sha256(source) != runtime.sha256(destination):
                raise ValueError('retained evidence identity mismatch: ' + str(destination))
            return
        shutil.copyfile(source, destination)

    for source, name in (
            (CANONICAL_DIR / 'host-gate.json', 'release.json'),
            (CANONICAL_DIR / 'construction.log', 'construction.log'),
            (OUT / 'carrier-summary.json', 'carrier-summary.json'),
            (ACCOUNTING, 'target-accounting.json')):
        copy_once(source, RETAINED / name)
    summary = json.loads((OUT / 'carrier-summary.json').read_text())
    if summary['result'] != 'PASS' or len(summary['runs']) != 4:
        raise ValueError('four passing Xemu runs required before retention')
    for evidence in summary['runs']:
        run = OUT / 'carrier-source-freeze' / evidence['run']
        destination = RETAINED / evidence['run']
        destination.mkdir(exist_ok=True)
        for name in ('evidence.json', 'result.bin', 'saved.prg', 'oracle.txt',
                     'screen.png', 'screen.txt', 'xemu.log',
                     'post-structure.json'):
            copy_once(run / name, destination / name)
    failed_log = OUT / 'carrier-source-freeze/ntsc-1/xemu.log'
    if failed_log.is_file() and not (OUT / 'carrier-source-freeze/ntsc-1/result.bin').exists():
        failed_destination = RETAINED / 'failed-xemu-environment'
        failed_destination.mkdir(exist_ok=True)
        copy_once(failed_log, failed_destination / 'xemu.log')


def main():
    global NAME, LABEL, OUT, CANONICAL_DIR, CANONICAL, RETAINED
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('command', choices=['all', 'resume-xemu', 'retain-xemu'])
    parser.add_argument('--name', required=True, help='new, exact uppercase FAT 8.3 identity')
    args = parser.parse_args()
    require_name(args.name)
    if args.name in ('R0FDIAG1.D81', 'R0FDIAG2.D81', 'R0FHOST1.D81', 'R0FSUCC10.D81'):
        raise ValueError('retired identity; never rebuild or reuse')
    NAME = args.name
    LABEL = NAME[:-4]
    OUT = ROOT / 'build/r0f/d81-workflow' / NAME[:-4]
    CANONICAL_DIR = OUT / 'canonical'
    CANONICAL = CANONICAL_DIR / NAME
    RETAINED = ROOT / 'docs/evidence/r0f/successor/2026-09-22-workflow' / NAME[:-4]
    require_name(NAME)
    if args.command == 'retain-xemu':
        gate = json.loads((CANONICAL_DIR / 'host-gate.json').read_text())
        if (gate['D81_STATE'] != 'XEMU_BOOT_VERIFIED'
                or gate['D81_FILENAME'] != NAME
                or runtime.sha256(CANONICAL) != gate['D81_SHA256']):
            raise ValueError('Xemu gate or canonical identity mismatch')
        retain()
        print(f'{NAME}: XEMU_BOOT_VERIFIED evidence retained')
        return
    if args.command == 'resume-xemu':
        if RETAINED.exists() or not CANONICAL.is_file():
            raise ValueError('resume requires an unretained, existing canonical image')
        gate = json.loads((CANONICAL_DIR / 'host-gate.json').read_text())
        if (gate['D81_STATE'] != 'HOST_CONTENT_VERIFIED'
                or gate['D81_FILENAME'] != NAME
                or runtime.sha256(CANONICAL) != gate['D81_SHA256']):
            raise ValueError('resume canonical host gate or identity mismatch')
        prg_bytes = PRG.stat().st_size
        prg_sha = runtime.sha256(PRG)
        if (prg_bytes != gate['TARGET_PRG_BYTES']
                or prg_sha != gate['TARGET_PRG_SHA256']
                or runtime.sha256(ACCOUNTING) != gate['TARGET_ACCOUNTING_SHA256']):
            raise ValueError('resume target input identity drift')
        failed_run = OUT / 'carrier-source-freeze/ntsc-1'
        if not failed_run.is_dir() or (failed_run / 'result.bin').exists():
            raise ValueError('resume requires retained failed ntsc-1 environment run')
        configure(prg_bytes, prg_sha)
        runtime.carrier_tests((('1', 2), ('1', 3), ('0', 1), ('0', 2)))
        retain()
        print(f'{NAME}: HOST_CONTENT_VERIFIED -> XEMU_BOOT_VERIFIED')
        print(f'd81_sha256={gate["D81_SHA256"]}')
        print('SD / physical NOT RUN')
        return
    if OUT.exists() or RETAINED.exists():
        raise ValueError('candidate identity already exists; never overwrite or reuse')
    runtime.checked_run([
        sys.executable, '-B',
        'tools/diagnostics/r0f_successor_integration.py', 'build',
    ])
    accounting = json.loads(ACCOUNTING.read_text())
    prg_bytes = PRG.stat().st_size
    prg_sha = runtime.sha256(PRG)
    if (accounting['prgBytes'] != prg_bytes
            or accounting['prgSha256'] != prg_sha):
        raise ValueError('target accounting identity mismatch')
    configure(prg_bytes, prg_sha)
    boot = PREDECESSOR / 'AUTOBOOT.C65'
    token = PREDECESSOR / 'TOKEN.prg'
    require_file(boot, EXPECTED_BOOT)
    require_file(token, EXPECTED_TOKEN)
    CANONICAL_DIR.mkdir(parents=True)
    image = runtime.fresh_d81(
        CANONICAL_DIR, CANONICAL, LABEL,
        {'autoboot.c65': boot, 'r0fsucc': PRG, 'token': token})
    CANONICAL.chmod(0o444)
    classes = OUT / 'classes'
    classes.mkdir()
    runtime.checked_run([
        platform_build.JAVA / 'javac', '-Xlint:all', '-Werror',
        '-d', classes, ROOT / runtime.ORACLE_SOURCE,
    ])
    fault_codes = json.loads((
        ROOT / 'interfaces/r0f_successor_integration_contract.json'
    ).read_text())['diagnosticFaults']
    manifest = {
        'identity': 'R0F-T06-PHYSICAL-FAULT-DIAGNOSTIC',
        'D81_FILENAME': NAME,
        'D81_STATE': 'HOST_CONTENT_VERIFIED',
        'D81_SHA256': image['sha256'],
        'D81_BYTES': image['bytes'],
        'DISK_LABEL': LABEL,
        'DISK_ID': runtime.CANONICAL_ID,
        'ENTRY_FILENAME': 'AUTOBOOT.C65 -> R0FSUCC',
        'SOURCE_BRANCH': runtime.SOURCE_BRANCH,
        'SOURCE_COMMIT': runtime.source_commit(),
        'SOURCE_STATE': 'working tree; exact accounting input hashes retained',
        'TARGET_PRG_BYTES': prg_bytes,
        'TARGET_PRG_SHA256': prg_sha,
        'TARGET_ACCOUNTING_SHA256': runtime.sha256(ACCOUNTING),
        'HOST_STRUCTURAL_RESULT': 'PASS',
        'HOST_CONTENT_RESULT': 'PASS',
        'XEMU_RESULT': 'NOT RUN',
        'XEMU_EVIDENCE': [],
        'SD_COPY_SHA256': None,
        'SD_FILESYSTEM': None,
        'SD_TRANSFER_METHOD': None,
        'SD_CONTIGUITY_RESULT': 'NOT RUN',
        'SD_EXTENT_COUNT': None,
        'SD_EXTENT_EVIDENCE': None,
        'SD_SAFE_EJECT_RESULT': 'NOT RUN',
        'PHYSICAL_CHOOSER_RESULT': 'NOT RUN',
        'PHYSICAL_EVIDENCE': None,
        'PHYSICAL_RUNTIME_RESULT': 'NOT RUN',
        'diagnosticFaults': fault_codes,
        'construction': 'fresh format plus all payload writes in one pinned c1541 invocation',
        'image': image,
        'fullAcceptance': False,
    }
    runtime.write_json(CANONICAL_DIR / 'host-gate.json', manifest)
    runtime.carrier_tests()
    retain()
    print(f'{NAME}: HOST_CONTENT_VERIFIED -> XEMU_BOOT_VERIFIED')
    print(f'd81_sha256={image["sha256"]}')
    print(f'prg_sha256={prg_sha}')
    print('SD / physical NOT RUN')


if __name__ == '__main__':
    main()
