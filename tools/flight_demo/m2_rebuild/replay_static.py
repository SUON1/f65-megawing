"""Read pinned target evidence into a fresh report. No compiler or target calls."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
PACKET = ROOT / "docs/evidence/flight-demo/2026-10-27-m2-min-rebuild/target-1793158803095519000"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    output = ROOT / "docs/evidence/flight-demo/2026-10-27-m2-min-rebuild-corrections" / ("historical-replay-" + str(time.time_ns()))
    output.mkdir(exist_ok=False)
    sealed = json.loads((PACKET / "seal.json").read_text())
    for name, identity in sealed.items():
        path = PACKET / name
        assert path.stat().st_size == identity["bytes"] and sha(path) == identity["sha256"], name
    report = json.loads((PACKET / "result.json").read_text())
    disassembly = (PACKET / "UNADMITTED.disassembly").read_text()
    symbol_text = (PACKET / "UNADMITTED.symbols").read_text()
    checker = load_module(ROOT / "tools/flight_demo/m2_rebuild/startup_check.py", "startup_check")
    stack = load_module(ROOT / "tools/flight_demo/m2/stack_check.py", "stack_check")
    changes = {name: {"linked": expected, "current": sha(ROOT / name)}
               for name, expected in report["inputs"].items() if sha(ROOT / name) != expected}
    # Validators may change; the measured application source must not change.
    result_scope = "historical input identities only; current corrected source may differ"
    # Replaying history never relabels current source as the old measured image.
    result = {key: report[key] for key in ["identity", "base", "compile_link", "prg", "sections",
              "resident_start", "resident_end", "resident_bytes", "resident_limit", "resident_fit",
              "deficit", "remaining_margin", "compiler_scratch", "software_stack_envelope",
              "hardware_stack_envelope", "stack_collision", "reserve_used", "retained_implementation"]}
    result.update(replayed_packet=str(PACKET.relative_to(ROOT)),
                  original_result_sha256=sha(PACKET / "result.json"), original_seal_sha256=sha(PACKET / "seal.json"),
                  application_source_parity=result_scope, current_input_changes=changes,
                  relinked=False, target_executed=False, banking=False, execution_admitted=False)
    result["startup_static"] = checker.check_normal_prefix(disassembly, symbol_text)
    try:
        result["terminal_handler"] = checker.check(disassembly, symbol_text, (PACKET / "UNADMITTED.prg").read_bytes())
    except ValueError as error:
        result["terminal_handler"] = {"status": "FAIL", "reason": str(error)}
    try:
        result["probe_stack_result"] = stack.check(disassembly)
    except (KeyError, ValueError) as error:
        result["probe_stack_result"] = {"status": "UNPROVEN", "reason": str(error)}
    result["whole_program_stack"] = "UNPROVEN; reachable compiler helpers, startup, trap, fault, IRQ/NMI paths lack a complete conservative proof"
    result["service"] = {"status": "UNPROVEN", "target_operation_grants": [0] * 8, "guard_grant": 0,
                         "units": "authoritative native clock counts; all unknown bounds deny work",
                         "100_hz_clock": "unchanged", "stages": 21, "skip_or_merge_ticks": False,
                         "target_launch": "disabled", "cycles_measured": False}
    symbols = []
    for line in symbol_text.splitlines():
        match = re.match(r"^([0-9a-f]+) ([0-9a-f]+) ([A-Za-z]) (.+)$", line)
        if match:
            symbols.append({"address": int(match[1], 16), "bytes": int(match[2], 16),
                            "kind": match[3], "name": match[4]})
    result["largest_code_symbols"] = sorted([s for s in symbols if s["kind"].lower() == "t"],
                                             key=lambda item: item["bytes"], reverse=True)[:20]
    result["all_bss_symbols"] = [s for s in symbols if s["kind"].lower() == "b"]
    result["renderer_workspace"] = next(s for s in symbols if s["name"] == "renderer")
    result["bss_symbol_sum"] = sum(s["bytes"] for s in result["all_bss_symbols"])
    result["static_layout"] = {"base_page": [0x200, 0x300], "compiler_pseudoregisters": [0x202, 0x222],
                               "flat_copy_pointer_scratch": [0x222, 0x22a],
                               "display_stores": [[0x20000, 0x2f840], [0x30000, 0x3f840]],
                               "color": [0xff80000, 0xff807d0], "rom_backup": [0x8000000, 0x8020000],
                               "protected_reserve": [0x58000, 0x60000], "reserve_used": 0,
                               "aliasing": "none; cache, bundles, tile/text and cursor have distinct storage"}
    result["unqualified_display"] = "No target visual proof. V200 physical row alignment, PAL/NTSC border cropping, palette/mode/readback and safe pointer-prefetch commit remain unqualified."
    tests = subprocess.run([sys.executable, "-B", "-m", "unittest", "discover", "-s",
                            "tests/flight_demo/m2_rebuild", "-p", "test_*.py", "-v"],
                           cwd=ROOT, capture_output=True, text=True)
    (output / "tests.txt").write_text(tests.stdout + tests.stderr)
    result["contract_and_startup_tests"] = {"exit": tests.returncode, "log": "tests.txt"}
    for name, identity in sealed.items():
        assert sha(PACKET / name) == identity["sha256"], name
    assert sha(PACKET / "seal.json") == result["original_seal_sha256"]
    result["sealed_packet_preservation"] = "PASS"
    result["verifiers"] = {str(path.relative_to(ROOT)): sha(path) for path in [
        Path(__file__).resolve(), ROOT / "tools/flight_demo/m2_rebuild/startup_check.py",
        ROOT / "tests/flight_demo/m2_rebuild/test_startup.py", ROOT / "tools/flight_demo/m2/stack_check.py"]}
    (output / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    (output / "seal.json").write_text(json.dumps({p.name: {"bytes": p.stat().st_size, "sha256": sha(p)}
                                                for p in sorted(output.iterdir()) if p.is_file()}, indent=2) + "\n")
    print(json.dumps({"output": str(output), "resident_fit": result["resident_fit"],
                      "deficit": result["deficit"], "startup_static": result["startup_static"],
                      "stack": result["probe_stack_result"], "tests_exit": tests.returncode}))
    return tests.returncode


if __name__ == "__main__":
    raise SystemExit(main())
