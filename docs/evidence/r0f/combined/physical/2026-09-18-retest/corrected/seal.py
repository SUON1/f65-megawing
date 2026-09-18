import pathlib,json,hashlib,subprocess,shutil
R=pathlib.Path('/Users/slice/Documents/ChatGPT/F65 Megawing');T=pathlib.Path('/tmp/r0f-corrected.3qt691');O=R/'docs/evidence/r0f/combined/physical/2026-09-18-retest/corrected'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
boots=json.loads((O/'fresh-xemu.json').read_text());assert len(boots)==2 and {r['video'] for r in boots}=={'0','1'}
for r in boots:assert r['oracle']=='PASS' and r['fault']==0 and r['ticks']==2640
v=json.loads((O/'verification.json').read_text());v['phase3ExistingCandidateVerification']='PASS_WITH_EXPLICIT_FULL_R0F_COVERAGE_GAPS';v['freshXemuModes']=['NTSC','PAL'];v['transportNegativesRejected']=8;v['retainedXemuCapturesRevalidated']=9;v['realEdgesDetected']=4;v['realEdgesConsumed']=4
(O/'verification.json').write_text(json.dumps(v,indent=2)+'\n')
shutil.copyfile(T/'seal.py',O/'seal.py')
for p in O.rglob('*.json'):json.loads(p.read_text())
manifest=''.join(f'{sha(p)}  {p.relative_to(O)}\n' for p in sorted(O.rglob('*')) if p.is_file() and p.name!='SHA256SUMS')
(O/'SHA256SUMS').write_text(manifest)
p=subprocess.run(['/usr/bin/shasum','-a','256','-c','SHA256SUMS'],cwd=O,capture_output=True,text=True);assert p.returncode==0,p.stderr
subprocess.run(['git','diff','--check'],cwd=R,check=True)
print(f'Corrected evidence SHA256 manifest PASS: {len(manifest.splitlines())} files; JSON validation PASS; git diff --check PASS')
