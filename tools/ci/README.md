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

The founder approved one additional whitespace pin on 2026-10-28 for
`docs/evidence/flight-demo/2026-10-27-m2-min-rebuild-corrections/sdk-path-20261028-1/focused.diff`,
SHA-256 `e0cf52a6bcfc72c4a73d3cea1a62af2dd19641353e7e6850e0edd8b18d4ec0a1`.
Its three blank patch-context lines remain sealed and unchanged. The exception
is exact-path only; changed, missing, renamed or symlinked evidence fails closed.
Nearby unlisted files remain subject to ordinary whitespace checking.

The founder approved these three additional whitespace pins for PR #32 on
2026-11-10. They are the complete set of unpinned whitespace
failures against main `9570f0a` at failed-checkpoint head `521bb58`:

| Exact path under `docs/evidence/flight-demo/` | SHA-256 |
| --- | --- |
| `2026-10-30-m2-extended-resident-publication/static-hygiene.txt` | `54f35360b92af2723dbcf348269a69875ef7ac7edd89b21e751a68963fb1f8e9` |
| `2026-10-30-m2-extended-resident/target-1793404701167257000/UNADMITTED.map` | `5cb9f9e9f475ab9f56df689b0c2f492028ba1a10187226f86577e71d2b2335da` |
| `2026-10-30-m2-extended-resident/target-1793405200824046000/UNADMITTED.map` | `5606cb0b50af4b9e777220994e3195ef62af1d22334dc14d6426bfb6febaf1e5` |

Each hash matches its original seal. Only these paths become eligible; no
flight-demo directory exception is introduced. Existing manifest pins and
artifact restrictions remain intact. Tests cover exact blobs, changed bytes,
missing/renamed/symlinked pins, invalid neighboring exception paths and unlisted
neighbor whitespace. The checker still reads committed Git objects.

This CI correction does not alter the 755-byte resident-fit failure or the
independent 298,776-cycle cold-frame deficit. PR #32 remains draft, NOT FOR
MERGE. No target relink or runtime testing is part of this correction.
