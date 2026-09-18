import sys,pathlib,json,subprocess,hashlib,shutil
R=pathlib.Path('/Users/slice/Documents/ChatGPT/F65 Megawing');T=pathlib.Path('/tmp/r0f-corrected.3qt691');O=R/'docs/evidence/r0f/combined/physical/2026-09-18-retest/corrected'
sys.path.insert(0,str(R/'tools/diagnostics'));import r0f_combined_build as cf
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
account=cf.current();release=cf.OUT/'manifests/r0f-d81-release.json';release_before=sha(release)
compile_cmd=next(a for a in account['commands'] if str(a[0]).endswith('mos-mega65-clang'))
target=T/'target';target.mkdir(exist_ok=True)
cmd=[s.replace(str(cf.OUT),str(target)) for s in compile_cmd]
p=subprocess.run(cmd,cwd=R,capture_output=True,text=True);(O/'target-compile.txt').write_text(p.stdout+p.stderr)
assert p.returncode==0 and sha(target/'R0F-COMBINED.prg')==account['prgSha256']
(O/'target-reproduction.json').write_text(json.dumps({'command':cmd,'exit':p.returncode,'prgSha256':sha(target/'R0F-COMBINED.prg'),'matchesCandidate':True},indent=2)+'\n')
boots=[]
for mode in ('1','0'):
 d,report=cf.xemu(mode,True,False)
 dest=O/d.name;dest.mkdir()
 for name in ('result.bin','durations.bin','evidence.json','oracle.txt','screen.png','screen.txt','xemu.log','memory.bin','accounting.json'):
  shutil.copyfile(d/name,dest/name)
 boots.append({'directory':d.name,**report})
 (O/'fresh-xemu.json').write_text(json.dumps(boots,indent=2)+'\n')
assert sha(release)==release_before
print('TARGET BYTE REPRODUCTION AND FRESH NTSC/PAL EXACT-CARRIER XEMU PASS; release manifest unchanged',flush=True)
