# Minimum renderer source baseline — READY FOR REVIEW

`65AERO-M2-MIN-REBUILD-1` is a new implementation from verified main
`b044440fa98c2dfc91ec590668049610afc98a1e`, on
`codex/65aero-m2-minimum-renderer-baseline`. It is not recovered historical
candidate source. The prior source-import failure remains intact. This task
has not committed or published the new baseline.

The complete target compiles and links. Actual resident fit **FAILS**:
**32,883 bytes against 24,575, a deficit of 8,308 bytes**. Runtime launch and
all eight target service grants remain zero. No optimization followed this
measurement. No banking or target execution was performed.

## Implementation and ownership

| Paths | Responsibility |
| --- | --- |
| `interfaces/m2_rebuild.json`, `tools/flight_demo/m2_rebuild/generate.py` | Pinned private profile, selected segment IDs, generated outer composition record and owner ledger |
| `interfaces/generated/m2_rebuild_profile.h`, `memory/m2-rebuild-ledger.json` | Generated artifacts; public M1/M2 records unchanged |
| `src/input/m2_rebuild_input.*` | Semantic diagnostic-camera press edges |
| `src/diagnostics/m2_rebuild/camera.*` | Bounded mutable presentation camera and revision exhaustion |
| `src/graphics/m2_rebuild*` | Snapshot capture, prepared transform, nine cached lines, horizon, resumable tile/pixel/text work and paired complete publication |
| `src/platform/m2_rebuild/*` | Checked display copy/commit seam, mode setup, deadline predicate and reset-only early startup |
| `src/diagnostics/m2_rebuild/main.c` | Real complete composition, unchanged simulation dispatcher, zero runtime admission grants |
| `tests/flight_demo/m2_rebuild/*` | Host/sanitizer behavior, private contracts, linked-startup mutation regressions |
| `tools/flight_demo/m2_rebuild/validate.py`, `replay_static.py`, `startup_check.py` | Fresh evidence, complete link/fit accounting, read-only artifact replay and normal-entry static check |

Environment retains all 17 canonical fixture segments unchanged. This private
profile draws `[0,1,2,3,4,5,7,11,15]`. The integrated Geometry implementation,
Q12 positions, Q24 clipping, Q46 rotation, Q16 screen coordinates and oracle
tolerances are unchanged. There is no precision or ABI reduction.

The renderer copies the newest immutable snapshot while holding its slot and
releases that slot before yielding. One transform is prepared and each selected
segment is projected once per captured generation. Tile construction never
projects geometry. The nine line records and visibility flags occupy 153 bytes;
they do not alias any continuation, tile, text or registration storage.
Cancellation invalidates the prepared context and all visibility flags before
another quantum. Camera identity includes pose and revision. Generation and
camera-revision exhaustion fail closed.

The hidden store receives all world tiles, cached runway pixels and telemetry
before publication. Deferred commit keeps the completed candidate pending.
Transfer failure retains the old front store; an uncertain hardware commit is
terminal and does not claim rollback. Each store has its own generated bundle.
The outer composition revision is 3; the inner public registration remains
revision 1. Optional registered cues and ranked labels remain disabled.

The host frame shows blue sky, green ground, projected runway, numeric counters,
`NON-FLIGHT DIAGNOSTIC`, and `ALTITUDE: NOT IMPLEMENTED` /
`AIRSPEED: NOT IMPLEMENTED`. Camera height is explicitly a diagnostic camera
quantity, not an aircraft altitude implementation. Host imagery is not Xemu
scanout or visual qualification.

Controls: W/S north/south, D/A east/west, R/F camera up/down, Q/E yaw,
I/K pitch, J/L roll, HOME reset. Each press advances one bounded step; held
keys do not repeat. Opposing edges cancel; reset takes precedence. Space uses
the unchanged M1 semantic command path. No aircraft or physics state exists.

## Actual complete-link accounting

The unchanged pinned LLVM-MOS compiler uses the integrated size flags:
`-mcpu=mos45gs02 -mlto-zp=0 -Oz -fno-inline-functions -fno-jump-tables
-Wall -Wextra -Wconversion -Werror`.

| Allocation | Actual bytes |
| --- | ---: |
| BASIC/entry prefix before `.text` | 22 |
| `.text` | 29,756 |
| Alignment before `.rodata` | 5 |
| `.rodata` | 1,435 |
| `.data` | 0 |
| `.bss` | 1,475 |
| Compiler `.noinit` scratch | 190 |
| **Resident union `$2001–$A073` (end `$A074`)** | **32,883** |
| **Resident acceptance ceiling** | **24,575** |
| **Deficit** | **8,308** |
| Renderer workspace within BSS | 676 |
| Protected reserve consumed | 0 |

All BSS symbols sum to 1,475 bytes. The PRG's 31,220 file bytes exclude runtime
BSS/scratch and include its two-byte load address; file length is not resident
usage. The SDK's larger default measurement region is not admission to use
memory beyond `$7FFF`. The image is named `UNADMITTED.prg` and is quarantined.
Its end remains below the software-stack floor, but that does not legalize the
resident allocation or establish stack safety.

Hardware stack remains `$0100–$01FF` (256 bytes), base page `$0200–$02FF`
(256 bytes), and software-stack envelope `$C000–$CFFF` (4,096 bytes).
Compiler pseudoregisters occupy physical `$0202–$0221`; the existing flat-copy
pointer scratch occupies `$0222–$0229`. No lifetime aliasing is claimed.

Display A and B each use 63,552 bytes at `$020000–$02F83F` and
`$030000–$03F83F`. Each has a 2,000-byte screen map, 48-byte alignment gap,
61,440 bytes of private full-color tiles and one 64-byte immutable black tile.
Color RAM `$0FF80000–$0FF807CF` is 2,000 immutable bytes. The explicit unchanged
M1 platform dependency retains its reset-only ROM-backup lifecycle at
`$08000000–$0801FFFF`. Simulation, audio, resource and reserve bands are not
borrowed. No DMA list, bank gateway, staging lease or code-bank allocation exists.

The historical missing candidate's 26,750 bytes / 2,175-byte deficit describes
another identity. This reimplementation adds 6,133 resident bytes relative to
that historical measurement. The approved RF design estimates remain preserved;
they are not new fit evidence. Hypothetical removal of the historical 4,374-byte
estimate from this link would still leave a 3,934-byte deficit before gateway
or additional data. Even ideal direct relocation of a full 8,192 bytes would
leave 116 bytes uncovered before the bank header, gateway and other overhead;
this is only a lower-bound budget observation, not a new placement decision.
The approved RF estimates cannot establish fit for this new identity. No
placement or banking work was started.

## Evidence and checks

Evidence root: [new packet](../evidence/flight-demo/2026-10-27-m2-min-rebuild/).
Each attempt has its own input hashes, commands, outputs and seal. None of the
failed attempts was overwritten.

- `host-1793158722615552000`: five contract checks passed; new host test compilation
  failed because Clang rejected a string-as-boolean assertion. Preserved.
- `host-1793158735932906000`: compilation passed; a speculative >100 runway-pixel
  assertion failed. The actual independently assembled frame has 86 white world
  pixels. The requirement is visible geometry, and exact comparison covers all
  40,960 world pixels. The arbitrary count threshold was removed. Preserved.
- `host-1793158762399896000`: ASan/UBSan behavior, camera limits/edges, common horizon,
  complete frame, nine-per-generation projection count, cancellation at all seven
  active stages, held snapshots, faults, exhaustion, deadline boundaries and
  600 per-tick deterministic replay comparisons passed (`DE675132`).
- The same successful host packet passed the unchanged geometry host, 3,672
  prepared-context segment comparisons, raster-cursor checks, the independent
  3,857-case Decimal geometry oracle and 841 near/far regressions. Maximum oracle
  projection errors were 0.000021225 and 0.035137 pixels respectively, within
  the unchanged tolerances. All 15 CI-policy unit tests passed.
- `target-1793158803095519000`: one complete target compile/link passed. The map,
  ELF, PRG, symbols and disassembly retain the real geometry, mutable camera,
  runtime, input, font, copy and commit dependencies. Resident fit failed.
  The first new static verifier also rejected a shared boundary address.
- `static-replay-1793158940264539000`: no relink. Corrected the verifier's equality
  boundary and replayed the exact sealed target. Twelve contract/startup tests
  passed, including wrong entry, early stack init, missing MAP, incorrect CPU
  port / I/O MAP and sealed-packet preservation. The original rejection remains
  intact. The target application source is unchanged.

PRG SHA-256:
`388a034707e10547c0bae65a4744a0090ef8c152f9c8eef355021f01e0a5df8a`.
The private profile SHA-256 is
`9567374c9b08c1f24e9d58caca081885841dea42ae08c04e8b898e1dd42c7efb`.
Additional exact identities and final preservation results are in the evidence
root. No binary identical-to-old-candidate or complete historical recovery claim
is made. Historical recovery remains 22 verified members and 15 unresolved;
eight prior checkouts remain **NOT VERIFIED at the Git-worktree tier**. No
missing file or Git metadata was reconstructed, and none was an input to this
implementation.

A second target link was not run after the failed fit gate. Bit-for-bit repeat
relink reproducibility is not claimed; the complete inputs and build recipe
are retained for that later check.

Reproduce from a checkout containing this focused change:

```sh
python3 -B tools/flight_demo/m2_rebuild/validate.py --tier host
python3 -B tools/flight_demo/m2_rebuild/validate.py --tier target --sdk /path/to/pinned/llvm-mos
python3 -B tools/flight_demo/m2_rebuild/replay_static.py
```

The target command intentionally returns failure for an oversized link. It never
executes a target. Fresh directories preserve every invocation. Actual commands
and the external pinned toolchain path are recorded in each result. Hosted CI
was verified for the base main; this uncommitted increment has no exact-head
hosted CI result. Untracked text and focused diff checks are local checks.

## Admission and handoff

| Gate | Result |
| --- | --- |
| Private contracts / generated bytes / public-source preservation | PASS at host/static tier |
| Host correctness / frozen independent oracles | PASS |
| Complete target compile/link | PASS |
| Normal reset-entry startup ordering | PASS at linked static tier |
| Runtime startup safety, including asynchronous/ROM-trap behavior | UNPROVEN |
| Whole-program hardware/software stack safety | UNPROVEN |
| Renderer service / clock-guard cost | UNPROVEN; all eight operation bounds and guard bound remain zero |
| Actual resident fit | FAIL, 8,308-byte deficit |
| Xemu / actual display behavior | NOT RUN / NOT OBSERVED |
| Banking / D81 / SD / physical tests | NOT IMPLEMENTED / NOT RUN |

The whole-program stack checker refuses unaccounted software-SP writes. It has
not been weakened or extended to suppress unknown paths. IRQ/NMI, reset/fault
and hypervisor-trap paths still require a complete conservative proof. The
linked normal entry clears both megabyte selectors and MAP, performs EOM,
sets E/page-1 stack, CPU-port and I/O state, installs terminal resident early
vectors, and selects B=$02/Z=0 before SDK stack/BSS initialization. Stock
`.init.010` port writes and `.init.250` CHROUT are excluded; their later B=$02
accesses would be unsafe. This is a static ordering result, not execution proof.

The eight continuation roles bound operation cardinality, not admitted cycles:
begin, one transform/registration, one segment, eight horizon samples, one
<=64-byte copy, one raster step/pixel, one glyph/telemetry row, or commit.
The integrated geometry primitives may be expensive. Until every operation and
guard has a justified nonzero conservative bound fitting authoritative slack,
the guard refuses them. The clock stays 100 Hz and the 21-stage order remains
unchanged; delayed ticks are caught up in order without skipping or merging.

The display adapter is source-complete but unqualified. Pinned source informs
V200 scanline duplication and X scaling; actual PAL/NTSC mode, border cropping,
font/palette, pointer prefetch and safe commit still require later admission.
The even physical top is 64 NTSC / 112 PAL; NTSC center-crop alignment differs
by one raster from an ideal odd origin. No exact output-offset acceptance is
claimed from a host image. No display redesign was attempted.

Recommended next action: founder review of this source baseline and its retained
failure. A separate publication authorization is needed before committing it.
After integration, re-evaluate residency and whole-program service/stack costs
against this new measured identity before authorizing any banked prototype.
M2 and FULL/Graphics v2.1 acceptance remain unclaimed.
