#!/usr/bin/env python3
"""Runtime evidence check for the composite R0-B Xemu baseline."""
from pathlib import Path
import hashlib
import json
import sys

root = Path(sys.argv[1]).resolve()
reports = root / "build/r0b/reports"
artifacts = root / "build/r0b/artifacts"
memory = (reports / "R0B-FINAL-XEMU.memory.bin").read_bytes()
screen = (reports / "R0B-FINAL-XEMU.screen.txt").read_text(errors="replace")
result = memory[0x1800:0x1860]
expected_status = [1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 3]
expected_reason = [0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 5]
if len(result) != 96 or result[:8] != b"R0B2\x02\x01\x03\x05" or result[46:48] != b"\x60\x00":
    raise SystemExit(f"R0B-FINAL-XEMU-001 FAIL: result header {result.hex()}")
if list(result[48:59]) != expected_status or list(result[59:70]) != expected_reason:
    raise SystemExit(f"R0B-FINAL-XEMU-001 FAIL: status/reason {list(result[48:70])}")
if result[78:83] != bytes([1, 3, 3, 1, 3]) or (sum(result[:83]) & 0xff) != result[83]:
    raise SystemExit(f"R0B-FINAL-XEMU-001 FAIL: state/checksum {result[78:84].hex()}")
if result[84:96] != bytes([7, 1, 3, 7, 0x24, 0xe0, 0x40, 0, 8, 0, 0, 0xff]):
    raise SystemExit(f"R0B-FINAL-XEMU-001 FAIL: register transaction {result[84:96].hex()}")
markers = (
    "R0-B FINAL COMPOSITE EVIDENCE CANDIDATE",
    "FCM SAFE D031+D054 READBACK: PASS",
    "COMPLETE MATRIX B + PRIOR A: PASS",
    "D060-D063 POINTER FLIP+RESTORE: PASS",
    "ACTIVE PALETTE WRITE/READ/RESTORE: PASS",
    "D031/D054/POINTER EXACT ROLLBACK: PASS",
    "HUD/MFD: COMPLETE BUFFER COMPOSITION PASS",
    "RENDERER: FCM 64-BYTE CARD / PROXY-SCENE-001 PASS",
    "INPUT ASCII EDGE: DEFERRED (NO KEY EVENT)",
    "SID 512-WRITE SERVICE / RASTER DELTA: PASS",
    "PCM/DMA: DEFERRED; NO PINNED R0-B DMA-AUDIO START/STOP WRAPPER",
)
if any(marker not in screen for marker in markers):
    raise SystemExit("R0B-FINAL-XEMU-001 FAIL: final status screen missing required marker")
lock = json.loads((root / "toolchain/f65_toolchain.lock.json").read_text())
evidence = {
    "id": "R0B-FINAL-XEMU-001",
    "status": "PASS_WITH_EXPLICIT_INPUT_AND_HARDWARE_DEFERRALS",
    "scope": "Composite Xemu baseline validates the bounded FCM/pointer/palette transaction, complete-buffer presentation, HUD/renderer composition, and timed SID write service. No physical key event or real-hardware identity exists in headless Xemu.",
    "environment": {"kind": "Xemu baseline", "source_commit": lock["xemu"]["source_commit"], "model": "03", "video": "PAL", "audio": "dummy backend"},
    "identity": {"contract_sha256": result[8:40].hex(), "llvm_mos": "v23.1.0", "abi_base_page": result[44], "lto_zp": result[45], "harness_revision": result[7], "d81_sha256": hashlib.sha256((artifacts / "F65-R0B-FINAL.d81").read_bytes()).hexdigest(), "prg_sha256": hashlib.sha256((artifacts / "F65-R0B-FINAL.prg").read_bytes()).hexdigest()},
    "result_block": {"address": "$1800", "size": 96, "statuses": expected_status, "reasons": expected_reason, "input_raster_delta": int.from_bytes(result[70:72], "little"), "audio_raster_delta": int.from_bytes(result[72:74], "little"), "complete_hash": int.from_bytes(result[74:76], "little"), "previous_hash": int.from_bytes(result[76:78], "little"), "transaction": {"begin": result[84], "swap": result[85], "palette": result[86], "restore": result[87], "d018": result[88], "d031": result[89], "d054": result[90], "d060_d063": list(result[91:95]), "d070": result[95]}},
}
(reports / "r0b-final-xemu-evidence.json").write_text(json.dumps(evidence, indent=2) + "\n")
print("R0B-FINAL-XEMU-001 PASS: composite reversible FCM/pointer/palette/presentation/audio proof; real key and hardware identity correctly deferred")
