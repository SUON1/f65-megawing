#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import sys

root = Path(sys.argv[1]).resolve()
reports = root / "build/r0b/reports"
artifacts = root / "build/r0b/artifacts"
memory = (reports / "R0B-D031-SAFE-XEMU.memory.bin").read_bytes()
screen = (reports / "R0B-D031-SAFE-XEMU.screen.txt").read_text(errors="replace").replace("{", "").replace("}", "")
result = memory[0x1800:0x1860]
if len(result) != 96 or result[:8] != b"R0B2\x02\x00\x01\x05" or result[46:48] != b"\x60\x00":
    raise SystemExit(f"R0B-D031-SAFE-XEMU-001 FAIL: result header {result.hex()}")
expected_status = [3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3]
expected_reason = [1, 0, 2, 1, 1, 1, 6, 3, 4, 1, 5]
if list(result[48:59]) != expected_status or list(result[59:70]) != expected_reason:
    raise SystemExit(f"R0B-D031-SAFE-XEMU-001 FAIL: status/reason {list(result[48:70])}")
if result[84:89] != b"\x07\x01\xe0\x60\x60" or (sum(result[:83]) & 0xff) != result[83]:
    raise SystemExit(f"R0B-D031-SAFE-XEMU-001 FAIL: flags/context/checksum {result[84:89].hex()}/{result[83]:02x}")
markers = ("R0B-D031-SAFE-001 LOCAL TEST: PASS", "D031 40-COL READBACK: PASS", "D031 EXACT RESTORE: PASS", "TEXT SENTINEL: PASS", "RESULT HEX $1800-$185F BELOW", "GATE OPEN; FCM CARD/SWAP NOT ENABLED")
if any(marker not in screen for marker in markers):
    raise SystemExit("R0B-D031-SAFE-XEMU-001 FAIL: missing screen marker")
evidence = {
    "id": "R0B-D031-SAFE-XEMU-001", "status": "PASS",
    "scope": "Xemu-only $D031 save/clear-H640/readback/exact-restore proof; no FCM, pointer, palette, DMA, MAP, or IRQ write",
    "identity": {"contract_sha256": result[8:40].hex(), "llvm_mos": "v23.1.0", "abi_base_page": result[44], "lto_zp": result[45], "harness_revision": result[7], "d81_sha256": hashlib.sha256((artifacts / "F65-R0B-D031-SAFE.d81").read_bytes()).hexdigest()},
    "result_block": {"address": "$1800", "size": 96, "statuses": expected_status, "reasons": expected_reason, "probe_flags": result[84], "saved_d031": result[86], "target_d031": result[87], "readback_d031": result[88]}
}
(reports / "r0b-d031-safe-xemu-evidence.json").write_text(json.dumps(evidence, indent=2) + "\n")
print("R0B-D031-SAFE-XEMU-001 PASS: isolated D031 transition/restore and text sentinel in Xemu")
