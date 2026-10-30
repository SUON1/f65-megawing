from pathlib import Path
import subprocess,sys,time,json,hashlib
r=Path('/Users/slice/Developer/f65-megawing-m2-option-b');out=r/'docs/evidence/flight-demo/2026-10-29-m2-option-b'/('text-'+str(time.time_ns()));out.mkdir()
base='9570f0ab427121a4e8f042041a14c89aaaeff9e2';reference=out/'reference_text.c';reference.write_bytes(subprocess.check_output(['git','show',base+':src/graphics/m2_rebuild_text.c'],cwd=r))
includes=['-Iinterfaces/generated','-Isrc/graphics','-Isrc/presentation','-Isrc/environment','-Isrc/core']
flags=['-std=c11','-Wall','-Wextra','-Wconversion','-Werror','-fsanitize=address,undefined']
cmds=[['/usr/bin/clang',*flags,*includes,'-Dm2rb_text_row=reference_text_row','-Dm2rb_glyph=reference_glyph','-c',str(reference),'-o',str(out/'reference.o')],['/usr/bin/clang',*flags,*includes,'src/graphics/m2_rebuild_text.c','tests/flight_demo/m2_lean/text_equivalence.c',str(out/'reference.o'),'-o',str(out/'compare')],[str(out/'compare')]]
record={'identity':'65AERO-M2-LEAN-1','scope':'host sanitizer exact formatter/glyph equivalence','base':base,'reference_sha256':hashlib.sha256(reference.read_bytes()).hexdigest(),'commands':[]}
try:
 for i,cmd in enumerate(cmds):
  result=subprocess.run(cmd,cwd=r,capture_output=True,text=True);log=str(i)+'.txt';(out/log).write_text(result.stdout+result.stderr);record['commands'].append({'argv':cmd,'exit':result.returncode,'log':log});print(result.stdout+result.stderr)
  if result.returncode:raise RuntimeError('host text check failed: '+log)
 record['result']='PASS'
except Exception as error:record['result']='FAIL';record['failure']=str(error)
finally:
 record['source_identities']={n:hashlib.sha256((r/n).read_bytes()).hexdigest() for n in ['src/graphics/m2_rebuild_text.c','tests/flight_demo/m2_lean/text_equivalence.c']}
 (out/'result.json').write_text(json.dumps(record,indent=2)+'\n');(out/'seal.json').write_text(json.dumps({p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in out.iterdir() if p.is_file()},indent=2)+'\n')
print(json.dumps({'output':str(out),'result':record['result']}));sys.exit(record['result']!='PASS')
