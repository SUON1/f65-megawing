#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import sys

root = Path(sys.argv[1]).resolve()
reports = root / "build/r0b/reports"
artifacts = root / "build/r0b/artifacts"
memory = (reports / "R0B-FCM-SAFE-XEMU.memory.bin").read_bytes()
screen = (reports / "R0B-FCM-SAFE-XEMU.screen.txt").read_text(errors="replace").replace("{", "").replace("}", "")
result = memory[0x1800:0x1860]
if len(result) != 96 or result[:8] != b"R0B2\x02\x00\x01\x03" or result[46:48] != b"\x60\x00":
    raise SystemExit(f"R0B-FCM-SAFE-XEMU-001 FAIL: result header {result.hex()}")
expected_status = [1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3]
expected_reason = [0, 0, 2, 1, 1, 1, 6, 3, 4, 1, 5]
if list(result[48:59]) != expected_status or list(result[59:70]) != expected_reason:
    raise SystemExit(f"R0B-FCM-SAFE-XEMU-001 FAIL: status/reason {list(result[48:70])}")
if result[84:86] != b"\x07\x01" or (sum(result[:83]) & 0xff) != result[83]:
    raise SystemExit(f"R0B-FCM-SAFE-XEMU-001 FAIL: flags/checksum {result[84:86].hex()}/{result[83]:02x}")
markers = ("R0B-FCM-SAFE-002 XEMU/TARGET PASS", "D054 LATCH READBACK: PASS", "D054 EXACT RESTORE: PASS", "TEXT SENTINEL: PASS", "RESULT HEX $1800-$185F BELOW", "GATE OPEN; FCM FRAME/SWAP NOT ENABLED")
if any(marker not in screen for marker in markers):
    raise SystemExit("R0B-FCM-SAFE-XEMU-001 FAIL: missing isolated-probe screen marker")
lock = json.loads((root / "toolchain/f65_toolchain.lock.json").read_text())
evidence = {
    "id": "R0B-FCM-SAFE-XEMU-001",
    "status": "PASS",
    "scope": "Xemu-only isolated $D054 latch/read-back/exact-restore proof; not a physical FCM or presentation pass",
    "environment": {"kind": "Xemu baseline", "source_commit": lock["xemu"]["source_commit"], "model": "03", "video": "PAL", "audio": "dummy backend"},
    "identity": {"contract_sha256": result[8:40].hex(), "llvm_mos": "v23.1.0", "abi_base_page": result[44], "lto_zp": result[45], "harness_revision": result[7], "d81_sha256": hashlib.sha256((artifacts / "F65-R0B-FCM-SAFE.d81").read_bytes()).hexdigest(), "prg_sha256": hashlib.sha256((artifacts / "F65-R0B-FCM-SAFE.prg").read_bytes()).hexdigest()},
    "result_block": {"address": "$1800", "size": 96, "statuses": expected_status, "reasons": expected_reason, "probe_flags": result[84], "text_sentinel": result[85]}
}
(reports / "r0b-fcm-safe-xemu-evidence.json").write_text(json.dumps(evidence, indent=2) + "\n")
print("R0B-FCM-SAFE-XEMU-001 PASS: isolated FCM control/restore and text sentinel in Xemu")
