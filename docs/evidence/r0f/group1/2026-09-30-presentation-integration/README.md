# Group 1 presentation integration, DOS-cache correction and local carrier gates

Local evidence from the dirty `codex/r0f-successor-physical-exact-carrier`
checkout at HEAD `9e2ffdb4786e4794119933a5edd4b1cf79f653f0`. This freeze is
not a commit, publication, SD delivery, physical result or full Group 1/R0-F
acceptance. The [integration report](../../../../reports/R0-F_GROUP1_PRESENTATION_INTEGRATION.md)
records authority, implementation, exact commands, failures and remaining gates.

## Identities and scope

- Corrected integrated PRG: 37623 bytes, SHA-256
  `25a18c23c750d0877103209fccd0114afe7cd30f31690731605b9687bfea94e1`.
  Resident end `$BFC5`, 59 bytes free; protected end `$30B1`. No reserve is
  borrowed. `build/` retains map, symbols, disassembly, target commands and
  the 93-input build identity. `source-inputs/` adds carrier tooling/tests for
  95 exact inputs. Generated private trace/scene bindings are retained.
- Trace version 5: 92-byte tick records, 16-byte world events, maximum 2000
  events / 327172 bytes inside the existing 327680-byte trace allocation.
  This is diagnostic transport capacity, not a production rate/capacity claim.
- Fresh direct NTSC/PAL evidence is under `development/presentation-ntsc-04/`
  and `development/presentation-pal-02/`. Each retains all 3200 actual records,
  SAVE, 19 closed chunks, raw disk, independent extraction/BAM/content checks,
  execution identity and reduction. Nominal misses/uncertain/below-floor cohorts
  are zero; 956 NTSC / 807 PAL complete registration pairs validate.
- Replacement canonical `R0FG1P02.D81`: 819200 bytes, SHA-256
  `60cea9c8dd51b0f2c199605e60574c0bebd7c758d5899fb9b1e7c2901f83e832`.
  `carrier/R0FG1P02/` retains fresh single-session construction, bootstrap
  entry `$30B1`, independently extracted initial payloads, exact-name clean
  autoload boot copies and their actual SAVE/export evidence. Canonical was
  never mounted writable. The final carrier summary establishes all four
  local boots (two NTSC, two PAL), XEMU_BOOT_VERIFIED only; no physical
  eligibility follows from it.

## Preserved failures and correction proof

- `development/presentation-ntsc-01/`: target compiler inline LOD error;
  `presentation-ntsc-02/`: valid presentation but 211 nominal deadline misses.
  Their original linked builds and exact source snapshots are retained. They
  are not passing evidence and their disks are never reused.
- `memory-fit-split-overshoot/`: first split link, 21 bytes over the envelope;
  `memory-fit-refresh-overshoot/`: first cache-refresh link, 43 bytes over.
  Neither was run or treated as a fit PASS.
- `pre-refresh-build/`: exact preceding presentation PRG `1ab31a8a...`, its
  89-input source/build identity, and 122-byte fit. Passing pre-refresh direct
  evidence remains in `development/presentation-ntsc-03/` and
  `development/presentation-pal-01/`; it did not establish carrier correctness.
- `retired-carrier/R0FG1P01/`: unchanged failed canonical and NTSC copy.
  Restoring an entry-time DOS/BAM cache caused RSSTATE and G1T00 to share
  sector 36/30, overwriting the returning SAVE. Independent structural
  validation failed despite target status 4/error 0. `retirement.json` retains
  exact hashes and forensic facts. No repair, rename or retest occurred.
- `cache-refresh-probe/`: fresh 60-second autoload proof of actual RSSTATE
  preservation and 33025 deterministic exported bytes after public DOS I0.
- `cache-refresh-negative-probe/`: exact-width disposable derivative simulates
  OPEN error 5; permit is consumed, no trace is written, original SAVE remains
  valid, and no retry occurs. Not an electrical/DOS fault-injection proof.
  The two probe tool snapshots were restored to their exact recorded SHA-256
  versions before this freeze, and all 73 inputs of each were verified.
- `cache-refresh-collision-probe/`: a separate 60-second PAL autoload retains
  an existing G1T00 sentinel and actual RSSTATE, stops with status 5/error 3,
  writes no chunks and does not retry. Its 77 exact source inputs are retained.

## Boundaries and preservation

The integrated scene is a private 65-byte diagnostic encoding copied into an
actual backbuffer. Per-pair CRCs verify the fixture's binding/anchors/clipping/
size-LOD outputs, not complete renderer geometry, physical pixels or scanout.
Stale displayed registration is invalidated during ROM restoration; explicit
fallback is excluded from current-epoch displayed-age observations. Original
returning context invalidation and the separate immutable pre-C export capsule
retain their admitted lifetimes. I0 refreshes DOS through its public command
channel; no private cache field is patched and no new physical range is added.

All 30 repaired-CRC corruption cases reject against each corrected direct trace.
Thirty host contract/admission/terminal/carrier tests pass. Host scene coverage
retains 3200 independent encodings, 720 anchor permutations, 2592 clipping cases
and 131072 LOD comparisons with sanitizers. `ordinary-preservation-final/`
rebuilds the ordinary successor byte-identically at `cf605bd3...`.

The earlier passing `ec259fc7...`, corrected `0d96a1b...`, six-order `c249f4e4...`
and all four preceding immutable freezes remain unchanged. The preservation
audit verified 248 prior manifest entries. This new freeze excludes large
disposable virtual-SD clones; their paths/hashes remain in execution reports.
It retains the actual post-run D81s and all exported chunks. No physical SD was
accessed or written, and no commit or push occurred.

`validation.json` records the final audit and its exact commands: all six
actual corrected reductions match, all 30 host tests pass, and three separate
30-case mutation suites reject. `sha256.json` freezes all retained files except
itself. The audit tool is retained under `final-audit/`; it refuses to overwrite
an already finalized manifest.

Production projection/directional hysteresis/terrain-carrier registration,
remaining geometry/audio/sensor pools, integrated near-capacity trace, compact
operator summary, whole ISR/entry latency and physical SI uncertainty remain
open. SD allocation/one-extent proof, physical chooser/entry/runtime evidence
and owner acceptance require their separate gates and authorization.
