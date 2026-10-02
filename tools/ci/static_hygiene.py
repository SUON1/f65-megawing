#!/usr/bin/env python3
"""Static CI exceptions for exact, immutable retained evidence only."""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


MANIFEST = "tools/ci/retained_evidence_sha256.json"
EVIDENCE_ROOTS = (
    "docs/evidence/r0f/group1/",
    "docs/evidence/r0f/successor/",
)
LEGACY_D81 = "docs/evidence/r0f/combined/F65BLK02.D81"
BLOCKED_PREFIXES = (
    "toolchain/runtime/",
    "toolchain/downloads/",
    "toolchain/vice/",
    "toolchain/xemu/",
)
BLOCKED_SUFFIXES = (".rom", ".d81", ".xemu-state")


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate manifest key: {key}")
        result[key] = value
    return result


def load_manifest(data):
    manifest = json.loads(data, object_pairs_hook=unique_object)
    if (
        set(manifest) != {"schema", "authority", "reviewed_commit", "whitespace", "d81"}
        or type(manifest["schema"]) is not int
        or manifest["schema"] != 1
        or not isinstance(manifest["authority"], str)
        or not re.fullmatch(r"[0-9a-f]{40}", manifest["reviewed_commit"])
    ):
        raise ValueError("Invalid retained-evidence manifest header")
    for category in ("whitespace", "d81"):
        entries = manifest[category]
        if not isinstance(entries, dict) or not entries:
            raise ValueError(f"Empty or invalid exception category: {category}")
        for path, digest in entries.items():
            parts = PurePosixPath(path).parts
            if (
                PurePosixPath(path).is_absolute()
                or ".." in parts
                or str(PurePosixPath(path)) != path
                or not (path.startswith(EVIDENCE_ROOTS) or path == LEGACY_D81)
                or not isinstance(digest, str)
                or not re.fullmatch(r"[0-9a-f]{64}", digest)
            ):
                raise ValueError(f"Invalid evidence exception: {path}")
            if category == "d81" and not path.endswith(".D81"):
                raise ValueError(f"Only retained uppercase D81s may be allowed: {path}")
            if category == "whitespace" and path.lower().endswith(BLOCKED_SUFFIXES):
                raise ValueError(f"Binary artifact cannot be a whitespace exception: {path}")
    return manifest


def tracked_blobs(root, head):
    blobs = {}
    for entry in git(root, "ls-tree", "-rz", "--full-tree", head).split(b"\0"):
        if not entry:
            continue
        metadata, path = entry.split(b"\t", 1)
        mode, kind, oid = metadata.decode("ascii").split()
        blobs[path.decode("utf-8", errors="surrogateescape")] = (mode, kind, oid)
    return blobs


def verify_pins(root, blobs, manifest):
    verified = {}
    for category in ("whitespace", "d81"):
        for path, expected in manifest[category].items():
            if path not in blobs or blobs[path][0] not in ("100644", "100755"):
                raise ValueError(f"Pinned evidence missing or not a regular file: {path}")
            mode, kind, oid = blobs[path]
            if kind != "blob":
                raise ValueError(f"Pinned evidence is not a blob: {path}")
            if path not in verified:
                verified[path] = hashlib.sha256(git(root, "cat-file", "blob", oid)).hexdigest()
            if verified[path] != expected:
                raise ValueError(f"Pinned evidence SHA-256 mismatch: {path}")


def guard_artifacts(paths, allowed_d81):
    rejected = []
    for path in paths:
        name = PurePosixPath(path).name
        if path.startswith(BLOCKED_PREFIXES) or (
            (name == "MEGA65.ROM" or name.lower().endswith(BLOCKED_SUFFIXES))
            and path not in allowed_d81
        ):
            rejected.append(path)
    if rejected:
        raise ValueError("Forbidden tracked artifacts:\n" + "\n".join(sorted(rejected)))


def check(root, base, head, merge_base=False):
    # Resolve revisions first; never allow caller-supplied options into diff.
    head = git(root, "rev-parse", "--verify", "--end-of-options", head + "^{commit}").decode().strip()
    if merge_base:
        base = git(root, "rev-parse", "--verify", "--end-of-options", base + "^{commit}").decode().strip()
        base = git(root, "merge-base", base, head).decode().strip()
    else:
        base = git(root, "rev-parse", "--verify", "--end-of-options", base + "^{tree}").decode().strip()
    blobs = tracked_blobs(root, head)
    manifest = load_manifest(git(root, "show", head + ":" + MANIFEST))
    verify_pins(root, blobs, manifest)
    guard_artifacts(blobs, manifest["d81"])
    exclusions = [":(exclude,literal)" + path for path in sorted(manifest["whitespace"])]
    result = subprocess.run(
        ["git", "-C", str(root), "diff", "--check", base, head, "--", ".", *exclusions],
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise ValueError("Changed-range whitespace failed:\n" + result.stdout + result.stderr)
    return {
        "whitespace_pins": len(manifest["whitespace"]),
        "d81_pins": len(manifest["d81"]),
        "tracked_paths": len(blobs),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--merge-base", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(check(Path.cwd(), args.base, args.head, args.merge_base), sort_keys=True))
    except (ValueError, TypeError, KeyError, subprocess.CalledProcessError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
