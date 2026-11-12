"""Read-only CC3 focused static/preservation check; outputs outside old seals."""
import ast
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[4]
PACKET = Path(__file__).resolve().parent
BASE = "fcba7cf4f742a216fba1a6954a4e74b7c9d59ec8"
MAIN = "9570f0ab427121a4e8f042041a14c89aaaeff9e2"
ALLOW = {
    "WORK_IN_PROGRESS.md",
    "docs/plans/65AERO_M2_CORRECTED_CLOCK_PREFLIGHT_INTENT.md",
    "docs/reports/M2_CORRECTED_CLOCK_PREFLIGHT.md",
    "tools/flight_demo/m2_rebuild/corrected_clock_preflight.py",
    "tests/flight_demo/m2_rebuild/test_corrected_clock_preflight.py",
}


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root)


def verify(root, inventory):
    for name, expected in inventory.items():
        path = root / name
        raw = path.read_bytes()
        if path.is_symlink() or len(raw) != expected["bytes"] or sha256(raw).hexdigest() != expected["sha256"]:
            raise ValueError(f"preservation mismatch: {path}")


baseline = json.loads((PACKET / "baseline-before.json").read_text())
verify(Path("/private/tmp/f65-m2-platform-clock"), baseline)
verify(ROOT, {p: x for p, x in baseline.items() if p != "WORK_IN_PROGRESS.md"})
if git(ROOT, "rev-parse", "HEAD").decode().strip() != BASE:
    raise ValueError("wrong base")
if git(ROOT, "rev-parse", "origin/main").decode().strip() != MAIN:
    raise ValueError("main changed")
if git(ROOT, "branch", "--show-current").decode().strip() != "codex/65aero-m2-corrected-clock-preflight":
    raise ValueError("wrong branch")
if git(ROOT, "merge-base", "HEAD", "origin/main").decode().strip() != MAIN:
    raise ValueError("unexpected ancestry")
if git(ROOT, "diff", "--cached", "--name-only"):
    raise ValueError("unexpected staged paths")
changed = set(git(ROOT, "ls-files", "--modified", "--others", "--exclude-standard", "-z").decode().split("\0")) - {""}
prefix = str(PACKET.relative_to(ROOT)) + "/"
if any(p not in ALLOW and not p.startswith(prefix) for p in changed):
    raise ValueError("out-of-scope path")

related = json.loads((PACKET / "related-before.json").read_text())
for name, expected in related.items():
    root = Path(name)
    actual = {"head": git(root, "rev-parse", "HEAD").decode().strip(),
              "status": git(root, "status", "--short").decode(),
              "diff_sha256": sha256(git(root, "diff", "--binary")).hexdigest()}
    if actual != {k: expected[k] for k in actual}:
        raise ValueError(f"related checkout changed: {root}")
    verify(root, expected["dirty_files"])
plan = "docs/plans/65AERO_M2_CORRECTED_CLOCK_PREFLIGHT_INTENT.md"
if (ROOT / plan).read_bytes() != (Path("/private/tmp/f65-m2-corrected-clock-preflight-intent") / plan).read_bytes():
    raise ValueError("approved intent changed")

counts = {"python": 0, "json": 0, "local_links": 0, "whitespace_files": 0}
for name in sorted(changed):
    path = ROOT / name
    if path.suffix == ".gz":
        continue
    text = path.read_text()
    if any(line.rstrip(" \t") != line for line in text.splitlines()):
        raise ValueError(f"trailing whitespace: {name}")
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
                    raise ValueError(f"broken documentation link: {name}: {link}")
                counts["local_links"] += 1
for name in ("spec/manifests/spec-corpus.json", "interfaces/m2_extended_resident.json", "memory/m2-extended-resident-ledger.json"):
    json.loads((ROOT / name).read_text())
    if (ROOT / name).read_bytes() != git(ROOT, "show", f"{BASE}:{name}"):
        raise ValueError(f"contract changed: {name}")
subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True)
historical = json.loads((PACKET / "historical-preservation.stdout").read_text())
if historical["unrelated_files"] != 480 or not historical["status"].startswith("PASS"):
    raise ValueError("historical preservation missing")
if not all(v in ("MATCHED", "NOT VERIFIED at the Git-worktree tier")
           for v in historical["historical_checkouts"].values()):
    raise ValueError("unresolved historical mismatch")
print(json.dumps({"status": "PASS for host-only static and preservation scope", "counts": counts,
                  "published_identities": len(baseline), "candidate_unchanged_identities": len(baseline) - 1,
                  "related_checkouts": len(related), "unrelated_paths": 480,
                  "historical_provenance": historical["historical_checkouts"],
                  "changed_paths": sorted(changed), "base": BASE, "main": MAIN,
                  "target_links": 0, "runtime_executions": 0}, indent=2))
