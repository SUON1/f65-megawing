from pathlib import Path
import json,sys
sys.path.insert(0,str(Path.cwd()/'tools/diagnostics'))
import r0f_group1_export_probe as probe
root=Path.cwd()
source=root/'build/r0f/group1/integration/irq-read-negative-07/NEGATIVE.prg'
out=root/'build/r0f/group1/integration/label-probe-03'
out.mkdir(exist_ok=False)
runtime=probe.emulator
expected='739e' # replaced below by checked source hash manifest
prior=runtime.read_json(source.parent/'injection.json')
assert prior['source']['prgSha256']=='ec259fc7611d8bb5809d15f6c333f5b224df4c945a8e9ffca5b2402d8444cb30'
assert runtime.sha256(source)==runtime.read_json(source.parent/'validation.json')['injectedPrgSha256']
data=bytearray(source.read_bytes())
changes=[]
runtime.PRG=out/'LABELPROBE.prg';runtime.PRG.write_bytes(data)
runtime.SOURCE_BRANCH=runtime.git_text('branch','--show-current')
runtime.write_json(out/'injection.json',{'scope':'screen row versus character-code diagnosis only','sourcePrgSha256':runtime.sha256(source),'programSha256':runtime.sha256(runtime.PRG),'changes':changes})
image=out/'G1LAB01.D81';token=root/'docs/evidence/r0f/successor/2026-09-21/TOKEN.prg'
initial=runtime.fresh_d81(out,image,'G1 LABEL PROBE',{'token':token})
result,env=runtime.run_xemu(out,'1',image,'GROUP1_DISPLAY_DIAGNOSTIC',False,90)
decoded=runtime.decode_result(result)
runtime.write_json(out/'validation.json',{'result':decoded,'environment':env,'sourcePrgSha256':runtime.sha256(source),'programSha256':runtime.sha256(runtime.PRG),'initialD81Sha256':initial['sha256'],'physical':'NOT RUN'})
print('fault',decoded['fault'],'tickAfter',decoded['tickAfter'])
