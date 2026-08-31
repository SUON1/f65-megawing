# R0-D Execution Plan

Status: **STAGE-1 CORRECTION COMPLETE — `F65R0D3.D81` is host-content-verified
only; awaiting local commit and VS Code publication before Xemu authorization.**

| Step | Deliverable | Status |
|---|---|---|
| D0 | Admission, authority reconciliation, ownership, checkpoint | Complete |
| D1 | Generated R0-D counter contract and memory ledger | Complete |
| D2 | Deterministic 21-stage, 530,000-clock historical fixture | Complete |
| D3 | Host counters, rolling windows, evidence, and static checks | Complete |
| D4 | Target diagnostic observability and map/symbol/listing review | Complete — host/build evidence only |
| D5 | Fresh R0-D D81 carrier, loadability validator, manifest, and host gate | Complete — `F65R0D3.D81`, SHA-256 `107c6a356b932e9ade875c24539d75b1b0a0078122a6a3910f524570aafec5ef`, fresh one-session construction with the OpenCBM-disabled builder and clean diagnostics |
| D6 | Stage-1 handoff and local commits | In progress — commit the builder correction, checkpoint, plans, and retained evidence; then hand off for VS Code publication |

The fixture is a historical comparison workload, not a production budget and
not a measured-limits selection. Both failed R0-D carrier identities remain
discarded; host/Xemu evidence cannot override their chooser failures. The
evidence-backed correction is an OpenCBM-disabled `c1541` plus strict zero-
stderr/diagnostic enforcement. D3 is a new identity, not a copy, patch, or
rename. It must now be committed, published through VS Code, and boot-verified
in Xemu before any physical transfer or chooser test.
