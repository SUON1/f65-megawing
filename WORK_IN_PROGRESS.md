# Work in Progress

- **Status: BLOCKED.**
- **Task:** M2 Extended Resident Profile and Xemu Admission, private identity `65AERO-M2-EXTRES-1`.
- **Base:** reviewed `aed5bfb2014e8f3df28118668e5f24ded0ddad9e`; fetched main remains `9570f0a`. Branch `codex/65aero-m2-extended-resident-admission`.
- **Authority:** Founder conditionally approves development-only resident end `$9000`; [versioned contract](interfaces/m2_extended_resident.json). Production `$8000`, public ABI, precision, owners, 100Hz/21 stages, retained 20Hz world floor and zero reserve remain.
- **Scope:** Implement residency/visibility and covering-MAP/staging exclusion; fresh complete pinned target link; exact startup/stack/interrupt/fault/service gates. Direct-PRG PAL/NTSC Xemu only after every mandatory gate passes. Stop at a failed gate with exact blocker and smallest correction.
- **Result:** [Measured admission checkpoint](docs/reports/M2_EXTENDED_RESIDENT_ADMISSION.md): corrected PRG `02430394…a1d48b9` fits at 27,023/28,671 (margin 1,648), zero reserve. Raw load/initialization and conditional application-stack checks pass. Whole-program privileged startup/stack remains UNPROVEN; normal-world service FAILS (background camera checks alone ≥152.968ms versus 50ms). PAL/NTSC Xemu NOT RUN.
- **Next:** Founder review of the preserved checkpoint. Smallest correction is bounded service-control batching with full coherence/deadline checks, plus unresolved privileged boot/entry/stack proof; not started. Launch/service grants remain zero. No further target link or optimization.
- **Publication:** Staged static whitespace FAILS on two unchanged sealed raw linker maps. Preserve their bytes and existing CI policy; push as a blocked checkpoint, no PR/merge or implicit exception.
- **Boundary:** Preserve PR30/31, prior failures, sealed packets, all other worktrees and 480 unrelated paths. No banking, further size optimization, ceiling expansion, D81, SD or physical work. Push verified progress; no merge without founder review.
