# Integrated capture budget — 2026-10-03

The approved redesign's existing tail traversal reduces empty-capture growth
from 769 to 253 bytes. Actual host-executed tail statements pass 403 boundary,
failure and corruption cases under ASan/UBSan, retaining the 2000-world maximum.
The image fits at $BF89 with 119 bytes free. This remains an empty compile-only
skeleton: no admitted trace-version change, live case proof or execution.

| Fresh experiment | Added over R2 | Resident end | Margin |
| --- | ---: | --- | ---: |
| Integrated empty | 253 | $BF89 | 119 |
| Live queue 1 | 1187 | $C32F | -815 |
| Live queue 2 | 1060 | $C2B0 | -688 |
| Live queue 3 | 883 | $C1FF | -511 |

The live trials hook the actual full queue at stage 13 in ticks 1 and 1601,
observing owner 0/9/255 rejection and whole-model CRC before/after restoring only
the intentionally introduced rejection flag. Two observations consume 24 bytes.
Draft framing serializes those observations into the proposed private extension.
Trial 2 removes per-byte divide/modulo and CRC calls; trial 3 outlines the live
hook and uses static framing plus two dynamic payload spans. Every trial fails
fit before execution. Their v8 contract/encoder drafts have no host behavioral
proof or independent admitted reducer and must not run.

Each subdirectory retains its exact result/input inventory, compile command,
map/symbol sizes, runner checkpoint, changed copied source and patch. Complete
local copied source and unexecuted PRG identities remain in `local-artifacts.json`.
Commands were `python3 -B tools/diagnostics/r0f_group2_integrated_capture.py` and
three fresh `python3 -B tools/diagnostics/r0f_group2_live_queue.py` experiments;
the preserved runner at each result identifies its actual implementation.

Capacities, reserves and every prior integrity/timing threshold are unchanged.
P09 and all baseline inventories remain hash-identical. No draft carrier was
constructed. The fitting R1/R2 normal control and selected export-collision case
are separate [evidence](../2026-10-03-export-collision/README.md); they do not
close the live case fit gap or the broader suite.
