#!/usr/bin/env python3
"""Fail-closed host gate for a D81 before Xemu or physical mounting."""
import hashlib
import json
import pathlib
import subprocess
import sys

root = pathlib.Path(sys.argv[1]).resolve()
candidate = pathlib.Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else root / "build/r0c/artifacts/F65-R0C-MEDIA.D81"
if not candidate.is_file():
    raise SystemExit("D81 loadability gate failed: candidate is absent")
data = candidate.read_bytes()
if len(data) != 819200:
    raise SystemExit("D81 loadability gate failed: exact size is %d, expected 819200" % len(data))
c1541 = root / "toolchain/vice/VICE.app/Contents/Resources/bin/c1541"
if not c1541.is_file():
    raise SystemExit("D81 loadability gate failed: pinned c1541 is absent")
result = subprocess.run([str(c1541), str(candidate), "-list"], capture_output=True, text=True)
if result.returncode != 0:
    raise SystemExit("D81 loadability gate failed: c1541 listing returned %d" % result.returncode)
listing = result.stdout.lower()
required = ("autoboot", "r0c-final", "r0cproof", "r0c-media")
missing = [name for name in required if name not in listing]
if missing:
    raise SystemExit("D81 loadability gate failed: missing=%s" % missing)
digest = hashlib.sha256(data).hexdigest()
out = root / "build/r0c/evidence/r0cload-d81-loadability.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps({"state":"HOST_STRUCTURALLY_VERIFIED", "candidate":str(candidate),
                           "exactBytes":len(data), "sha256":digest,
                           "construction":"fresh-format-one-c1541-session",
                           "requiredFiles":list(required)}, indent=2) + "\n")
print("D81 LOADABILITY GATE PASS sha256=" + digest)
