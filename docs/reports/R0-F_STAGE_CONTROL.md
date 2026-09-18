# R0-F Stage Control

## Current stage

Combined successor: **CF001 COMBINED EXPERIMENT IMPLEMENTED; FULL R0-F OPEN**.
Private contract: `R0-F_COMBINED_CONTRACT.md`. Reset-only ROM backup/reclaim/
restore, nominal counter-ratio calibration, concurrent synthetic workload,
IRQ/DMA/PCM/matrix input, complete-buffer rendering and raw-page capture now
execute together. Host and direct-PRG PAL/NTSC observations exist. Exact current
artifact and delivery state are recorded in `R0-F_COMBINED_HANDOFF.md` and
`build/r0f/combined/manifests/r0f-d81-release.json` when generated. F65BLK02 is
the intended native slot. Do not infer an SD write or physical pass from a build.
Production ROM/storage return, independent physical clock uncertainty, full
parent scene/input/latency/rolling-window coverage and owner acceptance remain
open; the experiment does not close those by relabelling proxy observations.
Existing F5 state:

`F65R0F5: HOST/XEMU PASS; SD TRANSFER PASS; PHYSICAL CAPTURE CRC/JAVA PASS; FULL R0-F OPEN`

See `R0-F_CAPTURE_HANDOFF.md`. Clock calibration and the full combined workload
remain incomplete. The 22-page physical capture is reconstructed and validated;
see `../evidence/r0f/capture/physical/REVIEW.md`. No repeat F5 capture requested.
The F4 state below is historical.

Owner selected full closure on the current design (`1`, 2026-09-17).
`docs/plans/R0_FULL_CLOSURE_WORK_PLAN.md` now controls work sequencing;
the program-direction question is resolved, not the acceptance gates.

`F65R0F4: HOST/JAVA AND XEMU PASS; PHYSICAL SCREEN OBSERVED; FULL R0-F OPEN`

Current handoff: `R0-F_CIA_TIMING_HANDOFF.md`. The reset-only timer contract,
raw capture and Java oracle advance measurement development, not gate acceptance.
F3 is withheld (serial-mode precondition added before release), not a carrier
failure. No F3 hardware run is recorded. The owner subsequently supplied F4
physical completion and platform photos, retained in
`docs/evidence/r0f/cia-timing/physical/`. F4 SD hash/extent/eject/chooser chain
and physical raw validation remain unverified; photographs do not advance
the complete F6–F8 gate chain. See `R0-F_CLOSEOUT_REVIEW.md` for the gap between
the bounded proxy and full combined-load requirements and the owner scope
decision subsequently recorded above. No further hardware action is requested yet.
F2's owner-reported Finder
crash means safe eject is NOT VERIFIED; its physical functional photo remains
valid as an observation. Do not repeat the eject command as though it had passed.

## Previous F2 state

Owner photo received 2026-09-17 shows functional PASS, 80 valid samples, and
F65R0F2 startup-fix identity. Matching SD hash and unchanged extent are retained;
safe-eject completion remains unconfirmed. See the current startup-fix handoff.
The pending physical-retest wording below describes the earlier handoff state.

2026-09-17: `R0F-STATIC-STARTUP-001` is corrected by excluding the unused SDK
character-set initializer from the R0-F link. The new F65R0F2.D81 passed host
gates and two clean Xemu boots with screenshots inspected. Hardware retest and
the full measurement contract remain pending. See `R0-F_STARTUP_FIX_HANDOFF.md`.
The Step 3 findings below describe the previous F65R0F1 build.

R0-F development is authorized by AD-001, but R0-F acceptance is not. On
2026-09-05 the owner-directed first test slice compiled, passed native functional
and timeout tests, and produced host-verified F65R0F1.D81. The owner subsequently supplied the other checkout location; its pinned ROM
and emulator enabled two clean Xemu boots, which both passed. SD transfer,
chooser runtime, and physical load were observed; DMA, IRQ, latency, and
platform-identity measurement remain incomplete.
Step 3 was executed on 2026-09-16. Native tests and compilation pass, including
358 validator rejection cases. The ledger now accounts for the existing 107-byte
compiler static stack. Static review found `R0F-STATIC-STARTUP-001`: startup
calls KERNAL `$FFD2` after setting B=$02, without the separately required thunk.
The audit stops advancement; see `R0-F_STEP3_AUDIT.md`.

Correction to the prior Step 2 statement: only the bounded proxy contract was
documented. Calibration is NOT PERFORMED; the full measurement contract and
Java oracle are incomplete. Source inspection was not formal architecture or
owner acceptance. Full F1→F2 and F2→F3 gates have not passed.

## Stage transitions

| Transition | Required condition | Authority |
|---|---|---|
| F0 → F1 | R0-F control records reviewed; exact R0-E configuration and non-claims retained | Repository task owner |
| F1 → F2 | Measurement contract has units, calibration, wrap handling, sample/phase/window rules, result encoding, and failure behavior | Architecture/platform review for any wrapper |
| F2 → F3 | Every target impact and validator is explicit; no public ABI/memory/reserve violation | Build/static validation |
| F3 → F4 | Host proof passes; fresh D81 identity/payload manifest is assigned | D81 loadability gate |
| F4 → F5 | Exact candidate is host structural/content verified | D81 loadability gate |
| F5 → F6 | Two clean Xemu boots of the exact filename/hash pass | Pinned Xemu/ROM evidence |
| F6 → F7 | Exact SD hash, one extent before/after in-place fill, identical allocation, and safe eject pass | Owner/admin/card action |
| F7 → F8 | Physical chooser, runtime capture, and complete attributed measurement matrix are retained | Owner physical capture |
| F8 → closed | Owner explicitly reviews and accepts complete R0-F evidence | Owner only |

## Stop conditions

Stop at `NOT VERIFIED` for missing tools, owner ROM, Xemu configuration, admin
authentication, SD-card movement, MEGA65 operation, platform identity, or
physical capture. A chooser `ERROR CODE FF` retires the tested identity and
requires diagnosis of construction, copied bytes, FAT32 allocation, safe eject,
and platform identity before any replacement. No stage permits measured-limit
selection, Phase 1, or gameplay implementation.
