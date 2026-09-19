#!/usr/bin/env python3
"""Exact CF001 native-slot admission; no SD write before all local gates."""
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import r0f_combined_build as cf

MOUNT=pathlib.Path('/Volumes/MEGA65FDISK')
SLOT=MOUNT/'F65BLK02.D81'
BLANK_SHA='ba963e2c0e8dd686e03568b41ca9d4c6196762e166a2de8a6fcbb829dd5bd4e8'

def blank(data):
    if len(data)!=819200:raise ValueError('slot size')
    def sec(t,s):return data[((t-1)*40+s)*256:((t-1)*40+s+1)*256]
    h=sec(40,0)
    if h[:3]!=bytes((40,3,0x44)):raise ValueError('slot header')
    if sec(40,3)!=bytes((0,255))+bytes(254):raise ValueError('not an untouched empty directory')
    for t in range(1,81):
        b=sec(40,1 if t<=40 else 2);i=16+((t-1)%40)*6
        expected=bytes((36,240,255,255,255,255)) if t==40 else bytes((40,255,255,255,255,255))
        if b[i:i+6]!=expected:raise ValueError('blank BAM track '+str(t))
        if b[2:6]!=bytes((0x44,0xbb))+h[22:24]:raise ValueError('blank BAM header')
    if sec(40,1)[:2]!=bytes((40,2)) or sec(40,2)[:2]!=bytes((0,255)):raise ValueError('blank BAM chain')

def inspect():
    if SLOT.is_symlink() or not SLOT.is_file():raise ValueError('exact native slot absent')
    data=SLOT.read_bytes();blank(data)
    if hashlib.sha256(data).hexdigest()!=BLANK_SHA:raise ValueError('native blank changed since read-only inspection')
    if (cf.ROOT/'build/d81-sd-transfer/F65BLK02.D81.slot-post.json').exists():raise ValueError('slot has prior delivery evidence; no reuse')
    print('F65BLK02 native blank: empty-directory/BAM/exact preimage PASS; extent not implied',flush=True)

def fill():
    cf.current()
    release_path=cf.OUT/'manifests/r0f-d81-release.json';r=json.loads(release_path.read_text())
    if r['D81_STATE']!='XEMU_BOOT_VERIFIED' or r['XEMU_RESULT']!='PASS':raise ValueError('exact-D81 Xemu gate')
    visual=r.get('VISUAL_REVIEW',{})
    if visual.get('result')!='PASS':raise ValueError('original screenshot review required')
    boots=r['XEMU_EVIDENCE']
    if [e['video'] for e in boots]!=['1','1','0','0'] or any(e['oracle']!='PASS' or e['artifactSha256']!=r['D81_SHA256'] for e in boots):raise ValueError('four matching boot identities required')
    if cf.sha(cf.OUT/cf.CARRIER_NAME)!=r['D81_SHA256']:raise ValueError('candidate hash')
    if len(visual.get('boots',[]))!=len(boots):raise ValueError('visual review count')
    for boot,review in zip(boots,visual['boots']):
        if review['directory']!=boot['directory'] or review['result']!='PASS' or review['screenshotSha256']!=cf.sha(cf.ROOT/boot['directory']/'screen.png'):raise ValueError('visual review identity')
    inspect()
    if os.geteuid()!=0:raise SystemExit('Validated local gates. Run this exact fill action with sudo for read-only raw FAT32 access and guarded native-slot fill.')
    helper=cf.ROOT/'tools/diagnostics/d81_sd_fill_mega65_slot.sh'
    proc=subprocess.run([str(helper),str(cf.OUT/cf.CARRIER_NAME),str(MOUNT),r['D81_SHA256']],cwd=cf.ROOT,capture_output=True,text=True)
    (cf.OUT/'sd-fill.log').write_text(proc.stdout+proc.stderr);print(proc.stdout+proc.stderr,flush=True)
    if proc.returncode:raise SystemExit(proc.returncode)
    if 'safe_eject=PASS' not in proc.stdout:raise ValueError('no eject evidence')
    audit=cf.ROOT/'build/d81-sd-transfer';pre=json.loads((audit/'F65BLK02.D81.slot-pre.json').read_text());post=json.loads((audit/'F65BLK02.D81.slot-post.json').read_text())
    from d81_sd_contiguity import same_allocation
    if not same_allocation(pre,post) or post['SD_EXTENT_COUNT']!=1 or post['D81_SHA256']!=r['D81_SHA256']:raise ValueError('allocation/hash evidence')
    r.update(D81_STATE='AWAITING_PHYSICAL_CHOOSER_VERIFICATION',SD_COPY_SHA256=post['D81_SHA256'],
      SD_FILESYSTEM=post['SD_FILESYSTEM'],SD_TRANSFER_METHOD='MEGA65 native empty F65BLK02 slot, exact-size in-place fill',
      SD_CONTIGUITY_RESULT='PASS',SD_EXTENT_COUNT=1,SD_EXTENT_EVIDENCE={'before':pre,'after':post},SD_SAFE_EJECT_RESULT='PASS')
    release_path.write_text(json.dumps(r,indent=2)+'\n')

if __name__=='__main__':
    if sys.argv[1:]==['inspect']:inspect()
    elif sys.argv[1:]==['fill']:fill()
    else:raise SystemExit('usage: r0f_combined_sd.py inspect|fill')
