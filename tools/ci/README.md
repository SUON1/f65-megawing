# Static hygiene and retained evidence

The owner approved this narrow CI correction after PR #10's original static
check conflicted with immutable R0-F evidence preservation. It does not grant
target, carrier, physical, measured-limit or R0-F acceptance.

`retained_evidence_sha256.json` is the reviewed exact-path exception list,
pinned from commit `6c037188ad5971515d1bc3490d665df6343ecf82`:

- 193 original whitespace-bearing evidence files.
- 117 original D81s, including the previously allowed `F65BLK02.D81`.

`static_hygiene.py` reads the specified committed head, verifies every pinned
file is present as a regular Git blob and matches its SHA-256, then checks the
incoming range. Only exact hash-verified text paths are excluded from whitespace
checking. Only exact hash-verified D81 paths are admitted by the artifact guard.
There is no blanket evidence-directory exclusion. New files and other paths
remain subject to the original whitespace and artifact rules; ROMs, emulator
states and private toolchain prefixes remain forbidden. Deletion, rename,
symlink replacement or changed bytes in a pin fails closed.

Later changes to this exception list require a new explicit evidence-preservation
review and owner approval, not automatic regeneration to make CI green.

Run the fixtures and the exact PR range locally:

```sh
python3 -B -m unittest discover -s tools/ci -p 'test_*.py' -v
python3 -B tools/ci/static_hygiene.py --base origin/main --head HEAD --merge-base
```

The helper requires the manifest to exist in the specified committed head.
Uncommitted checkout bytes do not substitute for the reviewed Git objects.
CI remains documentation/static evidence only.
