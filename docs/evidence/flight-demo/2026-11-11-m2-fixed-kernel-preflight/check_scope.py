"""Read-only checkpoint scope, syntax, links and preservation checks."""
import ast
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[4]
PACKET = Path(__file__).resolve().parent
ALLOW = {
    "WORK_IN_PROGRESS.md",
    "docs/plans/65AERO_M2_FIXED_KERNEL_BUILD_INTENT.md",
    "docs/reports/M2_FIXED_KERNEL_PREFLIGHT.md",
    "tools/flight_demo/m2_rebuild/fixed_preflight.py",
    "tests/flight_demo/m2_rebuild/test_fixed_preflight.py",
}


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root)


def verify(root, inventory):
    for path, expected in inventory.items():
        raw = (root / path).read_bytes()
        if len(raw) != expected["bytes"] or sha256(raw).hexdigest() != expected["sha256"]:
            raise ValueError(f"preservation mismatch: {root / path}")


baseline = json.loads((PACKET / "checkpoint-before.json").read_text())
verify(ROOT, {p: x for p, x in baseline.items() if p != "WORK_IN_PROGRESS.md"})
changed = set(git(ROOT, "ls-files", "--modified", "--others", "--exclude-standard", "-z")
              .decode().split("\0")) - {""}
prefix = str(PACKET.relative_to(ROOT)) + "/"
if any(p not in ALLOW and not p.startswith(prefix) for p in changed):
    raise ValueError("unexpected changed path")
if git(ROOT, "diff", "--cached", "--name-only"):
    raise ValueError("unexpected staged change")
counts = {"json": 0, "python": 0, "markdown_links": 0, "whitespace_files": 0}
for path in sorted(changed):
    file = ROOT / path
    text = file.read_text()
    if any(line.rstrip(" \t") != line for line in text.splitlines()):
        raise ValueError(f"trailing whitespace: {path}")
    counts["whitespace_files"] += 1
    if file.suffix == ".json":
        # The shell creates this output before this script runs; don't read it.
        if file.name != "static-checks.json":
            json.loads(text)
            counts["json"] += 1
    if file.suffix == ".py":
        ast.parse(text, filename=path)
        counts["python"] += 1
    if file.suffix == ".md":
        for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if "://" in link or link.startswith("#"):
                continue
            if not (file.parent / link.split("#")[0]).exists():
                raise ValueError(f"broken local link: {path}: {link}")
            counts["markdown_links"] += 1
subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True)

historic = ROOT / "docs/evidence/flight-demo/2026-10-30-m2-extended-resident"
unrelated = json.loads((historic / "unrelated-before.json").read_text())
other = Path("/Users/slice/Developer/f65-megawing")
actual = set(git(other, "ls-files", "--modified", "--others", "--exclude-standard", "-z")
             .decode().split("\0")) - {""}
if actual != set(unrelated):
    raise ValueError("unrelated path inventory changed")
verify(other, unrelated)
trees = {}
for path, expected in json.loads((historic / "worktrees-before.json").read_text()).items():
    location = Path(path)
    if not (location / ".git").exists():
        trees[path] = "NOT VERIFIED at the Git-worktree tier"
        continue
    current = {"head": git(location, "rev-parse", "HEAD").decode().strip(),
               "status": git(location, "status", "--short").decode(),
               "diff_sha256": sha256(git(location, "diff", "--binary")).hexdigest()}
    if current != expected:
        raise ValueError(f"historical checkout changed: {path}")
    trees[path] = "MATCHED"
failed = Path("/private/tmp/f65-m2-wide-arithmetic")
verify(failed, baseline)
if git(failed, "status", "--porcelain"):
    raise ValueError("failed experiment checkout changed")
print(json.dumps({"status": "PASS for stated static/preservation scope", "counts": counts,
                  "unchanged_checkpoint_files": len(baseline) - 1,
                  "unrelated_files": len(unrelated), "historical_checkouts": trees,
                  "failed_experiment_files": len(baseline), "changed_paths": sorted(changed),
                  "head": git(ROOT, "rev-parse", "HEAD").decode().strip(),
                  "main": git(ROOT, "rev-parse", "origin/main").decode().strip(),
                  "target_links": 0, "runtime_executions": 0}, indent=2))
