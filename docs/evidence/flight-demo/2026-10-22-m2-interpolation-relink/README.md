# Resumed interpolation single-relink evidence

**READY FOR REVIEW — 385 resident bytes saved; full fit FAIL by 9,189 bytes.**

See the [result report](../../../reports/M2_PR2_INTERPOLATION_RELINK_RESULT.md).
Current task-prompt authority resumes I1–I6 after approval of the BIT/CLV fix.

- `checkout-before.json`, `wip-before.md`: state captured before this resume.
- `preflight.py`, `preflight.json`, `standalone-static.json`: exact frozen
  inputs/tools, approved checker, retained host evidence and completion of the
  pending standalone static checks without rebuilding its artifact.
- `link-command.json`, `link.txt`: the single composed candidate relink's exact
  argv and actual exit-1 fit result; underlying compile/link/tools all exit 0.
- `01-candidate/`: fresh compile/link logs, map, symbols, disassembly and build
  record, explicitly identifying original host evidence reuse. PRG/ELF/backend
  and executable bytes remain in the new ignored raw directory.
- `account.py`, `comparison.json`, `static-accounting.json`: independent ELF
  allocated-section totals, symbol/owner changes, approved-checker closure
  bounds, unsupported full-program path and conservative instruction bounds.
- `candidate-artifacts.json`, `source/`: raw candidate identities and unchanged
  candidate geometry source snapshot.
- `verify.py`, `preservation.json`, `inventory.json`: final exact recipe,
  preservation, scope, generated-file, links/JSON/whitespace and packet seals.

Fresh raw output:
`/private/tmp/f65-m2-interpolation-experiment/build/flight-demo/m2-interpolation-resumed-1792701029486920000`.
Earlier raw directories and packet inventories remain exact. The new build's
first three host commands were run in their recorded original directory and
were reused, not rerun; only its four target/tool commands are new.

Projection-closure bounds are 24 hardware bytes including entry return and
8 dynamic software bytes; resident compiler scratch remains 200 bytes. These
do not establish whole-renderer stack, timing, full fit or runtime/display
admission. Complete-probe stack checking remains unsupported at `CLD` in both
artifacts. No further checker change, optimization, Xemu, D81, SD or physical
testing occurred.
