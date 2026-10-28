"""New source-complete baseline checks. Never executes a target or admits runtime.

Every invocation gets a fresh output directory. All failures remain sealed.
Use --tier target only after reviewing the corresponding host results.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import time
import zlib

ROOT = Path(__file__).resolve().parents[3]
BASE = "b044440fa98c2dfc91ec590668049610afc98a1e"
EVIDENCE = ROOT / "docs/evidence/flight-demo/2026-10-27-m2-min-rebuild-corrections"
INCLUDES = ["interfaces/generated", "src/core", "src/input", "src/presentation",
            "src/environment", "src/graphics", "src/diagnostics/m2_rebuild",
            "src/platform/m2_rebuild", "src/platform/m1", "src/diagnostics/r0f"]
GEOMETRY = ["src/environment/m2_fixture.c", "src/graphics/m2_geometry.c",
            "interfaces/generated/m2_tables.c"]
CORE = ["src/core/m1_runtime.c", "src/input/m1_input.c", "src/presentation/m1_snapshot.c"]
NEW = ["src/input/m2_rebuild_input.c", "src/diagnostics/m2_rebuild/camera.c",
       "src/graphics/m2_rebuild.c", "src/graphics/m2_rebuild_text.c",
       "src/platform/m2_rebuild/guard.c"]
PLATFORM = ["src/platform/m1/m1_platform.c", "src/diagnostics/r0f/combined_platform.c",
            "src/diagnostics/r0f/combined_model.c", "src/platform/r0f/qualification_45gs02.s",
            "src/platform/r0f/combined_45gs02.s", "src/platform/m2_rebuild/platform.c",
            "src/platform/m2_rebuild/startup_45gs02.s"]
FLAGS = ["-mcpu=mos45gs02", "-mlto-zp=0", "-Oz", "-fno-inline-functions",
         "-fno-jump-tables", "-Wall", "-Wextra", "-Wconversion", "-Werror"]
HOST_FLAGS = ["-std=c11", "-Wall", "-Wextra", "-Wconversion", "-Werror"]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def preview(raw, output):
    pixels = raw.read_bytes()
    assert len(pixels) == 320 * 200
    palette = {1: (0, 0, 0), 2: (0, 85, 255), 3: (0, 170, 34), 4: (255, 255, 255)}
    scanlines = bytearray()
    for y in range(200):
        scanlines.append(0)
        for index in pixels[y * 320:(y + 1) * 320]:
            scanlines.extend(palette[index])
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
    output.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 320, 200, 8, 2, 0, 0, 0))
                       + chunk(b"IDAT", zlib.compress(scanlines)) + chunk(b"IEND", b""))


def execute(tier, sdk, output):
    # Bind the caller's SDK before commands change cwd to ROOT. Use this same
    # absolute path for lock checks, inventories, subprocesses and evidence.
    sdk = sdk.resolve() if sdk is not None else None
    output.mkdir(parents=True, exist_ok=False)
    report = {"identity": "65AERO-M2-MIN-REBUILD-CORRECTIONS-1",
              "profile_identity": "65AERO-M2-MIN-REBUILD-1", "base": BASE, "tier": tier,
              "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "commands": [], "target_executed": False, "execution_admitted": False,
              "reserve_used": 0, "banking": False}
    report_path = output / "result.json"

    def save():
        report_path.write_text(json.dumps(report, indent=2) + "\n")

    def run(command, log, required=True):
        command = list(map(str, command))
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        (output / log).write_text(result.stdout + result.stderr)
        report["commands"].append({"argv": command, "exit": result.returncode, "log": log})
        save()
        if required and result.returncode:
            raise RuntimeError(log + " failed, exit " + str(result.returncode))
        return result

    try:
        ancestry = subprocess.run(["git", "merge-base", "--is-ancestor", BASE, report["head"]], cwd=ROOT)
        assert ancestry.returncode == 0, "baseline ancestry changed; inspect before proceeding"
        contract = module(ROOT / "tools/flight_demo/m2_rebuild/generate.py", "m2rb_generate")
        # A temporary generation proves bytes without modifying canonical inputs.
        generated = output / "generated"
        contract.generate(destination=generated)
        for path in ["interfaces/generated/m2_rebuild_profile.h", "memory/m2-rebuild-ledger.json"]:
            assert (ROOT / path).read_bytes() == (generated / path).read_bytes(), path
        report["generated"] = "PASS"
        includes = ["-I" + path for path in INCLUDES]
        if tier == "host":
            run([sys.executable, "-B", "-m", "unittest", "discover", "-s",
                 "tests/flight_demo/m2_rebuild", "-p", "test_*.py", "-v"], "contracts.txt")
            program = output / "host"
            run(["/usr/bin/clang", *HOST_FLAGS, "-fsanitize=address,undefined", *includes,
                 *GEOMETRY, *CORE, *NEW, "tests/flight_demo/m2_rebuild/host.c", "-o", program], "host-compile.txt")
            run([program, output / "host-frame.indices"], "host.txt")
            preview(output / "host-frame.indices", output / "host-frame.png")
            for name, sources in [
                ("geometry-host", GEOMETRY + CORE + ["tests/flight_demo/m2/host.c"]),
                ("prepared-host", GEOMETRY + ["tests/flight_demo/m2_full/prepared_host.c"]),
                ("cursor-host", GEOMETRY + ["tests/flight_demo/m2_pr2/cursor_host.c"])]:
                program = output / name
                run(["/usr/bin/clang", *HOST_FLAGS, "-fsanitize=address,undefined",
                     *includes, *sources, "-o", program], name + "-compile.txt")
                run([program], name + ".txt")
            library = output / "geometry.dylib"
            run(["/usr/bin/clang", *HOST_FLAGS, "-O2", "-shared", "-fPIC",
                 *includes, *GEOMETRY, "-o", library], "oracle-compile.txt")
            run([sys.executable, "-B", "tests/flight_demo/m2/oracle.py", library], "geometry-oracle.txt")
            run([sys.executable, "-B", "tests/flight_demo/m2/clip_regressions.py", library], "near-far-oracle.txt")
            run([sys.executable, "-B", "-m", "unittest", "discover", "-s", "tools/ci",
                 "-p", "test_*.py", "-v"], "ci-policy-tests.txt")
            report["host"] = "PASS; synthetic grants only"
        else:
            lock = json.loads((ROOT / "toolchain/f65_toolchain.lock.json").read_text())["llvm_mos"]
            for tool, key in [("mos-mega65-clang", "compiler_sha256"), ("llvm-objdump", "objdump_sha256")]:
                assert sha(sdk / "bin" / tool) == lock[key], tool
            report["toolchain"] = {"sdk": str(sdk), "compiler_sha256": lock["compiler_sha256"],
                                   "objdump_sha256": lock["objdump_sha256"], "flags": FLAGS}
            identity = module(ROOT / "tools/flight_demo/m2_rebuild/toolchain_identity.py", "m2rb_sdk_identity")
            sdk_inputs = identity.capture(sdk)
            sdk_record = output / "sdk-inputs-before.json"
            sdk_record.write_text(json.dumps(sdk_inputs, indent=2) + "\n")
            report["toolchain"].update(sdk_inventory="sdk-inputs-before.json",
                sdk_inventory_sha256=sha(sdk_record), sdk_identity_digest=identity.digest(sdk_inputs),
                sdk_identity_scope=sdk_inputs["scope"], sdk_entries=len(sdk_inputs["entries"]))
            # Create-once claim enforces the one founder-authorized target relink.
            claim = {"identity": report["identity"], "output": str(output.relative_to(ROOT)),
                     "authorized_relinks": 1, "sdk_identity_digest": identity.digest(sdk_inputs)}
            with (output.parent / "relink-claim.json").open("x") as stream:
                stream.write(json.dumps(claim, indent=2) + "\n")
            # Default SDK measurement envelope is NOT the resident admission limit.
            sources = GEOMETRY + CORE + NEW + PLATFORM + ["src/diagnostics/m2_rebuild/main.c"]
            target = output / "UNADMITTED.prg"
            try:
                compile_result = run([sdk / "bin/mos-mega65-clang", *FLAGS, *includes, *sources,
                      "-Wl,-T,src/platform/m2_rebuild/startup.ld",
                      "-Wl,-Map," + str(output / "UNADMITTED.map"), "-o", target], "target-compile.txt", required=False)
            finally:
                identity.verify(sdk, sdk_inputs)
                report["toolchain"]["sdk_unchanged_after_link"] = True
                save()
            report["compile_link"] = "PASS" if compile_result.returncode == 0 else "FAIL"
            sections = {}
            if (output / "UNADMITTED.map").exists():
                mapping = (output / "UNADMITTED.map").read_text()
                for name in [".text", ".rodata", ".data", ".bss", ".noinit"]:
                    match = re.search(r"^\s*([0-9a-f]+)\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+" + re.escape(name) + r"$", mapping, re.M)
                    if match:
                        start, size = [int(value, 16) for value in match.groups()]
                        sections[name] = {"start": start, "bytes": size}
            report["sections"] = sections
            if sections:
                end = max(item["start"] + item["bytes"] for item in sections.values())
                report.update(resident_start=0x2001, resident_end=end, resident_bytes=end - 0x2001,
                              resident_limit=24575, deficit=max(0, end - 0x8000),
                              resident_fit="PASS" if end <= 0x8000 else "FAIL",
                              remaining_margin=0x8000 - end,
                              software_stack_envelope=[0xc000, 0xd000], hardware_stack_envelope=[0x100, 0x200],
                              compiler_scratch=sections.get(".noinit"),
                              stack_collision=(end > 0xc000))
            if compile_result.returncode == 0:
                for tool, args, name in [("llvm-objdump", ["-d"], "UNADMITTED.disassembly"),
                                         ("llvm-nm", ["-S", "--size-sort"], "UNADMITTED.symbols")]:
                    run([sdk / "bin" / tool, *args, str(target) + ".elf"], name)
                report["prg"] = {"bytes": target.stat().st_size, "sha256": sha(target)}
                disassembly = (output / "UNADMITTED.disassembly").read_text()
                symbols = (output / "UNADMITTED.symbols").read_text()
                required = ["m2rb_dispatch", "m2rb_camera_edges", "m2rb_platform_init", "m2rb_glyph",
                            "m2_prepare", "m2_project_prepared", "m2_ground_prepared", "m2rb_io_commit",
                            "m1_tick", "m1_input_sample", "m1_acquire", "r0f_pf_flat_copy"]
                report["retained_implementation"] = {name: bool(re.search(r"\b" + name + r"$", symbols, re.M)) for name in required}
                assert all(report["retained_implementation"].values()), "incomplete target composition"
                startup = module(ROOT / "tools/flight_demo/m2_rebuild/startup_check.py", "m2rb_startup_check")
                report["startup_static"] = startup.check(disassembly, symbols, target.read_bytes())
                checker = module(ROOT / "tools/flight_demo/m2/stack_check.py", "m2rb_stack")
                try:
                    report["stack_probe"] = checker.check(disassembly)
                except (ValueError, KeyError) as error:
                    report["stack_probe"] = {"status": "UNPROVEN", "reason": str(error)}
                report["whole_program_stack"] = "UNPROVEN; probe checker does not admit startup, IRQ/NMI, trap/fault or all compiler paths"
            report["service"] = {"status": "UNPROVEN", "target_grants": [0] * 8,
                                 "guard_grant": 0, "runtime_launch": "disabled",
                                 "quantum_cardinality": {"prepare": "one integrated transform + registration",
                                    "project": "one segment; total nine per generation", "background": "eight exact horizon samples",
                                    "copy": "one copy <=64 bytes", "line": "one begin/advance or one pixel+one-byte copy",
                                    "text": "one <=40-character row format plus one 64-byte glyph",
                                    "commit": "one complete bundle validation + checked physical selector"},
                                 "note": "Cardinality is not timing admission. No nonzero cycle bounds invented."}
            if compile_result.returncode:
                raise RuntimeError("target compile/link failed; retained without optimization")
        report["checks_completed"] = True
    except Exception as error:
        report["checks_completed"] = False
        report["failure"] = str(error)
    finally:
        paths = set(GEOMETRY + CORE + NEW + PLATFORM + ["src/diagnostics/m2_rebuild/main.c",
                    "interfaces/m2_rebuild.json", "src/platform/m2_rebuild/startup.ld",
                    "toolchain/f65_toolchain.lock.json"])
        for directory in INCLUDES:
            paths.update(str(path.relative_to(ROOT)) for path in (ROOT / directory).glob("*.h"))
        for directory in ["tools/flight_demo/m2_rebuild", "tests/flight_demo/m2_rebuild"]:
            paths.update(str(path.relative_to(ROOT)) for path in (ROOT / directory).glob("*") if path.is_file())
        paths.update(["tests/flight_demo/m2/oracle.py", "tests/flight_demo/m2/clip_regressions.py",
                      "tests/flight_demo/m2/host.c", "tests/flight_demo/m2_full/prepared_host.c",
                      "tests/flight_demo/m2_pr2/cursor_host.c", "tools/flight_demo/m2/stack_check.py"])
        report["inputs"] = {name: sha(ROOT / name) for name in sorted(paths)}
        save()
        inventory = {str(path.relative_to(output)): {"bytes": path.stat().st_size, "sha256": sha(path)}
                     for path in sorted(output.rglob("*")) if path.is_file()}
        (output / "seal.json").write_text(json.dumps(inventory, indent=2) + "\n")
    print(json.dumps({"output": str(output), "checks_completed": report["checks_completed"],
                      "failure": report.get("failure"), "resident_bytes": report.get("resident_bytes"),
                      "deficit": report.get("deficit")}))
    passed = report["checks_completed"] and (tier == "host" or report.get("resident_fit") == "PASS")
    return 0 if passed else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", choices=["host", "target"], required=True)
    parser.add_argument("--sdk", type=Path)
    parser.add_argument("--evidence-root", type=Path, default=EVIDENCE,
                        help="fresh authorized packet root; each root permits one target relink")
    args = parser.parse_args()
    if args.tier == "target" and args.sdk is None:
        parser.error("--sdk is required for target; use the pinned existing SDK")
    output = args.evidence_root.resolve() / (args.tier + "-" + str(time.time_ns()))
    return execute(args.tier, args.sdk, output)


if __name__ == "__main__":
    raise SystemExit(main())
