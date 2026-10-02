# Group 1 physical closeout evidence — 2026-10-01

Disposition: development campaign closed with physical resume blocker,
**not Group 1/R0-F acceptance**. Owner confirms the photographed run selected
`R0FG1P05.D81`. Delivery/entry pass; runtime fails `$5D` at tick `$0640`.
Keep the tested SD copy and all predecessors; no rerun, repair or overwrite.

The [closeout and next-chat handoff](../../../../reports/R0-F_GROUP1_CLOSEOUT.md)
contains scope, exact source identity, analysis and remaining work.

## Packet contents

- `physical-result.json`: current failure disposition, complete inherited
  release identity and actual photographed fields. The immutable pre-run
  `delivery/sd-release.json` still says chooser pending; it is historical.
- `lockout.jpg`: unchanged original owner photo, SHA-256
  `7a9be86e8e9105b48d7b0e12e70b49c7568734a4b8e5284ee7ffa544cd186dba`.
- `delivery/`: unchanged original release/host gate, qualification,
  raw staged/final allocation records and allocator logs; P04 retirement/audit.
  Raw pre-write FAT/root/reserved backups remain locally at
  `build/r0f/group1/carriers/R0FG1P05/sd-install-01/`; not copied for publication.
- `owner-installer-output.txt`: exact supplied terminal output, separate from
  machine-produced installer records. `owner-observation.json` records the
  filename confirmation and unrecorded platform/video metadata.
- `returned/R0FG1P05.D81`: host snapshot of the actual returned card, read-only;
  819200 bytes, SHA-256
  `9816043f16eccad79c833419f19655ea0234d61be48854bae1d82a90fcf4197d`.
- `returned/actual/` and `returned/post-extracted/`: two pinned-tool extractions
  independently checked against chain/BAM parsing in `post-disk.json`.
- `returned/verification.json`: original-payload preservation, actual first
  SAVE/load address/bytes and independent tick-1600 golden validation. PASS
  here refers only to returned bytes, not physical workload timing.
- `xemu/`: unchanged P05 canonical and all four previous exact-name runs,
  admissions, actual SAVEs/traces/screens and reductions. Disposable SD fixture
  images are excluded. Fresh `closeout-validation/` reductions use the frozen
  version-7 source; no emulator was relaunched.
- `preservation-validation.json`: twelve prior freezes/7511 entries,
  original PRGs and P05 inputs audited unchanged.
- `retirement.json`: P05 invalid for further test/delivery; identical local
  ignored build guard prevents the existing controller from retesting it.
- `WIP-before-closeout.md`: exact 994-line pre-closeout WIP, SHA-256
  `4cde37a304201b11a3da832362a98d70bfa2f158a6ad6c0ac52ca7ee778d6b1d`.
- `checkpoint/`: exact review-time WIP and closeout/P04/P05 reports, preserving
  the source-document state even when later publication changes live WIP.
- `closeout-validation.json` and `sha256.json`: final local review checks and
  byte-identity manifest; the manifest excludes itself.

Evidence records intentionally retain their original absolute/build paths.
`delivery/` and `xemu/` preserve copies at equivalent relative locations;
do not rewrite historical provenance paths to make them look newly produced.

## Read-only analysis actually performed

The existing `d81_direct_delivery.verify_release` and `require_qualification`
checked canonical/release identity and the current pinned qualification.
Staging/final JSON hashes and extents were compared to `sd-release.json`.
`diskutil info -plist /Volumes/MEGA65FDISK` confirmed removable FAT32 UUID
`83FFC12E-67E1-307F-91AD-E584C2E01E87`, `disk4s1`. The sandboxed call could not
use DiskManagement; the approved read-only unsandboxed call succeeded.
No raw device read, SD write, unmount/eject or filesystem repair occurred.

`cp -n` preserved the mounted D81 to the fresh host evidence directory;
`cmp` and a later whole-file comparison confirmed the snapshot unchanged.
`d81_foundation_compare.Image` validated its exact size, chains, BAM and sector
ownership. `r0f_group1_export_probe.extract_actual` independently extracted all
four files with pinned c1541 twice and checked structure/content/free blocks.
Original payload hashes were compared to the untouched P05 canonical.

`r0f_group1_reduce.golden((1600,))` independently yields `6B765FDB`. The actual
saved 32-byte payload is checked against
`((checksum >> ((index & 3) * 8)) & 255) ^ index` for every index 0-31;
its two-byte load address is checked against the qualified `r0fsi_payload`
symbol `$3063`. No unseen physical terminal result is synthesized.

The existing `r0f_group1_owner_recovery.reduce_trace_files` ran the frozen
version-7 decoder on each retained P05 trace/SAVE into a fresh host-only
`closeout-validation/` directory; exact commands/exit codes are retained there.
The first wrong-version decoder rejection is recorded in preservation validation.

Fresh host command:

```sh
python3 -B -m unittest discover -s tools/diagnostics -p 'test_r0f_group1_*.py' -v
git diff --check
```

47 Group 1 tests and 18 delivery tests PASS. No target build or new Xemu/hardware execution. Physical trace
files are absent, so physical timing reduction and full-result Java validation
are unavailable, not passing. Video mode/core/ROM identities are unrecorded for
this run. Post-run FAT extent audit is not repeated; retained pre-run one-extent
evidence remains distinct from post-run internal D81 structure validation.
