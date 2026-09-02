# R0-E Execution Plan

Status: **Stages 1–3 are complete and published for the historical functional
proxy carrier. A bounded read-only raster observation is now in implementation;
it remains insufficient for R0-E/R0-F closure or a measured limit.**

| Step | Deliverable | Status |
|---|---|---|
| E0 | Admission, ownership, checkpoint, authority reconciliation | Complete |
| E1 | Generated proof contract, host independent-clock oracle, ledger | Complete |
| E2 | Target diagnostic, static validation, map/accounting | Complete |
| E3 | Fresh D81 construction and host structural/content gate | Complete |
| E4 | Local commits and Stage 1 stop | Complete |
| E5 | VS Code publication after `AUTHORIZE R0-E STAGE 2` | Complete — published source `ae2b0ae` |
| E6 | Xemu matrix/evidence after `AUTHORIZE R0-E STAGE 3` | Complete — two clean boots; published evidence `e2e2b46` |
| E7 | R0-F SD copy, physical chooser, and banner capture | Complete — exact hash, readable chooser directory, and physical banner retained |
| E8a | R0-E read-only raster phase observation | In progress — 16 low-byte phase bins/case, 33-tick windows, raw modulo-256 line deltas; no DMA/IRQ/MAP or limit claim |
| E8b | R0-F physical timing/DMA/IRQ measurement and full phase sweep | Still blocked — requires rebuilt carrier, complete D81 chain, pinned platform identity, and separately admitted DMA/IRQ instrumentation |

Candidate limits remain observations only. R0-E does not select a renderer, display mode, snapshot byte count, queue capacity, DMA duration, cadence, or memory layout.

The existing carrier is `TEST_ELIGIBLE` for the bounded functional-proxy scope
after its exact SD hash, chooser directory, and banner capture. Its source
identity remains historical: it did not contain the raster observation. Any
new measurement D81 is a new candidate and must begin at `UNVERIFIED`.
Read-only raster values do not measure CPU cycles, latency, DMA, IRQ, or a
limit. A real timing/DMA/IRQ phase sweep requires separately admitted target
instrumentation and a pinned physical platform identity.
