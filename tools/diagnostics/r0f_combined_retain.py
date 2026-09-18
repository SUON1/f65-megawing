#!/usr/bin/env python3
"""Retain exact CF001 generated evidence, never disposable SD images or ROM."""
import json
import pathlib
import shutil
import r0f_combined_build as cf

def main():
    cf.current()
    release=json.loads((cf.OUT/'manifests/r0f-d81-release.json').read_text())
    if release['XEMU_RESULT']!='PASS':raise ValueError('exact carrier not verified')
    destination=cf.ROOT/'docs/evidence/r0f/combined'
    if destination.exists():raise ValueError('retained set already exists; do not overwrite')
    destination.mkdir()
    names=['R0F-COMBINED.prg','R0F-COMBINED.prg.elf','R0F-COMBINED.map','R0F-COMBINED.symbols',
      'R0F-COMBINED.disassembly','accounting.json','host-test.txt','java-model.txt','construction.log',
      cf.CARRIER_NAME,'AUTOBOOT.C65','F65-R0F-PROOF.prg','R0F-EVID.txt','manifests/r0f-d81-release.json',
      'construction-replay.json','construction-replay/stdout.bin','construction-replay/stderr.bin']
    for name in names:
        target=destination/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(cf.OUT/name,target)
        if cf.sha(cf.OUT/name)!=cf.sha(target):raise ValueError('retention identity '+name)
    sources=[cf.ROOT/boot['directory'] for boot in release['XEMU_EVIDENCE']]
    sources += [cf.ROOT/boot['directory'] for boot in release['VISUAL_REVIEW']['diagnosticRuns']]
    for path in cf.OUT.glob('xemu-dev-*/evidence.json'):
        e=json.loads(path.read_text())
        if e.get('prgSha256')==cf.sha(cf.PRG) and e.get('oracle')=='PASS':sources.append(path.parent)
    for source in sources:
        target=destination/source.name;target.mkdir()
        for path in source.iterdir():
            if path.is_file() and path.suffix in ('.json','.bin','.png','.txt','.log','.prg'):
                shutil.copy2(path,target/path.name)
                if cf.sha(path)!=cf.sha(target/path.name):raise ValueError('retention identity '+path.name)
    # Delivery helpers are independently retained, not target build inputs.
    helpers=destination/'delivery-tools';helpers.mkdir()
    for name in ('r0f_combined_sd.py','d81_sd_fill_mega65_slot.sh','d81_sd_contiguity.py'):
        shutil.copy2(cf.ROOT/'tools/diagnostics'/name,helpers/name)
    inputs=destination/'source-inputs';inputs.mkdir()
    account=json.loads((cf.OUT/'accounting.json').read_text())
    for name in account['inputs']:
        target=inputs/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(cf.ROOT/name,target)
    for name in ('r0f_combined_finalize.py','r0f_combined_retain.py','r0f_combined_visual_probe.py','r0f_combined_visual_review.py'):
        shutil.copy2(cf.ROOT/'tools/diagnostics'/name,helpers/name)
    entries=sorted(p for p in destination.rglob('*') if p.is_file())
    (destination/'SHA256SUMS').write_text(''.join(f'{cf.sha(p)}  {p.relative_to(destination)}\n' for p in entries))
    print('Retained '+str(len(entries))+' hashed artifacts in '+str(destination))

if __name__=='__main__':main()
