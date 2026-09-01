#!/usr/bin/env python3
import json, pathlib, re, sys
root=pathlib.Path(sys.argv[1]); source_only="--source-only" in sys.argv
contract=json.loads((root/"interfaces/r0e_proof_contract.json").read_text())
ledger=json.loads((root/"memory/r0e-memory-ledger.json").read_text())
src=(root/"src/diagnostics/r0e/composite.c").read_text().lower()
if contract["simulation_hz"]!=100 or contract["tick_stages"]!=21: raise SystemExit("R0-E target validation: timeline contract invalid")
if contract["services"]["dma"]!="DMA_HARDWARE_PROBE_NOT_EXECUTED": raise SystemExit("R0-E target validation: DMA status must fail closed")
if "0x058000-0x05ffff" not in str(ledger) or ledger["reserveBytes"]!=0: raise SystemExit("R0-E target validation: reserve protection absent")
if any(x in src for x in ["malloc", "calloc", "realloc", "free(", "dma_", "map_", "irq_"]): raise SystemExit("R0-E target validation: forbidden direct platform operation")
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
report={"identity":contract["identity"],"codeBytes":sec(".text"),"rodataBytes":sec(".rodata"),"dataBytes":sec(".data"),"bssBytes":sec(".bss"),"linkedStackAddress":"0x"+m.group(1),"reserveBytes":0,"resultBlock":"0x1900-0x19ff","dma":"DMA_HARDWARE_PROBE_NOT_EXECUTED","result":"PASS","note":"Observed build accounting only; no measured limit selected."}
(root/"build/r0e/reports/r0e-build-accounting.json").write_text(json.dumps(report,indent=2)+"\n")
print("R0-E target static validation PASS")
