"""Build the opt-in exact-wide evidence. The target is never executed."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

from compact_validate import module, ROOT
from compact_check import check
import validate as builder

IDENTITY = "65AERO-M2-EXACT-WIDE-1"
BASE = "5ccfe124b53af6a755819d6ae4da3fc1ded0de02"
MATH = "src/platform/m2_rebuild/wide_math.c"
BUS = "tests/flight_demo/m2_rebuild/wide_math_bus.c"
GEOMETRY = ["src/environment/m2_fixture.c", "src/graphics/m2_limb.c",
            "src/graphics/m2_compact.c", "src/graphics/m2_compact_public.c",
            "src/graphics/m2_record_private.c", "interfaces/generated/m2_tables.c"]
BUILD_OPTION = "-DM2_EXACT_WIDE"


def host(output):
    # Keep all captures create-once and separate from previous evidence.
    output.mkdir()
    results = {"identity": IDENTITY, "commands": []}

    def run(argv, log):
        argv = list(map(str, argv))
        process = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True)
        (output / log).write_text(process.stdout + process.stderr)
        results["commands"].append({"argv": argv, "exit": process.returncode, "log": log})
        process.check_returncode()

    includes = ["-I" + name for name in builder.INCLUDES]
    clang = ["/usr/bin/clang", *builder.HOST_FLAGS, *includes]
    candidate = [BUILD_OPTION, "-DM2_MATH_HOST_BUS", *GEOMETRY, MATH, BUS]
    lib = output / "candidate.dylib"
    native = output / "native.dylib"
    sanitizer = "-fsanitize=address,undefined"
    try:
        native_camera = output / "native-camera.c"
        native_camera.write_bytes(subprocess.check_output(
            ["git", "show", "9570f0a:src/diagnostics/m2_rebuild/camera.c"], cwd=ROOT))
        run([*clang, "-O2", "-shared", "-fPIC", *candidate, "-o", lib], "oracle-compile.txt")
        run([*clang, "-O2", "-shared", "-fPIC", builder.GEOMETRY[0],
             "src/graphics/m2_geometry.c", "interfaces/generated/m2_tables.c",
             native_camera, "-o", native], "native-compile.txt")
        for script, arguments in [
            ("m2_rebuild/wide_math_oracle.py", [lib, native]),
            ("m2/oracle.py", [lib]),
            ("m2/clip_regressions.py", [lib]),
        ]:
            run([sys.executable, "-B", "tests/flight_demo/" + script, *arguments],
                Path(script).stem + ".txt")
        gateway = output / "gateway"
        run([*clang, sanitizer, "-DM2_MATH_HOST_BUS", "-DM2_MATH_SELF_TEST",
             MATH, BUS, "-o", gateway], "gateway-compile.txt")
        for mode in range(6):
            run([gateway, mode], f"gateway-{mode}.txt")
        integrated = output / "host"
        run([*clang, sanitizer, *candidate, *builder.CORE, *builder.NEW,
             "tests/flight_demo/m2_rebuild/host.c", "-o", integrated], "host-compile.txt")
        run([integrated, output / "frame.indices"], "host.txt")
        results["status"] = "PASS"
    except subprocess.CalledProcessError:
        results["status"] = "FAIL"
    finally:
        results["inputs"] = {name: builder.sha(ROOT / name) for name in
                             [*GEOMETRY, MATH, BUS, *builder.CORE, *builder.NEW,
                              "tests/flight_demo/m2_rebuild/wide_math_oracle.py",
                              "tests/flight_demo/m2_rebuild/limb_oracle.py",
                              "tests/flight_demo/m2_rebuild/host.c",
                              "src/graphics/m2_limb.h",
                              "src/platform/m2_rebuild/wide_math.h"]}
        (output / "result.json").write_text(json.dumps(results, indent=2) + "\n")
        seal(output)
    return int(results["status"] != "PASS")


def seal(output):
    files = {str(path.relative_to(output)): {"bytes": path.stat().st_size,
             "sha256": builder.sha(path)}
             for path in sorted(output.rglob("*")) if path.is_file()}
    with (output / "seal.json").open("x") as stream:
        stream.write(json.dumps(files, indent=2) + "\n")


def target(sdk, output):
    residency = module(ROOT / "tools/flight_demo/m2_rebuild/residency.py", "wide_residency")
    contract = residency.load()
    profile = {"identity": contract["identity"], "resident_end": contract["development_resident"][1],
               "production_end": contract["production_resident"][1],
               "link_script": "src/platform/m2_rebuild/extended_resident.ld",
               "compress_link_map": True}
    builder.GEOMETRY = GEOMETRY
    # Keep the real assertion and memory ranges. Retain over-limit bytes for
    # offline closure and cost analysis; builder independently reports FAIL.
    builder.FLAGS = [*builder.FLAGS, BUILD_OPTION, "-Wl,--noinhibit-exec"]
    return builder.execute(
        "target", sdk, output, identity=IDENTITY, composition_check=check,
        extra_inputs=[residency.CONTRACT, *residency.OUTPUTS, "src/graphics/m2_commands.inc"],
        archive_inputs=True, target_profile=profile,
        extra_target_sources=[MATH, "src/platform/m2_rebuild/extended_startup_45gs02.s"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tier", choices=["host", "target"])
    parser.add_argument("--sdk", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.tier == "target" and args.sdk is None:
        parser.error("--sdk is required for target")
    output = args.output.resolve()
    if args.tier == "target" and ROOT not in output.parents:
        parser.error("target output must be inside the focused checkout")
    current = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if current != BASE:
        # A reviewed successor can reproduce the evidence while recording its
        # real HEAD. An unrelated branch must not be tested against this base.
        subprocess.run(["git", "merge-base", "--is-ancestor", BASE, current], cwd=ROOT, check=True)
    return host(output) if args.tier == "host" else target(args.sdk, output)


if __name__ == "__main__":
    sys.exit(main())
