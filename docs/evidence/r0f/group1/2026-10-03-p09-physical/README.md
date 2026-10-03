# P09 physical resume, export and nominal timing proof — 2026-10-03

**PASS for this bounded physical fixture.** The actual returned P09 image
contains the qualified program, the returning SAVE and all twenty trace chunks.
The independent version-7 reducer validates 3200 tick records across returning
storage and reports WITHIN_OBSERVED_BOUNDS: zero nominal deadline misses, zero
cohorts below 20 Hz and zero boundary-uncertain ticks. This resolves the physical
resume/export blocker for P09. It does not grant full Group 1/R0-F acceptance,
approve measured limits, start Phase 1 or implement Groups 2/3.

## Authority and effects

Owner supplied the successful photo, then “Cards in.” authorizes read-only
returned-card verification and local evidence preservation. Current WIP,
Group 1 Build Intent, export amendment, measurement matrix, generated export
contract, development workflow and D81 gate/workflow govern. Branch remains
`codex/r0f-group1-resume-clock` at `c27d89787d1d5c4472e24262e0181c47943d46be`.
Only this evidence packet, ignored returned snapshot/protection guard and WIP
are added/updated. Target registers/clobbers, CPU-visible/physical allocations,
MAP/base-page, DMA, timing/deadline and IRQ/NMI effects are non-applicable.
Generated/public ABI, source, capacities, prior freezes and CURRENT_STATE remain
unchanged. No new target build, emulator run, SD write, filesystem check/repair,
raw allocation audit, unmount/eject or publication occurred.

## Delivery, identity and provenance

Retained owner installer records pass read-only pre/post filesystem checks,
staged/final/mounted canonical hash, one 819200-byte extent at device offset
66383872 (first cluster 2280), and safe eject. File count rises 187 to 188;
free space falls 800 KiB/200 clusters. The raw extent records establish
contiguity separately; no new raw audit was performed on the returned card.

The live removable FAT32 volume is UUID
`83FFC12E-67E1-307F-91AD-E584C2E01E87`, currently disk4s1. The mounted P09 was
copied to a new host-only snapshot and compared again after extraction and
analysis. Independent chain/BAM parsing and pinned c1541 extraction agree on
24 closed entries: AUTOBOOT.C65, R0FSUCC, TOKEN, RSSTATE and G1T00-G1T19.
All three original payloads match canonical exactly. No emulator bytes were
substituted. The complete snapshot remains locally at
`build/r0f/group1/carriers/R0FG1P09/returned-01/R0FG1P09.D81`.

- Canonical D81: `bd1b645630c93d0ef764f3b6167924c0962ad67ed528d4ac8172ff2d4f9c5959`.
- Returned D81: `ccd989151603fcfbeb130436c7be705e9b6f18804ce52012e142bdad1199a8ea`.
- Actual program, 37509 bytes: `acc735f280f9d4e86b3b2040e5b2bed987908331f7899a87f5382c6cd23cd4d8`.
- Actual trace, 327680 bytes: `e83b0b526c6fe22bb66285a93a25b8107da7c5c112d06f8ceb77af4cf6cc66dd`.
- Actual SAVE, 34 bytes: `7d2f63b8e8e970bb35c351174fae1ca365245f14acf35db0d3cf9016ba8ba5bd`.

The photograph reads S4/E00/F14 with green border, matching twenty successful
SAVE calls. It follows the P09 handoff, and the actual returned P09 contains
the exact program and complete physical data; explicit spoken filename
confirmation was not recorded. The trace records hardware-reference byte 2
and video-register byte $87. Fresh named core/ROM/HYPPO/Freezer versions were
not recorded and must not be copied from emulator metadata. Owner-reported
drive noise is retained as an observation; its precise cause is not established
by this packet.

## Actual physical checks

Each trace chunk is 16386 bytes including $4000 load address. Concatenating
only the twenty payloads yields the exact 327680-byte version-7 trace. Its
length, CRC, 3200 ordered records, model and AI lineage, snapshots, presentation
pairs, pool observations, service phase/order masks, IRQ/DMA progress and
capacity tail all pass the frozen decoder's existing checks.

The actual 512-byte result reports fault 0, lifecycle 9, ticks 1600 -> 3200,
checksums 6B765FDB -> 607348BD, resumed-service mask 1F, NMI 0, original context
invalidated, canonical base page 2 and CPU port $35. ROM, reserve, low-memory
and DOS before/after comparisons pass. Result CRC F05F2BCE matches independent
calculation. Actual RSSTATE loads at linked $3063 and matches the independent
tick-1600 model and payload encoding.

There are 16 measured cohorts before storage and 16 after it. Complete-world
cadence ranges approximately 28.134-30.123 nominal Hz before storage and
28.115-30.120 after it. All 955 retained complete-world pairs validate.
IRQ body-read intervals are nonzero in both epochs: 972 samples each, maxima
7 and 8 counter counts. These are not whole-ISR cost or entry-latency claims.
Hardware/software stack observed high-water is 67/123 bytes. Of the trace,
310580 bytes comprise real evidence including CRC; 17100 bytes are the declared
non-timing capacity-tail pattern, not fabricated workload observations.

See [physical verification](physical-verification.json),
[actual reduction](returned/reduction.json),
[extraction verification](returned/snapshot-verification.json) and
[exact reducer command and identity](returned/reducer-command.json).
The command uses the qualified copied-source version-7 decoder and independently
linked payload address, not the older root decoder. The generic frozen decoder
emits `physical: NOT RUN` as a fixed harness default; its raw output is retained
verbatim. `physical-verification.json` supplies actual card/photo provenance.
The historical Java T04 oracle is fixed to ticks 33/66 and payload $29C4 and
was not run or claimed as a Group 1 oracle PASS.

## Disposition and next work

P09 is preserved as a successfully tested physical identity, protected against
rerun, overwrite, repair or rename by its local guard. Earlier failed identities
remain unchanged. The card remains mounted and unchanged.

Review this bounded physical proof, then continue the originally approved
remaining R0-F campaign/Groups 2-3 with their applicable task intent and existing
admission/matrix boundaries. Do not replay these passing tests or invent a new
production feature checklist. SI uncertainty, universal phase/pool pressure,
whole-ISR and external latency, and production-renderer coverage remain their
existing boundaries. Owner acceptance and measured-limit approval remain named
decisions, not implications of the successful screen or a future Git merge.
