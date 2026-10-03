# Terminal diagnostic attempts — 2026-10-02

Both target variants fail resident fit and are **NOT EXECUTABLE / NOT FOR DELIVERY**.
See the [report](../../../../reports/R0-F_GROUP1_TERMINAL_DIAGNOSTIC.md).
Variant 1 exceeds by 42 bytes; variant 2 exceeds by 238 bytes. Both preserve
all validation predicates. Variant 2 native host analysis passes with mocked
hardware/transport. No new Xemu, SD or physical run occurred.

Each directory retains its preparation, exact changed sources, patch,
compiler result, build identity and failed PRG. Raw local map/symbol/listing/ELF
identities are retained in `local-build-artifacts.json`; those files remain
in the ignored build tree. Host executables are omitted from this packet.
The patch applies only to a fresh copy of the recorded P06 source inputs.
Do not apply it to root source or any retained carrier. The manifest preserves
this bounded failure evidence; it is not admission or acceptance.

Review patches use zero context to avoid whitespace-only diff context lines.
Original preparation patch bytes remain in the ignored build tree with hashes
in the local-artifact index. Both representations replay to identical source.
