#!/usr/bin/env python3
"""CF001 development build and fail-closed emulator evidence. No SD writes."""
import hashlib
import json
import pathlib
import re
import signal
import subprocess
import sys
import time
import os
import socket
import tempfile
import r0f_platform_build as pf

ROOT=pf.ROOT
OUT=ROOT/'build/r0f/combined'
PRG=OUT/'R0F-COMBINED.prg'
CONTRACT=ROOT/'interfaces/r0f_combined_contract.json'
SOURCES=['src/diagnostics/r0f/combined.c','src/diagnostics/r0f/combined_model.c',
         'src/diagnostics/r0f/combined_platform.c','src/platform/r0f/combined_45gs02.s',
         'src/platform/r0f/qualification_45gs02.s','src/platform/r0a_platform_45gs02.s']
COMMANDS=[]
CARRIER_NAME='F65BLK02.D81'
CARRIER_LABEL='F65 CF001'
ORACLE='tools/generators/src/main/java/f65/tools/R0FCombinedOracle.java'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(args,**kw):
    args=list(map(str,args));COMMANDS.append(args)
    return subprocess.run(args,cwd=ROOT,check=True,**kw)
def build():
    OUT.mkdir(parents=True,exist_ok=True)
    c=json.loads(CONTRACT.read_text())
    header='/* Generated from r0f_combined_contract.json. */\n#ifndef R0FC_GENERATED_H\n#define R0FC_GENERATED_H\n'
    header+=''.join(f'#define R0FC_{k} {v}ul\n' for k,v in c['constants'].items())
    header+=''.join(f'#define R0FC_O_{k.upper()} {v}u\n' for k,v in c['result']['offsets'].items())+'#endif\n'
    (ROOT/'interfaces/generated/r0f_combined.h').write_text(header)
    run(['/usr/bin/clang','-std=c11','-Wall','-Wextra','-Wconversion','-Werror','-fsanitize=address,undefined',
         '-Iinterfaces/generated','-Isrc/diagnostics/r0f','src/diagnostics/r0f/combined_model.c',
         'tools/diagnostics/r0f_combined_host_test.c','-o',OUT/'host-test'])
    native=run([OUT/'host-test'],capture_output=True,text=True).stdout
    (OUT/'host-test.txt').write_text(native);print(native,flush=True)
    pf.pin(pf.TOOLS/'mos-mega65-clang','cc557ae99a68ed36e098062b0f5376a878e94ac187b87446c8e603e4fb45a906')
    pf.pin(pf.TOOLS/'llvm-objdump','5327f031a741bfcd4104317fbad3d1e45275d70b49821f0da52391120848a8e9')
    run([pf.TOOLS/'mos-mega65-clang','-mcpu=mos45gs02','-mlto-zp=0','-Oz','-fno-inline-functions','-Wall','-Wextra','-Wconversion','-Werror',
         '-Iinterfaces/generated','-Isrc/diagnostics/r0f',*SOURCES,'-Wl,-T,src/platform/r0f/startup.ld','-Wl,-T,src/platform/r0f/combined.ld',
         f'-Wl,-Map,{OUT/"R0F-COMBINED.map"}','-o',PRG])
    elf=pathlib.Path(str(PRG)+'.elf')
    for tool,args,suffix in [('llvm-nm',[],'symbols'),('llvm-objdump',['-d','--print-imm-hex'],'disassembly')]:
        (OUT/f'R0F-COMBINED.{suffix}').write_bytes(run([pf.TOOLS/tool,*args,elf],capture_output=True).stdout)
    dis=(OUT/'R0F-COMBINED.disassembly').read_text()
    if re.search(r'\b(?:jsr|jmp)\s+\$[ef][0-9a-f]{3}\b',dis):raise ValueError('ROM call')
    mapping=(OUT/'R0F-COMBINED.map').read_text();sections={}
    for name in ('.basic_header','.text','.rodata','.data','.bss','.noinit','.zp.data','.zp.bss'):
        m=re.search(r'^\s*([0-9a-f]+)\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+'+re.escape(name)+r'$',mapping,re.M)
        if not m:raise ValueError('section '+name)
        start,size=(int(x,16) for x in m.groups());sections[name]={'start':start,'bytes':size}
        if size and (start<0x2001 or start+size>0x8000):raise ValueError(f'resident range {name}: {start:x}+{size:x}')
    for name,start,size in [('.r0fc_capture',0x300,5280),('.r0fc_hot',0x17a0,347)]:
        m=re.search(r'^\s*([0-9a-f]+)\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+'+re.escape(name)+r'$',mapping,re.M)
        if not m or tuple(int(x,16) for x in m.groups())!=(start,size):raise ValueError('hot-state layout '+name)
        sections[name]={'start':start,'bytes':size}
    if '__stack = 0xd000' not in mapping:raise ValueError('software stack top')
    symbols=(OUT/'R0F-COMBINED.symbols').read_text()
    for n in range(32):
        if not re.search(rf'^000000{n+2:02x} A __rc{n}$',symbols,re.M):raise ValueError('compiler scratch ABI')
    irq=dis.split('<r0f_pf_irq>:',1)[1].split('<r0f_pf_nmi>:',1)[0]
    if re.search(r'\b(?:jsr|map|eom)\b|\$d70[05]',irq):raise ValueError('IRQ forbidden operation')
    for op in ('pha','phx','phy','phz','pla','plx','ply','plz','tab','rti'):
        if not re.search(r'\b'+op+r'\b',irq):raise ValueError('IRQ preservation '+op)
    entry=dis.split('<r0f_pf_enter>:',1)[1].split('<r0f_pf_start_irq>:',1)[0]
    if not re.search(r'lda\s+#\$0\s*\n[^\n]*\btab\b\s*\n[^\n]*lda\s+#\$35\s*\n[^\n]*sta\s+\$1\b',entry):raise ValueError('B=0 CPU port regression')
    trap=dis.split('<r0fc_rom_toggle>:',1)[1].split('<r0fc_stack_seed>:',1)[0]
    if not re.search(r'sta\s+\$d640[^\n]*\n[^\n]*\bnop\b',trap):raise ValueError('ROM trap sequence')
    pf.pin(pf.JAVA/'java','34b9c157bedcebafc6033b8beaa72c2ff14e2b697e33f45aa959a8373d6581a0')
    pf.pin(pf.JAVA/'javac','ee7be919e8bc4f364a1de24c245eea5ff8bb8f5560c8eb182ad3e89007adb152')
    (OUT/'classes').mkdir(exist_ok=True)
    run([pf.JAVA/'javac','-Xlint:all','-Werror','-d',OUT/'classes',ORACLE])
    model=run([pf.JAVA/'java','-cp',OUT/'classes','f65.tools.R0FCombinedOracle','--model'],capture_output=True,text=True).stdout
    (OUT/'java-model.txt').write_text(model);print(model,flush=True)
    inputs=SOURCES+['interfaces/r0f_combined_contract.json','interfaces/generated/r0f_combined.h',
      'src/diagnostics/r0f/combined_model.h','src/diagnostics/r0f/combined_platform.h',
      'src/platform/r0f/startup.ld','src/platform/r0f/combined.ld','docs/reports/R0-F_COMBINED_CONTRACT.md',
      'tools/diagnostics/r0f_combined_host_test.c','tools/diagnostics/r0f_combined_build.py',ORACLE,
      'memory/r0f-memory-ledger.json','interfaces/f65_platform_abi.json5',
      'tools/diagnostics/r0f_d81_loadability_gate.py','src/r0f/autoboot.bas']
    account={'identity':'CF001-DEVELOPMENT','sections':sections,'prgSha256':sha(PRG),
      'inputs':{p:sha(ROOT/p) for p in inputs},'commands':COMMANDS,'compilerSha256':sha(pf.TOOLS/'mos-mega65-clang'),
      'references':{p.name:sha(p) for p in (OUT/'references').glob('*') if p.is_file()},
      'sourceCommit':run(['git','rev-parse','HEAD'],capture_output=True,text=True).stdout.strip(),
      'sourceState':'dirty tree; per-input hashes authoritative','reserveBytes':0,'physical':'NOT RUN','fullAcceptance':False}
    (OUT/'accounting.json').write_text(json.dumps(account,indent=2)+'\n')
    print(json.dumps(sections),flush=True)
def current():
    account=json.loads((OUT/'accounting.json').read_text())
    if sha(PRG)!=account['prgSha256'] or any(sha(ROOT/p)!=s for p,s in account['inputs'].items()):raise ValueError('rebuild stale inputs')
    return account

def xemu(mode='1',carrier=False,pages=False):
    account=current()
    emulator=ROOT/'toolchain/xemu/xmega65';rom=pathlib.Path('/Users/slice/Documents/Codex/f65-megawing/MEGA65.ROM')
    pf.pin(emulator,'dd37baf7846b9696adcb662ffe5da040031b07214c66aef9a7f48cc30040b738')
    pf.pin(rom,'af3c447f791a2fdc48cb21e1bd3fab015e32641228d9d30d21259b9e878c6fa0')
    directory=OUT/f'xemu-{"d81" if carrier else "dev"}-{mode}-{time.time_ns()}';directory.mkdir()
    run(['/bin/cp',PRG,OUT/'accounting.json',directory])
    sd=directory/'disposable-sd.img'
    run(['/bin/cp','-c','/Users/slice/Library/Application Support/xemu-lgb/mega65/mega65.img',sd])
    source=OUT/CARRIER_NAME if carrier else directory/PRG.name
    original_sha=sha(source)
    if carrier:
        release=json.loads((OUT/'manifests/r0f-d81-release.json').read_text())
        if release['D81_SHA256']!=original_sha or release['HOST_CONTENT_RESULT']!='PASS':raise ValueError('host gate missing')
    sockdir=pathlib.Path(tempfile.mkdtemp(prefix='cf001-'));sockpath=sockdir/'mon'
    args=[emulator,'-skipconfigfile','-headless','-fastboot','-videostd',mode,'-fastclock','40.5',
          '-rom',rom,'-sdimg',sd,'-uartmon',sockpath,
          *(['-8',source,'-autoload'] if carrier else ['-defd81fromsd','-prg',source]),
          '-dumpscreen',directory/'screen.txt','-dumpmem',directory/'memory.bin','-screenshot',directory/'screen.png']
    with (directory/'xemu.log').open('wb') as log:
        p=subprocess.Popen(list(map(str,args)),cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
        print('CF001 Xemu running: '+str(directory),flush=True)
        try:
            try:p.wait(timeout=80)
            except subprocess.TimeoutExpired:
                if pages:check_pages(sockpath,directory)
        finally:
            if p.poll() is None:p.send_signal(signal.SIGTERM);p.wait(timeout=10)
    if sha(source)!=original_sha:raise ValueError('emulator modified artifact')
    memory=(directory/'memory.bin').read_bytes();r=memory[0x1900:0x2000];(directory/'result.bin').write_bytes(r)
    address=int.from_bytes(r[68:70],'little');raw=memory[address:address+5280];(directory/'durations.bin').write_bytes(raw)
    report={'command':list(map(str,args)),'resultSha256':sha(directory/'result.bin'),'stage':r[5],'fault':r[6],
      'romState':r[12],'ticks':int.from_bytes(r[164:168],'little'),'prgSha256':account['prgSha256'],'physical':False,
      'artifactSha256':original_sha,'tier':'EXACT_D81' if carrier else 'DIRECT_PRG','video':mode,
      'romRestoredSha256':hashlib.sha256(memory[0x20000:0x40000]).hexdigest()}
    check=run([pf.JAVA/'java','-cp',OUT/'classes','f65.tools.R0FCombinedOracle',directory/'result.bin',directory/'durations.bin'],capture_output=True,text=True).stdout
    (directory/'oracle.txt').write_text(check);print(check,flush=True)
    if report['romRestoredSha256']!=sha(rom):raise ValueError('independent full ROM hash mismatch')
    report['oracle']='PASS';report['screenshotSha256']=sha(directory/'screen.png')
    (directory/'evidence.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
    print((directory/'screen.txt').read_text(),flush=True)
    if r[:5]!=b'RCF1\x01' or r[5]!=127 or r[6]:raise ValueError('CF001 acquisition failed; no D81/SD promotion')
    return directory,report

def check_pages(path,directory):
    # Test only after acquisition. No result/code writes: virtual key register
    # and reads of the final HUD screen through the pinned UART monitor.
    with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as s:
        s.settimeout(5);s.connect(str(path))
        def command(c):
            s.sendall((c+'\r').encode());out=b''
            while not out.endswith(b'.\r\n'):
                chunk=s.recv(8192)
                if not chunk:raise ValueError('monitor disconnected')
                out+=chunk
            if b'?' in out:raise ValueError('monitor syntax '+repr(out))
            return out.decode()
        def read(at,n):
            raw=bytearray()
            for a in range(at,at+n,256):
                response=command('M '+format(a,'x'))
                lines=re.findall(r':([0-9A-F]{8}):([0-9A-F]{32})',response)
                if len(lines)!=16:raise ValueError('monitor read framing '+response)
                for i,(address,hexed) in enumerate(lines):
                    if int(address,16)!=a+i*16:raise ValueError('monitor address')
                    raw.extend(bytes.fromhex(hexed))
            return bytes(raw[:n])
        def key(code):
            command(f's ffd3615 {code:x}');time.sleep(.10);command('s ffd3615 7f');time.sleep(.65)
        data=read(0x1900,1792)+read(0x300,5280)
        if data[5]!=127 or data[6]:raise ValueError('pager requires completed acquisition')
        recovered=bytearray()
        for page in range(14):
            key(39) # N, pinned input_devices.c matrix index 0x27
            raw=read(0x40000,2000)
            text=''.join(chr(c+64) if 1<=c<=26 else chr(c) for c in raw)
            (directory/f'page-{page+1:02}.txt').write_text('\n'.join(text[i:i+80] for i in range(0,2000,80))+'\n')
            header=text[320:400];amount=416 if page==13 else 512
            if int(header[:2],16)!=page+1 or int(header[8:12],16)!=page*512 or int(header[16:20],16)!=amount:raise ValueError('pager header')
            decoded=bytes.fromhex(''.join(text[row*80:row*80+64] for row in range(6,22)))
            recovered.extend(decoded[:amount])
        if bytes(recovered)!=data:raise ValueError('screen transport differs from raw capture')
        key(41) # P, previous -> page 13
        if read(0x40140,2)!=b'0\x04':raise ValueError('previous page')
        key(13) # S summary
        summary=read(0x40000,2000)
        if summary[80:86]!=bytes((18,48,45,6,32,3)):raise ValueError('summary key')
        (directory/'pager.txt').write_text('14 pages / 7072 bytes byte-for-byte PASS; previous + summary keys tested\n')
        parsed=run([pf.JAVA/'java','-cp',OUT/'classes','f65.tools.R0FCombinedOracle','--pages',
          *[directory/f'page-{p:02}.txt' for p in range(1,15)]],capture_output=True,text=True).stdout
        (directory/'page-oracle.txt').write_text(parsed)

def package():
    account=current();image=OUT/CARRIER_NAME
    if image.exists():raise ValueError('candidate identity already exists; never overwrite/repair')
    for mode in ('0','1'):
        valid=[]
        for path in OUT.glob('xemu-dev-*/evidence.json'):
            e=json.loads(path.read_text())
            if e.get('prgSha256')==account['prgSha256'] and e.get('video')==mode and e.get('oracle')=='PASS':valid.append(e)
        if not valid:raise ValueError('current PAL/NTSC development evidence missing')
    petcat=ROOT/'toolchain/vice/VICE.app/Contents/Resources/bin/petcat'
    c1541=ROOT/'toolchain/vice-clean/bin/c1541'
    pf.pin(petcat,'a2d0416c3a9f0361792990f0fa2b55cd50e297363148898b9a8b4326597fb433')
    pf.pin(c1541,'73235289aca30a7e2e8067e521bf604743156cc1d7499c888a3894d6e46fcb3c')
    run([petcat,'-w65','-o',OUT/'AUTOBOOT.C65','--',ROOT/'src/r0f/autoboot.bas'],capture_output=True)
    detoken=run([petcat,'-65',OUT/'AUTOBOOT.C65'],capture_output=True,text=True)
    if detoken.stderr or 'load "r0f-proof",8,1' not in detoken.stdout.lower():raise ValueError('autoboot mismatch')
    (OUT/'F65-R0F-PROOF.prg').write_bytes(PRG.read_bytes())
    (OUT/'R0F-EVID.txt').write_text('CF001 combined experiment, not R0-F acceptance. Reset-only.\n'+json.dumps(account,indent=2)+'\n')
    result=run([c1541,'-format',CARRIER_LABEL+',65','d81',image,'-write',OUT/'AUTOBOOT.C65','autoboot.c65',
      '-write',OUT/'F65-R0F-PROOF.prg','r0f-proof','-write',OUT/'R0F-EVID.txt','r0f-evid','-list'],capture_output=True,text=True)
    (OUT/'construction.log').write_text(result.stdout+result.stderr)
    if result.stderr or re.search(r'warning|error|failed|fatal|duplicate|truncat|allocation',result.stdout,re.I):raise ValueError('construction diagnostic')
    run([sys.executable,'tools/diagnostics/r0f_d81_loadability_gate.py',ROOT,image],env={**os.environ,'F65_R0F_VARIANT':'combined'})

def carrier_tests():
    boots=[]
    for mode in ('1','1','0','0'):
        directory,report=xemu(mode,True,len(boots)==0);boots.append({'directory':str(directory.relative_to(ROOT)),**report})
    release=OUT/'manifests/r0f-d81-release.json';r=json.loads(release.read_text())
    r.update(D81_STATE='XEMU_BOOT_VERIFIED',XEMU_RESULT='PASS',XEMU_EVIDENCE=boots)
    release.write_text(json.dumps(r,indent=2)+'\n')
if __name__=='__main__':
    if sys.argv[1:]==['build']:build()
    elif sys.argv[1:]==['xemu']:xemu()
    elif sys.argv[1:]==['xemu-pal']:xemu('0')
    elif sys.argv[1:]==['xemu-pages']:xemu('1',False,True)
    elif sys.argv[1:]==['package']:package()
    elif sys.argv[1:]==['carrier-tests']:carrier_tests()
    else:raise SystemExit('usage: r0f_combined_build.py build|xemu|xemu-pal|xemu-pages|package|carrier-tests')
