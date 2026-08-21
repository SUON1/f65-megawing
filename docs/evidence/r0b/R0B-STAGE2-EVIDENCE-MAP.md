# R0-B Stage 2 Evidence Map

This map describes the scope of one resident proof harness. It is not an R0-B
acceptance matrix and does not authorize production implementation.

| Required evidence | Harness method | Expected result |
|---|---|---|
| Safe FCM path (Stage 2) | `r0b_vic4_fcm_safe_gate()` checks the candidate ledger and performs no VIC I/O; target disassembly is rejected if it contains `$D054`. | `R0B-FCM-SAFE-001 DEFERRED` — clear only with the separate physical text-restore proof below. |
| Isolated FCM control/restore | `F65-R0B-FCM-SAFE.d81` checks C65 context through `$D018`, snapshots `$D054`, sets only documented `CHR16|FCLRHI` (`$05`), reads back, exactly restores `$D054`, and verifies a text-memory sentinel. Its assembly has no `$D02F`, `$D031`, pointer, DMA, MAP, or IRQ path. | `R0B-FCM-SAFE-002` passed in Xemu and has an owner physical readable PASS photograph with flags `$07` and sentinel `$01`. Artifact/machine identity details remain to be attached. It is not a visible-FCM pass. |
| Isolated `$D031` transition/restore | `F65-R0B-D031-SAFE.d81` first admits C65 context through `$D018`, saves `$D031`, clears only H640 (bit 7), reads back the intended byte, restores the exact saved byte, and checks a text sentinel. Static admission rejects `$D02F`, `$D054`, pointers, palette, DMA, MAP, and IRQ controls. | `R0B-D031-SAFE-XEMU-001 PASS` in Xemu with saved `$E0`, target/readback `$60`, exact restore, and sentinel pass. Physical owner photo + `$1800-$185F` dump is now the single prerequisite before the visible-card disk. |
| Isolated visible FCM card | `F65-R0B-FCM-VISIBLE.d81` admits only default C65 `$0800` screen context using read-only `$D018/$D031/$D060-$D063` checks; it saves 2,000 screen bytes and one aligned 64-byte FCM character, sets documented `$D054` bits `CHR16|FCLRHI|FCLRLO`, presents a deterministic card for a nominal dwell, restores the bytes and exact `$D054`, then records the results. No pointer/palette/DMA/MAP/IRQ write or `$D02F` access occurs. | Current Xemu context capture is `DEFERRED`: `$D031=$E0` is active 80-column state and no `$D054` write occurred. Do not run physical visible-card proof until the separate physical `$D031` restore proof passes. |
| Complete buffers | Compose buffer A at `$0400`, hash and present it only when complete; compose B at `$1000`, prove A hash unchanged, hash B, then CPU-copy B into the left 40 columns of the verified 80-column `$0800` matrix. | `R0B-PRES-001 COMPLETE+PREV PASS`; `R0B-SWAP-001 HW FLIP DEFERRED` until an atomic hardware flip/raster proof. |
| Candidate mode/palette | Generated candidate/palette ledger is checked by host and target safe gate. No active FCM mode/palette register is set. | `R0B-MODE-001 CANDIDATE PASS`; `R0B-PAL-001 ROLE MAP PASS`; `ACTIVE MODE/PALETTE: DEFERRED`. |
| Cockpit/HUD/MFD | Stage 2 composes readable cockpit/MFD status into B before B is made visible. | `R0B-HUD-001 COCKPIT/MFD PASS`. |
| Input edge timing | Host records a synthetic edge-service wall-time model. Target performs 2,048 synthetic edge bindings between read-only `$D012` samples. | `R0B-IN-003 EDGE RASTER: <nonzero>`; physical source remains `R0B-IN-004 PHYS EDGE DEFERRED` until CIA/keyboard/joystick capture. |
| Audio service timing | Host records a SID-write model wall-time. Target performs 512 six-register SID service batches between read-only `$D012` samples. | `R0B-AUD-001 SID RASTER: <nonzero>`; this is service duration, not audible latency. |
| Renderer candidate | Fixed wireframe proxy scene is written into buffer A by `wire_proxy()`. | `R0B-REN-001 WIRE PROXY PASS`. |
| Hardware run | The target screen asks for owner capture; the guide requires the matching result block and machine identity. | `R0B-HW-001 OWNER CAPTURE REQUIRED` until returned owner evidence. A physical isolated-FCM capture does not close this full-resident capture item. |
| Pinned identity | `$1800` header contains contract digest, SDK 23.1.0, B=02, LTO-ZP=00, revision and size; runner JSON pins environment and artifact hashes. | `R0B-BLD-001 PASS; GATE NOT CLOSED`. |

`DEFERRED` is intentional only where the exact clearing condition is stated
above. It is not a pass and must not be used as a substitute for hardware
evidence.

## Final composite candidate — `F65-R0B-FINAL.d81`

The final composite candidate supersedes the separate Stage 2 disks as the
single hardware-run artifact. It is still an R0-B bounded proof harness, not
a production graphics, input, audio, or gameplay implementation.

| Required R0-B evidence | Final-composite method | Xemu result | Physical clearing condition |
|---|---|---|---|
| 1. Safe VIC-IV FCM probe | Captures `$D018/$D031/$D054/$D060-$D063/$D070`; writes only `$D031` H640-clear and `$D054` low three FCM bits; reads them back and restores exact saved values. No `$D02F`, MAP, DMA, or IRQ access. | `R0B-FINAL-XEMU-001 PASS` | Same screen/result capture reports `FCM SAFE ... PASS` and exact rollback PASS. |
| 2. Complete-buffer presentation | Fully compose 2,000-byte matrix B at `$1000`, preserve/hash prior matrix A at `$0800`, set only documented pointer bytes `$D060-$D063`, hold visibly, then restore. | `COMPLETE MATRIX ... PASS`; `POINTER FLIP+RESTORE: PASS` | Visible complete B matrix and matching PASS rows. This is a controlled transition, not a raster-atomicity claim. |
| 3. Mode/palette behavior | Candidate uses 40-pair FCM context. The active palette mapping is observed through `$D070`; one active red palette byte is save/write/read/restore checked without changing the mapper. | `ACTIVE PALETTE ... PASS` | Matching PASS row and result block. |
| 4. Cockpit/HUD/MFD composition | The complete B matrix contains readable FCM/HUD identity/status before it is selected. | `HUD/MFD ... PASS` | Matching PASS row. |
| 5. Input edge plus latency | Reads one documented MEGA65 ASCII event from `$D610`, acknowledges it by writing that event byte, and measures the service with the raster timer. | `DEFERRED (NO KEY EVENT)` in headless Xemu; no synthetic pass claimed. | Press one key in the displayed input window; both input status bytes become `01` and the captured result has nonzero `input_ticks`. |
| 6. Timed audio service | Performs 512 real SID register service writes and reports raster-timer delta. | `SID 512-WRITE SERVICE ... PASS` | Matching PASS row with nonzero `audio_ticks`. PCM/DMA is documented as out of this bounded R0-B service proof because no pinned start/stop wrapper has been authorized. |
| 7. Bounded renderer | Writes an aligned 64-byte deterministic FCM proxy-scene card used by the complete matrix. | `RENDERER ... PASS` | Matching PASS row. |
| 8. Non-baseline hardware run | `$D60F.5` distinguishes physical MEGA65 from Xemu and is written into the resident result identity. | `HARDWARE: DEFERRED` by design in Xemu | Physical status line reports `ENV: PHYSICAL MEGA65 DETECTED`; hardware status byte is `01`. |
| 9. Pinned identity/results | Fixed 96-byte `$1800-$185F` record contains `R0B2`, schema, environment, outcome, revision, contract digest, toolchain/ABI identity, test statuses, reason codes, timings, hashes, and transaction observations. | Header: `52 30 42 32 02 01 03 05`; validator PASS | Photograph the status page and the on-screen `$1800` dump from the same run. |

Current composite identity: `F65-R0B-FINAL.d81`
`43fe855abac93b355b36fa509d83cd302920e87fe0a49e64287285f0a8e980f1`.
Its Xemu evidence is `R0B-FINAL-XEMU-001 PASS`; it does **not** close the
physical R0-B gate.
