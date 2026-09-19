import hashlib,json,pathlib,subprocess,sys,zlib,shutil,os
R=pathlib.Path('/Users/slice/Documents/ChatGPT/F65 Megawing');T=pathlib.Path('/tmp/r0f-corrected.3qt691')
E=R/'docs/evidence/r0f/combined/physical/2026-09-18-retest';O=E/'corrected';O.mkdir(exist_ok=True)
J=pathlib.Path('/Users/slice/Documents/Codex/f65-megawing/toolchain/runtime/jdk-full/jdk-21.0.12+8/Contents/Home/bin')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
records=[]
def run(name,args,cwd=R):
 p=subprocess.run(list(map(str,args)),cwd=cwd,capture_output=True,text=True)
 (O/(name+'.txt')).write_text(p.stdout+p.stderr)
 records.append({'name':name,'command':list(map(str,args)),'cwd':str(cwd),'exit':p.returncode})
 (O/'commands.json').write_text(json.dumps(records,indent=2)+'\n')
 print(name,p.returncode,p.stdout,p.stderr,flush=True);assert p.returncode==0,name
 return p.stdout
for n in ('segment.py','recognize.py','apply_corrections.py','manual-training.json','corrections.json','uncertain.py','absolute_review.py','row_review.py','photo12-row4.png','photo15-lastrows.png','uncertain-raw.png','absolute-review.png'):
 shutil.copyfile(T/n,O/n)
shutil.copytree(T/'transcripts',O/'transcripts',dirs_exist_ok=True)
for n in range(4,18):
 for suffix in ('rows.txt','coords.json'):
  shutil.copyfile(T/f'{n:02}-{suffix}',O/f'{n:02}-{suffix}')
b=(O/'transcripts/capture.bin').read_bytes();assert len(b)==7072
(O/'result.bin').write_bytes(b[:1792]);(O/'durations.bin').write_bytes(b[1792:])
assert zlib.crc32(b[:1788])==0x32b8a599 and zlib.crc32(b[1792:])==0x105995a3
assert sha(J/'java')=='34b9c157bedcebafc6033b8beaa72c2ff14e2b697e33f45aa959a8373d6581a0'
assert sha(J/'javac')=='ee7be919e8bc4f364a1de24c245eea5ff8bb8f5560c8eb182ad3e89007adb152'
classes=T/'fresh-classes';classes.mkdir(exist_ok=True)
run('javac',[J/'javac','-Xlint:all','-Werror','-d',classes,'tools/generators/src/main/java/f65/tools/R0FCombinedOracle.java'])
base=[J/'java','-cp',classes,'f65.tools.R0FCombinedOracle']
run('java-model',base+['--model'])
run('java-pages',base+['--pages']+sorted((O/'transcripts').glob('page-*.txt')))
run('java-binary',base+[O/'result.bin',O/'durations.bin'])
run('host-compile',['/usr/bin/clang','-std=c11','-Wall','-Wextra','-Wconversion','-Werror','-fsanitize=address,undefined','-Iinterfaces/generated','-Isrc/diagnostics/r0f','src/diagnostics/r0f/combined_model.c','tools/diagnostics/r0f_combined_host_test.c','-o',T/'host-test'])
run('host-test',[T/'host-test'])
sys.path.insert(0,str(R/'tools/diagnostics'));import r0f_combined_build as cf
account=cf.current()
run('retained-pre-sd-sha',['/usr/bin/shasum','-a','256','-c','SHA256SUMS'],R/'docs/evidence/r0f/combined')
run('retained-intake-sha',['/usr/bin/shasum','-a','256','-c','SHA256SUMS'],E)
originals=json.loads((E/'originals.json').read_text())
for p in originals:assert sha(pathlib.Path(p['source']))==p['sha256']==sha(E/p['retained'])
# Execute the unchanged gate's complete structural/content checks only; omit
# its release-record writer to preserve the already-delivered candidate state.
gate=R/'tools/diagnostics/r0f_d81_loadability_gate.py';text=gate.read_text();prefix=text.split('branch=subprocess.run',1)[0]
assert prefix.endswith('\n') and 'extraction/hash mismatch' in prefix
old=sys.argv;sys.argv=[str(gate),str(R),str(cf.OUT/cf.CARRIER_NAME)];os.environ['F65_R0F_VARIANT']='combined'
exec(compile(prefix,str(gate),'exec'),{'__file__':str(gate)});sys.argv=old
gatecheck={'mode':'unchanged validator prefix through all structural/content/extraction checks; release-record writer omitted','sourceSha256':sha(gate),'executedPrefixSha256':hashlib.sha256(prefix.encode()).hexdigest(),'result':'PASS','d81Sha256':sha(cf.OUT/cf.CARRIER_NAME)}
(O/'host-d81-gate.json').write_text(json.dumps(gatecheck,indent=2)+'\n')
report={'result':'PASS','resultCrc32':f'{zlib.crc32(b[:1788]):08X}','durationCrc32':f'{zlib.crc32(b[1792:]):08X}','captureSha256':sha(O/'transcripts/capture.bin'),'resultSha256':sha(O/'result.bin'),'durationSha256':sha(O/'durations.bin'),'oracleSourceSha256':sha(R/cf.ORACLE),'sourceInputsVerified':len(account['inputs']),'originalFilesVerified':len(originals),'d81Sha256':sha(cf.OUT/cf.CARRIER_NAME),'prgSha256':sha(cf.PRG),'fullR0FAcceptance':False}
(O/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2),flush=True)
