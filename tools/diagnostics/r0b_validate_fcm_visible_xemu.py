#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import sys

root = Path(sys.argv[1]).resolve()
reports = root / "build/r0b/reports"
artifacts = root / "build/r0b/artifacts"
memory = (reports / "R0B-FCM-VISIBLE-XEMU.memory.bin").read_bytes()
screen = (reports / "R0B-FCM-VISIBLE-XEMU.screen.txt").read_text(errors="replace").replace("{", "").replace("}", "")
result = memory[0x1800:0x1860]
if len(result) != 96 or result[:8] != b"R0B2\x02\x00\x01\x04" or result[46:48] != b"\x60\x00":
    raise SystemExit(f"R0B-FCM-VIS-XEMU-001 FAIL: result header {result.hex()}")
expected_status = [1, 1, 3, 1, 3, 3, 3, 3, 3, 1, 3]
expected_reason = [0, 0, 2, 0, 1, 1, 6, 3, 4, 0, 5]
if list(result[48:59]) != expected_status or list(result[59:70]) != expected_reason:
    raise SystemExit(f"R0B-FCM-VIS-XEMU-001 FAIL: status/reason {list(result[48:70])}")
if result[84:89] != b"\x0f\x01\x01\x01\x01" or (sum(result[:83]) & 0xff) != result[83]:
    raise SystemExit(f"R0B-FCM-VIS-XEMU-001 FAIL: flags/checksum {result[84:89].hex()}/{result[83]:02x}")
markers = ("R0B-FCM-VIS-001 LOCAL TEST: PASS", "D054 FCLRLO/HI+CHR16 LATCH: PASS", "D054 EXACT RESTORE: PASS", "SCREEN BYTES EXACT RESTORE: PASS", "FCM CARD BYTES EXACT RESTORE: PASS", "RESULT HEX $1800-$185F BELOW", "GATE OPEN; NO POINTER-SWAP OR PALETTE CLAIM")
if any(marker not in screen for marker in markers):
    raise SystemExit("R0B-FCM-VIS-XEMU-001 FAIL: missing visible-FCM result-screen marker")
lock = json.loads((root / "toolchain/f65_toolchain.lock.json").read_text())
evidence = {
    "id": "R0B-FCM-VIS-XEMU-001",
    "status": "PASS",
    "scope": "Xemu-only default-C65 screen FCM card, D054 latch, and exact-byte restoration; not a pointer-table swap or palette proof",
    "environment": {"kind": "Xemu baseline", "source_commit": lock["xemu"]["source_commit"], "model": "03", "video": "PAL", "audio": "dummy backend"},
    "identity": {"contract_sha256": result[8:40].hex(), "llvm_mos": "v23.1.0", "abi_base_page": result[44], "lto_zp": result[45], "harness_revision": result[7], "d81_sha256": hashlib.sha256((artifacts / "F65-R0B-FCM-VISIBLE.d81").read_bytes()).hexdigest(), "prg_sha256": hashlib.sha256((artifacts / "F65-R0B-FCM-VISIBLE.prg").read_bytes()).hexdigest()},
    "result_block": {"address": "$1800", "size": 96, "statuses": expected_status, "reasons": expected_reason, "flags": result[84], "card_alignment": result[85], "d054_restored": result[86], "screen_restored": result[87], "card_restored": result[88]}
}
(reports / "r0b-fcm-visible-xemu-evidence.json").write_text(json.dumps(evidence, indent=2) + "\n")
print("R0B-FCM-VIS-XEMU-001 PASS: default C65 FCM card and exact restoration in Xemu")
