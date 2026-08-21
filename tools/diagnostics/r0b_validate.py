#!/usr/bin/env python3
"""Static R0-B configuration and scope checks; target behavior has a separate gate."""
import hashlib
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
contract = json.loads((root / "interfaces/r0b_proof_contract.json").read_text())
if contract["schema_version"] != "r0b-0.1.0-proof":
    raise SystemExit("R0B-CFG-001 FAIL: proof contract version")
if contract["upstream_r0a_commit"] != "1ab5b62928d0e725c8dcf48e8a17783a525503b6":
    raise SystemExit("R0B-UPSTREAM-001 FAIL: unexpected R0-A identity")
full = next(item for item in contract["display_candidates"] if item["id"].endswith("320X200"))
if full["character_data_bytes"] != 64000 or full["pointer_table_bytes"] * 2 != 4000:
    raise SystemExit("R0B-MEM-001 FAIL: FCM ownership accounting")
ledger = json.loads((root / "memory/r0b-memory-ledger.json").read_text())
if ledger["reserve"] != {"range": "$058000-$05FFFF", "allocation": 0, "must_remain_untouched": True}:
    raise SystemExit("R0B-MEM-001 FAIL: reserve ownership")
for generated in ("interfaces/generated/r0b_interfaces.h", "interfaces/generated/r0b_interfaces.inc", "interfaces/generated/R0BInterfaces.java"):
    if "R0BHostTools" not in (root / generated).read_text():
        raise SystemExit(f"R0B-CFG-001 FAIL: stale generated binding {generated}")
print("R0B-CFG-001 PASS: upstream identity, generated bindings, candidate ledger, and reserve policy")
