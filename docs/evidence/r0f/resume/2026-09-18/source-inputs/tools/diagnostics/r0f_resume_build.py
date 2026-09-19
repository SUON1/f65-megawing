#!/usr/bin/env python3
"""RH001 isolated no-restart development test. NO SD/hardware delivery path.

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
import hashlib
import json
import pathlib
import re
import signal
import subprocess
import sys
import time
import r0f_platform_build as pf
from d81_foundation_compare import Image

ROOT=pf.ROOT
OUT=ROOT/'build/r0f/resume'
PRG=OUT/'R0F-RESUME.prg'
CONTRACT=ROOT/'interfaces/r0f_resume_contract.json'
SOURCES=['src/diagnostics/r0f/resume.c','src/diagnostics/r0f/resume_model.c',
         'src/diagnostics/r0f/combined_model.c','src/diagnostics/r0f/combined_platform.c',
         'src/platform/r0f/resume_45gs02.s','src/platform/r0f/combined_45gs02.s',
         'src/platform/r0f/qualification_45gs02.s','src/platform/r0a_platform_45gs02.s']
ORACLE='tools/generators/src/main/java/f65/tools/R0FResumeOracle.java'
COMMANDS=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(args,**kw):
    args=list(map(str,args));COMMANDS.append(args)
    return subprocess.run(args,cwd=ROOT,check=True,**kw)
def write_json(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
def build():
    OUT.mkdir(parents=True,exist_ok=True)
    c=json.loads(CONTRACT.read_text())
    h='/* Generated from r0f_resume_contract.json. */\n#ifndef R0FR_GENERATED_H\n#define R0FR_GENERATED_H\n'
    for group,prefix in [('constants',''),('states','S_'),('events','E_')]:
        h+=''.join(f'#define R0FR_{prefix}{k} {v}u\n' for k,v in c[group].items())
    (ROOT/'interfaces/generated/r0f_resume.h').write_text(h+'#endif\n')
    run(['/usr/bin/clang','-std=c11','-Wall','-Wextra','-Wconversion','-Werror','-fsanitize=address,undefined',
         '-Iinterfaces/generated','-Isrc/diagnostics/r0f','src/diagnostics/r0f/resume_model.c',
         'tools/diagnostics/r0f_resume_host_test.c','-o',OUT/'host-test'])
    native=run([OUT/'host-test'],capture_output=True,text=True).stdout
    (OUT/'host-test.txt').write_text(native);print(native,flush=True)
    pf.pin(pf.TOOLS/'mos-mega65-clang','cc557ae99a68ed36e098062b0f5376a878e94ac187b87446c8e603e4fb45a906')
    pf.pin(pf.TOOLS/'llvm-objdump','5327f031a741bfcd4104317fbad3d1e45275d70b49821f0da52391120848a8e9')
    run([pf.TOOLS/'mos-mega65-clang','-mcpu=mos45gs02','-mlto-zp=0','-Oz','-fno-inline-functions',
         '-Wall','-Wextra','-Wconversion','-Werror','-Iinterfaces/generated','-Isrc/diagnostics/r0f',*SOURCES,
         '-Wl,-T,src/platform/r0f/startup.ld',f'-Wl,-Map,{OUT/"R0F-RESUME.map"}','-o',PRG])
    elf=pathlib.Path(str(PRG)+'.elf')
    for tool,args,suffix in [('llvm-nm',[],'symbols'),('llvm-objdump',['-d','--print-imm-hex'],'disassembly')]:
        (OUT/f'R0F-RESUME.{suffix}').write_bytes(run([pf.TOOLS/tool,*args,elf],capture_output=True).stdout)
    dis=(OUT/'R0F-RESUME.disassembly').read_text();symbols=(OUT/'R0F-RESUME.symbols').read_text()
    def symbol(name):return int(re.search(r'^([0-9a-f]+) [Tt] '+name+r'$',symbols,re.M)[1],16)
    if not symbol('r0fr_kernel_snapshot')<symbol('f65_basepage_enter')<symbol('__do_zero_bss'):
        raise ValueError('KERNAL snapshot must precede C base-page and BSS initialization')
    # Pinned assembler's relaxed 16-bit branches landed one byte early in
    # Xemu. Use explicit short inverse branch + absolute JMP in this wrapper.
    for pc,op in re.findall(r'^\s*([0-9a-f]+): ([0-9a-f]{2}) ',dis,re.M):
        if symbol('r0fr_kernel_snapshot')<=int(pc,16)<symbol('r0fr_storage_end') and int(op,16) in {0x13,0x33,0x53,0x73,0x83,0x93,0xb3,0xd3,0xf3}:
            raise ValueError('unadmitted long branch in RH001 wrapper')
    for n in range(32):
        if not re.search(rf'^000000{n+2:02x} A __rc{n}$',symbols,re.M):raise ValueError('compiler base-page ABI')
    wrapper=dis.split('<r0fr_storage>:',1)[1].split('<r0fc_rom_toggle>:',1)[0]
    allowed={0xff87,0xff84,0xff8a,0xff81,0xffcc,0xff41,0xff90,0xff6b,0xffba,0xffbd,0xffd5,0xffd8}
    seen=set()
    for line in dis.splitlines():
        m=re.search(r'\b(?:jsr|jmp)\s+\$([ef][0-9a-f]{3})\b',line)
        if m:
            addr=int(m[1],16)
            if addr not in allowed or line not in wrapper:raise ValueError('unadmitted ROM call '+line)
            seen.add(addr)
    if seen!=allowed:raise ValueError('missing public API operation')
    # Disassembler annotations for absolute ROM addresses can be printed as
    # nearest-symbol+offset. Gate numeric targets, not those annotations.
    platform=int(re.search(r'^([0-9a-f]+) T r0f_pf_enter$',symbols,re.M)[1],16)
    for dest in re.findall(r'\bjsr\s+\$([0-9a-f]+)',wrapper):
        if int(dest,16) not in allowed|{platform}:raise ValueError('callback across KERNAL boundary '+dest)
    mapping=(OUT/'R0F-RESUME.map').read_text();sections={}
    for name in ('.basic_header','.text','.rodata','.data','.bss','.noinit','.zp.data','.zp.bss'):
        m=re.search(r'^\s*([0-9a-f]+)\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+'+re.escape(name)+r'$',mapping,re.M)
        if not m:raise ValueError('section '+name)
        start,size=(int(x,16) for x in m.groups());sections[name]={'start':start,'bytes':size}
        if size and (start<0x2001 or start+size>0x8000):raise ValueError('resident range '+name)
    if '__stack = 0xd000' not in mapping:raise ValueError('stack top')
    pf.pin(pf.JAVA/'java','34b9c157bedcebafc6033b8beaa72c2ff14e2b697e33f45aa959a8373d6581a0')
    pf.pin(pf.JAVA/'javac','ee7be919e8bc4f364a1de24c245eea5ff8bb8f5560c8eb182ad3e89007adb152')
    (OUT/'classes').mkdir(exist_ok=True)
    run([pf.JAVA/'javac','-Xlint:all','-Werror','-d',OUT/'classes',ORACLE])
    print(run([pf.JAVA/'java','-cp',OUT/'classes','f65.tools.R0FResumeOracle','--model'],capture_output=True,text=True).stdout,flush=True)
    inputs=SOURCES+[str(CONTRACT.relative_to(ROOT)),'interfaces/generated/r0f_resume.h',
      'src/diagnostics/r0f/resume_model.h','src/diagnostics/r0f/combined_model.h','src/diagnostics/r0f/combined_platform.h',
      'interfaces/r0f_combined_contract.json','interfaces/generated/r0f_combined.h','src/platform/r0f/startup.ld',
      'tools/diagnostics/r0f_resume_build.py','tools/diagnostics/r0f_resume_host_test.c',ORACLE,
      'tools/diagnostics/d81_foundation_compare.py','docs/decisions/R0-F-RH001-NO-RESTART-HANDOFF.md',
      'memory/r0f-resume-memory-ledger.json',
      '00_D81_LOADABILITY_GATE.md']
    write_json(OUT/'accounting.json',{'identity':'RH001-DEVELOPMENT-ONLY','prgSha256':sha(PRG),
       'inputs':{p:sha(ROOT/p) for p in inputs},'sections':sections,'commands':COMMANDS,
       'sourceCommit':run(['git','rev-parse','HEAD'],capture_output=True,text=True).stdout.strip(),
       'sourceState':'dirty tree; per-input hashes authoritative','reserveBytes':0,'physical':'NOT RUN','fullAcceptance':False})
    print('RH001 compile/link/static checks PASS',flush=True)

def c154(args):
    tool=ROOT/'toolchain/vice-clean/bin/c1541'
    pf.pin(tool,'73235289aca30a7e2e8067e521bf604743156cc1d7499c888a3894d6e46fcb3c')
    r=run([tool,*args],capture_output=True,text=True,encoding='latin-1')
    if r.stderr or re.search(r'warning|error|failed|fatal|duplicate|truncat|allocation',r.stdout,re.I):raise ValueError('c1541 diagnostic '+r.stdout+r.stderr)
    return r.stdout

def check_disk(image,expected):
    d=Image(image);h=d.sector((40,0))
    if h[2]!=0x44 or (d.label,d.identifier)!=('RH001 XEMU','65'):raise ValueError('D81 header/identity')
    for s,link in [(1,bytes((40,2))),(2,bytes((0,255)))]:
        b=d.sector((40,s))
        if b[:2]!=link or b[2:4]!=bytes((0x44,0xbb)) or b[4:6]!=h[22:24]:raise ValueError('BAM header')
    for loc in d.directory_sectors:
        b=d.sector(loc)
        if loc[0]!=40 or loc in {(40,0),(40,1),(40,2)} or (not b[0] and b[1]!=255):raise ValueError('directory metadata')
    if [e['name'] for e in d.entries]!=list(expected):raise ValueError('payload list')
    extracted=image.parent/f'extracted-{time.time_ns()}';extracted.mkdir()
    for e in d.entries:
        p=extracted/e['name'];c154([image,'-read',e['name'],p])
        wanted=expected[e['name']]
        if p.read_bytes()!=wanted or e['payloadSha256']!=hashlib.sha256(wanted).hexdigest():raise ValueError('D81 content '+e['name'])
    listing=c154([image,'-list'])
    reported=re.search(r'(\d+) blocks free',listing,re.I)
    # c1541 excludes unused track-40 directory sectors from its free count.
    excluded=sum(1 for s in range(40) if (40,s) not in d.occupied)
    if not reported or int(reported[1])!=d.free_blocks-excluded:raise ValueError('free count')
    report=d.describe()
    report['extracted']={name:str(extracted/name) for name in expected}
    return report

def xemu(mode):
    if mode not in ('0','1'):raise ValueError('video standard')
    a=json.loads((OUT/'accounting.json').read_text())
    if sha(PRG)!=a['prgSha256'] or any(sha(ROOT/p)!=h for p,h in a['inputs'].items()):raise ValueError('stale build')
    folder=OUT/f'xemu-{mode}-{time.time_ns()}';folder.mkdir()
    token=b'\x00\x20'+bytes(i^0x65 for i in range(32))
    token_path=folder/'TOKEN.prg';token_path.write_bytes(token)
    boot_source=folder/'autoboot.bas';boot_source.write_text('10 bank 0\n20 load "rh001",8,1\n30 run\n')
    petcat=ROOT/'toolchain/vice/VICE.app/Contents/Resources/bin/petcat'
    pf.pin(petcat,'a2d0416c3a9f0361792990f0fa2b55cd50e297363148898b9a8b4326597fb433')
    boot=folder/'AUTOBOOT.C65'
    r=run([petcat,'-w65','-o',boot,'--',boot_source],capture_output=True)
    if r.stderr:raise ValueError('tokenization diagnostic')
    expected={'autoboot.c65':boot.read_bytes(),'rh001':PRG.read_bytes(),'token':token}
    image=folder/'RH001IO.D81'
    if image.exists():raise ValueError('never overwrite fixture')
    log=c154(['-format','RH001 XEMU,65','d81',image,'-write',boot,'autoboot.c65',
               '-write',PRG,'rh001','-write',token_path,'token','-list'])
    (folder/'construction.log').write_text(log)
    initial=check_disk(image,expected)
    write_json(folder/'host-gate.json',{'state':'HOST_CONTENT_VERIFIED','structural':'PASS','content':'PASS',
       'image':initial,'entry':'AUTOBOOT.C65 -> RH001','source':a,'hardwareRelease':False,
       'sdTransfer':'NOT PERFORMED','physicalChooser':'NOT RUN'})
    emulator=ROOT/'toolchain/xemu/xmega65';rom=pathlib.Path('/Users/slice/Documents/Codex/f65-megawing/MEGA65.ROM')
    pf.pin(emulator,'dd37baf7846b9696adcb662ffe5da040031b07214c66aef9a7f48cc30040b738')
    pf.pin(rom,'af3c447f791a2fdc48cb21e1bd3fab015e32641228d9d30d21259b9e878c6fa0')
    sd=folder/'disposable-sd.img'
    run(['/bin/cp','-c','/Users/slice/Library/Application Support/xemu-lgb/mega65/mega65.img',sd])
    args=[emulator,'-skipconfigfile','-headless','-fastboot','-videostd',mode,'-fastclock','40.5',
          '-rom',rom,'-sdimg',sd,'-8',image,'-autoload','-dumpscreen',folder/'screen.txt',
          '-dumpmem',folder/'memory.bin','-screenshot',folder/'screen.png']
    with (folder/'xemu.log').open('wb') as out:
        p=subprocess.Popen(list(map(str,args)),cwd=ROOT,stdout=out,stderr=subprocess.STDOUT)
        print('RH001 Xemu running: '+str(folder),flush=True)
        try:
            p.wait(timeout=80)
        except subprocess.TimeoutExpired:
            p.send_signal(signal.SIGTERM);p.wait(timeout=10)
        finally:
            if p.poll() is None:p.kill();p.wait()
    mem=(folder/'memory.bin').read_bytes();result=mem[0x1900:0x1a00]
    (folder/'result.bin').write_bytes(result)
    print('result='+result[:64].hex(),flush=True)
    if (folder/'screen.txt').exists():print((folder/'screen.txt').read_text()[:2400],flush=True)
    if result[:6]!=b'RRH1\x01\x7f' or result[6]:raise ValueError('target incomplete/failed; retain debug dump '+str(folder))
    screen=(folder/'screen.txt').read_text()
    if 'ROM RESTORED / FILE LOADED SAVED RELOADED / C RESUMED' not in screen or 'NOT FULL R0-F ACCEPTANCE' not in screen:
        raise ValueError('final display incomplete')
    if hashlib.sha256(mem[0x20000:0x40000]).hexdigest()!=sha(rom):raise ValueError('independent ROM hash')
    saved=result[166:168]+result[96:128]
    saved_path=folder/'expected-saved.prg';saved_path.write_bytes(saved)
    post=check_disk(image,{**expected,'rhstate':saved})
    actual_saved=pathlib.Path(post['extracted']['rhstate'])
    oracle=run([pf.JAVA/'java','-cp',OUT/'classes','f65.tools.R0FResumeOracle',folder/'result.bin',actual_saved],capture_output=True,text=True).stdout
    (folder/'oracle.txt').write_text(oracle);print(oracle,flush=True)
    write_json(folder/'evidence.json',{'identity':'RH001','video':mode,'tier':'XEMU_DISPOSABLE_STORAGE_FIXTURE',
      'resultSha256':sha(folder/'result.bin'),'prgSha256':a['prgSha256'],'initialD81Sha256':initial['sha256'],
      'postTransactionD81Sha256':post['sha256'],'postTransactionStructureAndContent':'PASS','oracle':'PASS',
      'extractedSaveSha256':sha(actual_saved),'extractedSavePath':str(actual_saved),
      'screenshotSha256':sha(folder/'screen.png'),'source':a,
      'commands':COMMANDS+[list(map(str,args))],'fullAcceptance':False,'physical':'NOT RUN','hardwareRelease':False})

if __name__=='__main__':
    if sys.argv[1:]==['build']:build()
    elif len(sys.argv)==3 and sys.argv[1]=='xemu':xemu(sys.argv[2])
    else:raise SystemExit('usage: r0f_resume_build.py build | xemu 0|1 (no SD release)')
