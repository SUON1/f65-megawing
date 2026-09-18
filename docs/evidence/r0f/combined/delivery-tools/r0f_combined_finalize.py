#!/usr/bin/env python3
"""Close CF001 construction-report encoding gap without altering the candidate.

The original c1541 invocation completed its writes, but Python's UTF-8 output
decoder failed on PETSCII format output. Independently reproduce all bytes in a
fresh session and fresh directory, capture raw output losslessly, and require
the identical image hash. Never append to or rewrite the original D81.
"""
import json
import re
import subprocess
import sys
import r0f_combined_build as cf

def construction():
    cf.current()
    destination=cf.OUT/'construction-replay';destination.mkdir()
    image=destination/cf.CARRIER_NAME;c1541=cf.ROOT/'toolchain/vice-clean/bin/c1541'
    cf.pf.pin(c1541,'73235289aca30a7e2e8067e521bf604743156cc1d7499c888a3894d6e46fcb3c')
    args=[str(x) for x in [c1541,'-format',cf.CARRIER_LABEL+',65','d81',image,
      '-write',cf.OUT/'AUTOBOOT.C65','autoboot.c65','-write',cf.OUT/'F65-R0F-PROOF.prg','r0f-proof',
      '-write',cf.OUT/'R0F-EVID.txt','r0f-evid','-list']]
    result=subprocess.run(args,cwd=cf.ROOT,capture_output=True)
    (destination/'stdout.bin').write_bytes(result.stdout);(destination/'stderr.bin').write_bytes(result.stderr)
    text=result.stdout.decode('latin-1');(cf.OUT/'construction.log').write_text(text)
    if result.returncode or result.stderr or re.search(r'warning|error|failed|fatal|duplicate|truncat|allocation',text,re.I):raise ValueError('construction diagnostics')
    if image.read_bytes()!=(cf.OUT/cf.CARRIER_NAME).read_bytes():raise ValueError('fresh replay differs; no delivery')
    report={'command':args,'exit':result.returncode,'stdoutSha256':cf.sha(destination/'stdout.bin'),
      'stderrBytes':len(result.stderr),'d81Sha256':cf.sha(image),'matchOriginal':'BYTE_FOR_BYTE',
      'originalMutated':False,'construction':'fresh format plus all three writes in one session',
      'diagnosis':'PETSCII format-output byte is not UTF-8; binary capture plus latin-1 lossless reporting'}
    (cf.OUT/'construction-replay.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)

def tests():
    proof=json.loads((cf.OUT/'construction-replay.json').read_text())
    if proof['d81Sha256']!=cf.sha(cf.OUT/cf.CARRIER_NAME):raise ValueError('construction proof stale')
    boots=[]
    for mode in ('1','1','0','0'):
        directory,report=cf.xemu(mode,True,False)
        boots.append({'directory':str(directory.relative_to(cf.ROOT)),**report})
        (cf.OUT/'carrier-test-progress.json').write_text(json.dumps(boots,indent=2)+'\n')
    path=cf.OUT/'manifests/r0f-d81-release.json';r=json.loads(path.read_text())
    r.update(D81_STATE='XEMU_BOOT_VERIFIED',XEMU_RESULT='PASS',XEMU_EVIDENCE=boots,CONSTRUCTION_REPLAY=proof)
    path.write_text(json.dumps(r,indent=2)+'\n')

if __name__=='__main__':
    if sys.argv[1:]==['construction']:construction()
    elif sys.argv[1:]==['tests']:tests()
    else:raise SystemExit('usage: r0f_combined_finalize.py construction|tests')
