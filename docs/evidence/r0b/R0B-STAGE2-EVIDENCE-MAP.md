# R0-B Stage 2 Evidence Map

This map describes the scope of one resident proof harness. It is not an R0-B
acceptance matrix and does not authorize production implementation.

| Required evidence | Harness method | Expected result |
|---|---|---|
| Safe FCM path (Stage 2) | `r0b_vic4_fcm_safe_gate()` checks the candidate ledger and performs no VIC I/O; target disassembly is rejected if it contains `$D054`. | `R0B-FCM-SAFE-001 DEFERRED` — clear only with the separate physical text-restore proof below. |
| Isolated FCM control/restore | `F65-R0B-FCM-SAFE.d81` checks C65 context through `$D018`, snapshots `$D054`, sets only documented `CHR16|FCLRHI` (`$05`), reads back, exactly restores `$D054`, and verifies a text-memory sentinel. Its assembly has no `$D02F`, `$D031`, pointer, DMA, MAP, or IRQ path. | `R0B-FCM-SAFE-002 XEMU/TARGET PASS` only when flags are `$07` and sentinel is `PASS`. Xemu is passed; physical requires the exact D81, readable screen photograph (including the on-screen `$1800-$185F` dump), D81 hash, and MEGA65 identity. It is not a visible-FCM pass. |
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
