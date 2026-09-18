import sys,pathlib,json,hashlib,subprocess,shutil,textwrap
R=pathlib.Path('/Users/slice/Documents/ChatGPT/F65 Megawing');T=pathlib.Path('/tmp/r0f-corrected.3qt691');O=R/'docs/evidence/r0f/combined/physical/2026-09-18-retest/corrected'
sys.path.insert(0,str(R/'tools/diagnostics'));import r0f_combined_build as cf
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for p in ('verify.py','phase3.py','post.py'):shutil.copyfile(T/p,O/p)
shutil.copyfile(R/'build/r0f/combined/xemu-d81-1-1789761135551983000/xemu.log',O/'xemu-sandbox-failed.log')
cf.pf.pin(cf.pf.TOOLS/'mos-mega65-clang','cc557ae99a68ed36e098062b0f5376a878e94ac187b87446c8e603e4fb45a906')
cf.pf.pin(cf.pf.TOOLS/'llvm-objdump','5327f031a741bfcd4104317fbad3d1e45275d70b49821f0da52391120848a8e9')
source=R/'tools/diagnostics/r0f_combined_build.py';text=source.read_text()
checks=textwrap.dedent(text.split("    elf=pathlib.Path(str(PRG)+'.elf')",1)[1].split("    pf.pin(pf.JAVA/'java'",1)[0])
checks="elf=pathlib.Path(str(PRG)+'.elf')\n"+checks
env=vars(cf).copy();env.update(OUT=T/'target',PRG=T/'target/R0F-COMBINED.prg')
exec(compile(checks,str(source),'exec'),env)
c=json.loads(cf.CONTRACT.read_text())
header='/* Generated from r0f_combined_contract.json. */\n#ifndef R0FC_GENERATED_H\n#define R0FC_GENERATED_H\n'+''.join(f'#define R0FC_{k} {v}ul\n' for k,v in c['constants'].items())+''.join(f'#define R0FC_O_{k.upper()} {v}u\n' for k,v in c['result']['offsets'].items())+'#endif\n'
assert header==(R/'interfaces/generated/r0f_combined.h').read_text()
for name in ('R0F-COMBINED.map','R0F-COMBINED.symbols','R0F-COMBINED.disassembly'):shutil.copyfile(T/'target'/name,O/name)
static={'result':'PASS','generatedHeader':'EXACT_MATCH','buildCheckSourceSha256':sha(source),'executedStaticCheckSha256':hashlib.sha256(checks.encode()).hexdigest(),'sections':env['sections'],'commands':cf.COMMANDS}
(O/'static-checks.json').write_text(json.dumps(static,indent=2)+'\n')
b=(O/'result.bin').read_bytes();u16=lambda a:int.from_bytes(b[a:a+2],'little');u32=lambda a:int.from_bytes(b[a:a+4],'little')
one=('version','stage','fault','reference','video','speed','base_page','cpu_port','rom_state','nmi','features','trap_flags','snapshot_high','queue_high','controlled_faults','tier_mask')
two=('duration_address','duration_bytes','irq_count','dma_jobs','storage_rejects','hardware_stack','software_stack','active_slots','calibration_samples')
fields={k:(b[v] if k in one else u16(v) if k in two else u32(v)) for k,v in c['result']['offsets'].items() if k!='phase_swaps'}
(O/'decoded-result.json').write_text(json.dumps(fields,indent=2)+'\n')
p=subprocess.run([sys.executable,str(O/'verify_capture.py')],capture_output=True,text=True,check=True);(O/'capture-reproduction.txt').write_text(p.stdout)
print(p.stdout);print('STATIC CHECKS AND GENERATED HEADER PASS')
