# Group 2 target admission — blocked resident fit

The approved target-admission increment built a fresh copied-source G2-Q probe
on 2026-10-03. **Host probe PASS; resident fit FAIL.** No target execution,
Xemu, carrier construction, SD action, hardware test or publication occurred.

Command from repository root:

```sh
python3 -B tools/diagnostics/r0f_group2_target_admission.py
```

The runner intentionally exits 1 on fit failure. [Admission](admission.json)
retains exact commands, all copied input hashes and frozen-input preservation;
[summary](summary.json) records section deltas and PRG identity. Host compilation
used ASan/UBSan with non-recovering sanitizer failures and strict warnings.
[Host output](host-run.txt) proves the actual frozen event owner passes this
probe and that the original model and peer are restored byte-for-byte; a
nonempty model rejects before mutation. Existing passing suites were not rerun.

The full P09 command and workload are retained. One volatile admission-result
byte and a queue-probe call after initial model reset keep the new work live
under LTO. The probe saves 64 queue bytes on the C stack, fills the queue,
checks one-over/sticky rejection with model CRC, and restores temporary changes.
This is a minimal **pre-workload compile-only admission probe**, not complete
G2-Q coverage, combined-load injection or final case-result capture. Its result
byte is not wired to a runtime acceptance path; the image must never execute.
A fit pass alone would still not authorize execution of this admission image.

Baseline resident end `$BFF5`; candidate end `$C16F`. Growth is 378 bytes,
leaving **367 bytes over** the unchanged `$C000` ceiling. Protected section
is unchanged (4495 bytes). The minimal probe does not include G2-S/P/D/A/L,
invalid-ID target cases or suite result capture; this shortfall is not a final
full-suite size estimate. Link completion is not fit acceptance.

The complete frozen source comes from the retained build.json sourceRoot;
all baseline input hashes were checked before copying and afterward. The first
preparation attempt looked only in the checked-in packet and stopped on its
omitted local-only spec file before any compilation. The corrected runner
uses the complete hash-verified local snapshot. P09 and all older evidence
remain unchanged. The new copied source, binary and full map remain at the
source/output paths in these records; retained source delta and tooling are
included here with a SHA-256 manifest.

## Bounded remedy for owner review

The [Build Intent](../../../../plans/R0-F_GROUP2_BUILD_INTENT.md) requires a
reviewed remedy after fit failure. Propose at most two compile-only copied-source
trials: first outline the existing `cfframe_wait()` helper with `noinline`, then
separately outline `cfratio()` if the first trial is insufficient. Do not change
helper bodies, numeric arithmetic, read/capture checks, workload, capacities,
reserves, linker regions, MAP or lifecycle semantics. Both currently have no
standalone symbol in the P09 size output; `cfcalibrate` is 2235 bytes and calls
frame-wait multiple times. This suggests an outlining opportunity, **not proven
savings**. LTO effects are non-additive: accept only measured whole-image fit.
Retain both trial identities; do not alter the failed admission image.

Changed calling overhead, stack use and timing would require subsequent focused
host equivalence and fresh target timing evidence before execution/carrier work.
Recovering 367 bytes would fit only this probe, not admit the complete suite.
If outlining does not provide sufficient bounded headroom, return the measured
result for a new decision; no silent overlay, reserve borrowing or standalone
substitute for combined-load proof.

Registers/clobbers: ordinary compiler-managed C only; no hardware register
access added. CPU-visible changes are the measured linked growth, one volatile
result byte and automatic scratch; dynamic target stack high-water is unmeasured.
No physical allocation, MAP/base-page, DMA or IRQ/NMI policy changes. No generated
contract, threshold or reserve changes. Group 2 remains unfinished, with no
commit/push until completion and separate owner acceptance thereafter.
