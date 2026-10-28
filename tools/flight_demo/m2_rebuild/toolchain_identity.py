"""Read-only identities for the complete SDK tree, including driver configuration.

The inventory conservatively includes every SDK file, rather than guessing the
compiler's transitive configuration/header/runtime closure. Symlinks must resolve
entirely within that tree; external, dangling and cyclic links fail closed.
Capture immediately before linking and verify again after linking. These helpers
never run a tool, copy a binary, write an inventory or modify SDK/evidence bytes.
"""
from collections import deque
import hashlib
import json
import os
from pathlib import Path
import stat


def _stamp(details):
    return (details.st_dev, details.st_ino, details.st_mode, details.st_size,
            details.st_mtime_ns, details.st_ctime_ns)


def _kind(details):
    if stat.S_ISREG(details.st_mode):
        return "file"
    if stat.S_ISDIR(details.st_mode):
        return "directory"
    raise ValueError("SDK contains an unsupported file type")


def _resolve_confined(root, path):
    """Resolve every link hop without traversing a path outside the SDK."""
    pending = deque(path.relative_to(root).parts)
    resolved = root
    hops = 0
    while pending:
        part = pending.popleft()
        if part == ".":
            continue
        if part == "..":
            if resolved == root:
                raise ValueError("SDK symlink escapes its root: " + str(path))
            resolved = resolved.parent
            continue
        candidate = resolved / part
        details = candidate.lstat()
        if stat.S_ISLNK(details.st_mode):
            hops += 1
            if hops > 40:
                raise ValueError("SDK symlink cycle or excessive link chain: " + str(path))
            target = Path(os.readlink(candidate))
            if target.is_absolute():
                try:
                    target = target.relative_to(root)
                except ValueError as error:
                    raise ValueError("SDK symlink escapes its root: " + str(candidate)) from error
                resolved = root
            pending.extendleft(reversed(target.parts))
        else:
            if pending and not stat.S_ISDIR(details.st_mode):
                raise ValueError("SDK symlink traverses a non-directory: " + str(path))
            _kind(details)
            resolved = candidate
    return resolved


def _file(path, expected):
    digest_value = hashlib.sha256()
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(descriptor, "rb") as stream:
        if _stamp(os.fstat(stream.fileno())) != _stamp(expected):
            raise ValueError("SDK file changed before hashing: " + str(path))
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest_value.update(block)
        if _stamp(os.fstat(stream.fileno())) != _stamp(expected):
            raise ValueError("SDK file changed while hashing: " + str(path))
    return {"kind": "file", "bytes": expected.st_size,
            "sha256": digest_value.hexdigest(), "mode": stat.S_IMODE(expected.st_mode)}


def capture(sdk):
    """Return a deterministic, JSON-compatible SDK identity without any writes.

    Directory entries preserve tree structure. File records bind content, size
    and permissions; link records bind literal targets and confined resolved
    identities. Modification while scanning is an error, never a partial result.
    """
    try:
        root = Path(sdk).resolve(strict=True)
        if not root.is_dir():
            raise ValueError("SDK root is not a directory: " + str(root))
        entries = {}

        def visit(directory):
            before = directory.lstat()
            if not stat.S_ISDIR(before.st_mode):
                raise ValueError("SDK directory changed before scanning: " + str(directory))
            with os.scandir(directory) as scan:
                children = sorted(scan, key=lambda child: child.name)
            for child in children:
                path = directory / child.name
                name = path.relative_to(root).as_posix()
                details = path.lstat()
                if stat.S_ISLNK(details.st_mode):
                    target = os.readlink(path)
                    resolved = _resolve_confined(root, path)
                    entries[name] = {"kind": "symlink", "target": target,
                                     "resolved": resolved.relative_to(root).as_posix(),
                                     "resolved_kind": _kind(resolved.lstat())}
                elif stat.S_ISDIR(details.st_mode):
                    entries[name] = {"kind": "directory", "mode": stat.S_IMODE(details.st_mode)}
                    visit(path)
                elif stat.S_ISREG(details.st_mode):
                    entries[name] = _file(path, details)
                else:
                    raise ValueError("SDK contains an unsupported file type: " + name)
                if _stamp(path.lstat()) != _stamp(details):
                    raise ValueError("SDK entry changed while scanning: " + name)
            if _stamp(directory.lstat()) != _stamp(before):
                raise ValueError("SDK directory changed while scanning: " + str(directory))

        visit(root)
        return {"schema_version": 1,
                "scope": "complete SDK tree; directories, regular files and confined symlinks",
                "sdk_root": str(root), "entries": dict(sorted(entries.items()))}
    except (OSError, RuntimeError) as error:
        raise ValueError("SDK inventory cannot be captured: " + str(error)) from error


def digest(inventory):
    """Hash canonical JSON independently of pretty-printing or dictionary order."""
    canonical = json.dumps(inventory, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def verify(sdk, inventory):
    """Raise ValueError if the SDK differs from its pre-link identity; return None."""
    current = capture(sdk)
    if current == inventory:
        return
    previous = inventory.get("entries", {})
    observed = current["entries"]
    removed = sorted(previous.keys() - observed.keys())
    added = sorted(observed.keys() - previous.keys())
    changed = sorted(name for name in previous.keys() & observed.keys()
                     if previous[name] != observed[name])
    raise ValueError("SDK identity changed: removed=" + repr(removed[:5])
                     + ", added=" + repr(added[:5]) + ", changed=" + repr(changed[:5])
                     + "; before=" + digest(inventory) + "; after=" + digest(current))
