# R0-D Execution Plan

Status: **DIAGNOSTIC HOLD — two R0-D D81 carriers failed physical chooser with
`ERROR CODE FF`; no third carrier without a specific evidence-backed change.**

| Step | Deliverable | Status |
|---|---|---|
| D0 | Admission, authority reconciliation, ownership, checkpoint | Complete |
| D1 | Generated R0-D counter contract and memory ledger | Complete |
| D2 | Deterministic 21-stage, 530,000-clock historical fixture | Complete |
| D3 | Host counters, rolling windows, evidence, and static checks | Complete |
| D4 | Target diagnostic observability and map/symbol/listing review | Complete — host/build evidence only |
| D5 | Fresh R0-D D81 carrier, loadability validator, manifest, and host gate | Blocked — `F65R0D.D81` and `F65R0D2.D81` are invalid after physical chooser `ERROR CODE FF`; D2 SD-copy SHA-256 matched exactly |
| D6 | Stage-1 handoff and local commits | Blocked — require a same-card, hash-verified physical control of `F65-R0C-MEDIA.D81` before admitting a specific carrier correction |

The fixture is a historical comparison workload, not a production budget and
not a measured-limits selection. Both failed R0-D carrier identities remain
discarded; host/Xemu evidence cannot override their chooser failures. The only
next physical action is a read-only control of the retained physical-pass
`F65-R0C-MEDIA.D81` identity. A new R0-D image requires a fresh format, a new
identity, and every D81 gate only after a concrete construction change is
identified.
