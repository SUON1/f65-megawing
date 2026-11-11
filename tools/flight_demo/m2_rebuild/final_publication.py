"""Read-only publication/preservation checks for the failed final fit checkpoint."""
import ast
import gzip
import json
from pathlib import Path
import re
import subprocess
import tarfile

from compact_validate import ROOT, module

PARENT = "d48c9ea884ea3dee1c7dcc90fa36891268b0dc14"
PACKET = ROOT / "docs/evidence/flight-demo/2026-10-30-m2-final-unbanked-fit"
TARGET = PACKET / "target-1793382249042750000"
HELPERS = module(ROOT / "tools/flight_demo/m2_rebuild/compact_publication.py", "checkpoint_helpers")
git, identity, sha = HELPERS.git, HELPERS.identity, HELPERS.sha
MODIFIED = {"WORK_IN_PROGRESS.md", "src/diagnostics/m2_rebuild/camera.c",
    "src/graphics/m2_compact.c", "src/graphics/m2_compact.h", "src/graphics/m2_compact_public.c",
    "src/graphics/m2_rebuild.c", "src/graphics/m2_rebuild.h", "tests/flight_demo/m2_rebuild/host.c",
    "tests/flight_demo/m2_rebuild/limb_oracle.py", "tools/flight_demo/m2_rebuild/validate.py"}
NEW = {"src/graphics/m2_record_private.c", "src/graphics/m2_record_private.h",
    "src/graphics/m2_commands.inc", "tests/flight_demo/m2_rebuild/command_host.c",
    "tools/flight_demo/m2_rebuild/commands.py", "tools/flight_demo/m2_rebuild/commands_validate.py",
    "tools/flight_demo/m2_rebuild/final_publication.py", "docs/reports/M2_FINAL_UNBANKED_FIT.md"}


def verify():
    assert git(ROOT, "branch", "--show-current").decode().strip() == "codex/65aero-m2-final-unbanked-fit"
    assert git(ROOT, "merge-base", PARENT, "HEAD").decode().strip() == PARENT
    assert set(git(ROOT, "diff", "--diff-filter=M", "--name-only", PARENT).decode().splitlines()) == MODIFIED
    added = set(filter(None, git(ROOT, "ls-files", "--others", "--exclude-standard", "-z").decode().split("\0")))
    added.update(git(ROOT, "diff", "--diff-filter=A", "--name-only", PARENT).decode().splitlines())
    prefix = str(PACKET.relative_to(ROOT)) + "/"
    assert all(name in NEW or name.startswith(prefix) for name in added)
    before = json.loads(gzip.decompress((PACKET / "before.json.gz").read_bytes()))
    for name, expected in before.items():
        if name not in MODIFIED:
            assert identity(ROOT / name) == expected, name
    unrelated = json.loads((PACKET / "unrelated-before.json").read_text())
    original = Path("/Users/slice/Developer/f65-megawing")
    names = set(filter(None, git(original, "ls-files", "--modified", "--others", "--exclude-standard", "-z").decode().split("\0")))
    assert names == set(unrelated)
    for name, expected in unrelated.items():
        assert identity(original / name) == expected, name
    worktrees = json.loads((PACKET / "worktrees-before.json").read_text())
    for name, expected in worktrees.items():
        path = Path(name)
        assert git(path, "rev-parse", "HEAD").decode().strip() == expected["head"]
        assert git(path, "status", "--porcelain=v1").decode() == expected["status"]
        import hashlib
        assert hashlib.sha256(git(path, "diff", "--binary")).hexdigest() == expected["diff_sha256"]
    sealed = {}
    for path in sorted(PACKET.rglob("seal.json")):
        if path == PACKET / "seal.json":
            continue
        inventory = json.loads(path.read_text())
        for name, expected in inventory.items():
            assert identity(path.parent / name) == expected, str(path.parent / name)
        sealed[str(path.relative_to(PACKET))] = {"members": len(inventory), "sha256": sha(path)}
    target = json.loads((TARGET / "result.json").read_text())
    for name, digest in target["inputs"].items():
        assert sha(ROOT / name) == digest, name
    import hashlib
    with tarfile.open(TARGET / "source.tar.gz", "r:gz") as archive:
        assert set(archive.getnames()) == set(target["inputs"])
        for member in archive:
            assert member.isfile()
            assert hashlib.sha256(archive.extractfile(member).read()).hexdigest() == target["inputs"][member.name]
    for name in MODIFIED | NEW:
        if name.endswith(".py"):
            ast.parse((ROOT / name).read_text(), filename=name)
    json_count = 0
    for path in PACKET.rglob("*.json"):
        if path.name == "publication.json" or path == PACKET / "seal.json":
            continue
        json.loads(path.read_text())
        json_count += 1
    links = 0
    for name in ["WORK_IN_PROGRESS.md", "docs/reports/M2_FINAL_UNBANKED_FIT.md"]:
        path = ROOT / name
        for target_link in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if not re.match(r"[a-z]+://", target_link):
                assert (path.parent / target_link.split("#")[0]).exists(), target_link
                links += 1
    result = subprocess.run(["git", "diff", "--check"], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    for name in NEW | added:
        path = ROOT / name
        if b"\0" in path.read_bytes()[:8192] or path.suffix in {".gz", ".dylib", ".elf", ".prg", ".png", ".indices"}:
            continue
        try:
            content = path.read_text()
        except UnicodeDecodeError:
            continue
        assert all(line.rstrip(" \t") == line for line in content.splitlines()), name
    return {"identity": "65AERO-M2-COMMAND-1", "status": "PASS", "tier": "publication-only",
        "commands": [{"argv": ["git", "diff", "--check"], "exit": result.returncode}],
        "reviewed_before": len(before), "unchanged_before_identities": len(before)-len(MODIFIED),
        "authorized_modified": sorted(MODIFIED), "new_source_scope": sorted(NEW),
        "unrelated_paths_preserved": len(unrelated), "other_worktree_git_snapshots_preserved": len(worktrees),
        "prior_experiments_and_evidence": "UNCHANGED; no reconstruction or provenance promotion",
        "target_inputs_match": len(target["inputs"]), "target_source_archive": identity(TARGET / "source.tar.gz"),
        "sealed_attempts": sealed, "json_syntax": json_count, "local_links": links,
        "generated_public_contracts_platform_and_memory": "UNCHANGED", "target_executed": False,
        "checker_sha256": sha(Path(__file__))}


if __name__ == "__main__":
    report = verify()
    text = json.dumps(report, indent=2) + "\n"
    path = PACKET / "publication.json"
    if path.exists():
        assert path.read_text() == text
    else:
        path.write_text(text)
    print(json.dumps({key:report[key] for key in ["status","reviewed_before",
        "unchanged_before_identities","unrelated_paths_preserved","target_inputs_match"]}))
