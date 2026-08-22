#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import sys

root = Path(sys.argv[1]).resolve()
reports = root / "build/r0b/reports"
memory = (reports / "R0B-XEMU.memory.bin").read_bytes()
screen = (reports / "R0B-XEMU.screen.txt").read_text(errors="replace").replace("{", "").replace("}", "")
result = memory[0x1800:0x1860]
if len(result) != 96 or result[:8] != b"R0B2\x02\x00\x01\x02" or result[46:48] != b"\x60\x00":
    raise SystemExit(f"R0B-BLD-001 FAIL: result block {result.hex()}")
expected_status = [3, 1, 3, 1, 3, 1, 1, 3, 1, 1, 3]
expected_reason = [1, 0, 2, 0, 1, 0, 0, 3, 0, 0, 5]
if list(result[48:59]) != expected_status or list(result[59:70]) != expected_reason:
    raise SystemExit(f"R0B-XEMU-001 FAIL: status/reason {list(result[48:70])}")
input_lines = int.from_bytes(result[70:72], "little")
audio_lines = int.from_bytes(result[72:74], "little")
if input_lines == 0 or audio_lines == 0 or (sum(result[:83]) & 0xff) != result[83]:
    raise SystemExit(f"R0B-XEMU-001 FAIL: timing/checksum {input_lines}/{audio_lines}/{result[83]}")
markers = ("R0B-FCM-SAFE-001 DEFERRED", "R0B-PRES-001 COMPLETE+PREV PASS", "R0B-HUD-001 COCKPIT/MFD PASS", "R0B-REN-001 WIRE PROXY PASS", "R0B-IN-003 EDGE RASTER:", "R0B-AUD-001 SID RASTER:", "R0B-HW-001 OWNER CAPTURE REQUIRED", "R0B-BLD-001 PASS; GATE NOT CLOSED")
if any(marker not in screen for marker in markers):
    raise SystemExit("R0B-XEMU-001 FAIL: missing stage-2 markers")
lock = json.loads((root / "toolchain/f65_toolchain.lock.json").read_text())
artifacts = root / "build/r0b/artifacts"
evidence = {
    "id": "R0B-XEMU-001",
    "status": "PASS",
    "environment": {"kind": "Xemu baseline", "source_commit": lock["xemu"]["source_commit"], "model": "03", "video": "PAL", "audio": "dummy backend"},
    "identity": {"contract_sha256": result[8:40].hex(), "llvm_mos": "v23.1.0", "abi_base_page": result[44], "lto_zp": result[45], "harness_revision": result[7], "d81_sha256": hashlib.sha256((artifacts / "F65-R0B-PROOF.d81").read_bytes()).hexdigest(), "prg_sha256": hashlib.sha256((artifacts / "F65-R0B-PROOF.prg").read_bytes()).hexdigest()},
    "result_block": {"address": "$1800", "size": 96, "statuses": expected_status, "reasons": expected_reason, "input_raster_lines": input_lines, "audio_raster_lines": audio_lines, "complete_hash": int.from_bytes(result[74:76], "little"), "previous_hash": int.from_bytes(result[76:78], "little")}
}
(reports / "r0b-xemu-evidence.json").write_text(json.dumps(evidence, indent=2) + "\n")
print(f"R0B-XEMU-001 PASS: resident stage-2 proof in Xemu; input={input_lines} raster lines audio={audio_lines} raster lines")
