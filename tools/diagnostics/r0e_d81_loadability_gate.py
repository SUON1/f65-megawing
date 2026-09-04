#!/usr/bin/env python3
"""Fail-closed structural and extracted-content gate for fresh R0-E4 D81."""
import hashlib, json, pathlib, subprocess, sys, tempfile

root=pathlib.Path(sys.argv[1]).resolve(); image=pathlib.Path(sys.argv[2]).resolve(); art=root/"build/r0e/artifacts"; out=root/"build/r0e"
def fail(s): raise SystemExit("R0-E D81 loadability gate failed: "+s)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
if image.name != "F65R0E4.D81": fail("unexpected or retired carrier identity: "+image.name)
if not image.is_file() or image.stat().st_size!=819200: fail("image absent or not exact 819200 bytes")
lock=json.loads((root/"toolchain/f65_toolchain.lock.json").read_text()); b=lock["r0d_d81_builder"]; c1541=root/b["c1541_relative_path"]
if not c1541.is_file() or sha(c1541)!=b["c1541_sha256"]: fail("pinned clean c1541 identity mismatch")
d=image.read_bytes()
def sec(t,s):
 if not(1<=t<=80 and 0<=s<40): fail("out-of-range sector")
 n=((t-1)*40+s)*256; return d[n:n+256]
def name(x): return bytes(v&127 for v in x[3:19]).decode("ascii","replace").rstrip(" \xa0").lower()
h=sec(40,0)
if h[:2]!=bytes((40,3)): fail("header directory link")
label=bytes(v&127 for v in h[4:20]).decode("ascii","replace").rstrip(" \xa0"); ident=bytes(v&127 for v in h[22:24]).decode("ascii","replace").rstrip(" \xa0")
if (label,ident)!=("F65 R0-E4","65"): fail("disk label/ID mismatch")
free=set()
for t in range(1,81):
 block=sec(40,1 if t<=40 else 2); off=16+((t-1)%40)*6; bits=block[off+1:off+6]; avail={(t,s) for s in range(40) if bits[s//8]&(1<<(s%8))}
 if block[off]!=len(avail): fail("BAM count mismatch track %d"%t)
 free|=avail
entries=[]; dirs=set(); cur=(40,3)
while cur:
 if cur in dirs: fail("directory loop")
 dirs.add(cur); z=sec(*cur); cur=(z[0],z[1]) if z[0] else None
 for off in range(2,256,32):
  e=z[off:off+32]
  if e[0]:
   if e[0]!=0x82 or not e[1]: fail("invalid directory type/start")
   entries.append((name(e),(e[1],e[2]),e[28]|e[29]<<8))
expected=[("autoboot.c65",art/"AUTOBOOT.C65"),("r0e-proof",art/"F65-R0E-PROOF.prg"),("r0e-evid",art/"R0E-EVID.txt")]
if [x[0] for x in entries]!=[x[0] for x in expected]: fail("unexpected PETSCII payload list")
owned={(40,0),(40,1),(40,2)}|dirs; payload={}
for n,cur,blocks in entries:
 raw=bytearray(); seen=set()
 while cur:
  if cur in owned or cur in seen or cur[0]<1 or cur[0]>80 or cur[1]>39: fail("cross-link/range failure for "+n)
  seen.add(cur); owned.add(cur); z=sec(*cur)
  if z[0]==0:
   if not 2<=z[1]<=255: fail("invalid terminal byte count")
   raw+=z[2:z[1]+1]; cur=None
  else: raw+=z[2:]; cur=(z[0],z[1])
 if len(seen)!=blocks: fail("block count mismatch for "+n)
 payload[n]=bytes(raw)
allocated={(t,s) for t in range(1,81) for s in range(40) if (t,s) not in free}
if allocated!=owned: fail("BAM sector ownership mismatch")
def c154(args,purpose):
 r=subprocess.run([str(c1541),*args],capture_output=True,text=True)
 if r.returncode or r.stderr or any(x in r.stdout.lower() for x in ("warning","error","failed","fatal","duplicate","truncat","allocation")): fail("c1541 "+purpose+" diagnostic failure")
 return r.stdout
listing=c154([str(image),"-list"],"listing")
for n,p in expected:
 if payload[n]!=p.read_bytes(): fail("raw payload mismatch "+n)
 with tempfile.TemporaryDirectory(prefix="r0e-d81-") as td:
  x=pathlib.Path(td)/n; c154([str(image),"-read",n,str(x)],"extraction "+n)
  if not x.is_file() or x.read_bytes()!=p.read_bytes(): fail("extraction/hash mismatch "+n)
branch=subprocess.run(["git","branch","--show-current"],cwd=root,capture_output=True,text=True,check=True).stdout.strip(); commit=subprocess.run(["git","rev-parse","HEAD"],cwd=root,capture_output=True,text=True,check=True).stdout.strip()
release={"D81_STATE":"HOST_CONTENT_VERIFIED","D81_FILENAME":image.name,"D81_SHA256":sha(image),"D81_BYTES":819200,"DISK_LABEL":label,"DISK_ID":ident,"ENTRY_FILENAME":"AUTOBOOT.C65 -> R0E-PROOF","SOURCE_BRANCH":branch,"SOURCE_COMMIT":commit,"BUILDER_IDENTITY":{"path":str(c1541),"sha256":sha(c1541),"version":b["version"],"realdevice":"disabled"},"STRUCTURAL_VALIDATOR_IDENTITY":"tools/diagnostics/r0e_d81_loadability_gate.py","HOST_STRUCTURAL_RESULT":"PASS","HOST_CONTENT_RESULT":"PASS","XEMU_RESULT":"AWAITING_STAGE_3","XEMU_EVIDENCE":None,"SD_COPY_SHA256":None,"SD_CONTIGUITY_RESULT":"AWAITING_AUTHORIZED_TRANSFER","PHYSICAL_CHOOSER_RESULT":"AWAITING_HUMAN","PHYSICAL_EVIDENCE":None,"payloads":[{"hostFilename":p.name,"petsciiFilename":n,"bytes":p.stat().st_size,"sha256":sha(p)} for n,p in expected],"construction":"fresh format plus all payload writes in one pinned c1541 invocation","c1541Listing":listing}
(out/"manifests").mkdir(parents=True,exist_ok=True); (out/"reports").mkdir(parents=True,exist_ok=True)
(out/"manifests/r0e-d81-release.json").write_text(json.dumps(release,indent=2,sort_keys=True)+"\n")
(out/"reports/R0E-D81-LOADABILITY.md").write_text("# R0-E4 D81 Loadability\n\nState: `HOST_CONTENT_VERIFIED`\n\n- Candidate: `%s`\n- SHA-256: `%s`\n- Host structural/content: `PASS`\n- Xemu: `AWAITING_STAGE_3`\n- SD transfer: `AWAITING_AUTHORIZED_TRANSFER`\n- Physical chooser: `AWAITING_HUMAN`\n"%(image.name,sha(image)))
print("R0-E4 D81 STRUCTURAL+CONTENT PASS sha256="+sha(image))
