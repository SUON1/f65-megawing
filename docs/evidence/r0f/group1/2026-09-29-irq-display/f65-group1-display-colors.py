import sys,json,re
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'tools/diagnostics'))
import r0f_group1_export_probe as p
r=p.emulator
case=sys.argv[1]; out=Path('build/r0f/group1/integration')/('display-colors-'+case+'-01');out.mkdir(exist_ok=False)
build=out.parent; src=(build/'GROUP1.prg').read_bytes(); data=bytearray(src); syms=(build/'symbols.txt').read_text(); dis=(build/'disassembly.txt').read_text()
sym=lambda n:p.integration.symbol(syms,n)
load=int.from_bytes(src[:2],'little'); ofs=lambda a:a-load+2
flag=sym('r0f_pf_nmi_seen' if case=='early' else 'r0fg1_irq_error');begin=sym('r0fg1_irq_begin'); assert data[ofs(begin)]==0xd8
data[ofs(begin):ofs(begin)+6]=bytes([0xa9,1,0x8d,flag&255,flag>>8,0x60])
main=dis.split('<main>:',1)[1].split('\n\n',1)[0]
loops=re.findall(r'^\s*([0-9a-f]+):\s+80 fe\s+bra',main,re.M)
assert len(loops)==1,loops
loop=int(loops[0],16); codeaddr=0xbb00; dest=sym('transfer')
code=bytes([0x8d,0x11,0xd0,0xa2,0x7f,0xbd,0x00,0xd0,0x9d,dest&255,dest>>8,0xca,0x10,0xf7,0x80,0xfe])
request=sym('r0f_pf_copy_request');copy=sym('r0f_pf_flat_copy')
code=bytearray(code[:-2])
for offset in range(0,2000,255):
 values=(0xff80000+offset).to_bytes(4,'little')+(0x50000+offset).to_bytes(4,'little')+bytes([min(255,2000-offset)])
 for i,value in enumerate(values):
  address=request+i
  code.extend([0xa9,value,0x8d,address&255,address>>8])
 code.extend([0x20,copy&255,copy>>8])
code.extend([0x80,0xfe])
assert codeaddr+len(code)<0xc000
assert len(data)+load-2 < codeaddr
data.extend(bytes(ofs(codeaddr)+len(code)-len(data)))
data[ofs(codeaddr):ofs(codeaddr)+len(code)]=code
assert data[ofs(loop)-3:ofs(loop)]==bytes([0x8d,0x11,0xd0])
data[ofs(loop)-3:ofs(loop)]=bytes([0x4c,codeaddr&255,codeaddr>>8])
r.PRG=out/'REGISTERS.prg';r.PRG.write_bytes(data); r.SOURCE_BRANCH=r.git_text('branch','--show-current')
r.write_json(out/'injection.json',dict(scope='terminal-only VIC register snapshot; disposable diagnostic',sourcePrg=r.sha256(build/'GROUP1.prg'),prgSha256=r.sha256(r.PRG),destination=dest,loop=loop,code=code.hex()))
image=out/'G1REG02.D81';r.fresh_d81(out,image,'G1 REGISTERS',{'token':r.ROOT/'docs/evidence/r0f/successor/2026-09-21/TOKEN.prg'})
r.run_xemu(out,'1',image,'DISPLAY_DIAGNOSTIC',False,60 if case=='early' else 180)
m=(out/'memory.bin').read_bytes();r.write_json(out/'registers.json',{f'D{i:03X}':f'{m[dest+i]:02X}' for i in range(128)})
print('registers captured',case)

print('colors',m[0x50000:0x50060].hex())
