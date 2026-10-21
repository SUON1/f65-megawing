# M2 PR2 full-composition increment — prepared-context fit stop

**READY FOR REVIEW — stopped at a failed integrated regression gate.**
Full composition is not complete. Baseline main
`0d42a8ce271a98abbffada019c403e31e7590e5d`; branch
`codex/65aero-m2-pr2-full-composition`.
[Fresh evidence](../evidence/flight-demo/2026-10-21-m2-full-composition/README.md).

## Authority and completed scope

Founder approved N1–N6 of the
[full-composition intent](../plans/65AERO_M2_PR2_FULL_COMPOSITION_ADMISSION_INTENT.md),
including its failed-gate stop and host/oracle/compile-only boundary. N6 still
excludes Xemu. The planning file remains unchanged provenance. D1's clarified
lower-resolution backing scaled within the high-resolution output is retained;
no output mapping or register contract has been changed or admitted.

Added a distinct `65AERO-M2-FULL-1` source contract, generated header and owner
ledger. New `M2Anchor`/`M2Bundle` records reference existing generated PR1 types.
The bundle's outer composition revision 2 identifies the new full-display
profile; its nested PR1 record retains its original revision semantics. No
existing generated schema/header/table/ledger is changed. Source-hash admission
rejects any unreviewed contract drift before writes. Allocations remain two
63,552-byte display resources, immutable 2,000-byte Color RAM, unchanged CPU/
stack/base-page ranges and zero reserve. The ledger identifies required owner
classes; final object/asset sizes are still pending actual full composition.

Graphics adds a private prepared context containing a copied camera, its Q46
rotation and readiness state. Successful preparation validates and computes
once; private projection, horizon and registration helpers reuse it. The owner
must keep it immutable until cancellation/replacement; it is not a public input
record accepting arbitrary matrices. Failed preparation clears readiness so a
stale context cannot be consumed accidentally. The public legacy APIs retain
their signatures and output/failure behavior by preparing then delegating.
Geometry, Q24 clip arithmetic, Q46 transforms, rounding, fixture/query ownership,
projection bounds and acceptance limits are preserved. The build evidence now
hashes the additional private header.

No renderer/font/camera-command/platform-display code was added after the
failed regression. No existing R0/M1 source was modified. The new code does not
write hardware registers or change clobber conventions, physical allocation,
MAP/base-page, DMA, IRQ/NMI or serialized state. Runtime costs remain unadmitted.

## Validation and the exact stop

The geometry refactor was checked before dependent renderer implementation.

1. `python3 -B tools/flight_demo/m2/build.py` — PASS.
   Fresh output `build/flight-demo/m2-pr1-1792582284356607000/`.
   Five contract tests, original ASan/UBSan/replay checks (`DE675132`), 3,857
   independent Decimal oracle cases and 841 near/far regressions all pass.
   Maximum endpoint errors remain 0.000021224219 and 0.035136325 pixel respectively;
   raster error remains within one logical pixel. Standalone target compile/link/
   static passes at `$7356`; hardware/dynamic software stack bounds 25/16 bytes,
   compiler static scratch 511 bytes. These are standalone probe results only.
2. `python3 -B tools/flight_demo/m2_pr2/fit.py` — **FAIL, exit 1**.
   Fresh output `build/flight-demo/m2-pr2-fit-1792582301133356000/`.
   Cursor sanitizer checks and target compiler/linker pass; resident admission
   fails at **`$8014`, 20 bytes over `$8000`**. Other existing provisional checks
   pass. No check was bypassed and no memory limit was raised.
3. Independent follow-up checks on already-written code: three new contract
   tests PASS (generated identity, drift rejection, resource/mapping arithmetic).
   Prepared-context ASan/UBSan checks PASS on 3,672 segment comparisons across
   216 poses, reused horizon samples, captured-camera lifetime, registration
   identity, invalidation and output preservation. These equivalence tests
   supplement the independent oracle; they are not a replacement for it.
   Exact compiler/run commands are in `prepared-commands.json`.
4. Generated PR2 header compiles under the target compiler with warnings-as-errors
   in an include-only syntax check. No target execution. Whitespace and corpus/
   ledger scope checks pass.

### Failed integrated candidate accounting

| Section | Start | Bytes |
|---|---|---:|
| text | `$2017` | 22,564 |
| read-only data | `$7840` | 848 |
| initialized data | `$7B90` | 22 |
| BSS | `$7BA6` | 859 |
| static compiler scratch | `$7F01` | 275 |

Text ends at `$783B`, followed by five bytes alignment. Resident end is `$8014`.
The prior reviewed probe ended at `$7E85`: this regression adds 399 resident
bytes, exhausting its 379-byte margin. Static scratch is included once, not
counted again as dynamic stack. Failed PRG SHA-256:
`09cefa1a8326cd055e99334b1c4f0f30c17d32233f715376f126e45fdfb63425`.

This target remains the existing reachability regression probe, using legacy
wrappers that now prepare contexts. It is **not** the planned final renderer
root using one prepared context for the whole generation. Its failure is a real
regression under the current gate, not proof that every prepared-context design
or full composition is infeasible. The next step must make that distinction
explicit; do not hide the failed result by replacing its evidence with a later
probe. Integrated dynamic stack, runtime ABI/service and display admission were
not completed past this failure.

## Gate disposition

| Gate | Status |
|---|---|
| 1: complete owner/state contract | PARTIAL: generated composition records, ranges, owner classes and rejection checks exist; final renderer/font/state bill of materials is not implemented or measured |
| 2: full host renderer | PARTIAL: prepared geometry passes oracle/equivalence checks; complete renderer, telemetry, ranking, cancellation and camera integration remain unbuilt |
| Integrated regression prerequisite | FAIL: resident end `$8014`, 20-byte excess |
| 3: actual full-composition link/ABI/service | NOT REACHED; the failed target is the earlier regression probe |
| 4: display/scanout contract | NOT REACHED; no device code, mode table or activation |
| Execution/visual acceptance | NOT RUN / NOT ADMITTED |

## Preservation and recommendation

All earlier evidence inventories remain byte-identical. Of the 846 captured
baseline files, 844 remain unchanged in place; the two authorized changed files
(`m2_geometry.c`, PR1 build input list) have original-byte snapshots in this new
packet. All 20 unrelated entries are untouched. Original planning/report status
wording and every previous failed/successful output remain preserved.

Review this failed prerequisite before proceeding. A bounded next proposal is
to measure the generation-owned prepared path in a truthful integration root,
while retaining the legacy-path regression as a distinct result. If a legacy
regression must itself fit, explicitly optimize/relink that path under the same
limits. Neither choice establishes room for the final renderer, font or service
logic. Do not add memory, reduce precision or silently redefine a passing gate.

Stopped under the approved failure condition. No Xemu, D81, SD or physical
testing, commit, push, PR or merge. No full-composition completion claim.
