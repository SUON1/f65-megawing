#!/usr/bin/env python3
import hashlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1]); out = root / "build/r0c"
screen = (out / "reports/R0C-XEMU.screen.txt").read_text(errors="replace")
memory = (out / "reports/R0C-XEMU.memory.bin").read_bytes()
required = ["R0-C TEST RUN COMPLETE", "R0C-ID-001", "R0C-PKG-001", "R0C-CAP-001", "R0C-RES-001", "R0C-STG-001", "R0C-ATTIC-001", "R0C-NODISK-001"]
missing = [x for x in required if x not in screen]
block = memory[0x1800:0x1860]
if missing or len(block) != 96 or block[:4] != b"R0C1" or block[10] != 0:
    raise SystemExit("R0-C Xemu validation failed: missing=%s result=%s" % (missing, block[:16].hex()))
evidence = {"identity":"r0c-0.1.0-proof","class":"XEMU","result":"PASS","tests":["R0C-ID-001","R0C-PKG-001","R0C-CAP-001","R0C-RES-001","R0C-STG-001","R0C-ATTIC-001","R0C-NODISK-001"],"resultBlockSha256":hashlib.sha256(block).hexdigest(),"deferred":["R0C-ROM-001 authoritative post-ROM storage restoration","R0C-SAVE-001 DEC-012 physical medium","R0C-ATTIC-001 physical MEGA65 ABI measurement"]}
(out / "evidence/r0c-xemu-evidence.json").write_text(json.dumps(evidence, indent=2) + "\n")
print("XEMU PASS")
