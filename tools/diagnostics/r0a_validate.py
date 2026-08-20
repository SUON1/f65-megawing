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
scope = json.loads((root / 'docs/plans/r0-a-ownership-map.json').read_text())
if not scope['authorized_prefixes'] or not scope['prohibited_prefixes']:
    raise SystemExit('invalid scope policy')
print('R0A-CFG-001 PASS: corpus, ledger reserve, and scope policy validated')
