# M1 focused P2 corrections

Authority: founder direction to fix the three review findings on the current M1 branch, preserve historical evidence and unrelated paths, rerun affected checks, and stop at READY FOR REVIEW. The original [M1 Build Intent](../plans/65AERO_PHASE1_ENTRY_AND_DEVELOPER_FLIGHT_PLAN.md#8-next-fresh-window-m1-first-pr-build-intent) and adopted authorities remain governing. No new public ABI or production owner is introduced.

The original [M1 report](M1_VISIBLE_FOUNDATION.md), its retained evidence packet, and all previous `build/flight-demo/m1/` outputs are preserved unchanged. This correction uses development identity `65AERO-M1-DEV-2` and fresh `build/flight-demo/m1-p2/` outputs. The earlier report describes the pre-correction source; this report supplies the current contract corrections and validation.

## P2 closures

1. **Generated contract enforcement.** `tools/flight_demo/admission.py` rejects unsupported changes before either generated file is written. This is the approved fixed 100 Hz/21-stage/80×25 profile, not a newly configurable runtime. Admission binds physical allocations to unchanged generated CF001 constants, fixes the admitted CPU/stack/base-page envelope, and rejects changes to the render service bound or capacities. The clock uses `R0FC_CPU_HZ / M1_TICK_HZ`; map and stack checks consume schema bounds; screen-bank selection consumes generated display addresses; watermark arithmetic and decoding consume declared stack/result bounds. The generated ledger now derives its hardware stack, base page and result ranges from the schema instead of independent literals. Fixed-profile constraints are explicit admission restrictions, not silently competing configuration.
2. **Retained initialization accounting.** The schema and generated ledger record the CPU-visible write interval `$09E0–$0A14` (53 bytes, end-exclusive `$0A15`), owner/call chain, initialization lifetime and retained implementation SHA-256. Admission checks that source pin and derives the actual message interval from the unchanged `cfrom_begin` call to `cfline`. This dependency is deliberately retained and fully declared; R0 proof source is not edited. The helper also populates its private result block (ROM state/CRC and its historical storage-rejection marker); that bookkeeping is not M1 storage-test evidence. The old screen write precedes the first M1 display-store selection and cannot write the active M1 world/overlay stores.
3. **Graphics owns scene color policy.** Graphics declares overlay extent, horizon, scene palette and colors in one location. It produces bounded color rows and rejects invalid row requests without modifying the caller's buffer. Platform accepts those bytes and palette values, applying only bounded register/memory writes. The character renderer uses the same Graphics overlay constant. The red fatal-platform border remains a Platform fault indication, not scene policy.

## Hardware and ownership effects

CPU registers/clobbers, canonical B=`$02`, cleared MAP/EOM, local IRQ/NMI/vector ownership, CIA clock, flat-copy primitive and reset-only restoration behavior remain those in the inspected M1/CF001 contract. No new assembly, DMA list, interrupt work, audio or storage call is introduced. Code/data size changes are accounted by fresh maps. Color initialization still writes only 25×80 bytes at `$0FF80000`; the existing row buffer is reused before ticks begin. This removes the Platform-local color-policy buffer. The ROM backup range and display stores are unchanged; reserve allocation remains zero.

CoreRuntime, semantic Input and snapshot publication code are unchanged by these corrections. Presentation remains independent of the authoritative checksum. The fixed profile requires explicit re-admission if the retained platform or layout changes; updating a generated header alone does not grant authority to move memory or change timing.

## Validation

Commands:

```
python3 -B tools/flight_demo/build.py
python3 -B tools/flight_demo/xemu.py replay 0
python3 -B tools/flight_demo/xemu.py replay 1
python3 -B tools/flight_demo/xemu.py slow-render 0
python3 -B tools/flight_demo/xemu.py slow-render 1
```

The build includes five admission tests with mutation subtests for each declared allocation, each fixed runtime parameter, the startup interval and the retained source pin. Native ASan/UBSan tests add full-row color checks and invalid-row buffer preservation alongside the original deterministic replay/queue/snapshot/cancellation coverage. Generated files are compared with regeneration in a temporary directory. Xemu uses the previously authorized direct-PRG path with isolated preferences and disposable in-memory boot media; no D81, file-backed SD image, SD transfer/allocation or physical device testing.

**READY FOR REVIEW.** Five admission tests and sanitizer-backed host tests PASS; all three compile/link/map/disassembly profiles PASS. Four direct-PRG Xemu runs (PAL/NTSC, normal/slow render) PASS with checkpoint checksum `DE675132`. All four actual screenshots show complete sky/ground, readable counters and altitude/airspeed marked `NOT IMPLEMENTED`. Observed stack maxima are 31 hardware / 28 software bytes; these remain emulator observations, not physical limits.

The [correction evidence packet](../evidence/m1/2026-10-20-p2-corrections/README.md) records exact run identities, source manifests and screenshots. A 60-second NTSC onboarding failure is preserved as FAIL; the target had not loaded. Restoring the runner's 120-second window enabled subsequent validation. The earlier PAL pass is bound to the archived 60-second runner/manifest; target binaries match the current build exactly.

Independent checks verified all 56 current input hashes, all reported raw artifact hashes and symbol values, and the 53-byte retained startup screen-code write in each successful memory dump. Temporary regeneration matches both generated files byte-for-byte. All 417 historical/unrelated file hashes and all 20 unrelated untracked status entries match the pre-correction snapshot; retained R0 tracked paths have no diff. `python3 -B tools/diagnostics/r0a_validate.py .` and scoped whitespace/artifact checks PASS. No commit, push, PR or merge was performed. Recommended next action: review the three corrections and their new evidence.

### Linked memory accounting

| Profile | PRG bytes | Text | Read-only data | BSS + noinit | Resident end (exclusive) |
|---|---:|---:|---:|---:|---:|
| interactive | 9330 | 8847 | 459 | 820 | `$47A5` |
| replay | 9672 | 9189 | 459 | 820 | `$48FB` |
| slow-render | 9733 | 9250 | 459 | 820 | `$4938` |

Initialized data remains zero bytes. All target sections fit within the admitted resident envelope below `$8000`; the `$058000–$05FFFF` reserve remains untouched. Stack bounds remain 256 hardware / 4096 software bytes; observed usage is recorded separately with each run.
