# M2 PR2 20-byte overrun correction

**READY FOR REVIEW — integrated regression size gate restored.**
Baseline `0d42a8ce271a98abbffada019c403e31e7590e5d`; branch
`codex/65aero-m2-pr2-full-composition`. Founder authorized the focused overrun
correction with precision, limits and history preserved. The
[failed-gate report](M2_PR2_FULL_COMPOSITION_GATE.md) remains unchanged.
[Fresh evidence](../evidence/flight-demo/2026-10-21-m2-fit-overrun-fix/README.md).

## Correction

`m2_registration_prepared` no longer constructs a second complete registration
record and copies it to the destination. After all input/readiness/generation/
store checks succeed, it assigns every generated field directly to the output.
There are no fallible operations after the first output write. This preserves
failure-without-output-mutation and the existing private-owner construction
lifetime; it does not introduce concurrent publication. The public wrapper
still captures the camera before writing, including when the input camera is
inside the output record.

Q12/Q24/Q46/Q16 numeric representation, transformation/clipping/raster/horizon
arithmetic, generated layouts and all memory limits remain unchanged. The
119-byte target registration layout has no unassigned field; native C padding
is not a serialized contract. No shader/raster simplification, precision change,
compiler flag change or probe behavior removal was used to recover space.

Only the registration helper and focused host tests changed in this correction,
plus WIP and a new report/evidence packet. Prior full-composition work remains
pending on the same branch. No new register/clobber convention, CPU/physical
allocation, MAP/base-page operation, DMA, IRQ/NMI or persistent-state behavior.

## Measured integrated result

Command: `python3 -B tools/flight_demo/m2_pr2/fit.py`.
Output: `build/flight-demo/m2-pr2-fit-1792594724651538000/`.
Compiler/linker and the provisional static gate PASS.

Resident end moves from **`$8014` to `$7FDC`**, a **56-byte reduction**, leaving
**36 bytes** below the unchanged `$8000` ceiling. Text decreases by 52 bytes;
linker alignment decreases by four bytes. All other section sizes are unchanged.

| Section | Start | Bytes |
|---|---|---:|
| text | `$2017` | 22,512 |
| read-only data | `$7808` | 848 |
| initialized data | `$7B58` | 22 |
| BSS | `$7B6E` | 859 |
| static compiler scratch | `$7EC9` | 275 |

Text ends at `$7807`; the one-byte alignment gap is included. Static scratch
is charged once in resident extent, not again as dynamic stack.
Target SHA-256: `b10c3105867c36c995d4ce3383bb1c4ce5208e9d27968c2422b529d78966f9bf`.
The source-pinned integrated probe and compiler policy are unchanged; the fix
restores the same regression gate that failed, rather than substituting a
prepared-only probe or enlarging the limit.

## Validation

- `python3 -B tools/flight_demo/m2/build.py`: PASS in fresh output
  `build/flight-demo/m2-pr1-1792594726160400000/`. Five contract tests, original
  host/sanitizer/replay checks (`DE675132`), 3,857 independent oracle cases and
  841 near/far cases pass. Projection errors remain 0.000021224219 and
  0.035136325 pixel; raster error stays within one logical pixel.
- Standalone target compile/link/static PASS, resident end `$732A`, hardware
  stack bound 25 bytes, dynamic software stack bound 16 bytes, compiler static
  scratch 443 bytes. These are not integrated stack/high-water claims.
- Integrated cursor sanitizer checks, compile/link, resident ranges, stack
  envelope declaration, expected entry seams and no-direct-ROM-call check PASS.
- Three PR2 contract tests and prepared-context ASan/UBSan checks PASS in
  `build/flight-demo/m2-overrun-host-1792594764764830000/`. Exact commands are
  retained in `prepared-commands.json`. Includes 3,672 segment comparisons,
  horizon/registration reuse, poisoned output storage, public input-camera/output
  aliasing, invalid store/generation/readiness/null inputs and output preservation.
- Corpus/ledger scope, whitespace, evidence inventories and input hashes PASS.

The new tests check actual field validity and output preservation, not native
padding byte equality between independently constructed records. No generated
contract or oracle was changed. All earlier evidence inventories remain exact;
15,753 captured current-file fingerprints are unchanged and the two authorized
modified files have original-byte snapshots. All 20 unrelated entries are intact.

## Stop

The requested overrun correction is complete at READY FOR REVIEW. **36 bytes is
only the remaining regression-probe margin.** Full renderer/font/state fit,
actual integrated stack/ABI/service bounds, output mapping and display admission
remain open as recorded in the full-composition intent. No renderer work or
new execution admission is inferred from this result.

No Xemu, D81, SD or physical testing. No commit, push, PR or merge. Review the
focused correction before resuming the larger composition task.
