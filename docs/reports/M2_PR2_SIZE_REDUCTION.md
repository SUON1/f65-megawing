# M2 PR2 bounded size reductions

**READY FOR REVIEW — provisional integrated size check now passes.**
This does not complete PR2, admit target execution or establish full-renderer fit.
Baseline `a9d3f796291f2941002b4d1f4c8fc48a9dba3c89`, branch
`codex/65aero-m2-pr2-integration`. Founder authorized bounded size reductions,
host/oracle and integrated compile/link checks, preserving precision and limits.
The [failed fit report](M2_PR2_INTEGRATED_FIT.md) and its evidence remain unchanged.
[New evidence packet](../evidence/flight-demo/2026-10-20-m2-pr2-size-reduction/README.md).

## Changes and measured effect

The integrated probe uses `-Oz -fno-inline-functions` with the same pinned
LLVM-MOS compiler, CPU, zero-page and jump-table settings. Measurements on the
unchanged pre-reduction probe isolate the compiler-policy effect:

| Probe/profile | Resident end | Margin below `$8000` |
|---|---|---:|
| Original `-Os` | `$9335` | -4,917 bytes |
| Original `-Oz` | `$8594` | -1,428 bytes |
| Original `-Oz -fno-inline-functions` | `$8311` | -785 bytes |
| Streaming probe, `-Oz -fno-inline-functions` | **`$7E85`** | **379 bytes** |

The equivalent `-fno-inline` experiment also ended at `$8311`; it is retained,
not used as a second independent success. Raw experiments and commands are
preserved. Size settings apply to the integrated probe; the original PR1
standalone builder retains `-Os` for regression comparability.

Graphics now owns a private resumable Bresenham cursor. `m2_raster_begin`
validates the line and initializes its bounded state; `m2_raster_next` emits at
most one pixel without a loop. Exhaustion leaves the cursor exhausted and output
unchanged. Invalid begin leaves the old cursor unchanged, and the caller must
not consume a failed attempt. Callers may pause/interleave independent cursors
or replace a successfully initialized cursor when cancelling prior work.
The cursor is exclusive transient implementation workspace, not a serialized
record, public layout contract or WorldRegistrationRecord extension.

The existing `m2_raster_line` API delegates to that same implementation and
preserves its capacity-failure/output/count behavior. The integrated probe
consumes every streamed pixel and the count; it cannot discard output as dead
work. Its old 1,280-byte array is replaced by a **16-byte cursor + 4-byte pixel**,
verified in the target symbols (the compiler splits the cursor into eight
2-byte symbols). No second raster algorithm or hand-copied generated layout.

Total resident reduction is **5,296 bytes**. The final map is:

| Section | Start | Bytes |
|---|---|---:|
| text | `$2017` | 22,093 |
| read-only data | `$7668` | 848 |
| initialized data | `$79B8` | 22 |
| BSS | `$79CE` | 859 |
| static compiler scratch | `$7D29` | 348 |

Text ends at `$7664`; the four-byte alignment gap is included in resident extent.
Static `.noinit` scratch is counted once, not double-charged as dynamic stack.
The increase in this scratch under the new compiler policy is included.
Target SHA-256: `19524fd973f1011c6264df2820d7a032615defa97b9b95a44adf0478263695a9`.
No full integrated dynamic-stack or cycle bound is claimed. Disabling inlining
may increase call/return cost; size improvement does not establish throughput.

## Precision, contracts and hardware

Q24 clipping, Q46 rotation, projection, horizon, registration validation,
fixture and camera limits are unchanged. Numeric source before the raster
implementation and after it was compared byte-for-byte to the preserved source.
Generated header, table, schema and memory ledgers are unchanged. The original
0.5-pixel projection and one-pixel raster limits are not relaxed.

No new registers/clobber conventions, physical allocations, MAP/base-page,
DMA, IRQ/NMI behavior or persistent state. The existing reset-only M1 Platform
seam is linked but not executed. No reserve draw or owner-band reassignment.
The `$8000` resident limit and `$C000–$CFFF` software-stack envelope remain.
Full helper ABI/stack/cycle and scanout admission remain later gates.

Only Graphics raster code/header/private workspace, the integrated fit probe
and builder, new cursor host checks, and the PR1 builder's input-hash list change.
The latter now includes the private header so the evidence binds all new inputs.
Prepared-transform caching was not added in this bounded change: the size gate
was closed with compiler policy and streaming. It remains required engineering
for the future renderer; do not recompute a transform per background pixel.

## Actual validation

`python3 -B tools/flight_demo/m2_pr2/fit.py`:
`build/flight-demo/m2-pr2-fit-1792542725786099000/`.

- Cursor ASan/UBSan host checks PASS: explicit pixel sequence, pause/interleaving,
  restart, null/invalid inputs, output preservation and stable exhaustion.
- Integrated compile/link and resident-range checks PASS at `$7E85`.
- Stack-envelope declaration, expected entry seams and no direct ROM calls PASS.
- Batch raster array/function absent from the integrated target; every streamed
  pixel is consumed. This is provisional reachability/static evidence only.

`python3 -B tools/flight_demo/m2/build.py`:
`build/flight-demo/m2-pr1-1792542572158454000/`.

- Five contract tests, original host/sanitizer replay checks PASS; `DE675132`.
- Unchanged independent Decimal oracle: **3,857 cases PASS**, maximum projection
  error 0.000021224219 pixel, raster error within one pixel. This exercises the
  batch wrapper over the same cursor, not a separate untested raster path.
- **841 near/far cases PASS**, including sanitizer vectors; maximum new-suite
  error 0.035136325 pixel, identical to the prior result.
- Standalone `-Os` target compile/link/static PASS: end `$748E`, 25-byte hardware
  and 16-byte dynamic software stack bounds, 471-byte compiler static scratch.
  Those stack figures belong only to the standalone PR1 probe.

Corpus/ledger scope validator and whitespace checks PASS. Three intentionally
changed files from the earlier 790-file baseline have archived original-byte
snapshots; the other **787 current fingerprints**, all historical packet
inventories and all **20 unrelated entries** remain unchanged. Prior failed
links and both earlier reports are retained. New evidence has its own inventory.

## Stop and recommendation

The bounded size-reduction task is complete at READY FOR REVIEW. Review the
compiler policy, cursor behavior and 379-byte margin before continuing PR2.
That margin is not a budget claim for the full renderer, font, camera commands,
registration bundles or scanout integration. Gate B, integrated stack/service
proof and exact high-resolution output mapping remain open. Retain the approved
low-resolution backing image scaled within high-resolution output; no native
large framebuffer or new display allocation was introduced.

No Xemu, D81, SD or physical testing. No commit, push, PR or merge. Do not infer
PR2/M2 visual acceptance or full integrated runtime admission from this fit.
