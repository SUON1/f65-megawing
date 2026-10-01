# Group 1 presentation integration and local gates - 2026-09-30

The bounded presentation fixture is linked into the actual incremental display
path. Fresh NTSC and PAL acquisitions pass independent export/SAVE reduction,
all bound registration/occlusion/LOD checks, sampled service phase/order
coverage and nominal timing. Resident fit is proven without reserve borrowing.
The first carrier exposed and isolated stale DOS allocation-cache restoration;
the terminal-only correction passes short normal/error probes and repeated
fresh NTSC/PAL timing. Replacement exact-name local carrier passes all four
clean boots; SD, physical and full Group 1 acceptance are not established.

## Authority and scope

The approved [Group 1 Build Intent](../plans/R0-F_GROUP1_BUILD_INTENT.md),
[measurement matrix](../plans/R0-F_GROUP1_MEASUREMENT_MATRIX.md), Main Concept
v1.6 sections 10/17, Graphics v2.1 sections 2.6/3.1/6.4/7, candidate Runtime v1
sections 8/14, T02/T03 generated interfaces and memory ledgers govern. The root
D81 gate, reproducible D81 workflow, programming principles and C standard
apply. This is local implementation/validation only: no SD writes, physical
runs, commit or push.

The two views/tiers/buffers, four anchors/columns, six candidate cues, size
thresholds and scene coordinates remain private diagnostic parameters. This
is not a production GraphicsEngine or public WorldRegistrationRecord layout.
No per-service latency limit, maximum world age, 530000-clock tick allowance,
production capacity or flight/terrain model is selected.

## Integrated behavior

- One immutable snapshot binds generation, source tick, requested view,
  selected tier, physical backbuffer and horizon. Requests every 128 fixture
  ticks cancel only superseded unfinished/ready work; the complete displayed
  pair remains unchanged until a matching new pair is ready.
- Six candidate anchors exercise actual four-entry priority eviction. Four
  columns exercise front, clipped, hidden and above-ridge fragments. Size LOD
  chooses once before binding, with the previous displayed tier as hysteresis
  state. None of this state feeds authoritative simulation or world queries.
- A generated 65-byte encoding contains the actual bound key, registration,
  retained anchors, envelope and clipping outputs. Those bytes are copied nine
  times into the real backbuffer; the independently reconstructed CRC is
  retained for every swap. It is a diagnostic byte pattern, not a complete
  visual scene or physical pixel-readback proof.
- Clear, scene construction, each copy and final completion are resumable
  foreground steps. The snapshot is held through all steps and rechecked by
  CRC before release. Ready is set only after the last copy. Registration/view
  publication and VIC store selection have one foreground owner, no IRQ
  readers. The two stores share pointer low/mid bytes; only the bank byte
  changes at a valid swap. This is not an instruction-atomic C-structure or
  independently observed scanout/blanking guarantee.
- Returning storage necessarily restores ROM over both display stores. Before
  display/clock restart, the restored staging workspace is reseeded, pending
  work discarded, registration invalidated and the front store cleared to an
  explicit unregistered fallback. The first fresh attempt starts cheap; buffer
  parity and generation history continue. DISPLAY_VALID distinguishes fallback
  from a complete current-epoch pair. No stale image/registration or
  cross-storage age is claimed. This is restoration during the storage pause,
  not an extra simulation tick or warmup.

## Exact failures and corrections

The first integrated PRG `a8d50072...` exported 3200 records and 1097 worlds,
but independent reduction rejected world 9: source tick 24 should select the
cheap tier at size 8, yet the target retained tier 1. Disassembly at
`$766A-$7682` proves the pinned compiler's inline fold uses NZ from `LDX #1`
after `STZ $06`; STZ does not update NZ. Its following BNE skips the zero-tier
path. Keeping the pure LOD C function `noinline` corrects this target path;
no assembly policy replacement or toolchain upgrade was made. Host exhaustive
LOD checks and fresh actual target evidence cover the correction.

The next PRG `1c18d340...` passed all 1091 presentation pairs but had 211
nominal deadline misses (no cadence-floor failures). Large display steps
combined scene construction and all nine copies, increasing pre-release
lateness. Splitting construction/copies/completion removes this carry-in burst
without changing the fixed 100 Hz release policy or inventing a service budget.
The first split link exceeded resident memory by 21 bytes and correctly
failed admission. Its bounded copy offset was unnecessarily 32-bit; narrowing
the maximum 520-byte offset to uint16 recovered fit. Failed runs, their exact
sources/builds and the rejected link map are retained; none is reused as PASS.

The first clean carrier boot, `R0FG1P01/ntsc-01`, completed acquisition/export
status 4/error 0 but failed independent structure validation. `RSSTATE` records
one block yet has a 65-sector chain; both it and `G1T00` point to sector 36/30.
Their extracted 16386-byte payloads are identical, SHA-256
`f80ca47965e15b76be101af73a82c04f45ddf328bd4282cab125f43e7687c300`.
The trace's first SAVE overwrote the prior returning SAVE. No carrier PASS or
nominal-timing PASS is inferred from its in-memory success flags.

The retained entry-time DOS backup contains the canonical BAM at `$055800`
and `$055900`; its track-36 bitmap still marks sector 30 free. Terminal restore
rewinds this valid cache to before returning storage allocated RSSTATE. Direct
PRG/token-only fixtures did not enter with that loaded-file cache state, which
explains why they passed without detecting this path. The failed canonical and
tested copy are retired, unchanged, with a forensic retirement record. They
are never repaired, renamed or retested.

After capsule restore/consumption and before any terminal trace SAVE, the
exporter now sends `OPEN 0,8,15,"I0"`, followed by the documented special CLOSE.
The [official OPEN/CLOSE reference](https://raw.githubusercontent.com/MEGA65/mega65-user-guide/master/appendix-kernal-jumptable.tex)
provides this command-channel sequence; the [official DCLEAR description](https://files.mega65.org/files/m/mega65-userguide_Q5jaf7.pdf)
specifies rereading the BAM. No private DOS field is patched, capsule refreshed,
original context retained past its lifetime, or second returning-storage call
introduced. Protected common setup shares SETNAM/SETBNK/SETLFS for the command
and SAVE; every public call retains the existing mapping macro. Static checks
use linked instruction addresses to handle aliased end/start labels, verify
the sole returning setup helper and ensure initialization precedes SAVE.

Two 60-second fresh autoload probes qualify this correction. The normal probe
preserves actual RSSTATE and exports all 33025 deterministic bytes with exact
directory/BAM/chain/content checks. An exact-width disposable PRG derivative
simulates OPEN error 5: export fails status 5/error 5, permit consumed, zero
chunks, no retry, and original on-disk RSSTATE remains valid. This is a
simulated public-call error, not an electrical/DOS fault-injection claim.

A separate 60-second PAL autoload collision probe retains an existing G1T00
sentinel and actual RSSTATE unchanged, rejects export with status 5/error 3,
writes zero chunks and does not retry. The cache correction does not relax
the original no-overwrite rule.

The first refresh link exceeded the resident end by 43 bytes and was not run.
The private 32-bit wire writer now shifts its value by a fixed eight bits per
iteration rather than recomputing a variable-width shift. This preserves the
little-endian format, saves 102 target bytes and recovers fit. Actual independent
trace reduction and repaired-CRC negatives validate the changed encoding.

## Memory and exact identity

Passing PRG:
`25a18c23c750d0877103209fccd0114afe7cd30f31690731605b9687bfea94e1`,
37623 bytes. Resident end is `$BFC5`, leaving **59 bytes** before `$C000`.
The target map charges presentation state at 125 bytes, encoded pixels at 65
bytes and compiler static scratch at 36 bytes; host native state size is not
used as target accounting. Protected content remains `$2017-$30B0`, below
terminal staging at `$4000`. Fresh direct-run observed stacks are NTSC 61 / PAL
63 hardware and 118 software bytes, not a universal worst-case proof.

Group 1 alone enables the compiler's size-directed inlining; the LOD function
retains its explicit noinline boundary. Flags, exact compiler command,
map/symbol/disassembly and 93 input hashes are in the build identity. The
ordinary successor latest-source rebuild remains byte-identical at `cf605bd3...`.
Passing `ec259fc7...`, corrected `0d96a1b...`, six-order `c249f4e4...` and all
preceding immutable evidence manifests are preserved.
The preceding integrated PRG `1ab31a8a...` (37560 bytes, 122 bytes free), exact
89-input build and passing direct NTSC/PAL traces are also retained. They
establish the pre-refresh presentation/timing checkpoint, not a carrier pass.

Trace version 5 uses 92-byte tick records and 16-byte world events. It removes
only the tick record's duplicated swap timestamp, retaining the timestamp in
the append-only event log, and adds bound registration evidence. Maximum 2000
events still yields 327172 bytes within `$08030000-$0807FFFF` (327680 bytes).
Overflow rejects acquisition; no event is dropped or saturated. The allocation
bound is not a production capacity or rate claim. Generated trace and private
scene bindings are regenerated from their JSON authorities.

## Fresh direct-entry timing evidence

Both runs used the unchanged passing PRG and 120-second allowance, unique
token-only local fixtures, actual disk extraction and an independent
chain/BAM/content check. Status 4, error 0 and all 19 closed chunks pass.

| Mode / run | Trace bytes | Complete pairs | Nominal misses / uncertain / below-20Hz cohorts | Requests / cancels | Anchor drops |
| --- | ---: | ---: | --- | --- | ---: |
| NTSC `presentation-ntsc-04` | 310468 | 956 | 0 / 0 / 0 | 25 / 25 | 1946 |
| PAL `presentation-pal-02` | 308084 | 807 | 0 / 0 / 0 | 25 / 25 | 1662 |

Both epochs/modes have service-start masks FFFF and completed-order masks 3F.
Both views and tiers occur; actual anchor/column high-water is 4/4. Exact model
lineage remains `6B765FDB` at 1600 and `607348BD` at 3200; actual returning
SAVE, context invalidation, reserve CRC and resumed-service mask pass. IRQ
samples are NTSC 806/804 and PAL 702/721, with all body-read intervals still
zero at this Xemu resolution. This is unresolved, not a zero-cost IRQ claim.
Whole ISR/entry latency and traceable physical SI uncertainty remain open.

NTSC trace SHA-256:
`ec5770073637ec6acf84842b002f93ee3b91d1b36202663a47b720d12f397e7c`.
PAL trace SHA-256:
`ce3c4edb022323478cc9e5302cfb59fd92159fa3c4f193431cd9643bce01bfac`.
All 30 repaired-CRC corruption cases reject against each actual trace.

## Local carrier gate

Replacement candidate `R0FG1P02.D81`, 819200 bytes, SHA-256
`60cea9c8dd51b0f2c199605e60574c0bebd7c758d5899fb9b1e7c2901f83e832`
was fresh-formatted and populated in one pinned c1541 session. Independent
structure, directory/BAM/chains and extraction of AUTOBOOT.C65, R0FSUCC and
TOKEN pass. The canonical is read-only and never mounted writable.

The existing admitted carrier bootstrap is reused with only its final jump
derived from the current linked `_start` (`$30B1`), replacing the old successor
entry `$2B07`. Generated source, stage, tokenized boot and exact bytes are
retained. Five carrier host tests reject names, failed/inconclusive timing
admission, construction after failed admission and retired candidate reuse;
structural gate failure retires the identity automatically. Four terminal
boundary tests reject return, application calls and wrong refresh/SAVE order.
Boot validation shares the
direct-entry actual-export reducer, rather than duplicating that pipeline.

All four fresh exact-name autoload copies pass, with no PRG injection:

| Clean boot | Actual trace bytes / pairs | Nominal misses / uncertain / below-floor cohorts | SAVE / structure / original payloads |
| --- | --- | --- | --- |
| NTSC 01 | 310468 / 956 | 0 / 0 / 0 | PASS / PASS / unchanged |
| NTSC 02 | 310468 / 956 | 0 / 0 / 0 | PASS / PASS / unchanged |
| PAL 01 | 308084 / 807 | 0 / 0 / 0 | PASS / PASS / unchanged |
| PAL 02 | 308084 / 807 | 0 / 0 / 0 | PASS / PASS / unchanged |

Each run used a unique exact-name writable copy of the unchanged read-only
canonical, its own disposable virtual-SD fixture, a 120-second allowance,
actual exported data and independent reduction. Every tick, closed chunk,
complete registration pair, actual returning SAVE, directory/BAM/chain and
original AUTOBOOT/R0FSUCC/TOKEN payload validates. Individual mutated-image
and trace hashes are in each run's `validation.json` and `carrier-summary.json`.
The passing NTSC carrier trace also rejects all 30 corruption cases.
The canonical is now **XEMU_BOOT_VERIFIED only**, not hardware-loadable or
test-eligible. No SD copy/allocation, physical chooser/entry or physical
runtime gate has run.

## Validation commands

```sh
python3 -B tools/diagnostics/r0f_group1_scene_validate.py
python3 -B tools/diagnostics/r0f_group1_host_validate.py
python3 -B tools/diagnostics/r0f_group1_integration.py
python3 -B -m unittest discover -s tools/diagnostics -p 'test_r0f_group1_carrier.py' -v
python3 -B -m unittest discover -s tools/diagnostics -p 'test_r0f_group1_terminal.py' -v
python3 -B tools/diagnostics/r0f_group1_export_probe.py build --build-dir build/r0f/group1/cache-refresh-probe
python3 -B tools/diagnostics/r0f_group1_export_probe.py run --out build/r0f/group1/cache-refresh-probe/ntsc-autoload-01 --build-dir build/r0f/group1/cache-refresh-probe --mode 1 --case normal --timeout-seconds 60 --carrier-boot
python3 -B tools/diagnostics/r0f_group1_export_probe.py build --build-dir build/r0f/group1/cache-refresh-negative-probe
python3 -B tools/diagnostics/r0f_group1_export_probe.py run --out build/r0f/group1/cache-refresh-negative-probe/ntsc-open-failure-01 --build-dir build/r0f/group1/cache-refresh-negative-probe --mode 1 --case initialize-error --timeout-seconds 60 --carrier-boot
python3 -B tools/diagnostics/r0f_group1_run.py --out build/r0f/group1/integration/presentation-ntsc-04 --mode 1 --timeout-seconds 120
python3 -B tools/diagnostics/r0f_group1_run.py --out build/r0f/group1/integration/presentation-pal-02 --mode 0 --timeout-seconds 120
python3 -B tools/diagnostics/test_r0f_group1_reduce.py build/r0f/group1/integration/presentation-ntsc-04/trace.bin
python3 -B tools/diagnostics/test_r0f_group1_reduce.py build/r0f/group1/integration/presentation-pal-02/trace.bin
python3 -B tools/diagnostics/r0f_group1_carrier.py build --name R0FG1P02.D81 --ntsc build/r0f/group1/integration/presentation-ntsc-04 --pal build/r0f/group1/integration/presentation-pal-02
python3 -B tools/diagnostics/r0f_group1_carrier.py boot --name R0FG1P02.D81 --mode 1 --number 1
python3 -B tools/diagnostics/r0f_group1_carrier.py boot --name R0FG1P02.D81 --mode 1 --number 2
python3 -B tools/diagnostics/r0f_group1_carrier.py boot --name R0FG1P02.D81 --mode 0 --number 1
python3 -B tools/diagnostics/r0f_group1_carrier.py boot --name R0FG1P02.D81 --mode 0 --number 2
python3 -B tools/diagnostics/r0f_group1_carrier.py finish --name R0FG1P02.D81
python3 -B tools/diagnostics/test_r0f_group1_reduce.py build/r0f/group1/carriers/R0FG1P02/ntsc-01/trace.bin
python3 -B -m unittest discover -s tools/diagnostics -p 'test_r0f_group1_*.py' -v
python3 -B tools/diagnostics/r0f_group1_export_probe.py build --build-dir build/r0f/group1/cache-refresh-collision-probe
python3 -B tools/diagnostics/r0f_group1_export_probe.py run --out build/r0f/group1/cache-refresh-collision-probe/pal-existing-01 --build-dir build/r0f/group1/cache-refresh-collision-probe --mode 0 --case existing --timeout-seconds 60 --carrier-boot
```

All listed completed commands exit 0. The retired first-carrier boot command
`r0f_group1_carrier.py boot --name R0FG1P01.D81 --mode 1 --number 1`
exited 1 at independent directory/chain validation. Failed target fits were
never executed. Probe tool versions/source hashes are frozen separately;
their exact snapshots are verified against their own build identities.
Scene validation compares 3200 actual C encodings
with an independent rank/enumeration oracle under ASan/UBSan, and reruns the
720 anchor permutations, 2592 clipping cases, 131072 LOD comparisons and
coherence/overflow corpus. Thirteen private-contract tests pass. Target build
passes resident/protected/terminal/IRQ static gates. No 180/360-second run was
used. A compile check caught an unused legacy-only loop variable during the
split; it is now excluded in this variant and strict warnings pass. The final
combined host suite passes 30 tests. The preservation audit checks all 248
entries of the preceding four immutable manifests, plus exact `ec259fc7...`
and `c249f4e4...` PRGs. Latest ordinary successor source compiles into a
separate `ordinary-preservation-final/` output and matches `cf605bd3...`
byte-for-byte; no predecessor carrier is rebuilt or retested.

The final freeze audit reruns all 30 host tests, independently recomputes all
six corrected direct/carrier reductions with their actual SAVE, and repeats
the three 30-case corruption suites. It verifies all 93 current build inputs,
95 final source inputs, exact historical probe snapshots, all 248 preceding
manifest entries, protected PRGs and both retired-carrier hashes. Exact audit
commands/results are in the new freeze's `validation.json`; `sha256.json`
covers every retained file except itself. This freezes evidence only, not a
commit or a release.

## Changed paths and retained evidence

- `successor_integration.c`: private incremental display integration, view
  cancellation, ROM-restoration fallback, observation hooks and Group 1-only
  staging/pointer behavior; ordinary successor bytes preserved.
- `group1_presentation.c`, `group1_scene.c/.h`: pure bound policy and private
  scene construction/encoding, with target-safe LOD call boundary.
- `group1_capture.c/.h`, trace/presentation JSON contracts, their generators
  and generated bindings: versioned observations, fixed-width encoding,
  high-water and independent per-pair evidence within the admitted allocation.
- `group1_terminal_export_45gs02.s`: public terminal DOS initialization and
  protected shared parameter setup; original returning trampoline unchanged.
- Group 1 builder/runner/reducer/scene tests, export probe and carrier tools:
  target fit, exact source/artifact identity, independent scene/trace checking,
  shared bootstrap, short normal/error qualification and fail-closed retirement.
- Measurement matrix, WIP and reports: explicit current coverage and next
  action; no production contract or acceptance promotion.

The [new evidence freeze](../evidence/r0f/group1/2026-09-30-presentation-integration/README.md)
retains 95 exact final inputs, linked artifacts, actual direct/carrier data,
failed builds/PRGs/images, probe tool versions and authoritative checkpoints.
Large disposable virtual-SD clones are excluded; their hashes/paths stay in
execution identities. Canonical and failed carrier files remain unchanged.

## Contract/hardware impact and remaining gates

C ABI clobbers are compiler-managed. CPU-visible new state is charged only to
the admitted resident envelope; software stack remains `$C000-$CFFF`, B=2 and
MAP/base-page rules unchanged. Existing VIC pointer/config registers, flat-copy
ABI, synchronous application DMA list at `$056000-$056010`, ROM/display stores
`$020000-$03FFFF`, staging workspace and CIA reader/restart owners are reused.
No new physical allocation or reserve write occurs. No IRQ reads presentation
state or calls C; NMI lockout is unchanged. The canonical-entry bootstrap keeps
the existing KERNAL LOAD/MAP/B restoration behavior. Terminal export retains
its separate no-return capsule and dead-resident staging lifetime. The added
OPEN/CLOSE public calls run only in exclusive terminal KERNAL ownership with
B=0 and its existing ROM map, after acquisition/IRQ/audio/display/DMA stop.
All CPU register/status and page-1 clobbers remain terminal-owned. No new
acquisition hardware register or IRQ/NMI change accompanies the DOS refresh;
the command refreshes only the disposable local device-8 fixture.

These results establish this bounded integrated fixture, not all current-parent
graphics requirements. Directional angle hysteresis, projection/terrain/carrier
visual registration, geometry/audio/sensor pool coverage, integrated
near-capacity trace and compact operator summary remain open. Sampled phase
coverage is not exhaustive independent relative-phase or external latency
proof. Complete these local coverage gates before proposing SD/physical
testing; separate owner approval and all physical carrier gates are still
required. Groups 2/3 and R0-F acceptance remain separate.
