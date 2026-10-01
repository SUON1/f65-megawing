# Group 1 terminal-export capacity checkpoint — 2026-09-29

The private development transport now has bounded Xemu evidence at its full
327,680-byte capacity, at the final `G1T19` name collision and at one byte
over capacity. This closes the **development transport boundary check**, not
the integrated Group 1 workload, a delivery carrier or R0-F acceptance.

The [approved export amendment](../plans/R0-F_GROUP1_EXPORT_AMENDMENT.md),
generated export contract and memory ledger govern this work. The probe's
length is now a builder parameter rather than a fixed C literal. One runner
checks the actual result/SAVE and independently extracted chunks for short,
full-capacity and collision cases. The one-over case checks that no terminal
export starts. No public ABI, resource allocation or product threshold
changed. The probe retains existing Attic trace `$08030000-$0807FFFF`,
terminal staging `$4000-$7FFF` and one-use capsule behavior. It adds no
register, MAP/base-page, DMA, acquisition timing or IRQ/NMI effect; its C
clobbers are compiler managed. Export occurs after measured work stops.

| Case | Exact observation from the post-run D81 and target state |
| --- | --- |
| NTSC full capacity, `ntsc-01/G1MAX01.D81` | 20 files `G1T00`–`G1T19`, terminal status 4/error 0; all 327,680 deterministic bytes extracted in order, CRC32 `BDCC0FCA`; actual result and returning SAVE valid. |
| PAL final-name collision, `pal-existing-last-01/G1MAX01.D81` | Pre-existing `G1T19` remained unchanged; 19 preceding files contained 311,296 expected bytes. Terminal status 5/error 3, files 19, with no export success or retry. Actual result and returning SAVE valid. |
| NTSC 327,681-byte request, `ntsc-01/G1OVR01.D81` | Result fault 107 at tick 66; export permit/status/error/files all zero. Actual D81 contains only `TOKEN` and returning `RSSTATE`, with no trace file. |
| NTSC short regression, `ntsc-01/G1EXP01.D81` | Rebuilt 33,025-byte probe exported three chunks, CRC32 `F2CEE7CB`, status 4/error 0; actual result and SAVE valid. |

All four D81s were freshly formatted in separate output directories and
populated in one pinned-tool construction session. Post-run directory, chain,
BAM, free-block and content checks passed through independent parsing and
pinned-tool extraction. Each target binary passed pre-C capture ordering,
protected/staging bounds, ROM-call allowlist and no-return static checks.
`G1MAX01.D81` is a reused basename in **two distinct disposable directories**;
neither image was copied, renamed, reused or overwritten. The max-case PRG
SHA-256 is `13c8586c1ae94c6ca4ab98cd68bcc74f8d47c01090904d1e8a0fff088531db1f`.
The original integrated Group 1 PRG and ordinary CAP14 predecessor were not
changed by the probe parameterization. Their checked SHA-256 values remain
`ec259fc7611d8bb5809d15f6c333f5b224df4c945a8e9ffca5b2402d8444cb30`
and `cf605bd377ddcee2c72cdc4abfd20c3ae9eee350b7b78b36cbde8ff1adf8fc23`,
respectively.

After these runs, the probe's local `255`-byte copy-buffer literal was
replaced with generated `R0FG1X_COPY_CHUNK_BYTES` to keep that rule in one
contract. Fresh target builds for all three lengths produced PRGs byte-identical
to the tested binaries. The [source-equivalence freeze](../evidence/r0f/group1/2026-09-29-export-source-equivalence/README.md)
retains both C versions, build reports and exact binary comparisons; no D81
was reused or rerun for this source-only correction.

Commands run from the repository root:

```text
python3 -B tools/diagnostics/r0f_group1_export_probe.py build --build-dir build/r0f/group1/export-max --bytes 327680
python3 -B tools/diagnostics/r0f_group1_export_probe.py run --build-dir build/r0f/group1/export-max --out build/r0f/group1/export-max/ntsc-01 --mode 1 --timeout-seconds 180
python3 -B tools/diagnostics/r0f_group1_export_probe.py run --build-dir build/r0f/group1/export-max --out build/r0f/group1/export-max/pal-existing-last-01 --mode 0 --case existing-last --timeout-seconds 180
python3 -B tools/diagnostics/r0f_group1_export_probe.py build --build-dir build/r0f/group1/export-overflow --bytes 327681
python3 -B tools/diagnostics/r0f_group1_export_probe.py run --build-dir build/r0f/group1/export-overflow --out build/r0f/group1/export-overflow/ntsc-01 --mode 1 --case overflow --timeout-seconds 120
python3 -B tools/diagnostics/r0f_group1_export_probe.py build --build-dir build/r0f/group1/export-regression-02
python3 -B tools/diagnostics/r0f_group1_export_probe.py run --build-dir build/r0f/group1/export-regression-02 --out build/r0f/group1/export-regression-02/ntsc-01 --mode 1 --timeout-seconds 90
python3 -B tools/diagnostics/r0f_group1_build.py
python3 -B -m unittest discover -s tools/diagnostics -p test_r0f_group1_export_admission.py -v
```

Xemu terminal programs halt indefinitely; timed shutdown produced memory and
D81 captures, while the checked state and extracted bytes establish each
result. The host/target-object suite passed one million timing-release cases,
256 export-readiness combinations and bounded-copy/lifetime checks; the eight
export-admission unit cases also passed. Evidence-manifest rehash, Python
syntax and `git diff --check` passed. Frozen evidence and source-input hashes are in the
[full-capacity](../evidence/r0f/group1/2026-09-29-export-capacity/README.md),
[overflow](../evidence/r0f/group1/2026-09-29-export-overflow/README.md) and
[short-regression](../evidence/r0f/group1/2026-09-29-export-short-regression/README.md)
directories. These are development direct-PRG Xemu runs. The integrated
workload's remaining phase/view/pool coverage, compact success summary and
exact-name two-NTSC/two-PAL carrier gates remain open. Whole-ISR cost,
entry latency, physical SI uncertainty, SD delivery, physical execution and
owner acceptance are unproven.
