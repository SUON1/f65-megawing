"""Seal verified extended-profile progress; no build or target execution."""
import ast
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile

import residency
import toolchain_identity

ROOT = Path(__file__).resolve().parents[3]
BASE = "aed5bfb2014e8f3df28118668e5f24ded0ddad9e"
PACKET = ROOT / "docs/evidence/flight-demo/2026-10-30-m2-extended-resident"
CHECKPOINT = ROOT / "docs/evidence/flight-demo/2026-10-30-m2-extended-resident-publication"
TARGET = PACKET / "target-1793405200824046000"
FINAL = PACKET / "qualification-1793405443233721000"
MODIFIED = {"WORK_IN_PROGRESS.md", "tools/flight_demo/m2_rebuild/commands_validate.py",
            "tools/flight_demo/m2_rebuild/validate.py"}
NEW = {"interfaces/m2_extended_resident.json", "interfaces/generated/m2_extended_resident.h",
       "memory/m2-extended-resident-ledger.json", "src/platform/m2_rebuild/extended_resident.ld",
       "src/platform/m2_rebuild/extended_startup_45gs02.s",
       "tests/flight_demo/m2_rebuild/residency_ranges.c",
       "tests/flight_demo/m2_rebuild/test_extended_residency.py",
       "tests/flight_demo/m2_rebuild/test_linked_admission.py",
       "tests/flight_demo/m2_rebuild/test_stack_admission.py",
       "tools/flight_demo/m2_rebuild/extended_admit.py",
       "tools/flight_demo/m2_rebuild/linked_admission.py",
       "tools/flight_demo/m2_rebuild/residency.py",
       "tools/flight_demo/m2_rebuild/stack_admission.py",
       "tools/flight_demo/m2_rebuild/extended_publication.py",
       "docs/reports/M2_EXTENDED_RESIDENT_ADMISSION.md"}


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root)


def identity(path):
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def check_seal(seal):
    inventory = json.loads(seal.read_text())
    for name, expected in inventory.items():
        if identity(seal.parent / name) != expected:
            raise ValueError("sealed identity changed: " + str(seal.parent / name))
    members = {str(p.relative_to(seal.parent)) for p in seal.parent.rglob("*")
               if p.is_file() and p != seal}
    if members != set(inventory):
        raise ValueError("sealed membership changed: " + str(seal))
    return len(inventory)


def preserve_checker_sources():
    """Copy only bytes already present, whose SHA matches each recorded run."""
    destination = PACKET / "verification-sources"
    if destination.exists():
        return
    by_digest = {}
    for archive_path in sorted(PACKET.glob("*/source.tar.gz")):
        with tarfile.open(archive_path, "r:gz") as archive:
            for member in archive:
                if member.isfile():
                    raw = archive.extractfile(member).read()
                    by_digest[hashlib.sha256(raw).hexdigest()] = raw
    destination.mkdir(exist_ok=False)
    records = {}
    for qualified in sorted(PACKET.glob("qualification-*/result.json")):
        report = json.loads(qualified.read_text())
        inputs = report["checker_inputs"]
        target = destination / (qualified.parent.name + ".tar.gz")
        with target.open("xb") as raw_file, gzip.GzipFile(fileobj=raw_file, mode="wb", mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w") as archive:
                for name, digest in sorted(inputs.items()):
                    current = (ROOT / name).read_bytes()
                    raw = current if hashlib.sha256(current).hexdigest() == digest else by_digest[digest]
                    assert hashlib.sha256(raw).hexdigest() == digest
                    member = tarfile.TarInfo(name)
                    member.size = len(raw); member.mode = 0o644; member.mtime = 0
                    archive.addfile(member, io.BytesIO(raw))
        records[qualified.parent.name] = {"inputs": inputs, "archive": identity(target),
            "provenance": "exact current or already archived bytes matched by original run SHA; no reconstruction"}
    (destination / "identities.json").write_text(json.dumps(records, indent=2) + "\n")
    (destination / "seal.json").write_text(json.dumps({p.name: identity(p) for p in destination.iterdir()}, indent=2) + "\n")


def verify():
    assert git(ROOT, "branch", "--show-current").decode().strip() == "codex/65aero-m2-extended-resident-admission"
    assert git(ROOT, "merge-base", BASE, "HEAD").decode().strip() == BASE
    modified = set(git(ROOT, "diff", "--diff-filter=M", "--name-only", BASE).decode().splitlines())
    assert modified == MODIFIED, modified
    new = set(filter(None, git(ROOT, "ls-files", "--others", "--exclude-standard", "-z").decode().split("\0")))
    new.update(git(ROOT, "diff", "--diff-filter=A", "--name-only", BASE).decode().splitlines())
    assert all(name in NEW or name.startswith((str(PACKET.relative_to(ROOT)) + "/",
                    str(CHECKPOINT.relative_to(ROOT)) + "/")) for name in new)
    before = json.loads(gzip.decompress((PACKET / "before.json.gz").read_bytes()))
    for name, expected in before.items():
        if name not in MODIFIED:
            assert identity(ROOT / name) == expected, name
    original = Path("/Users/slice/Developer/f65-megawing")
    unrelated = json.loads((PACKET / "unrelated-before.json").read_text())
    names = set(filter(None, git(original, "ls-files", "--modified", "--others", "--exclude-standard", "-z").decode().split("\0")))
    assert names == set(unrelated) and len(names) == 480
    for name, expected in unrelated.items():
        assert identity(original / name) == expected, name
    worktrees = json.loads((PACKET / "worktrees-before.json").read_text())
    for name, expected in worktrees.items():
        path = Path(name)
        assert git(path, "rev-parse", "HEAD").decode().strip() == expected["head"]
        assert git(path, "status", "--porcelain=v1").decode() == expected["status"]
        assert hashlib.sha256(git(path, "diff", "--binary")).hexdigest() == expected["diff_sha256"]
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory); residency.generate(destination=root)
        for name in residency.OUTPUTS:
            assert (ROOT / name).read_bytes() == (root / name).read_bytes(), name
    target = json.loads((TARGET / "result.json").read_text())
    application = [name for name in target["inputs"] if name.startswith(("src/", "interfaces/", "memory/"))]
    for name in application:
        assert identity(ROOT / name)["sha256"] == target["inputs"][name], name
    qualifier = json.loads((FINAL / "result.json").read_text())
    for name, digest in qualifier["checker_inputs"].items():
        assert identity(ROOT / name)["sha256"] == digest, name
    assert target["resident_fit"] == "PASS" and target["resident_bytes"] == 27023
    assert target["resident_limit"] == 28671 and target["remaining_margin"] == 1648
    assert target["production_resident_fit"] == "FAIL" and target["reserve_used"] == 0
    assert qualifier["renderer_service"]["status"] == "FAIL" and qualifier["Xemu"] == "NOT RUN"
    assert qualifier["application_stack"]["whole_program_status"].startswith("UNPROVEN")
    sdk = json.loads((TARGET / "sdk-inputs-before.json").read_text())
    toolchain_identity.verify(Path(target["toolchain"]["sdk"]), sdk)
    for archive_path in PACKET.glob("*/source.tar.gz"):
        result = json.loads((archive_path.parent / "result.json").read_text())
        with tarfile.open(archive_path, "r:gz") as archive:
            assert set(archive.getnames()) == set(result["inputs"])
            for member in archive:
                assert member.isfile() and not member.name.startswith("/") and ".." not in Path(member.name).parts
                assert hashlib.sha256(archive.extractfile(member).read()).hexdigest() == result["inputs"][member.name]
                assert not member.name.lower().endswith((".rom", ".key", ".pem", ".journal"))
    preserve_checker_sources()
    seals = {str(p.relative_to(PACKET)): check_seal(p) for p in sorted(PACKET.rglob("seal.json"))
             if p != PACKET / "seal.json"}
    for name in MODIFIED | NEW:
        path = ROOT / name
        if path.suffix == ".py":
            ast.parse(path.read_text(), filename=name)
        assert all(line == line.rstrip(" \t") for line in path.read_text().splitlines()), name
    for path in PACKET.rglob("*.json"):
        json.loads(path.read_text())
    for name in ["WORK_IN_PROGRESS.md", "docs/reports/M2_EXTENDED_RESIDENT_ADMISSION.md"]:
        path = ROOT / name
        for url in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if not re.match(r"[a-z]+://", url):
                assert (path.parent / url.split("#")[0]).exists(), url
    run = subprocess.run(["git", "diff", "--check", BASE], cwd=ROOT, capture_output=True, text=True)
    # The initial pre-stage check did not cover untracked raw map output.
    # Preserve that original result. Record the real staged failure separately;
    # do not trim sealed maps or silently extend the owner's CI exception list.
    return {"status": "PASS" if run.returncode == 0 else "BLOCKED BY SEALED EVIDENCE WHITESPACE",
        "preservation": "PASS", "tier": "publication/preservation only", "base": BASE,
        "whitespace_command": ["git", "diff", "--check", BASE],
        "whitespace_exit": run.returncode, "whitespace_output": run.stdout + run.stderr,
        "before_identities": len(before), "preserved_identities": len(before) - len(MODIFIED),
        "modified": sorted(MODIFIED), "new_source_scope": sorted(NEW),
        "unrelated_paths_preserved": len(unrelated), "other_existing_worktrees_preserved": len(worktrees),
        "missing_historical_worktree_tier": "NOT VERIFIED; no metadata reconstruction or complete recovery claim",
        "application_inputs_match_target": len(application), "link_inputs_archived": len(target["inputs"]),
        "postlink_verifier_only_paths": [n for n, digest in target["inputs"].items()
            if identity(ROOT / n)["sha256"] != digest],
        "all_qualification_source_versions": "exact previously present bytes retained in verification-sources",
        "sealed_packets": seals, "SDK": "complete pinned inventory unchanged",
        "production_contracts_and_all_other_owners": "unchanged", "target_links": 2,
        "reason_for_second_link": "bounded Platform startup branch correctness; no renderer optimization",
        "target_executed": False, "Xemu": "NOT RUN", "merge": "NOT AUTHORIZED"}


if __name__ == "__main__":
    result = verify()
    CHECKPOINT.mkdir(exist_ok=False)
    path = CHECKPOINT / "result.json"
    content = json.dumps(result, indent=2) + "\n"
    path.write_text(content)
    print(json.dumps({key: result[key] for key in ["status", "before_identities", "preserved_identities",
        "unrelated_paths_preserved", "other_existing_worktrees_preserved", "application_inputs_match_target"]}))
    raise SystemExit(0 if result["status"] == "PASS" else 1)
