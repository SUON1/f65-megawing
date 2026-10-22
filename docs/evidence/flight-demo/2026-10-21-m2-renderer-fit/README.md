# M2 PR2 early renderer fit failure

[Handoff](../../../reports/M2_PR2_RENDERER_FIT_GATE.md).
Base `8ee5214ea9c63b86e92ca9bc4fa0779115dbd57f`; founder-approved F1–F6.

- `01-backend-option/`: original host PASS and backend invocation failure;
  exact pre-correction builder retained. Original inputs otherwise unchanged.
- `02-linked-overrun/`: successful host/compile/link logs, target map/symbols/
  disassembly, five host PPM images and original failed accounting assertion.
- `link-analysis.json`: additive map accounting; resident end `$A41F`, 9,247
  bytes over unchanged `$8000`; no rebuild or mutation of the failed record.
- `regression/`: fresh unchanged geometry host/oracle/standalone target results.
- `source/`: exact new implementation/test/build inputs for the linked attempt.
- `preservation.json`: current baseline and unrelated-path preservation result.
- `inventory.json`: SHA-256 of every other file in this packet.

Raw PRG/ELF and other outputs remain in the fresh build directories named in the
handoff. The PRG is oversized and not admitted for execution. Host images are
not Xemu or hardware screenshots. No display/runtime admission claim.
