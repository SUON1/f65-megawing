# M2 PR2 renderer fit — failed gate

**BLOCKED — early renderer fit FAIL. Implementation stopped under F2/F6.**
Baseline: `8ee5214ea9c63b86e92ca9bc4fa0779115dbd57f` (PR #21).
Branch: `codex/65aero-m2-pr2-renderer-fit`.
The founder approved F1–F6 of the [Build Intent](../plans/65AERO_M2_PR2_RENDERER_ADMISSION_BUILD_INTENT.md).
[Retained evidence](../evidence/flight-demo/2026-10-21-m2-renderer-fit/README.md).
The planning document retains its original pending wording; this task records
the subsequent approval without rewriting that historical artifact.

## Outcome and gate disposition

The early real-renderer target compiles and links, but resident extent reaches
**`$A41F`**, **9,247 bytes above `$8000`**. No ceiling, precision, protected
reserve or owner allocation was relaxed. The oversized artifact is rejected;
its linker placement is diagnostic evidence, not an admitted allocation.
The compiler's default link success does not enforce the project ceiling.

| Gate | Actual result |
|---|---|
| Existing geometry contracts/host/oracle/standalone target | PASS at their stated tiers |
| New renderer host checks | PASS bounded five-pose, transaction, camera, ranking and replay checks; broader full-composition correctness is not claimed |
| Early renderer target compile/link | PASS compiler/linker; opaque test backend only |
| Early renderer resident fit | FAIL, `$A41F` end, 9,247-byte excess |
| Full target adapter/normal and stress variant fit | NOT REACHED |
| Integrated stack/ABI and service bounds | UNPROVEN; not reached |
| Display mapping/activation contract | NOT STARTED |
| Execution, real scanout, visual acceptance, physical proof | NOT RUN |

The complete Graphics tile path, font, telemetry, camera controls and state were
linked early. The root uses mutable semantic camera input through a separately
compiled non-LTO test backend, so LTO cannot replace it with a fixed camera.
This is explicitly an intermediate renderer link, not the actual display adapter
or an execution-ready program. It has no new display-mode/register implementation.

## Changes and responsibilities

- `src/graphics/m2_renderer.[ch]`: private Graphics state, both generated bundles,
  captured prepared context/snapshot, one tile, cursor/line, text/counters;
  full world/telemetry/footer construction, all canonical segments, protected
  corner anchors, equal-priority stable-ID optional labels, cancellation and
  synchronous hidden-store copy/activation seams. Inner registration revision 1
  and outer bundle revision 2 are checked separately.
- `src/graphics/m2_font.c`: original owned bitmap glyphs in 8×8 cells, shared by
  host and target; 472 actual target bytes. The two missing flight states remain
  NOT IMPLEMENTED; camera height is explicitly local test datum, counters hex.
- `src/diagnostics/m2/camera.[ch]`: requested camera, approved step sizes,
  envelope/revision rejection, opposite-step cancellation and reset precedence.
- `src/input/m2_camera_input.[ch]`: semantic press-edge extraction; no keyboard
  register mapping or authoritative aircraft state.
- `tests/flight_demo/m2_full/renderer_cases.json`, `renderer_host.c`: frozen
  analytic/text/transaction expectations and host checks/images.
- `tests/flight_demo/m2_full/fit_root.c`, `fit_backend.c`: compile-only early
  integration with existing Core/Input/Presentation and lifecycle seams. The
  backend's volatile mailbox/staging is charged test scaffolding; it neither
  initializes real display stores nor implements physical tile writes/scanout.
- `tools/flight_demo/m2_full/renderer_build.py`: fresh attempt directories,
  host/sanitizer checks, pinned compile/link and retained maps/symbols/disassembly.
  It reuses the existing pure/runtime source lists. Its post-link owner assertion
  failed on compiler scalarization/elimination; see the additive accounting below.

Existing geometry, generated interfaces, schemas, generators, numeric oracles,
platform code and historical evidence remain byte-identical. No changes to
Q12/Q24/Q46/Q16, clipping/raster tolerances or memory ledgers.

## Actual accounting

Read directly from the completed map, retained independently in `link-analysis.json`:

| Section | Start | Bytes | End exclusive |
|---|---|---:|---|
| BASIC header | `$2001` | 22 | `$2017` |
| text | `$2017` | 30,471 | `$971E` |
| alignment gap | `$971E` | 2 | `$9720` |
| read-only data | `$9720` | 1,505 | `$9D01` |
| initialized data | `$9D01` | 2 | `$9D03` |
| BSS | `$9D03` | 1,591 | `$A33A` |
| static compiler scratch | `$A33A` | 229 | `$A41F` |

Total resident span: 33,822 bytes versus 24,575 allowed. Static compiler scratch
is charged once in the span; dynamic software/hardware stack bounds remain
unproven for this root. Do not import the standalone probe's stack bounds.
The text section alone exceeds the entire resident allowance by 5,896 bytes;
removing data or backend staging alone cannot close this artifact's gap.

Actual symbols include Graphics renderer 834 bytes, font 472 bytes, Core 64,
snapshots 46, requested camera 22, previous camera keys 2 and `input.0` 1 byte.
Test-backend data totals 71 bytes (64 staging plus mailbox/status fields).
The unobserved `stages` array is eliminated; no array bytes are charged. This
is not proof of scheduler ordering or ABI readiness. Other platform/runtime
state, strings/tables and scratch remain included in the section totals.

No allocations were made in display slack, other-owner bands or reserve.
The approved two 63,552-byte stores, 2,000-byte shared Color RAM and all
stack/base-page ranges remain declarations for later actual adapter admission.
The host backend models tile storage only; it does not prove maps, palette or
Color RAM initialization or immutable resource behavior on target.

Target SHA-256:
`ac3f212bac05a58cbb994adc8c2ac52433e2667c2f60d1c0fcd7165306b748d3`.
Raw artifact: `build/flight-demo/m2-renderer-1792599384707283000/RENDER.prg`.
**Do not execute this oversized, unadmitted artifact.**

## Commands, results and retained failures

1. `python3 -B tools/flight_demo/m2_full/renderer_build.py`
   - Attempt `m2-renderer-1792599363333544000`: three contract tests and host
     ASan/UBSan PASS; backend compile rejected the LTO-only `-mlto-zp=0` option
     used with `-fno-lto`. This was an invocation error before the size gate.
     Exact original builder bytes and logs retained.
   - Corrected only that separate object's invocation; main target LTO policy,
     warnings and optimization flags remain unchanged.
   - Attempt `m2-renderer-1792599384707283000`: host checks, backend compile,
     target compile/link, disassembly and symbols succeed. Post-link report
     assertion fails because LTO names `input.0` and eliminates `stages`.
     Original `build.json` error retained. Additive `link-analysis.json` parses
     the completed map/symbols, charges actual symbols and records the size FAIL.
     No target rebuild or source optimization followed this failed fit.
2. `python3 -B tools/flight_demo/m2/build.py`
   - Fresh `m2-pr1-1792599368420594000`: PASS five contract tests,
     host/sanitizer/replay `DE675132`, 3,857 Decimal independent oracle cases,
     841 near/far cases and standalone target compile/link/static checks.
   - Maximum projection errors remain 0.000021224219 and 0.035136325 pixel;
     raster tolerance remains one pixel. Standalone resident end `$732A`;
     hardware bound 25, dynamic software bound 16, static scratch 443 bytes.
3. `git diff --check` and `python3 -B tools/diagnostics/r0a_validate.py .`:
   PASS. New packet hashes, input identities and preservation verified.

New host tests cover reset/all-sky/all-ground/bank/south views, every hidden tile
and blank footer, visible counters/missing-state strings, 24 label permutations,
held/opposite/reset camera commands and range/revision rejection, cancellation
at every declared construction/ready phase, copy/activation failures, stale
revision, outer composition mismatch and generation exhaustion. Replay checks
600 per-tick Core checksums during partial/cancelled construction, plus held/full
snapshot pool semantics. These do not yet establish completed-frame normal/slow/
fault replay, every possible injected failure, independent full-image oracle,
exact target scanout or throughput. Five native-resolution PPM images are host
output only; the reset image was inspected for full sky/ground and readable labels.

## Contract/hardware impact and remaining work

Pure C additions introduce no register writes, assembly clobber conventions,
MAP/base-page operations, DMA, IRQ/NMI handlers or persistent storage. Existing
platform lifecycle costs remain linked and unchanged. The early root has no
admitted scheduler return margin or safe activation window; it must not run.
The tile strategy replays segment projection/raster per world tile to retain a
single staging tile; its cost is unbounded for admission purposes until analysed.
Expensive prepare/anchor/text work is not yet split or deadline-admitted.

Stop here. No full-target adapter, hardware mapping research/implementation,
stack/ABI/service admission, stress target variants or further size reductions
were attempted after the failed fit. No Xemu, D81, SD, physical testing,
commit/push/PR/merge, aircraft behavior or later milestone.

Recommended next decision: authorize a focused **read-only size and service
feasibility review** of this exact linked artifact and renderer design before
approving another optimization increment. Identify actual call-graph and owner
costs, distinguish backend scaffolding from required platform work, and propose
a bounded pure-C strategy that preserves every requirement. Do not assume a
9,247-byte recovery is feasible, silently shrink behavior/precision or enlarge
the resident ceiling. Preserve this failure and the existing successful probe.
