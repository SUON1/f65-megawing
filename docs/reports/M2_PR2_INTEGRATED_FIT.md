# M2 PR2 integrated-fit gate

**READY FOR REVIEW — failed fit gate; PR2 renderer not implemented.**
Baseline main `a9d3f796291f2941002b4d1f4c8fc48a9dba3c89`;
branch `codex/65aero-m2-pr2-integration`.
[Fresh evidence](../evidence/flight-demo/2026-10-20-m2-pr2-fit/README.md).

## Authority and clarified display scope

Founder approved D2–D7 of the [PR2 Build Intent](../plans/65AERO_M2_PR2_BUILD_INTENT.md)
and changed D1 to high-resolution output, 720×480 or 720×572 PAL. On identifying
that native 8-bit images would exceed the approved 64 KiB per display bank,
the founder explicitly selected: **keep the approved lower-resolution backing
image, scaled within a high-resolution output**. This supersedes D1's output
interpretation without changing the approved backing layout, logical PR1
projection, memory ownership or acceptance tolerances. The original plan remains
unchanged provenance; its pending-status wording predates this authorization.

Do not silently substitute PAL 576 for the requested 572 or claim a hardware
output mapping already exists. Exact active-area/border/aspect/scale and mode
register admission remain unimplemented. They need source-grounded validation
before display activation; no execution was authorized. D5 requires stopping
on failed fit without enlarging the allocation. D6 permits host/oracle and
compile/link/static checks only. Publication remains unauthorized.

## Integrated preflight and actual result

Command: `python3 -B tools/flight_demo/m2_pr2/fit.py`.
Output: `build/flight-demo/m2-pr2-fit-1792542030866784000/`.
Compiler/linker succeeded (exit 0); the fit gate returned **exit 1 / FAIL**.

The new compile-only probe links actual unchanged M1 Core/Input/Presentation,
the narrow M1 Platform initialization/clock/input/fault/stack-measure lifecycle,
and corrected PR1 Environment/Graphics/generated table. It excludes both old
entry points, the M1 renderer and display activation. Outputs are consumed to
prevent dead-code elimination. The current PR1 raster API's 320-point array is
explicitly retained and charged at 1,280 bytes. This is an initial reachability
measurement, not the final resumable renderer or full scheduling composition.

| Section | Start | Bytes |
|---|---|---:|
| text | `$2017` | 26,255 |
| read-only data | `$86A8` | 847 |
| initialized data | `$89F7` | 22 |
| BSS | `$8A0D` | 2,119 |
| compiler static scratch | `$9254` | 225 |

Resident end is **`$9335`**, **4,917 bytes above `$8000`**, before the new renderer,
font, camera-command integration and display contract. There is a two-byte
alignment gap before read-only data. Text alone ends at `$86A6`, already 1,702
bytes beyond the ceiling. Removing the entire 1,280-byte raster array alone
would still leave 3,637 bytes excess, assuming everything else unchanged; that
is arithmetic, not a tested optimized link.

The largest text symbol is compiler-inlined `main` (13,141 bytes), followed by
`m2_transform` (4,649), `interpolate_delta` (1,487), `cfcopy` (1,150) and
`plane_distance` (982). Inlining prevents attributing all main bytes to one owner;
these figures guide investigation, not an assurance of attainable savings.
Static compiler scratch is charged once in `.noinit`; no integrated dynamic
stack or exercised high-water PASS is claimed. Full ABI/stack/service/scanout
admission stops at the earlier failed size gate. The generated PRG is a failed
compile-only candidate, never an executable-admitted deliverable.

## Host/oracle and standalone target regression

Command: `python3 -B tools/flight_demo/m2/build.py`.
Fresh output: `build/flight-demo/m2-pr1-1792542041697467000/`.
This reruns the unchanged PR1 baseline, **not a completed PR2 renderer**.

- Five contract tests PASS.
- ASan/UBSan host/replay checks PASS, checkpoint `DE675132`.
- 3,857 independent Decimal cases PASS, maximum endpoint error
  0.000021224219 logical pixel; raster distance within one pixel.
- 841 near/far regressions PASS, also through the sanitizer runner; maximum
  error 0.035136325 pixel. The reported clipping case remains corrected.
- Standalone PR1 target compile/link/static PASS, resident end `$7466`, hardware
  stack bound 25 bytes, dynamic software bound 16 bytes, static scratch 471 bytes.
  These standalone bounds do not apply to the failed integrated candidate.

No existing source, generated header/table/ledger or historical evidence was
changed. New work is the compile-only fit probe/tool, this report and new packet,
plus WIP. The earlier uncommitted planning document remains present unchanged.
All 790 planning-baseline fingerprints and 20 unrelated entries were verified.
No new register behavior, physical allocation, DMA, MAP/base-page operation,
IRQ/NMI handler, serialized state or timing allowance was introduced. The probe
links the existing B=`$02`/MAP-clear reset-only seam but does not execute it.

## Recommendation and stop

Keep the clarified D1 scaled-output choice and D2/D5 memory ceilings. Review a
bounded size-reduction step before renderer integration: first investigate
prepared-transform reuse and inlining/code duplication, then replace the full
raster-output array with a proved streaming cursor. Preserve Q24/Q46 precision,
independent oracle and old API behavior; measure each change with a fresh link.
Even eliminating the array cannot alone close the deficit. Do not assume these
optimizations will suffice or promise the full renderer fits.

If acceptable implementation cannot close the ledger, return for an explicit
allocation/architecture decision. No automatic reserve use, other-owner memory,
assembly rewrite, precision reduction or relaxed service criteria. The build
has reached the approved failure stop, not PR2 completion or visual acceptance.
No Xemu, D81, SD or physical testing; no commit, push, PR or merge.
