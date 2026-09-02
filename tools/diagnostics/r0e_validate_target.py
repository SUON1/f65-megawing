#!/usr/bin/env python3
import json, pathlib, re, sys
root=pathlib.Path(sys.argv[1]); source_only="--source-only" in sys.argv
contract=json.loads((root/"interfaces/r0e_proof_contract.json").read_text())
ledger=json.loads((root/"memory/r0e-memory-ledger.json").read_text())
src=(root/"src/diagnostics/r0e/composite.c").read_text().lower()
platform=(root/"src/platform/r0e/raster_observation.c").read_text()
if contract["simulation_hz"]!=100 or contract["tick_stages"]!=21: raise SystemExit("R0-E target validation: timeline contract invalid")
if contract["services"]["dma"]!="DMA_HARDWARE_PROBE_NOT_EXECUTED": raise SystemExit("R0-E target validation: DMA status must fail closed")
timing=contract.get("timing",{})
if timing.get("status")!="RASTER_LINE_DELTA_MODULO_256_OBSERVED" or timing.get("sampleCountPerCase")!=16 or timing.get("phaseBins")!=16 or timing.get("windowTicks")!=33: raise SystemExit("R0-E target validation: timing-observation contract invalid")
if "0x058000-0x05ffff" not in str(ledger) or ledger["reserveBytes"]!=0: raise SystemExit("R0-E target validation: reserve protection absent")
if any(x in src for x in ["malloc", "calloc", "realloc", "free(", "dma_", "map_", "irq_"]): raise SystemExit("R0-E target validation: forbidden direct platform operation")
if "vicii" in src: raise SystemExit("R0-E target validation: raster register access must remain inside the private observation helper")
if "VICII.rasterline" not in platform or re.search(r"VICII\.rasterline\s*=",platform): raise SystemExit("R0-E target validation: raster helper must be read-only")
if any(x in platform.lower() for x in ["dma_", "map_", "irq_"]): raise SystemExit("R0-E target validation: raster helper exceeds read-only scope")
required=["snapshot_records", "R0E_STATE_PUBLISHING", "R0E_STATE_READY", "R0E_STATE_READING", "R0E_CASE_COUNT", "record_case", "timing_samples", "observe_timing_case", "TIMING: RASTER PHASE OBSERVED"]
if any(x.lower() not in src for x in required): raise SystemExit("R0-E target validation: target ownership/matrix evidence is incomplete")
if any("0x018000" in str(a) for a in ledger["allocations"]): raise SystemExit("R0-E target validation: stale fabricated snapshot physical range")
if not any(a.get("owner")=="R0-E raster-observation sample scratch" and a.get("bytes")==16 for a in ledger["allocations"]): raise SystemExit("R0-E target validation: raster-observation scratch is not charged")
if source_only:
 print("R0-E source static validation PASS")
 raise SystemExit(0)
mp=root/"build/r0e/reports/F65-R0E-PROOF.map"; text=mp.read_text()
def sec(n):
 m=re.search(r"^\s*[0-9a-f]+\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+"+re.escape(n)+r"$",text,re.M)
 if not m: raise SystemExit("R0-E accounting missing "+n)
 return int(m.group(1),16)
m=re.search(r"__stack = 0x([0-9a-f]+)",text)
if not m: raise SystemExit("R0-E accounting missing stack")
report={"identity":contract["identity"],"codeBytes":sec(".text"),"rodataBytes":sec(".rodata"),"dataBytes":sec(".data"),"bssBytes":sec(".bss"),"linkedStackAddress":"0x"+m.group(1),"snapshotStorage":"linked C .bss; 3 x 64 bytes; exact symbol/map review required","rasterObservationScratch":"linked C .bss; 16 x 1-byte samples reused per case; exact symbol/map review required","reserveBytes":0,"resultBlock":"0x1900-0x19ff","dma":"DMA_HARDWARE_PROBE_NOT_EXECUTED","timing":{"status":"RASTER_LINE_DELTA_MODULO_256_OBSERVED","unit":"raster-line low-byte delta modulo 256","sampleCountPerCase":16,"phaseBins":16,"windowTicks":33,"resultOrdering":"raw-byte numeric rank only; not elapsed-time p50/p95/worst after possible wrap","limitations":["not CPU cycles","not latency","not DMA or IRQ measurement","not a measured limit"]},"result":"PASS","note":"Functional target accounting plus read-only raster observation; no measured limit selected."}
(root/"build/r0e/reports/r0e-build-accounting.json").write_text(json.dumps(report,indent=2)+"\n")
print("R0-E target static validation PASS")
