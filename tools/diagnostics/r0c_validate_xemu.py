#!/usr/bin/env python3
import hashlib, json, pathlib, re, sys
root = pathlib.Path(sys.argv[1]); out = root / "build/r0c"
screen = (out / "reports/R0C-XEMU.screen.txt").read_text(errors="replace")
media_screen = (out / "reports/R0C-MEDIA-XEMU.screen.txt").read_text(errors="replace")
memory = (out / "reports/R0C-XEMU.memory.bin").read_bytes()
required = ["R0-C TEST RUN COMPLETE", "R0C-ID-001", "R0C-PKG-001", "R0C-CAP-001", "R0C-RES-001", "R0C-STG-001", "R0C-ATTIC-001", "R0C-NODISK-001"]
missing = [x for x in required if x not in screen]
block = memory[0x1800:0x1860]
if missing or len(block) != 96 or block[:4] != b"R0C1" or block[10] != 0:
    raise SystemExit("R0-C Xemu validation failed: missing=%s result=%s" % (missing, block[:16].hex()))
media_text = re.sub(r"\{([^}])\}", r"\1", media_screen)
media_required = ["TWO-GENERATION MEDIA FIXTURE", "DEVICE 9 ONLY", "DEVICE 8 IS NOT USED", "I=INITIALIZE"]
media_missing = [x for x in media_required if x not in media_text]
if media_missing:
    raise SystemExit("R0-C media-fixture Xemu validation failed: missing=%s" % media_missing)
evidence = {"identity":"r0c-0.1.0-proof","class":"XEMU","result":"PASS","tests":["R0C-ID-001","R0C-PKG-001","R0C-CAP-001","R0C-RES-001","R0C-STG-001","R0C-ATTIC-001","R0C-NODISK-001","R0C-MEDIA-BOOT-001 explicit device-9 boot entry","R0C-MEDIA-XEMU-001 fixture menu","R0C-MEDIA-INPUT-001 PETSCII/ASCII input normalization static pass"],"resultBlockSha256":hashlib.sha256(block).hexdigest(),"mediaFixture":{"carrier":"ROCFINAL.D81","d81MountedAt":[9],"bootLoadsFrom":9,"transactionExecution":"NOT_CLAIMED; physical fault matrix remains required"},"deferred":["R0C-ROM-001 authoritative post-ROM storage restoration","R0C-SAVE-001 physical media transaction evidence","R0C-MEDIA-001 physical fault matrix","R0C-ATTIC-001 physical MEGA65 ABI measurement"]}
(out / "evidence/r0c-xemu-evidence.json").write_text(json.dumps(evidence, indent=2) + "\n")
print("XEMU PASS")
