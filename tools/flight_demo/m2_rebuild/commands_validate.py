"""One fresh complete command candidate; target and emulator remain separate gates."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

from compact_validate import module, ROOT

IDENTITY = "65AERO-M2-COMMAND-1"
EVIDENCE = ROOT / "docs/evidence/flight-demo/2026-10-30-m2-final-unbanked-fit"


def focused(builder, output):
    output.mkdir(parents=True, exist_ok=False)
    report = {"identity": IDENTITY, "tier": "focused-host", "target_executed": False,
              "commands": [], "status": "FAIL"}

    def run(argv, log):
        argv = list(map(str, argv))
        result = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True)
        (output / log).write_text(result.stdout + result.stderr)
        report["commands"].append({"argv": argv, "exit": result.returncode, "log": log})
        if result.returncode:
            raise RuntimeError(log + " failed")

    try:
        includes = ["-I" + path for path in builder.INCLUDES]
        program = output / "command-negative"
        run(["/usr/bin/clang", *builder.HOST_FLAGS, "-fsanitize=address,undefined", *includes,
             *[name for name in builder.GEOMETRY if name != "src/graphics/m2_compact.c"],
             "src/diagnostics/m2_rebuild/camera.c", "tests/flight_demo/m2_rebuild/command_host.c",
             "-o", program], "command-compile.txt")
        run([program], "command.txt")
        program = output / "text"
        run(["/usr/bin/clang", *builder.HOST_FLAGS, "-fsanitize=address,undefined", *includes,
             "src/graphics/m2_rebuild_text.c", "tests/flight_demo/m2_rebuild/text_compact.c",
             "-o", program], "text-compile.txt")
        run([program], "text.txt")
        report["status"] = "PASS"
    except Exception as error:
        report["failure"] = str(error)
    finally:
        report["inputs"] = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for folder in ["src/graphics", "tests/flight_demo/m2_rebuild", "tools/flight_demo/m2_rebuild"]
            for path in (ROOT / folder).glob("*") if path.is_file()}
        report["source_archive"] = builder.archive_sources(output, report["inputs"])
        (output / "result.json").write_text(json.dumps(report, indent=2) + "\n")
        (output / "seal.json").write_text(json.dumps({str(path.relative_to(output)):
            {"bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            for path in sorted(output.rglob("*")) if path.is_file()}, indent=2) + "\n")
    print(json.dumps({"output": str(output), "status": report["status"]}))
    return 0 if report["status"] == "PASS" else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=["host", "independent", "focused", "target"], required=True)
    parser.add_argument("--sdk", type=Path)
    parser.add_argument("--profile", choices=["extended"])
    args = parser.parse_args()
    evidence = EVIDENCE
    identity = IDENTITY
    profile = None
    extra = []
    sources = []
    if args.profile == "extended":
        import tempfile
        residency = module(ROOT / "tools/flight_demo/m2_rebuild/residency.py", "extended_residency")
        data = residency.load()
        with tempfile.TemporaryDirectory() as directory:
            generated = Path(directory)
            residency.generate(destination=generated)
            for name in residency.OUTPUTS:
                assert (ROOT / name).read_bytes() == (generated / name).read_bytes(), name
        profile = {"identity": data["identity"], "resident_end": data["development_resident"][1],
                   "production_end": data["production_resident"][1],
                   "link_script": "src/platform/m2_rebuild/extended_resident.ld"}
        evidence = ROOT / "docs/evidence/flight-demo/2026-10-30-m2-extended-resident"
        identity = data["identity"]
        extra = [residency.CONTRACT, *residency.OUTPUTS]
        sources = ["src/platform/m2_rebuild/extended_startup_45gs02.s"]
    builder = module(ROOT / "tools/flight_demo/m2_rebuild/validate.py", "m2_command_builder")
    builder.GEOMETRY = ["src/environment/m2_fixture.c", "src/graphics/m2_limb.c",
        "src/graphics/m2_compact.c", "src/graphics/m2_compact_public.c",
        "src/graphics/m2_record_private.c", "interfaces/generated/m2_tables.c"]
    parent = module(ROOT / "tools/flight_demo/m2_rebuild/compact_validate.py", "m2_independent_checks")
    parent.IDENTITY = identity
    if args.tier == "independent":
        capture = evidence / ("independent-" + str(time.time_ns()))
        capture.mkdir()
        inputs = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for folder in ["src/graphics", "src/diagnostics/m2_rebuild", "tools/flight_demo/m2_rebuild",
                           "tests/flight_demo/m2_rebuild"]
            for path in (ROOT / folder).glob("*") if path.is_file()}
        builder.archive_sources(capture, inputs)
        (capture / "inputs.json").write_text(json.dumps(inputs, indent=2) + "\n")
        return parent.extra_host(builder, capture / "run")
    if args.tier == "focused":
        return focused(builder, evidence / ("focused-" + str(time.time_ns())))
    if args.tier == "target" and args.sdk is None:
        parser.error("absolute pinned --sdk required")
    checker = module(ROOT / "tools/flight_demo/m2_rebuild/compact_check.py", "m2_command_link_check")
    checker.REQUIRED += ["m2_bundle_fields", "m2_camera_same", "m2_command_service"]
    if args.tier == "host":
        generation = module(ROOT / "tools/flight_demo/m2_rebuild/commands.py", "m2_command_generation")
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            generated = Path(directory) / "commands.inc"
            generation.generate(generated)
            assert generated.read_bytes() == (ROOT / "src/graphics/m2_commands.inc").read_bytes()
    return builder.execute(args.tier, args.sdk, evidence / (args.tier + "-" + str(time.time_ns())),
        identity=identity, composition_check=checker.check,
        extra_inputs=["src/graphics/m2_commands.inc", "tools/flight_demo/m2_rebuild/commands.py",
                      "tests/flight_demo/m2_rebuild/command_host.c", *extra],
        target_profile=profile, extra_target_sources=sources,
        archive_inputs=True,
        service_cardinality={"prepare": "one checked command or one kernel unit plus finalization",
          "project": "one checked command or one kernel unit plus finalization",
          "background": "eight cached-boundary comparisons and tile writes",
          "copy": "one checked64-byte copy", "line": "one cursor begin/step or pixel+one-bytecopy",
          "text": "one40-character row format and one64-byte glyph",
          "commit": "exact field verification and checked physical selector/latch"})


if __name__ == "__main__":
    sys.exit(main())
