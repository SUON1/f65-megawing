#!/usr/bin/env python3
"""Read-only returned-file checks for G2-L; never assert physical photo evidence.

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

Read docs/D81_WORKFLOW.md as well.
This tool reads images and writes new host evidence only; it never executes a
target, modifies an image, opens a raw card or authorizes a physical run.
"""
import argparse
import json
from pathlib import Path

from d81_direct_delivery import verify_release
from d81_foundation_compare import Image
import r0f_group1_export_probe as probe
import r0f_group1_reduce as oracle
from r0f_group2_experiment import verify_inputs
from r0f_group2_target_admission import ROOT, sha


def validate_returned(actual, initial, expected_save):
    if list(actual) != [*initial, 'rsstate']:
        raise ValueError('Returned directory must contain only four inputs and RSSTATE')
    for name, payload in initial.items():
        if actual[name] != payload:
            raise ValueError('Pre-existing payload changed: ' + name)
    if actual['rsstate'] != expected_save:
        raise ValueError('Returning SAVE differs from independent oracle/address')


def inspect(image, release_path, output):
    release = json.loads(release_path.read_text())
    canonical = release_path.parent / release['D81_FILENAME']
    verify_release(canonical, release_path)
    if release['CASE'] != 'G2-L-EXPORT-COLLISION' or image.name != release['D81_FILENAME']:
        raise ValueError('Case/exact returned filename mismatch')
    experiment = Path(release['SOURCE_BUILD'])
    build = json.loads((experiment / 'result.json').read_text())
    linked = json.loads((experiment / 'linked-artifacts.json').read_text())
    verify_inputs(experiment, linked['files'])
    if (build['prgSha256'] != release['PROGRAM_SHA256']
            or sha(experiment / 'CANDIDATE.prg') != release['PROGRAM_SHA256']):
        raise ValueError('Program freeze mismatch')
    # Saved data is the existing 32-byte checksum fixture, not the 512-byte
    # lifecycle result. Its target load address comes from the admitted link.
    symbols = (experiment / 'symbols.txt').read_text()
    before_checksum = int(oracle.golden((1600, 3200))[0], 16)
    payload = probe.emulator.save_bytes(before_checksum)[2:]
    expected_save = probe.integration.symbol(symbols, 'r0fsi_payload').to_bytes(2, 'little') + payload
    host = json.loads((release_path.parent / 'host-gate.json').read_text())
    initial = {entry['name']: Path(host['image']['extracted'][entry['name']]).read_bytes()
               for entry in host['image']['entries']}
    if list(initial) != ['autoboot.c65', 'r0fsucc', 'token', 'g1t00']:
        raise ValueError('Collision stimulus identity missing')
    import hashlib
    for entry in Image(canonical).entries:
        if hashlib.sha256(initial[entry['name']]).hexdigest() != entry['payloadSha256']:
            raise ValueError('Original extraction drift')
    if not output.is_relative_to(ROOT / 'build/r0f/group2'):
        raise ValueError('Evidence output must be in the Group 2 host build directory')
    output.mkdir(parents=True, exist_ok=False)
    before = sha(image)
    actual = probe.extract_actual(image, output, [*initial, 'rsstate'], release['DISK_LABEL'])
    validate_returned(actual, initial, expected_save)
    if sha(image) != before:
        raise ValueError('Read-only acquisition changed the image')
    result = {'result': 'RETURNED_FILE_CHECKS_PASS_OPERATOR_PHOTO_PENDING',
              'case': release['CASE'], 'image': str(image), 'returnedImageSha256': before,
              'canonicalImageSha256': release['D81_SHA256'],
              'preExistingPayloads': 'PASS', 'extraTraceFiles': 0, 'returningSave': 'PASS',
              'expectedScreen': 'G1 EXPORT S:5 E:03 F:00',
              'physicalChooser': 'SEPARATE OWNER EVIDENCE REQUIRED',
              'physicalOperatorPhoto': 'NOT CHECKED', 'physicalTiming': 'NOT PROVEN',
              'fullLifecycleResult': 'NOT ON CARD', 'group2Complete': False}
    (output / 'validation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--image', required=True, type=Path)
    parser.add_argument('--release', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    inspect(args.image.resolve(), args.release.resolve(), args.out.resolve())


if __name__ == '__main__':
    main()
