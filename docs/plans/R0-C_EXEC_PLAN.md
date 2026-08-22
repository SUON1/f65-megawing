# R0-C Execution Plan

Status: **authorized development — implementation in progress**.

| Stage | Deliverable | Status |
|---|---|---|
| C0 | Configuration reconciliation, admission, ownership, inspection/risk record | Complete — `491af24` |
| C1 | Canonical proof schemas and generated C/Java bindings | Complete — candidate `r0c-0.1.0-proof` |
| C2 | Deterministic asset converters and technical fixture | Complete for bounded fixture profile |
| C3 | Capacity witnesses, package, resource/D81 manifests | Complete for bounded proof package |
| C4 | Target residency/staging/no-disk diagnostic proof | Real Attic bounded CPU-copy wrapper implemented; host/XEMU PASS; physical ABI evidence pending |
| C5 | Save fault model and ROM-reclaim/storage handoff proof record | Host model complete; `DEC-012` approved for sacrificial fixture only; target storage adapter and post-reclaim service remain unadmitted |
| C6 | Xemu evidence, physical guide, handoff/acceptance matrix | In progress |

Formal R0-C passage remains blocked by admitted platform contracts and exact
physical storage/save/media evidence. `DEC-012` is approved only for the
sacrificial R0-C fixture; `DEC-015` remains explicitly undecided.
