#!/usr/bin/env python3
"""Validate two clean R0-E4 Xemu boots with bounded raw-raster observations."""
import hashlib, json, pathlib, subprocess, sys

root = pathlib.Path(sys.argv[1]).resolve(); out = root / "build/r0e"; reports = out / "reports"; artifacts = out / "artifacts"
expected_cases = [(0,1000,1000,0,1000,1000,0,0),(1,1000,202,798,1000,1000,0,0),(2,1000,1000,0,1000,1000,0x3f,0),(3,1000,1000,0,1000,1000,0,1),(4,1000,1000,0,2000,2000,0,0)]
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def u16(block, offset): return block[offset] | (block[offset + 1] << 8)
def validate(label):
 screen_path=reports/f"R0E-XEMU-{label}.screen.txt"; memory_path=reports/f"R0E-XEMU-{label}.memory.bin"
 screen=screen_path.read_text(errors="replace").replace("{","").replace("}",""); memory=memory_path.read_bytes(); block=memory[0x1900:0x1a00]
 if len(block)!=256 or block[:8]!=b"R0E1\x03\x64\x15\x7f": raise SystemExit(f"R0E-XEMU-001 FAIL: {label} result header")
 if sum(block[:-1]) & 0xff != block[-1]: raise SystemExit(f"R0E-XEMU-001 FAIL: {label} result checksum")
 for case_id,ticks,published,skipped,input_edges,audio_services,shedding,faults in expected_cases:
  offset=64+case_id*16; actual=(block[offset],u16(block,offset+2),u16(block,offset+4),u16(block,offset+6),u16(block,offset+8),u16(block,offset+10),block[offset+12],block[offset+13])
  if block[offset+1]!=1 or actual!=(case_id,ticks,published,skipped,input_edges,audio_services,shedding,faults): raise SystemExit(f"R0E-XEMU-001 FAIL: {label} case {case_id}")
 if block[144:154]!=bytes((ord("R"),ord("T"),1,16,33,5,16,0x7f,1,0)): raise SystemExit(f"R0E-XEMU-RASTER-001 FAIL: {label} timing header")
 for case_id in range(5):
  actual=block[160+case_id*16:176+case_id*16]
  if actual[0]!=case_id or actual[1]!=1 or actual[2]!=16 or actual[8:11]!=bytes((16,1,1)) or not(actual[7]<=actual[4]<=actual[5]<=actual[6]): raise SystemExit(f"R0E-XEMU-RASTER-001 FAIL: {label} timing case {case_id}")
 markers=["R0-E COMBINED-LOAD FUNCTIONAL PROXY","SNAPSHOT OWNERSHIP","TIMING: RASTER PHASE OBSERVED","RAW LINE DELTA MOD256","RAW Q50/Q95/MAX BYTE","DMA: HARDWARE PROBE NOT EXECUTED"]
 if [marker for marker in markers if marker not in screen]: raise SystemExit(f"R0E-XEMU-001 FAIL: {label} screen markers")
 return {"screenSha256":sha(screen_path),"resultBlockSha256":hashlib.sha256(block).hexdigest(),"memorySha256":sha(memory_path)}
boot1=validate("boot1"); boot2=validate("boot2")
if boot1["screenSha256"]!=boot2["screenSha256"] or boot1["resultBlockSha256"]!=boot2["resultBlockSha256"]: raise SystemExit("R0E-XEMU-001 FAIL: clean boots are not deterministic")
commit=subprocess.run(["git","rev-parse","HEAD"],cwd=root,capture_output=True,text=True,check=True).stdout.strip()
evidence={"identity":"r0e-0.1.0-combined-load-proof","carrier":"F65R0E4.D81","class":"XEMU_FUNCTIONAL_PROXY_WITH_RASTER_OBSERVATION","result":"PASS","sourceCommit":commit,"d81Sha256":sha(artifacts/"F65R0E4.D81"),"tests":["R0E-TICK-001","R0E-SNAP-001","R0E-RENDER-001","R0E-FAULT-001","R0E-INPUT-AUDIO-001","R0E-RASTER-001","R0E-STORAGE-001"],"dma":"DMA_HARDWARE_PROBE_NOT_EXECUTED","timing":{"status":"RASTER_LINE_DELTA_MODULO_256_OBSERVED","unit":"raster-line low-byte delta modulo 256","sampleCountPerCase":16,"phaseBins":16,"windowTicks":33,"resultOrdering":"raw-byte numeric rank only; not elapsed-time p50/p95/worst after possible wrap","reason":"Xemu validates the target-side read-only observation record; it is not CPU-cycle, latency, DMA, IRQ, physical-MEGA65, or measured-limit evidence"},"boots":{"boot1":boot1,"boot2":boot2}}
(out/"evidence").mkdir(parents=True,exist_ok=True); (out/"evidence/r0e-xemu-evidence.json").write_text(json.dumps(evidence,indent=2,sort_keys=True)+"\n")
release_path=out/"manifests/r0e-d81-release.json"; release=json.loads(release_path.read_text())
if release["D81_SHA256"]!=evidence["d81Sha256"]: raise SystemExit("R0E-XEMU-001 FAIL: D81 identity differs from host-gated release record")
release["D81_STATE"]="XEMU_BOOT_VERIFIED"; release["XEMU_RESULT"]="PASS"; release["XEMU_EVIDENCE"]="build/r0e/evidence/r0e-xemu-evidence.json"; release_path.write_text(json.dumps(release,indent=2,sort_keys=True)+"\n")
print("R0E-XEMU-001 PASS: two clean functional-proxy boots verified with raw raster observation; no measured limit is claimed")
