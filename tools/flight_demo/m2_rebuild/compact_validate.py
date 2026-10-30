"""Fresh evidence for one integrated unbanked candidate. Never runs the target."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
IDENTITY = "65AERO-M2-UNBANKED-1"
EVIDENCE = ROOT / "docs/evidence/flight-demo/2026-10-30-m2-unbanked-renderer"


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def extra_host(builder, output):
    output.mkdir(parents=True, exist_ok=False)
    result = {"identity": IDENTITY, "tier": "independent-host", "commands": [],
              "target_executed": False}

    def run(command, log):
        command = list(map(str, command))
        process = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        (output / log).write_text(process.stdout + process.stderr)
        result["commands"].append({"argv": command, "exit": process.returncode, "log": log})
        if process.returncode:
            raise RuntimeError(log + " failed")

    try:
        includes = ["-I" + path for path in builder.INCLUDES]
        flags = ["/usr/bin/clang", *builder.HOST_FLAGS, "-O2", "-shared", "-fPIC", *includes]
        candidate = output / "compact.dylib"
        reference = output / "native.dylib"
        native_camera = output / "native-camera.c"
        native_camera.write_bytes(subprocess.check_output(
            ["git", "show", "9570f0a:src/diagnostics/m2_rebuild/camera.c"], cwd=ROOT))
        run([*flags, *builder.GEOMETRY, "src/diagnostics/m2_rebuild/camera.c",
             "-o", candidate], "compact-compile.txt")
        run([*flags, "src/environment/m2_fixture.c", "src/graphics/m2_geometry.c",
             "interfaces/generated/m2_tables.c", native_camera,
             "-o", reference], "native-compile.txt")
        run([sys.executable, "-B", "tests/flight_demo/m2_rebuild/limb_oracle.py",
             candidate, reference], "bigint-native-oracle.txt")
        result["status"] = "PASS"
    except Exception as error:
        result.update(status="FAIL", failure=str(error))
    finally:
        result["inputs"] = {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
                            for path in [*builder.GEOMETRY, "src/graphics/m2_geometry.c",
                                         "tests/flight_demo/m2_rebuild/limb_oracle.py",
                                         str(Path(__file__).relative_to(ROOT))]}
        (output / "result.json").write_text(json.dumps(result, indent=2) + "\n")
        seal = {str(path.relative_to(output)): {"bytes": path.stat().st_size,
                 "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                for path in sorted(output.rglob("*")) if path.is_file()}
        (output / "seal.json").write_text(json.dumps(seal, indent=2) + "\n")
    print(json.dumps({"output": str(output), "status": result["status"]}))
    return 0 if result["status"] == "PASS" else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=["host", "independent", "target"], required=True)
    parser.add_argument("--sdk", type=Path)
    args = parser.parse_args()
    builder = module(ROOT / "tools/flight_demo/m2_rebuild/validate.py", "m2_compact_builder")
    builder.GEOMETRY = ["src/environment/m2_fixture.c", "src/graphics/m2_limb.c",
                        "src/graphics/m2_compact.c", "src/graphics/m2_compact_public.c",
                        "interfaces/generated/m2_tables.c"]
    checker = module(ROOT / "tools/flight_demo/m2_rebuild/compact_check.py", "m2_compact_check")
    if args.tier == "independent":
        return extra_host(builder, EVIDENCE / ("arithmetic-" + str(time.time_ns())))
    if args.tier == "target" and args.sdk is None:
        parser.error("--sdk required")
    output = EVIDENCE / (args.tier + "-" + str(time.time_ns()))
    code = builder.execute(args.tier, args.sdk, output, identity=IDENTITY,
                           composition_check=checker.check)
    if code == 0 and args.tier == "host":
        code = extra_host(builder, EVIDENCE / ("arithmetic-" + str(time.time_ns())))
    return code


if __name__ == "__main__":
    sys.exit(main())
