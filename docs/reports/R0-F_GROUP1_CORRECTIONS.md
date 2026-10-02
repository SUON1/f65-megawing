# Group 1 correction checkpoint — 2026-09-29

The owner approved the terminal-export correction and required immediate DRY,
ETC (Easy to Change), and orthogonality. These corrections have host/static
and bounded development-Xemu evidence. The complete Group 1 diagnostic and
its delivery carrier are still in progress; this is not R0-F completion.

## Changes and ownership

- `docs/PROGRAMMING_PRINCIPLES.md` makes the three principles mandatory for
  new and materially changed programming, including R0 tests. AGENTS.md,
  the C standard and development workflow link it. Retained evidence is not
  a mass-refactoring target; independent oracles remain independent.
- `group1_timing.[ch]` owns pure release/deadline arithmetic;
  `group1_export.[ch]` owns a separate one-use export policy. Neither selects
  a workload or accesses hardware. A failed transport cannot rewrite the
  frozen acquisition CRC or length.
- The export contract owns constants and generates C/assembly bindings.
  The delta ledger admits a separate guarded context, bounded trace, retained
  DOS backup and terminal staging. Original T02 invalidation stays intact.
- Shared assembly includes own opaque-context capture and admitted KERNAL
  call mapping. The target compiler invocation is shared with the successor
  builder. The new host builder uses one pipeline for the two pure modules.
- The development probe adapter and protected terminal exporter qualify the
  transport independently of workload timing. Terminal export cannot return
  to C or resume measured work. It writes unique chunks without replacement.

Hardware/register/memory, MAP/base-page, stack, IRQ/NMI and DMA effects are
recorded in [the approved amendment](../plans/R0-F_GROUP1_EXPORT_AMENDMENT.md).
No resource or measured reserve bytes are used. Generated bindings are current.

## Validation performed

Commands are run from the repository root:

| Command | Actual result |
| --- | --- |
| `python3 -B tools/diagnostics/r0f_group1_build.py` | PASS: ASan/UBSan; one million independent release comparisons; deadline/uncertainty/wrap boundaries; 256 export-readiness combinations, bounded reads and one-use policy; pinned target-object builds |
| `python3 -B -m unittest discover -s tools/diagnostics -p test_r0f_group1_export_admission.py -v` | PASS: eight tests, including original lifecycle preservation, prohibited overlaps/reserves and unsupported copy geometry |
| `python3 -B tools/diagnostics/r0f_successor_integration.py build` | PASS: successor, IRQ, capture, CF001 and RH001 host/Java/static regressions |
| `python3 -B tools/diagnostics/r0f_group1_export_probe.py build` | PASS: target link, protected/staging bounds, pre-C ordering, terminal no-return/mapped-reference checks and ROM-call allowlist |
| `python3 -B tools/diagnostics/r0f_group1_export_probe.py run --out build/r0f/group1/export-probe/ntsc-02 --mode 1` | PASS: actual result/SAVE and three exported chunks |
| `python3 -B tools/diagnostics/r0f_group1_export_probe.py run --out build/r0f/group1/export-probe/pal-01 --mode 0` | PASS: same checks; Xemu log confirms PAL |
| `python3 -B tools/diagnostics/r0f_group1_export_probe.py run --out build/r0f/group1/export-probe/existing-01 --mode 1 --case existing` | PASS: existing G1T00 unchanged, zero chunks saved, terminal FAILED status 5/error 3, no retry or workload resumption |

Normal runs exported 33,025 bytes, CRC32 `F2CEE7CB`. The first 512 bytes are
the actual successor result; the remainder is a deterministic transport
pattern. Files were extracted using pinned c1541 and checked against the
independent directory/chain/BAM parser. Result semantics and actual RSSTATE
payload were validated. These are development direct-PRG runs on fresh
token-only images, not exact-name delivery boot gates or physical evidence.

The first sandboxed launch (`ntsc-01`) failed before runtime because Xemu could
not write its macOS config template. Its directory is retained. The permitted
retry used a separate fresh image. The first host-pipeline extension lacked
the generated-header include path; correcting that path made both modules
pass without changing target flags or code.

The three successful development runs inherited an old helper's branch label
in execution metadata. Their commit, PRG and results are retained. The runner
now resolves the actual branch and freezes build/input identity for future
runs. This metadata correction does not alter the target program.

## Identity and preservation

Export probe PRG: 27,892 bytes, SHA-256
`f1535ebb961b8c033a51548d468087e2c3b1a3b470763b15145ba392e3dc6a39`.
Protected end is `$3006`, below staging at `$4000`; resident end is `$9680`,
below `$C000`. Current build map, symbols, disassembly and input hashes are
under `build/r0f/group1/export-probe/`.

The predecessor PRG still has exact CAP13/CAP14 identity:
`cf605bd377ddcee2c72cdc4abfd20c3ae9eee350b7b78b36cbde8ff1adf8fc23`.
Independent before/after `.init.005` byte comparison also passed for the shared
capture refactor. All pre-existing retained evidence hashes match the
317-path prebuild manifest. Existing dirty source changes were preserved.
No SD write, tested-disk overwrite, physical rerun, commit or push occurred.

## Remaining work

Finish the requirement-to-case matrix, representative Group 1 workload,
timestamp/overhead calibration, bounded versioned recorder and independent
deadline/phase/window/world-age/high-water reduction, including the first
resumed tick and the post-storage interval. Qualify actual capsule corruption,
NMI and full-capacity transport cases with that integrated format; the host
readiness tests are not target fault-injection evidence. Then run the complete
fresh exact-carrier gates before proposing SD delivery. Groups 2 and 3 and
physical/owner acceptance remain separate. No further approval is needed to
continue the already authorized local Group 1 implementation.
