#!/usr/bin/env python3
"""Fail closed while R0-E has no admitted D81 carrier identity."""

import pathlib
import sys


if len(sys.argv) != 3:
    raise SystemExit("usage: r0e_d81_loadability_gate.py ROOT CANDIDATE.D81")

image = pathlib.Path(sys.argv[2])
if image.name in ("F65R0E2.D81", "F65R0E3.D81"):
    raise SystemExit(
        "R0-E D81 loadability gate failed: retired carrier identity after "
        "physical chooser ERROR CODE FF"
    )

raise SystemExit(
    "R0-E D81 loadability gate failed: no current carrier is admitted; "
    "capture the failed R0-E3 SD extent map before assigning R0-E4"
)
