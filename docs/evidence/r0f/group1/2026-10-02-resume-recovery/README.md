# Group 1 resume recovery evidence — 2026-10-02

Local fit, native and exact-carrier Xemu gates PASS. Physical verification
and Group 1/R0-F acceptance remain outstanding; P05 remains retired.
See [the review report](../../../../reports/R0-F_GROUP1_RESUME_RECOVERY.md).

- `source/`: exact changed C source. The other 133 source inputs come from the
  immutable P05 version-7 snapshot identified in `experiment/runtime-01/build.json`.
- `experiment/`: fit, PRG/disassembly, native checks, source identities,
  patch replay, preservation audit and reviewed restart ordering.
- `focused/`: fresh NTSC/PAL acquisition and expected export-collision failure.
- `carrier/`: canonical payloads and four clean exact-name P06 boots, actual
  extracted SAVE/chunks, traces, reductions, full-capacity checks and screens.
- `prior-attempts/`: malformed preparation/unchanged compile, non-fitting first
  variant, and sandbox launch without target evidence. None is a passing run.
- `checkpoint/`: review-time tools, report and WIP.
- `local-images.json`: exact paths/hashes of raw D81s retained in ignored
  `build/`. Those images, whitespace-bearing raw text outputs and disposable SD fixtures
  are not copied here; their originals remain unchanged in build.
  No new D81 tracking exception or publication approval is implied.
- `sha256.json`: packet integrity manifest, excluding itself.

Absolute paths and commands retain original execution provenance. The full
live qualified source is in `build/r0f/group1/resume-recovery/clock-03-execution/source-inputs/`.
The target patch applies to the frozen P05 snapshot, never the earlier root
working source. No SD transfer or physical hardware run occurred.
