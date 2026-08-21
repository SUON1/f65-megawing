# R0-B Execution Plan and Evidence Log

Status: **implementation in progress**. This is an action/evidence log, not a
production design decision.

## Starting identity

- Branch: `codex/r0-b-development`
- Accepted upstream R0-A commit: `1ab5b62928d0e725c8dcf48e8a17783a525503b6`
- R0-A D81 SHA-256: `40d95171389e3825793216ed54176084a87bad5bac630b942955c8b90668b3b4`
- R0-A PRG SHA-256: `c7360a2dd978181d63ce6fcd5c39eecd55001e12f106a5d9f84f937c8d49af08`
- Toolchain lock SHA-256: `fc56c2017da8d4adf9daed17efed05dc93ea14ae6dbbbbeaa3125e530a68fa5f`
- Platform ABI SHA-256: `ca3c2c95e1c3e7f553557b7a2a22e1a2143874ceec1e13c91e502ca0faddfccc`
- Interface registry SHA-256: `b26941225ea6ff5827d915b0678d20827809b7829e9e32bbc5ed45bd031538f7`

## Work and evidence ledger

| Stage | Action | Status | Evidence / constraint |
|---|---|---|---|
| B0 | Branch, admission contract, ownership, registry, official-record log | Complete | This commit; R0-A physical base-page/pointer proof is retained unaltered |
| B1 | Single-source candidate contracts, Java oracle, generated C/Java/assembly bindings, proxy fixtures | Complete | `R0B-MODE-001`, `R0B-FCM-001`, `R0B-PAL-001`, and `R0B-IN-002` pass as host-side accounting/oracle evidence; no target rendering claim |
| B2 | Officially documented VIC-IV candidate layouts and FCM characterization | In progress | `R0B-FCM-REG-001` passed in Xemu: `$D054` FCM-related bits unlock, latch/read-back, and restore. Visible FCM, pointers, DMA, swap, and raster behavior remain unproved |
| B3 | Complete-buffer renderer tiers, views, overflow behavior | Pending | Synthetic scene only; no gameplay |
| B4 | Cockpit/HUD/MFD proxy, semantic palette and grayout validation | Pending | Technical art; human readability review remains open |
| B5 | Input sample/edge/arbitration corpus and latency procedure | Pending | 10,000 host transitions; physical latency unresolved without calibrated capture |
| B6 | Representative SID/optional PCM priority proof | Pending | No final content/format selection |
| B7 | RRB/affine disposition or separately bounded candidates | Pending | Cannot replace bucket/painter primary path |
| B8 | Integrated graphics/input/audio proof | Pending | Complete-store, range, reserve, and contention observations |
| Xemu | Exact D81 boot/capture/metadata | In progress | `R0B-XEMU-001` passes for the local owned ROM/Xemu identity; Xemu is not physical hardware evidence |
| Hardware | Owner test guide and returned-exact-build evidence | Pending | Do not mark pass before owner review |
| Handoff | Acceptance matrix, clean validation, commit, push | Pending | Implementation complete only when every listed deliverable exists |

## Proof memory envelope

| Owner | Physical range | R0-B status |
|---|---|---|
| Display control | `$01C000-$01CFFF` | candidate proof control only |
| Display store A | `$020000-$02FFFF` | candidate proof store |
| Display store B | `$030000-$03FFFF` | candidate proof store |
| Cockpit/HUD/MFD/palette assets | `$040000-$047FFF` | proof-only assets |
| Renderer workspace | `$048000-$04FFFF` | bounded proof workspace |
| Resource/audio/DMA staging | `$050000-$057FFF` | bounded proof staging |
| Measured reserve | `$058000-$05FFFF` | forbidden/untouched |

Target ceiling candidates are charged, not approved: renderer/cockpit/HUD/radar
code 6 KiB; input/audio/resource service code 4 KiB; core/platform/IRQ/MAP/DMA
code 10 KiB. Runtime, constants, thunks, stack, lists, assets, and records must
also be reported.

## Revalidation triggers

Rebuild and revalidate for any controlling-document/status change; changed
compiler, flags, linker/runtime/base page/platform wrapper; candidate layout,
fixture, palette, asset, input/audio/DMA method; ROM/core/system/video/Xemu
identity; evidence schema/instrumentation; or replacement of the R0-B proxy
scene in R0-C.
