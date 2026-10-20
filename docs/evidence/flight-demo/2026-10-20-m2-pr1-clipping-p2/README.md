# M2 PR1 clipping correction evidence

READY FOR REVIEW. See the [correction handoff](../../../reports/M2_PR1_CLIPPING_P2.md).

`build.json` records exact commands, current input/tool hashes, original and new
oracle results, linked sections, owner sizes and refreshed stack analysis.
`host.txt`, `clip-host.txt`, `contract-tests.txt`, `oracle.json` and
`clip-regressions.json` are actual results. `clip_vectors.h` is the independently
computed host-only regression input/expectation set. Maps, symbols and disassembly
are compile-only evidence. `preservation-before.json` and `verification.json`
record preserved identities; `inventory.json` hashes every other packet file.

The original PR1 packet and prior local outputs remain unchanged. The first
correction build's static-gate stop remains in its local output directory; only
the final complete build is marked PASS here. No target execution, PR2, Xemu,
D81, SD, physical testing or integrated display/timing acceptance is claimed.
