"""Publication-only scope/preservation checks. No compilation or target execution."""
import argparse
import ast
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[3]
PACKET = ROOT / "docs/evidence/flight-demo/2026-10-30-m2-unbanked-renderer"
BASE = "9570f0ab427121a4e8f042041a14c89aaaeff9e2"
TARGET = PACKET / "target-1793345752710330000"
MODIFIED = {
    "WORK_IN_PROGRESS.md", "src/diagnostics/m2_rebuild/camera.c",
    "src/graphics/m2_rebuild.c", "src/graphics/m2_rebuild.h",
    "src/graphics/m2_rebuild_text.c", "tests/flight_demo/m2_rebuild/host.c",
    "tests/flight_demo/m2_rebuild/test_contract.py", "tools/flight_demo/m2_rebuild/validate.py"
}
NEW = {
    "docs/reports/M2_UNBANKED_RENDERER.md", "src/graphics/m2_compact.c",
    "src/graphics/m2_compact.h", "src/graphics/m2_compact_public.c",
    "src/graphics/m2_limb.c", "src/graphics/m2_limb.h",
    "tests/flight_demo/m2_rebuild/limb_oracle.py",
    "tests/flight_demo/m2_rebuild/test_compact_check.py",
    "tests/flight_demo/m2_rebuild/test_compact_specialization.py",
    "tests/flight_demo/m2_rebuild/text_compact.c",
    "tools/flight_demo/m2_rebuild/compact_check.py",
    "tools/flight_demo/m2_rebuild/compact_validate.py",
    "tools/flight_demo/m2_rebuild/compact_publication.py"
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(path):
    assert path.is_file() and not path.is_symlink(), str(path)
    return {"bytes": path.stat().st_size, "sha256": sha(path)}


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root)


def verify(output_path):
    report = {"identity": "65AERO-M2-UNBANKED-1", "tier": "publication-only",
              "target_executed": False, "commands": []}
    assert git(ROOT, "branch", "--show-current").decode().strip() == "codex/65aero-m2-unbanked-renderer"
    assert git(ROOT, "merge-base", BASE, "HEAD").decode().strip() == BASE
    baseline = json.loads(gzip.decompress((PACKET / "main-before.json.gz").read_bytes()))
    assert set(git(ROOT, "diff", "--diff-filter=M", "--name-only", BASE).decode().splitlines()) == MODIFIED
    for name, expected in baseline.items():
        if name not in MODIFIED:
            assert identity(ROOT / name) == expected, name
    report["baseline"] = {"tracked_identities": len(baseline),
                          "preserved": len(baseline) - len(MODIFIED),
                          "authorized_changed": sorted(MODIFIED)}
    additions = set(filter(None, git(ROOT, "ls-files", "--others", "--exclude-standard", "-z").decode().split("\0")))
    additions.update(git(ROOT, "diff", "--diff-filter=A", "--name-only", BASE).decode().splitlines())
    packet_prefix = str(PACKET.relative_to(ROOT)) + "/"
    assert all(name in NEW or name.startswith(packet_prefix) for name in additions), additions - NEW
    report["new_source_scope"] = sorted(NEW)
    unrelated = json.loads((PACKET / "unrelated-before.json").read_text())
    original = Path("/Users/slice/Developer/f65-megawing")
    now_names = set(git(original, "ls-files", "--modified", "--others", "--exclude-standard", "-z").decode().strip("\0").split("\0"))
    assert now_names == set(unrelated)
    for name, expected in unrelated.items():
        assert identity(original / name) == expected, name
    report["unrelated_paths_preserved"] = len(unrelated)
    worktrees = json.loads((PACKET / "worktrees-before.json").read_text())
    for name, expected in worktrees.items():
        path = Path(name)
        assert git(path, "rev-parse", "HEAD").decode() == expected["head"], name
        assert git(path, "status", "--porcelain=v1").decode() == expected["status"], name
        assert hashlib.sha256(git(path, "diff", "--binary")).hexdigest() == expected["diff_sha256"], name
    report["other_worktree_git_snapshots_preserved"] = len(worktrees)
    report["historical_provenance"] = "No reconstruction; old incomplete packet and missing worktree-tier limitations unchanged"
    seals = {}
    for seal in sorted(PACKET.glob("*/seal.json")):
        inventory = json.loads(seal.read_text())
        for name, expected in inventory.items():
            assert identity(seal.parent / name) == expected, str(seal.parent / name)
        seals[str(seal.parent.relative_to(PACKET))] = {"members": len(inventory), "seal_sha256": sha(seal)}
    report["sealed_attempts"] = seals
    target = json.loads((TARGET / "result.json").read_text())
    for name, expected in target["inputs"].items():
        assert sha(ROOT / name) == expected, "target input changed after link: " + name
    report["target_source_identities_preserved"] = len(target["inputs"])
    archive = PACKET / "candidate-source.tar.gz"
    if not archive.exists():
        with archive.open("xb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w") as stream:
                for name in sorted(target["inputs"]):
                    content = (ROOT / name).read_bytes()
                    entry = tarfile.TarInfo(name)
                    entry.size = len(content)
                    entry.mode = 0o644
                    entry.mtime = 0
                    stream.addfile(entry, io.BytesIO(content))
    with tarfile.open(archive, "r:gz") as stream:
        assert set(stream.getnames()) == set(target["inputs"])
        for entry in stream:
            assert entry.isfile() and hashlib.sha256(stream.extractfile(entry).read()).hexdigest() == target["inputs"][entry.name]
    report["candidate_source_archive"] = identity(archive)
    report["generated_artifacts"] = "UNCHANGED; full baseline identities and host regeneration checked"
    python_paths = [ROOT / name for name in MODIFIED | NEW if name.endswith(".py")]
    for path in python_paths:
        ast.parse(path.read_text(), filename=str(path))
    report["python_syntax"] = len(python_paths)
    json_count = 0
    for path in PACKET.rglob("*.json"):
        if path in {output_path, PACKET / "seal.json"}:
            continue
        json.loads(path.read_text())
        json_count += 1
    report["json_syntax"] = json_count
    local_links = 0
    for name in ["WORK_IN_PROGRESS.md", "docs/reports/M2_UNBANKED_RENDERER.md"]:
        path = ROOT / name
        for link in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if not re.match(r"[a-z]+://", link):
                assert (path.parent / link.split("#")[0]).exists(), (name, link)
                local_links += 1
    report["local_document_links"] = local_links
    for argv, log in [(["git", "diff", "--check"], "publication-whitespace.txt")]:
        result = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True)
        log_path = PACKET / log
        if log_path.exists():
            assert log_path.read_text() == result.stdout + result.stderr, log
        else:
            log_path.write_text(result.stdout + result.stderr)
        report["commands"].append({"argv": argv, "exit": result.returncode, "log": log})
        assert result.returncode == 0, log
    for name in NEW | {str(path.relative_to(ROOT)) for path in PACKET.rglob("*") if path.is_file()}:
        path = ROOT / name
        if b"\0" in path.read_bytes()[:8192] or path.suffix in {".gz", ".dylib", ".elf", ".prg", ".png", ".indices"}:
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        assert all(line.rstrip(" \t") == line for line in text.splitlines()), name
    report["new_text_whitespace"] = "PASS"
    report["checker_sha256"] = sha(Path(__file__))
    report["status"] = "PASS"
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=PACKET / "publication-checks.json")
    path = parser.parse_args().output.resolve()
    assert path.parent == PACKET, "publication receipt must stay in this packet"
    result = verify(path)
    text = json.dumps(result, indent=2) + "\n"
    if path.exists():
        assert path.read_text() == text, "sealed report differs; use a fresh publication attempt"
    else:
        path.write_text(text)
    print(json.dumps({key: result[key] for key in ["status", "baseline", "unrelated_paths_preserved",
                     "target_source_identities_preserved", "candidate_source_archive"]}, indent=2))
