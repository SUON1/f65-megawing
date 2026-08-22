#!/usr/bin/env python3
"""Static R0-C target guard: layout identity, no protected reserve reference, no disk service."""
import pathlib, sys
root = pathlib.Path(sys.argv[1])
text = (root / "src/diagnostics/r0c/composite.c").read_text()
required = ["R0C-ID-001", "R0C-PKG-001", "R0C-CAP-001", "R0C-RES-001", "R0C-STG-001", "R0C-ATTIC-001", "R0C-NODISK-001", "R0C-ROM-001", "R0C-SAVE-001", "R0C-MEDIA-001", "R0C_RESULT_ADDRESS", "R0C_RESOURCE_HANDLE_INVALID"]
missing = [value for value in required if value not in text]
forbidden = ["0x058", "fopen", "malloc", "DMA", "D081"]
bad = [value for value in forbidden if value in text]
if missing or bad:
    raise SystemExit("R0-C target validation failed: missing=%s forbidden=%s" % (missing, bad))
print("R0-C static target validation PASS")
