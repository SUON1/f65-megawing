# Work in Progress

This is the sole routine active-work record, not project history or design
authority. Status is ACTIVE, BLOCKED, READY FOR REVIEW or NONE.

## Current status

- **Status:** `READY FOR REVIEW`
- **Active task:** Compact terminal readiness reporting, owner-authorized by
  “Continue with size-focused revision of terminal reporting” on 2026-10-03.
  Branch `codex/r0f-group1-resume-clock`; freshly verified remote main
  `c27d89787d1d5c4472e24262e0181c47943d46be`.
- **Build Intent:** Fresh copied readiness-01 source; shorten only two failure
  screen strings while retaining every numeric field and non-acceptance label.
  Preserve all readiness/integrity checks and existing boolean interface.
  Fit/host before focused NTSC/PAL and exact-carrier gates. No SD write,
  physical run, publication, Group 2 implementation or acceptance included.
- **Result:** First new variant fits at $BFFC, 4 bytes free. Two shorter strings
  save 22 bytes; executable/protected section sizes match readiness-01.
  Source: `build/r0f/group1/terminal-recovery/readiness-compact-01/source-inputs/`.
  PRG 37516 bytes, SHA-256
  `1c842e345a3d5ec15b3eb167535a776da5e78eaf26a0d0d6239f7073f5a3b468`.
- **Validation:** Native owner/workload/scene/audio/display/pool/CRC and resume
  checks pass, including 83 codec rejects. Dedicated tests pass 18 transport
  cases and 2,624,256 policy comparisons under ASan/UBSan. All 47 Group 1 Python
  tests pass. Focused NTSC/PAL export full 3200-record/20-chunk traces; collision
  case preserves the existing file. Exact source/patch/contract checks pass.
- **Carrier:** Fresh `R0FG1P08.D81`, 819200 bytes, SHA-256
  `9e2030ef8f45077aa29890e60b4d904e37b14b15115e9a6b1611eb0b44849abe`.
  Independent structure/content and all four exact-name NTSC/PAL boots pass.
  State `XEMU_BOOT_VERIFIED` only; SD and physical checks NOT RUN.
- **Impact:** Existing status byte $2F98; new pure diagnostic policy reports
  first rejection, original boolean interface preserved. 6B generic preparation;
  70 policy state, 71 null readiness, 72 acquisition, 73 DMA, 74 display,
  75 audio, 76 IRQ masking, 77 ROM, 78 capsule, 79 NMI, 7A/7B length bounds.
  No new hardware access, allocation, MAP/base-page, DMA, deadline, IRQ/NMI,
  public/generated ABI, capacity or reserve changes. Ordinary C clobbers;
  reporting is outside acquisition. Four bytes are not expansion headroom.
- **Physical boundary:** P07's 6F at tick 3200/mask 1F remains unresolved.
  Its actual returned original payloads and tick-1600 SAVE pass; no trace exists.
  [P07 returned verification](docs/evidence/r0f/group1/2026-10-03-p07-physical/returned/README.md).
  Photo filename/PAL-NTSC confirmation remains unrecorded. Card remains mounted
  unchanged. P07/P06/P05 and earlier tested identities remain retired.
- **Handoff:** [Compact readiness report](docs/reports/R0-F_GROUP1_READINESS_COMPACT.md)
  and [frozen evidence](docs/evidence/r0f/group1/2026-10-03-readiness-compact/README.md).
- **Next action:** Review the qualified P08 diagnostic. Any owner-approved SD
  delivery must use fresh live allocator/hash/one-extent/safe-eject gates,
  followed by physical chooser/entry and one diagnostic observation. No P08
  installer or release manifest prepared yet. Do not repeat completed tests
  or prior installers. Group 1/full R0-F acceptance and Group 2 remain pending.
- **Preservation:** Previous failed readiness builds and all prior freezes,
  CURRENT_STATE, root target source and unrelated work unchanged. No publication.
