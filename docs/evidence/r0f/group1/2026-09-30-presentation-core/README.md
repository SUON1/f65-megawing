# Isolated Group 1 presentation policy evidence

The isolated kernel passes host ASan/UBSan, 720 priority-anchor permutations,
2592 independently enumerated occlusion cases, 131072 size-LOD comparisons,
view/common-identity/overflow rejection, four private-contract tests and pinned
LLVM-MOS target-object compilation. It is not linked into the acquisition.

Command, from the repository root:

```sh
python3 -B tools/diagnostics/r0f_group1_presentation_build.py
git diff --check
```

Both exit 0. `build/validation.json` retains individual compiler/test commands,
host output and all thirteen input hashes. The source inputs, including generated
diagnostic parameters and governing design/matrix bytes, are retained here.
Target object SHA-256 is
`6773993f99434b12a230c5e8b4cf6fb683343280823e2870ac70a3db9e2bcc6a`.
Host native state is 138 bytes; this is not target-linked accounting or stack
evidence. The baseline guard also rejected a copied metadata object with a
false PRG hash before any write; no original input was altered for that check.

The existing integrated PRG remains
`c249f4e4da972cdc0c5d0958a1a3a148387eb1ad4de602404c6b79fb7c79492b`
and all 74 build inputs match before/after. Its full NTSC and PAL evidence
remains in the separate preceding freezes. The original `ec259fc7...` and
corrected `0d96a1b...` baselines remain preserved. Branch is
`codex/r0f-successor-physical-exact-carrier`, HEAD
`9e2ffdb4786e4794119933a5edd4b1cf79f653f0`, plus retained dirty inputs.

The [frozen checkpoint report](report.md)
maps this narrow slice and remaining obligations. Graphics rules informed
complete-pair publication, priority anchors, presentation-only clipping and
stable tier binding. Capacities/thresholds are generated private fixture
parameters, not production limits. Native C records are not a public wire ABI.
No registers, physical allocation, MAP/base-page, DMA, deadlines or IRQ/NMI
semantics change because the new kernel is not integrated.

`sha256.json` pins this evidence. Target link/fit/stack/timing, actual VIC
publication, integrated presentation/pool coverage, angle-bin hysteresis,
terrain/carrier registration, near-capacity acquisition, operator summary and
exact-name carrier gates remain open. No new-kernel Xemu run, SD write,
physical test, commit, push, hardware readiness or acceptance is claimed.
