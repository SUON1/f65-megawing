#!/usr/bin/env python3
import hashlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1])
manifest = json.loads((root / 'spec/manifests/spec-corpus.json').read_text())
for document in manifest['documents']:
    relative = document.get('relative_path')
    if relative and document.get('present'):
        actual = hashlib.sha256((root / relative).read_bytes()).hexdigest()
        if actual != document['sha256']:
            raise SystemExit(f'corpus hash mismatch: {relative}')
ledger = json.loads((root / 'memory/r0a-memory-ledger.json').read_text())
if any(region.get('must_remain_untouched') and region['r0a_allocation'] for region in ledger['physical_regions']):
    raise SystemExit('measured-limits reserve was allocated')
base_page = ledger.get('r0a_base_page', {})
if base_page != {'logical_abi_registers': '$0002-$0021', 'physical_window_when_b_02': '$0202-$0221', 'lto_direct_page_allocation': 0}:
    raise SystemExit('invalid R0-A B-register base-page ledger')
lock = json.loads((root / 'toolchain/f65_toolchain.lock.json').read_text())
llvm_mos = lock['llvm_mos']
if llvm_mos.get('release') != 'v23.1.0' or llvm_mos.get('sdk_release_commit') != '7e47e7d':
    raise SystemExit('R0-A requires LLVM-MOS SDK v23.1.0 / 7e47e7d')
if llvm_mos.get('lto_direct_page_allocation') != '-mlto-zp=0 for R0-A; no general compiler-managed LTO direct-page allocation is admitted.':
    raise SystemExit('R0-A requires -mlto-zp=0')
vice = lock.get('vice', {})
if vice.get('version') != '3.10' or not vice.get('c1541_sha256') or not vice.get('petcat_sha256') or vice.get('role') != 'deterministic D81 format/write/list validation; not a MEGA65 runtime emulator':
    raise SystemExit('R0-A requires the pinned VICE D81 container tool')
for relative, expected in (
    ('toolchain/vice/VICE.app/Contents/Resources/bin/c1541', vice['c1541_sha256']),
    ('toolchain/vice/VICE.app/Contents/Resources/bin/petcat', vice['petcat_sha256']),
):
    actual = hashlib.sha256((root / relative).read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f'VICE tool hash mismatch: {relative}')
scope = json.loads((root / 'docs/plans/r0-a-ownership-map.json').read_text())
if not scope['authorized_prefixes'] or not scope['prohibited_prefixes']:
    raise SystemExit('invalid scope policy')
print('R0A-CFG-001 PASS: corpus, ledger reserve, and scope policy validated')
