# Work in Progress

This is the sole routine active-work record. It is not a project history or
design authority. Its operational status is exactly one of: `ACTIVE`,
`BLOCKED`, `READY FOR REVIEW`, or `NONE`.

It records the current task, branch, Build Intent summary or link, governing
authority, authorized area, blocker if any, validation/evidence state, and exact
next action. If no substantive work is active, status is `NONE`.

Completed work leaves this file. Durable project changes belong in
`CURRENT_STATE.md` only when they change enduring project reality.

## Current status

- **Status:** `ACTIVE`
- **Task:** R0-F successor first-fault diagnostic after a physically loadable
  `R0FDIAG3.D81` reported post-storage lockout.
- **Branch:** `codex/r0f-successor-physical-exact-carrier`
- **Build Intent:** The owner's 2026-09-21 recovery request supersedes the
  earlier frozen host filename: diagnose photographed chooser FF, fix fresh
  host construction/delivery, and fill the owner-created `R0FSUC10.D81` blank
  slot while also preparing a fresh host-transfer candidate `R0FHOST1.D81`.
  Preserve T04 program/bootstrap bytes and all predecessor evidence. Repeat
  host and exact-name Xemu gates; require raw FAT allocation/hash verification
  and safe eject before either new candidate reaches the physical chooser.
  On 2026-09-21 the owner additionally authorized a narrow target diagnostic
  revision after physical fault `0x58`: preserve the failed run, split the
  aggregate final predicate into distinct fail-closed codes, display the
  service mask/NMI/reserve values, build a fresh carrier identity, and repeat
  every applicable D81 gate.
  On 2026-09-22 the owner explicitly authorized rebuilding the D81 workflow,
  documenting it in AGENTS.md and engineering requirements, and fresh-building
  `R0FGIAG4.D81`. Keep T06 payloads unchanged to isolate carrier delivery.
  The prior prohibition on automatic CLI card transfers remains respected.
  After the four-extent GIAG4 audit, the owner explicitly approved one new
  SD candidate using the direct allocator, administrator authentication,
  unchanged existing files, verification and safe eject. This is a narrow
  exception to the earlier no-CLI-transfer instruction. New identity:
  `R0FHOST2.D81`; unchanged T06 diagnostic payload; repeat exact-name gates.
  On 2026-09-23, after the direct allocator stopped on the existing
  `F65BLK02.D81` filesystem error, the owner explicitly approved filling the
  previously MEGA65-formatted `R0FDIAG3.D81` blank after verifying it. This
  does not authorize filesystem repair or modification of any other SD file.
  On 2026-09-23, after confirming the physical `FAULT 57` screen came from
  `R0FDIAG3.D81`, the owner said "Continue" to the proposed narrow correction:
  preserve the first post-storage fault instead of overwriting it with `0x57`.
  Do not alter the tested D81 or its SD copy.
- **Governing authority:** `spec/manifests/spec-corpus.json` current authority
  order; Main Concept v1.6; Gameplay v1; Runtime v1 candidate; T01 successor
  reconciliation; frozen T02 contracts/ledgers; reviewed T03 implementation,
  private integration contract/ledger and handoff; and
  `00_D81_LOADABILITY_GATE.md`, the T05 Build Intent and the owner's explicit
  carrier/workflow recovery amendment.
- **Authorized area:** Host builder/transfer/verification repairs and regression
  tests; fresh D81 construction from frozen payloads; native-slot fill and
  fresh host transfer; SD hash, FAT32 one-extent and safe-eject evidence;
  physical platform, chooser and functional evidence; independent reduction;
  WIP and focused handoff. Narrow changes to the private successor diagnostic's
  final fault classification/display and corresponding private contract/tests
  are now authorized. No public ABI, high-level memory map, frozen T02 range,
  100 Hz/stage order, production StorageService,
  measured-limit freeze, Runtime v1 finalization, Phase 1, or founder acceptance.
- **Validation state:** Fresh refs established local `main`, `origin/main` and
  live GitHub `main` at the required integrated baseline
  `ae2b397698cc7197d03349e57cd058b4fb9f3987`. The clean canonical local
  `R0FSUCC10.D81` is present at 819,200 bytes with the authorized SHA-256
  `3721dff9b84cfb7842cc154f6885861e0c7cbd3c3408c8ecec190bf6b405d461`.
  Retained T04 records identify the 21,481-byte target SHA-256
  `d0979c56c373f8885e4741670141ebf22c0a2e9ef8a84f6a931eaef05592d9df`,
  source-freeze commit `20b2aab382d0590037443b6a352fbc77fda7aa42`, passing host structural/content
  gates and four passing exact-name Xemu carrier runs. The recovery carrier has
  now also passed SD copy, raw one-extent verification, safe eject and the
  physical chooser/entry-load gate. Physical runtime failed as recorded below.
  The intended `/Volumes/MEGA65FDISK` was identified as `/dev/disk4s1`, a
  29.1 GB writable, removable MS-DOS FAT32 partition on Secure Digital media.
- **Incident:** Owner photos show chooser `ERROR CODE FF` for `R0FSUCC10.D81`
  and an eight-character limit in the native creation dialog. The failed SD
  file matches the canonical SHA-256 exactly and passes internal structural
  comparison with the retained physical CF001 control. The failed physical
  copy is `INVALID — DO NOT USE`; it remains untouched for diagnosis. Earlier
  speculation about pasted whitespace causing the helper rejection was wrong:
  its nine-character basename is rejected by the helper's explicit 8.3 rule.
- **Current recovery state:** Fresh `R0FSUC10.D81` and `R0FHOST1.D81` each pass
  host structural/content gates and reproduce the original disk bytes exactly.
  Two NTSC plus two PAL exact-name Xemu runs pass for each candidate, including
  independent result/SAVE checks. Eighteen host regression tests, corpus validation,
  syntax and whitespace checks pass. A temporary non-D81 probe returned success
  for preallocation; the earlier inference that this proved a contiguous
  allocation capability was wrong (FSKit ignores that flag). The probe was
  removed. `R0FHOST1.D81` was then transferred and independently verified as the
  single-extent physical candidate described below. See
  `docs/reports/D81_DELIVERY_RECOVERY_2026-09-21.md` for the repair and evidence.
- **Active diagnostic:** Physical runtime ended in aggregate fault `0x58`.
  A fresh diagnostic preserves the success predicate but gives
  reserve, lifecycle, NMI, each required resumed service, unexpected mask and
  tick failures distinct codes and displays their source values. The tested
  `R0FHOST1.D81` copy must not be rerun.
  `R0FDIAG2.D81` is 819,200 bytes with SHA-256
  `912df16828f1c60127e4fcdd8d545dfca0c2ad8fe6a24a64ae01b4ac280df17d`.
  Fresh one-session construction, host structure/content verification, and two
  NTSC plus two PAL exact-name Xemu runs pass. All four Xemu results show fault
  `00`, lifecycle `09`, tick `0042`, mask `1F`, NMI `00`, and matching reserve
  CRCs. `R0FDIAG1.D81` is retained only as a parser-harness failure and is not a
  release candidate. See
  `docs/reports/R0-F_SUCCESSOR_T06_PHYSICAL_DIAGNOSTIC.md`.
- **Physical result:** The owner authenticated and the host-created transfer
  passed for `R0FHOST1.D81`: exact SHA-256, one 819,200-byte FAT32 extent at
  device offset 111,132,672, exclusive rename and safe eject all passed. The
  MEGA65 subsequently mounted and ran the image, closing the chooser/attach
  failure for this carrier. Physical runtime did not pass. Supplied photos show
  startup ROM verification, then `SUCCESSOR LOCKOUT - NO ACCEPTANCE` with
  fault `58`, lifecycle `0A`, tick `0042` and displayed CRC32 `20452538`.
  The owner observed brief graphics and sound. Evidence is retained under
  `docs/evidence/r0f/successor/2026-09-21-recovery/R0FHOST1/physical-1/`.
- **Latest raw evidence:** `build/r0f/successor-t05-recovery/sd-diagnostic.json`
  confirms the retired `R0FSUCC10.D81` has the exact expected hash but nine
  FAT32 extents. `R0FSUC10.D81` is absent at the root. `F65BLK02.D81` records
  819,200 bytes but its chain contains only 72 of the required 200 clusters
  (4,096 bytes each). Do not use that on-card file as a healthy control.
  This is not evidence of a card-wide fault; no card repair is authorized.
  The owner reaffirmed creation/delivery recovery. The unrelated on-card
  control is excluded as a transfer input; its anomaly remains unresolved.
  Raw geometry/FAT mirrors/root checks and the actual candidate's full raw
  hash/chain/one-extent gates remain mandatory and fail closed.
- **Completed host build:** Verified the retained CF001 successful path used a fresh
  single-session build and native contiguous-slot fill, not an ordinary copy.
  Completing the independent host-created path: contiguous/all preallocation,
  source hash recheck before creation, raw preflight before allocation,
  exclusive rename, staged/final raw validation and safe-eject gating.
  Eighteen host tests pass, including shell control-flow simulations at each
  failure boundary without SD access. Fresh reconstruction and four exact-name
  R0FHOST1 Xemu boots (two NTSC, two PAL) pass in `attempt-2`, with independent
  Python/Java result and SAVE checks. Prior attempts remain retained; current
  delivery-tool hashes are recorded. Candidate remains 819,200 bytes with
  SHA-256 `3721dff9b84cfb7842cc154f6885861e0c7cbd3c3408c8ecec190bf6b405d461`.
  Offline execution of the real manifest preflight passes against both real
  manifests and images (mocked device identity, not an SD gate).
- **Current incident:** On 2026-09-22 the owner reported chooser FF after
  manually copying `R0FDIAG2.D81`. That SD copy is retired. The card is back
  with a newly native-formatted `R0FDIAG3.D81` (actual filename). Both images
  pass internal filesystem checks; the failed SD copy exactly matches the
  canonical source hash. The earlier 22-extents record belongs to a removed
  staging file, not this manual copy. Apple FSKit FAT source explicitly ignores
  contiguous preallocation requests; the current mount uses FSKit. This
  disproves the earlier claim of reliable host contiguous allocation via that
  request. The T06 wrapper is disabled before any media access. See
  `docs/reports/D81_NATIVE_COMPARISON_2026-09-22.md`.
- **Raw comparison resolved:** Owner-supplied raw audit confirms exact failed
  `R0FDIAG2.D81` bytes in 13 extents; native `R0FDIAG3.D81` and previously
  hardware-mounted `R0FHOST1.D81` each occupy one extent. This establishes the
  candidate-specific allocation difference, not a card-wide defect.
- **New build:** `R0FGIAG4.D81`, SHA-256
  `90a819f49c5b6cb3bf66f71317c1f40e3cae3f4059fb422b46b05589e86915fa`,
  is 819,200 bytes. Host structure/content and two NTSC plus two PAL exact-name
  Xemu boots PASS. Target PRG remains the T06 diagnostic, unchanged. A pinned
  official allocator has passed fragmented disposable FAT32 fixture writes and
  full unrelated-byte preservation checks. See `docs/D81_WORKFLOW.md` and
  `docs/reports/D81_WORKFLOW_R0FGIAG4_2026-09-22.md`.
- **Latest physical failure:** Owner photo shows `R0FGIAG4.D81` chooser FF;
  that tested copy is `INVALID — DO NOT USE`. The same-card Alpha control
  `A. MegaWing/F65-R0A-PROOF.D81` shows a readable directory. Read-only host
  comparison confirms GIAG4's SD bytes exactly match canonical; both images
  pass structural parsing and their headers differ only in label bytes.
  See `docs/reports/D81_GIAG4_ALPHA_COMPARISON_2026-09-22.md`.
- **Allocation finding:** Owner-authenticated `giag4-raw-audit.json` confirms
  the exact canonical hash but four extents for GIAG4. Allocation gate FAIL;
  no card-wide defect is inferred. Preserve Alpha and all failed copies.
- **Current operation:** Build/check new `R0FHOST2.D81`, revalidate allocator
  qualification, then attempt the expressly approved direct install to volume
  UUID `83FFC12E-67E1-307F-91AD-E584C2E01E87`. Device name must be resolved
  again; last read-only observation was `disk4s1`. Administrator authentication
  is required; no SD write has occurred at this checkpoint. Stop on any gate
  failure without repairs, overwrite, force unmount or fallback copying.
- **Current checkpoint:** HOST2 host checks and all four exact-name NTSC/PAL
  boots PASS, SHA-256 `49e8c104e6def9f0557bd55ce1149b8e1d0fe111b3454e022e06642dcff5c2bd`.
  Sector-aligned raw FSInfo I/O correction passed 12 allocator tests; 18
  existing delivery tests and corpus validation PASS. The approved install
  was requested through the standard macOS administrator dialog. After owner
  authentication, the process failed at its first read-only raw-device open:
  `PermissionError: [Errno 1] Operation not permitted: /dev/rdisk4s1`.
  Session 1620 has exited. No unmount or SD write occurred and no install
  evidence directory was created. Next action: run the same approved installer
  from the owner's Terminal, where authenticated raw audits previously worked;
  do not change system permissions or bypass any gate. See
  `docs/reports/D81_R0FHOST2_INSTALL_2026-09-22.md`.
- **Latest Terminal attempt:** Raw read succeeded, but preflight stopped at
  `info_sectors` with `invalid FSInfo signature`, before unmount or writes.
  The validator does not identify whether primary or presumed backup failed.
  Added read-only `d81_fsinfo_audit.py` to retain the actual boot pointers and
  selected reserved sectors. Obtain that evidence before modifying the write
  gate; no repair, new carrier or repeated install is authorized by this error.
- **FSInfo correction:** Owner-supplied sector evidence establishes valid
  primary FSInfo at sector 1, boot backup at 6, and all-zero presumed backup
  FSInfo at 7. Corrected the erroneous requirement that sector 7 be populated.
  Preserve it byte-for-byte; reject invalid primary, nonzero invalid backup,
  or out-of-range layout. Sixteen allocator tests PASS, including complete
  allocation/rename/FSInfo/audit with a blank backup and filesystem check.
  Exact recorded card bytes also pass primary-only handling. Current
  qualification: `build/r0f/d81-workflow/R0FHOST2/allocator-qualification-2.json`.
  HOST2 identity and release gates rechecked unchanged. No SD writes in this
  correction. Next: retry the already authorized install from owner Terminal
  using the new qualification; all other gates remain mandatory.
- **Latest blocking gate (2026-09-23):** The owner-run retry identified the
  intended partition and unmounted it. `fsck_msdos -n` then returned 206:
  `A. MegaWing/F65BLK02.D81` has a cross-linked chain at cluster 12417 and
  an 819200-byte size with at most 4096 bytes reachable; 623 orphan clusters
  were also reported. The installer stopped at the mandatory clean-filesystem
  check before `deliver`, staging, FAT allocation or SD writes. Its local
  report directory does not exist. The volume remains unmounted according to
  the supplied command output; the owner subsequently remounted it. Other
  working files are not thereby declared bad; no filesystem repair or deletion
  is authorized. Do not bypass the
  current gate or rerun this installer on unchanged card state.
- **Current native-slot candidate:** The owner authorized filling the existing
  never-tested `R0FDIAG3.D81` blank. Its current mounted SHA-256 still equals
  the retained empty native image:
  `357078cd97a9aae0bf676ed844e5a01bfcafd32994309cf0d657f53e2a590018`.
  The fresh same-name host image is 819200 bytes, SHA-256
  `30508cb424e526b09f9f923e3ae4e35e449d89a5ec239f769b7da8a8cb2e1d60`,
  with unchanged T06 PRG SHA-256
  `3ce9aeb1029676465d47755145ec31d6b30ab2ca0c8ae95dc88e9703dd99446b`.
  Host structure/content and four exact-name Xemu boots (two NTSC, two PAL)
  passed. One earlier Xemu invocation failed for an app configuration permission
  error; its log is retained, and no carrier bytes were changed. The owner-run
  slot-fill helper passed: the preimage was the verified blank, the raw FAT32
  audit proved one 819200-byte extent, and the postimage hash is the canonical
  `30508cb4...e1d60` at the unchanged device offset 114716672. The helper
  retained a host-side blank backup and reported safe eject PASS. Evidence:
  `build/d81-sd-transfer/R0FDIAG3.D81.slot-pre.json` and `slot-post.json`.
  The owner then supplied a MEGA65 photo of the successor diagnostic screen:
  `FAULT 57` (hex), `STATE 0A`, `TICK 0021`, `MASK 00`, `NMI 00`, equal reserve
  CRCs. Code `0x57` is the post-storage tick-loop failure; the first post-
  storage tick did not complete, and an inner fault could be overwritten by
  the outer code. The owner explicitly confirmed selecting exact
  `R0FDIAG3.D81` to reach that screen: physical chooser and entry-load gate
  PASS for this carrier. This is not a D81 chooser `FF`; physical R0-F runtime
  acceptance failed. The native blank-fill route is therefore physically
  validated once, while the host-created direct allocator remains blocked by
  its clean-filesystem gate and has no physical pass. Retained photo and interpretation:
  `docs/reports/D81_R0FDIAG3_NATIVE_SLOT_2026-09-23.md`. No wider R0-F test
  is eligible.
- **T07 diagnostic checkpoint:** The private post-storage tick failure branch
  now preserves a nonzero inner fault and uses `0x57` only when no inner fault
  exists. Four host cases for fallback/first-fault preservation passed within
  the full `1,527,538`-check T03 host build, as did CF001, RH001, target
  compile/link and static accounting. The new target PRG is 21,922 bytes,
  SHA-256 `5600782308a16976d0d20303e0c8d215b9db0f1dab1680f17e9a07ccfea47d7c`.
  Resident usage is 24,098 of 40,959 bytes; protected end remains `0x2B07`,
  reserve consumption 0. Fresh token-only direct-PRG NTSC and PAL Xemu probes
  passed with independent result reduction and Java oracle; this is development
  evidence, not a physical pass. A fresh `R0FDBG07.D81` canonical image was
  then built in one session: 819,200 bytes, SHA-256
  `c780d79a0e24ff00f10fbb7f3829ec943783c8b2d4413417ba389d900edcc775`.
  Independent host content/structure and four exact-name NTSC/PAL Xemu boots
  passed. Its release and run evidence is under
  `docs/evidence/r0f/successor/2026-09-22-workflow/R0FDBG07/`. The previously
  tested `R0FDIAG3.D81` remains byte-identical and untouched. Next: review
  the narrow change/source provenance, then use only an authorized new SD
  placement that proves hash and one extent before physical testing. No SD or
  physical claim exists for `R0FDBG07`; broader R0-F testing stays stopped.
- **T07 source-freeze checkpoint (2026-09-24):** The reviewed diagnostic,
  private contract, generated header, delivery workflow/tooling and tests were
  committed as `e8caf09002b7793be2effd9f5badd825aeedf301` and pushed to
  `origin/codex/r0f-successor-physical-exact-carrier`. The post-commit target
  rebuild retained the 21,922-byte PRG SHA-256
  `5600782308a16976d0d20303e0c8d215b9db0f1dab1680f17e9a07ccfea47d7c`;
  the existing canonical `R0FDBG07.D81` retained SHA-256
  `c780d79a0e24ff00f10fbb7f3829ec943783c8b2d4413417ba389d900edcc775`.
  Four fresh exact-name post-push Xemu boots (two NTSC, two PAL) passed with
  independent reduction and Java oracle. See the T07 report and retained
  `post-source-freeze-e8caf09/` evidence. Its construction occurred before
  the source freeze; the post-freeze runs preserve that provenance distinction.
  SD copy, one-extent audit, safe eject, physical chooser and physical runtime
  for this candidate remain NOT RUN. The separate evidence commit records these
  historical and post-freeze results. Next: provide the canonical host path
  for owner-selected Finder transfer; read-only audit and safe eject are
  mandatory before any hardware test.
