# BIT/CLV verifier correction evidence

**READY FOR REVIEW — host regressions and pinned static replay only; zero relinks.**

See the [result report](../../../reports/M2_BIT_CLV_VERIFIER_FIX.md).
Current task-prompt approval authorizes the bounded verifier change and tests.

- `reference_stack_check.py`, `reference_test_contract.py`, `wip-before.md` and
  `checkout-before.json`: preserved state before any edit.
- `run_checks.py`, `commands.json`, `regressions.txt`: exact approved host
  commands and 11 passing tests, including six new regression methods.
- `replay.py`, `replay.json`, `replay.txt`: exact hash-pinned before/after replay
  of the predecessor and interpolation standalone disassemblies; original
  failure reproduced and corrected results recorded. Both prove 20 hardware
  bytes including entry return and zero dynamic software bytes in their stated
  direct-call scope. No original record is replaced.
- `source/`: corrected verifier/test snapshots.
- `preservation.json`, `verify.py`, `inventory.json`: original path/content,
  historical packet, raw artifact, generated-file, scope and handoff checks;
  this packet's final inventory excludes only itself.

No target code or precision change, compiler or link command, target execution,
full-renderer fit/stack/timing admission, Xemu, D81, SD or physical testing.
Retain every previous evidence packet and failure unchanged.
