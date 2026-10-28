"""Finalize local source/evidence scope; never builds, executes or publishes."""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time
import tarfile

from toolchain_identity import digest, verify

ROOT = Path(__file__).resolve().parents[3]
HISTORICAL = ROOT / "docs/evidence/flight-demo/2026-10-27-m2-min-rebuild"
HERE = ROOT / "docs/evidence/flight-demo/2026-10-27-m2-min-rebuild-corrections"
BASE = "b044440fa98c2dfc91ec590668049610afc98a1e"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root)


def main():
    output = HERE / ("final-check-" + str(time.time_ns()))
    output.mkdir(exist_ok=False)
    assert git(ROOT, "rev-parse", "HEAD").decode().strip() == BASE
    assert git(ROOT, "rev-parse", "origin/main").decode().strip() == BASE
    branch = git(ROOT, "branch", "--show-current").decode().strip()
    assert branch == "codex/65aero-m2-minimum-renderer-baseline"
    main = json.loads((HISTORICAL / "main-verification.json").read_text())
    assert main["remote_main"] == BASE and main["main_ci"]["head"] == BASE
    assert main["main_ci"]["conclusion"] == "success"
    assert git(ROOT, "diff", "--name-only", BASE).decode().splitlines() == ["WORK_IN_PROGRESS.md"]
    assert not git(ROOT, "diff", "--cached", "--name-only")
    diff_check = subprocess.run(["git", "diff", "--check"], cwd=ROOT, capture_output=True, text=True)
    assert diff_check.returncode == 0, diff_check.stdout + diff_check.stderr
    prefixes = ("docs/evidence/flight-demo/2026-10-27-m2-min-rebuild/",
                "docs/evidence/flight-demo/2026-10-27-m2-min-rebuild-corrections/",
                "docs/evidence/flight-demo/2026-10-27-m2-source-baseline-preflight/",
                "src/diagnostics/m2_rebuild/", "src/platform/m2_rebuild/",
                "tests/flight_demo/m2_rebuild/", "tools/flight_demo/m2_rebuild/")
    exact = {"WORK_IN_PROGRESS.md", "docs/plans/65AERO_M2_MINIMUM_REBUILD_BUILD_INTENT.md",
             "docs/reports/M2_MINIMUM_REBUILD_BASELINE.md", "docs/reports/M2_MINIMUM_REBUILD_CORRECTIONS.md", "interfaces/m2_rebuild.json",
             "interfaces/generated/m2_rebuild_profile.h", "memory/m2-rebuild-ledger.json",
             "src/input/m2_rebuild_input.c", "src/input/m2_rebuild_input.h",
             "src/graphics/m2_rebuild.c", "src/graphics/m2_rebuild.h", "src/graphics/m2_rebuild_text.c"}
    paths = ["WORK_IN_PROGRESS.md"] + [name.decode() for name in
        git(ROOT, "ls-files", "--others", "--exclude-standard", "-z").split(b"\0") if name]
    for name in paths:
        assert name in exact or name.startswith(prefixes), name
        path = ROOT / name
        assert path.is_file() and not path.is_symlink(), name
        try:
            text = path.read_text()
        except UnicodeError:
            continue
        assert all(line == line.rstrip(" \t") for line in text.splitlines()), name
        if path.suffix == ".py":
            ast.parse(text, filename=name)
    before = json.loads((HERE / "before.json").read_text())
    original_files = {str(p.relative_to(ROOT)) for p in HISTORICAL.rglob("*") if p.is_file()}
    assert original_files == set(before["original_packet_files"])
    for name, identity in before["original_packet_files"].items():
        assert sha(ROOT / name) == identity["sha256"] and (ROOT / name).stat().st_size == identity["bytes"]
    assert sha(HERE / "before-source.tar.gz") == before["archive_sha256"]
    with tarfile.open(HERE / "before-source.tar.gz", "r:gz") as archive:
        assert {m.name for m in archive.getmembers()} == set(before["source"])
        for name, identity in before["source"].items():
            raw = archive.extractfile(name).read()
            assert len(raw) == identity["bytes"] and hashlib.sha256(raw).hexdigest() == identity["sha256"]
    packet_results = {}
    for parent in [HISTORICAL, HERE]:
        for packet in parent.iterdir():
            if packet == output or not packet.is_dir() or not (packet / "seal.json").is_file():
                continue
            identities = json.loads((packet / "seal.json").read_text())
            members = {str(p.relative_to(packet)) for p in packet.rglob("*")
                       if p.is_file() and p != packet / "seal.json"}
            assert members == set(identities), packet.name
            for name, identity in identities.items():
                path = packet / name
                assert sha(path) == identity["sha256"] and path.stat().st_size == identity["bytes"], str(path)
            packet_results[str(packet.relative_to(ROOT))] = {
                "members": len(identities), "seal_sha256": sha(packet / "seal.json"), "status": "UNCHANGED"}
    claim = json.loads((HERE / "relink-claim.json").read_text())
    assert claim["authorized_relinks"] == 1
    target_packet = ROOT / claim["output"]
    target = json.loads((target_packet / "result.json").read_text())
    assert sum(c["argv"][0].endswith("mos-mega65-clang") for c in target["commands"]) == 1
    application = {name: expected for name, expected in target["inputs"].items()
                   if not name.startswith(("tools/", "tests/"))}
    assert all(sha(ROOT / name) == expected for name, expected in application.items())
    assert target["resident_bytes"] == target["resident_end"] - 0x2001
    assert target["deficit"] == max(0, target["resident_bytes"] - 24575)
    sdk_inventory_path = target_packet / target["toolchain"]["sdk_inventory"]
    assert sha(sdk_inventory_path) == target["toolchain"]["sdk_inventory_sha256"]
    sdk_inventory = json.loads(sdk_inventory_path.read_text())
    assert digest(sdk_inventory) == claim["sdk_identity_digest"] == target["toolchain"]["sdk_identity_digest"]
    verify(Path(target["toolchain"]["sdk"]), sdk_inventory)
    assert target["toolchain"]["sdk_unchanged_after_link"] is True
    original = Path("/Users/slice/Developer/f65-megawing")
    approved = json.loads((ROOT / "docs/evidence/flight-demo/2026-10-27-m2-residency-feasibility/accounting.json").read_text())["original_checkout_before"]
    original_paths = sorted({name.decode() for name in git(original, "ls-files", "--modified", "--others", "--exclude-standard", "-z").split(b"\0") if name})
    original_status = hashlib.sha256(git(original, "status", "--porcelain=v1")).hexdigest()
    original_diff = hashlib.sha256(git(original, "diff", "--binary")).hexdigest()
    assert original_status == approved["status_sha256"]
    assert original_diff == approved["diff_sha256"]
    assert len(original_paths) == approved["path_count"] == 480
    old_inventory = json.loads((HISTORICAL / "final-check-1793159584829644000/original-checkout-current-inventory.json").read_text())
    assert set(original_paths) == set(old_inventory)
    assert all(sha(original / name) == item["sha256"] and (original / name).stat().st_size == item["bytes"]
               for name, item in old_inventory.items())
    assert git(original, "rev-parse", "HEAD").decode().strip() == approved["head"]
    assert git(original, "branch", "--show-current").decode().strip() == approved["branch"]
    inventory = {name: {"bytes": (original / name).stat().st_size, "sha256": sha(original / name)}
                 for name in original_paths}
    (output / "original-checkout-current-inventory.json").write_text(json.dumps(inventory, indent=2) + "\n")
    design = Path("/Users/slice/Developer/f65-megawing-m2-residency-feasibility")
    assert git(design, "rev-parse", "HEAD").decode().strip() == "cacb6e9d88c7cfd297a2d57c854b5861323902d9"
    assert not git(design, "status", "--porcelain=v1")
    inputs = {name: {"bytes": (ROOT / name).stat().st_size, "sha256": sha(ROOT / name)}
              for name in sorted(paths) if not name.startswith("docs/evidence/")}
    result = {"identity": "65AERO-M2-MIN-REBUILD-CORRECTIONS-1", "status": "READY FOR REVIEW",
              "base": BASE, "branch": branch, "main_verified": main,
              "public_and_historical_tracked_bytes": "unchanged; only tracked diff is WIP",
              "scope_paths": sorted(paths), "scope": "PASS", "whitespace_and_python_syntax": "PASS",
              "sealed_packets": packet_results,
              "measured_application_input_parity": "PASS; corrected target inputs unchanged after the one authorized relink",
              "relinks_used": 1, "before_archive_verified": True, "original_packet_files_verified": len(original_files),
              "original_checkout": {"head": approved["head"], "branch": approved["branch"],
                  "status_sha256": original_status, "diff_sha256": original_diff,
                  "path_count": len(original_paths), "status_diff_and_count_match_prior": True,
                  "current_inventory": "original-checkout-current-inventory.json",
                  "current_inventory_sha256": sha(output / "original-checkout-current-inventory.json"),
                  "prior_aggregate_content_digest": approved["content_inventory_sha256"],
                  "prior_aggregate_encoding_reproduced": False,
                  "scope": "current file hashes recorded; prior aggregate encoding not reproduced; not an ignored-path or full historical-worktree inventory"},
              "approved_design_checkout": "clean at cacb6e9d88c7cfd297a2d57c854b5861323902d9",
              "historical_recovery": {"members": 37, "previously_verified": 22, "unresolved": 15,
                   "git_worktree_tier": "8 prior checkouts remain NOT VERIFIED",
                   "reconstructed_files": 0, "reconstructed_metadata": 0},
              "sdk_inventory": str(sdk_inventory_path.relative_to(ROOT)),
              "sdk_identity_digest": digest(sdk_inventory),
              "sdk_inventory_entries": len(sdk_inventory["entries"]), "sdk_unchanged_after_link_and_final_check": True, "final_source_identities": inputs,
              "target_relinked": True, "target_executed": False, "committed": False,
              "pushed": False, "xemu": "NOT RUN", "banking": "NOT IMPLEMENTED",
              "resident_fit": target["resident_fit"], "resident_bytes": target["resident_bytes"], "deficit": target["deficit"], "reserve_used": 0}
    (output / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    (output / "seal.json").write_text(json.dumps({p.name: {"bytes": p.stat().st_size, "sha256": sha(p)}
                for p in sorted(output.iterdir()) if p.is_file()}, indent=2) + "\n")
    print(json.dumps({"output": str(output), "scope": "PASS", "sealed_packets": len(packet_results),
                      "original_paths": len(original_paths), "sdk_inputs": len(sdk_inventory["entries"]),
                      "resident_bytes": target["resident_bytes"], "deficit": target["deficit"], "status": "READY FOR REVIEW"}))


if __name__ == "__main__":
    main()
