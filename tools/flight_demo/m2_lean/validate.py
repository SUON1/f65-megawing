"""Option B orchestration, fresh evidence only; fit failure stops continuation."""
import argparse
import importlib.util
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
HERE = ROOT / "docs/evidence/flight-demo/2026-10-29-m2-option-b"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=["host", "target"], required=True)
    parser.add_argument("--sdk", type=Path)
    args = parser.parse_args()
    if args.tier == "target" and args.sdk is None:
        parser.error("target requires pinned --sdk")
    spec = importlib.util.spec_from_file_location("m2_lean_validation",
        ROOT / "tools/flight_demo/m2_rebuild/validate.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    output = HERE / (args.tier + "-" + str(time.time_ns()))
    return module.execute(args.tier, args.sdk, output, identity="65AERO-M2-LEAN-1")


if __name__ == "__main__":
    sys.exit(main())
