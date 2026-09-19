import pathlib,subprocess,json,hashlib,shutil
R=pathlib.Path('/Users/slice/Documents/ChatGPT/F65 Megawing');T=pathlib.Path('/tmp/r0f-corrected.3qt691');O=R/'docs/evidence/r0f/combined/physical/2026-09-18-retest/corrected'
J='/Users/slice/Documents/Codex/f65-megawing/toolchain/runtime/jdk-full/jdk-21.0.12+8/Contents/Home/bin/java'
base=[J,'-cp',str(T/'fresh-classes'),'f65.tools.R0FCombinedOracle'];pages=sorted((O/'transcripts').glob('page-*.txt'));records=[]
for name in ('missing','duplicate','offset','mixed-crc-header','padding','raw-byte','result-byte','missing-row'):
 target=T/('negative-'+name);target.mkdir(exist_ok=True)
 copies=[]
 for p in pages:
  dest=target/p.name;shutil.copyfile(p,dest);copies.append(dest)
 if name=='missing':copies=copies[:-1]
 elif name=='duplicate':copies[-1]=copies[0]
 else:
  idx=13 if name=='padding' else 5 if name=='raw-byte' else 0
  lines=copies[idx].read_text().splitlines()
  if name=='offset':lines[0]=lines[0].replace('0000','0010',1)
  elif name=='mixed-crc-header':lines[0]=lines[0].replace('32B8A599','32B8A598')
  elif name=='padding':lines[-1]='1'+lines[-1][1:]
  elif name=='missing-row':lines.pop()
  else:lines[1]=('0' if lines[1][0]!='0' else '1')+lines[1][1:]
  copies[idx].write_text('\n'.join(lines)+'\n')
 args=base+['--pages']+list(map(str,copies));p=subprocess.run(args,capture_output=True,text=True)
 assert p.returncode!=0,name
 records.append({'case':name,'command':args,'exit':p.returncode,'stderr':p.stderr,'result':'REJECTED'})
(O/'transport-negative.json').write_text(json.dumps(records,indent=2)+'\n')
retained=[]
for p in sorted((R/'docs/evidence/r0f/combined').glob('xemu-*/result.bin')):
 args=base+[str(p),str(p.with_name('durations.bin'))];r=subprocess.run(args,capture_output=True,text=True);assert r.returncode==0,p
 retained.append({'resultFile':str(p.relative_to(R)),'command':args,'exit':r.returncode,'stdout':r.stdout})
(O/'retained-xemu-reduction.json').write_text(json.dumps(retained,indent=2)+'\n')
shutil.copyfile(T/'transport_tests.py',O/'transport_tests.py')
print(f'PASS: {len(records)} transport negatives rejected; {len(retained)} archived Xemu captures revalidated with freshly compiled Java')
