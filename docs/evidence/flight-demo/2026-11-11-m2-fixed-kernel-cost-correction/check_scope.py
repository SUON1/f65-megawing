"""Read-only FC checkpoint documentation, source scope and preservation checks."""
import ast
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[4]
PACKET = Path(__file__).resolve().parent
ORIGINAL = Path("/private/tmp/f65-m2-fixed-kernel-preflight")
ALLOW = {
    "WORK_IN_PROGRESS.md",
    "docs/plans/65AERO_M2_FIXED_KERNEL_COST_CORRECTION_INTENT.md",
    "docs/reports/M2_FIXED_KERNEL_COST_CORRECTION.md",
    "tools/flight_demo/m2_rebuild/fixed_schedule_preflight.py",
    "tests/flight_demo/m2_rebuild/test_fixed_schedule_preflight.py",
}


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])


def identity(path):
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": sha256(raw).hexdigest()}


before = json.loads((PACKET / "checkpoint-before.json").read_text())
for name, expected in before.items():
    if identity(ORIGINAL / name) != expected:
        raise ValueError("published original changed: " + name)
    if name != "WORK_IN_PROGRESS.md" and identity(ROOT / name) != expected:
        raise ValueError("baseline file changed: " + name)
related = json.loads((PACKET / "related-before.json").read_text())
for name, expected in related.items():
    root = Path(name)
    dirty = [p.decode() for p in git(root, "ls-files", "--modified", "--others",
                                    "--exclude-standard", "-z").split(b"\0") if p]
    current = {"head": git(root, "rev-parse", "HEAD").decode().strip(),
               "status": git(root, "status", "--porcelain").decode(),
               "diff_sha256": sha256(git(root, "diff", "--binary")).hexdigest(),
               "dirty_files": {p: identity(root / p) for p in dirty}}
    if current != expected:
        raise ValueError("related checkout changed: " + name)
plan = "docs/plans/65AERO_M2_FIXED_KERNEL_COST_CORRECTION_INTENT.md"
if (ROOT / plan).read_bytes() != (Path("/private/tmp/f65-m2-fixed-kernel-cost-intent") / plan).read_bytes():
    raise ValueError("approved intent changed")
head = git(ROOT, "rev-parse", "HEAD").decode().strip()
if head != "6c0caa8d453bb647696ef85b5b31b35ef2310def":
    raise ValueError("unexpected baseline")
if git(ROOT, "diff", "--cached", "--name-only"):
    raise ValueError("unexpected staged change")
changed = {p.decode() for p in git(ROOT, "ls-files", "--modified", "--others",
                                  "--exclude-standard", "-z").split(b"\0") if p}
prefix = str(PACKET.relative_to(ROOT)) + "/"
if any(p not in ALLOW and not p.startswith(prefix) for p in changed):
    raise ValueError("changed path outside FC scope")
counts = {"python": 0, "json": 0, "local_links": 0, "whitespace_files": 0}
for name in sorted(changed):
    path = ROOT / name
    if path.suffix not in (".md", ".py", ".json"):
        continue
    text = path.read_text()
    if any(line != line.rstrip(" \t") for line in text.splitlines()):
        raise ValueError("trailing whitespace: " + name)
    counts["whitespace_files"] += 1
    if path.suffix == ".py":
        ast.parse(text, filename=name)
        counts["python"] += 1
    if path.suffix == ".json":
        json.loads(text)
        counts["json"] += 1
    if path.suffix == ".md":
        for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if "://" not in link and not link.startswith("#"):
                if not (path.parent / link.split("#")[0]).exists():
                    raise ValueError("broken link: " + name + ": " + link)
                counts["local_links"] += 1
subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True)
original_check = ORIGINAL / "docs/evidence/flight-demo/2026-11-11-m2-fixed-kernel-preflight/check_scope.py"
preservation = json.loads(subprocess.check_output(["python3", "-B", str(original_check)], cwd=ORIGINAL))
old = ORIGINAL / "docs/evidence/flight-demo/2026-11-11-m2-fixed-kernel-preflight"
for name, expected in json.loads((old / "seal.json").read_text()).items():
    if identity(old / name) != expected:
        raise ValueError("old seal mismatch: " + name)
for name, expected in json.loads((old / "source-identities.json").read_text()).items():
    if identity(ORIGINAL / name) != expected:
        raise ValueError("old pinned source mismatch: " + name)
seal = PACKET / "seal.json"
if seal.exists():
    members = json.loads(seal.read_text())
    actual = {str(p.relative_to(PACKET)) for p in PACKET.rglob("*") if p.is_file() and p != seal}
    if actual != set(members):
        raise ValueError("new sealed inventory differs")
    for name, expected in members.items():
        if identity(PACKET / name) != expected:
            raise ValueError("new sealed member differs: " + name)
print(json.dumps({"status": "PASS for FC static and preservation scope", "head": head,
                  "changed_paths": sorted(changed), "counts": counts,
                  "published_original_files": len(before), "unchanged_baseline_except_WIP": len(before)-1,
                  "related_checkouts": list(related), "old_sealed_members": 20,
                  "old_source_identities": 6, "unrelated_paths": preservation["unrelated_files"],
                  "historical_checkouts": preservation["historical_checkouts"],
                  "failed_experiment_files": preservation["failed_experiment_files"],
                  "target_links": 0, "runtime_executions": 0}, indent=2))
