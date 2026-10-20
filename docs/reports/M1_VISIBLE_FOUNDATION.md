# M1 visible 65Aero foundation

## Authority and boundary

Founder-authorized [entry-plan Build Intent](../plans/65AERO_PHASE1_ENTRY_AND_DEVELOPER_FLIGHT_PLAN.md#8-next-fresh-window-m1-first-pr-build-intent), following adoption [PR #17](https://github.com/SUON1/f65-megawing/pull/17), merged at `df1347b663c960e307870268f0b08ceaa6988d5c`. Local, fetched and GitHub main agreed; post-merge hygiene run `39456914587` passed. Implementation is local on `codex/65aero-m1-visible-foundation`; M1 publication is not authorized.

Inspected authority: Main 1.8, Gameplay 1.2, Runtime 1.2 candidate (including its incorporated Runtime 1.1 PDF), Physics 4.1, Graphics 2.1, development workflow, programming principles and C standard. Runtime remains a candidate. This is a fixed-view NON-FLIGHT DIAGNOSTIC, not a flight model, production graphics implementation, R0-F PASS, physical timing proof or carrier qualification.

The development schema `interfaces/m1_development.json` is the sole source for the M1 generated constants/records and memory ledger. These are not production ABI layouts. Existing generated public interfaces and retained R0 source/evidence are unchanged. The explicitly selected legacy JDK is `/Users/slice/Documents/Codex/f65-megawing/toolchain/runtime/jdk-full/jdk-21.0.12+8/Contents/Home`; `bin/java -version` reports Temurin 21.0.12+8, matching the lock version. Python generation/build does not invoke Java; the JDK-dependent retained generators are not rerun or replaced.

## Owner contracts

- CoreRuntime owns the tick, bounded FIFO of tick-tagged semantic edges, deterministic application and checksum. Stage 1 increments; stage 2 latches the eligible batch; stage 3 applies it; stages 4–18 are explicitly disabled; stage 19 extracts; stage 20 hashes explicit authoritative fields and future queued commands; stage 21 publishes. No equal division of 10 ms across stages is assumed.
- Input owns edge detection. Holding SPACE creates no repeated commands. Rejection leaves queued commands intact, latches an authoritative fault, and does not advance input's accepted previous state.
- Presentation owns three immutable snapshot slots. Full publication rejects with a separate presentation counter; it does not mutate the authoritative checksum. Acquisition chooses the newest available complete snapshot and frees only older READY slots. HELD slots cannot be overwritten. Graphics takes a value copy before releasing its slot.
- Graphics owns an inactive 80×25 character store and renders one bounded row per service. World and overlay share one snapshot and one display store. Only a completed, newer generation may swap; cancellation retains the previous store. After completion the dispatcher arms a fresh frame-counter transition before swapping. Fixed blue sky and green ground use immutable color RAM; there is no terrain/runway projection or aircraft state.
- The overlay reports hexadecimal counters sampled at frame construction: current/source tick, semantic command count, checksum, published count, displayed generation, source age and maximum CIA-count debt. Altitude and airspeed remain NOT IMPLEMENTED. The sampling labels are explicit; displayed source age also remains available as live diagnostic memory.
- The scheduler advances a Q16 release deadline, services overdue ticks in order and never merges ticks. Rendering is subordinate to debt. Semantic faults appear in snapshots; fatal platform faults freeze work, set a red border and preserve a diagnostic status (255 initialization, 254 sticky platform/NMI, 253 row-copy, 252 swap/commit). There is no invented production deadline threshold.

## Inspected platform seam and effects

The narrow `src/platform/m1` adapter calls unchanged CF001/PF001 primitives from `combined_platform.c`, `combined_model.c`, `qualification_45gs02.s`, `combined_45gs02.s`, and `r0a_platform_45gs02.s`, under the retained R0-F platform qualification and CIA timing contracts. Their reuse is limited to this reset-only emulator development profile, not promotion to production Platform ABI.

| Operation | Effects and ownership |
|---|---|
| Entry | SEI/CLD, MAP clear/EOM, CPU port `$35`, VIC-IV unlock `$D02F`, ROM selection `$D030`, canonical B=`$02`; page-1 hardware stack. Local `$FFFA/$FFFE` vectors, CIA masks and raster IRQ setup replace ROM ownership. Entry is not register-preserving. |
| Flat copy | Unchanged CF mailbox `$0222–$0229`, 1–255 bytes; M1 restricts callers to a single 80-byte display/color row. Wrapper preserves X/Y/Z/B/P/SP; A is result (Q overlaps A). CPU-visible local buffers are in bank 0; physical destination is explicitly 32-bit. No ordinary pointer impersonates a physical pointer. |
| ROM-backed display storage | `cfrom_begin` backs up `$020000–$03FFFF` to Attic `$08000000–$0801FFFF`, compares blocks/CRC and uses the retained `$D640`/A=`$70`/NOP protection toggle. Displays consume only 2000 bytes at `$020000` and `$030000`. No ROM calls are permitted after takeover. Reset-only exit; backup is retained, ROM return/restoration is not attempted. |
| Clock | CIA1 timers A/B cascade, bounded coherent B/A/B read. Calibration measures 16 complete video frames and applies the pinned Xemu PAL/NTSC cycle ratio. Logical 100 Hz is nominal emulator timing; physical SI accuracy remains open. No IRQ calls C. IRQ saves/restores A/X/Y/Z/B and P/PC via RTI; sticky NMI invalidates the run. |
| Display/input | Static color RAM `$0FF80000–$0FF807CF`; border/background `$D020/$D021`; screen pointer `$D060–$D065`, meaningful store selector `$D062`; frame `$D7FA`; video mode `$D06F`; SPACE is direct keyboard matrix row 7 bit 4 through `$D614/$D613` (pinned Xemu matrix index 60). No ownership claim outside this profile. |
| DMA/audio/storage | No DMA list allocation/submission and no audio service/start. No runtime storage dependency. Emulator boot uses disposable in-memory virtual media, never a D81, file-backed SD image or physical device. |

Memory: code/data/runtime support must fit `$2001–$7FFF`; hardware stack `$0100–$01FF`; base page `$0200–$02FF`; inherited result block `$1900–$1FFF`; software stack `$C000–$CFFF`, top `$D000`. `$058000–$05FFFF` reserve allocation is zero. Map sections and owner symbols account actual linked usage; stack watermark is measured at tick 600, not inferred from the 4096-byte envelope. The inherited stack-seeding primitive excludes live frames; the watermark is observational, not a proof of all possible paths.

## Reproduction and evidence

```
python3 -B tools/flight_demo/build.py
python3 -B tools/flight_demo/xemu.py replay 0
python3 -B tools/flight_demo/xemu.py replay 1
python3 -B tools/flight_demo/xemu.py slow-render 0
python3 -B tools/flight_demo/xemu.py slow-render 1
```

Build emits `build/flight-demo/m1/build.json`, native ASan/UBSan results, three PRGs, maps, symbols and disassemblies. The build record hashes schema, generated outputs, source/headers, scripts, tests, linker script and toolchain lock. Compiler and objdump identities are verified against the lock. The emulator runner rechecks inputs and exact PRG bytes, pinned emulator/ROM, records SDL/configuration hashes, and retains each attempt in a unique directory. It creates a hash-identical application bundle with SDL's `Contents/Resources/mega65/prefdir-is-here.txt` isolation marker and a read-only copy of the existing I2C configuration. Logs must confirm the isolated preference path for PASS. A normal visible onboarding Return/reconfiguration may be required; no target code or result is patched by the runner.

Host acceptance compares checksums at every tick across presentation disabled and divisors 1/3/17. It checks stage order, input edges, queue exhaustion/invalid commands, held-reader/full-slot rejection, incomplete cancellation and obsolete generation rejection. Tick 600 has 23 commands and checksum `DE675132`; the emulator validator independently calculates the recurrence from the semantic script. Interactive mode uses real keyboard input and is built separately from scripted replay.

Early boot-only, missing-library and preference-fallback attempts remain in their original output directories and do not qualify as final acceptance. Logs may contain standard pinned-Xemu startup warnings; target status, source identity, checksum and isolation are evaluated explicitly.

Final evidence is retained under [2026-10-20-visible-foundation](../evidence/m1/2026-10-20-visible-foundation/). Raw logs, maps, symbols, disassembly, PRGs and memory dumps remain at the exact local build paths recorded in each result. Full dumps may contain owner ROM bytes and are deliberately excluded from the review packet; their hashes remain in the results. No ROM, emulator binary, SD image or D81 is added to tracked evidence.

The current three target profiles pass compile/link/static checks. Native tests pass under AddressSanitizer and UndefinedBehaviorSanitizer; generated outputs regenerate byte-identically. `python3 -B -m unittest discover -s tools/ci -p 'test_*.py' -v`: 14 passed. `python3 -B tools/diagnostics/r0a_validate.py .`: PASS. Source identity, local links, tracked-source preservation and scoped whitespace checks pass.

| Profile | PRG bytes | Text | Read-only data | BSS + noinit | Resident end (exclusive) |
|---|---:|---:|---:|---:|---:|
| Interactive | 9348 | 8865 | 459 | 820 | `$47B7` |
| Replay | 9723 | 9240 | 459 | 820 | `$492E` |
| Slow renderer service | 9719 | 9236 | 459 | 820 | `$492A` |

Initialized data is zero bytes. Core state is 64 bytes, snapshot pool 46 bytes and graphics state 38 bytes on target; these are included in BSS, not additional allocations. The build JSON includes other owner symbols and complete source/tool identity. All sections fit below `$8000`; no reserve allocation occurs.

Final execution matrix (tick-600 checkpoint; end-of-run tick/generation vary with onboarding duration):

| Profile | Result | Checkpoint checksum | End tick | Display generations | End source age (ticks) | Max debt (CIA counts) | Stack HW/SW bytes |
|---|---|---|---:|---:|---:|---:|---:|
| pal-replay | PASS | `DE675132` | 1316 | 658 | 4 | 540 | 31/108 |
| ntsc-replay | PASS | `DE675132` | 8394 | 5021 | 3 | 542 | 31/108 |
| pal-slow-render | PASS | `DE675132` | 8057 | 4034 | 4 | 502 | 31/108 |
| ntsc-slow-render | PASS | `DE675132` | 8576 | 5129 | 3 | 537 | 34/108 |

All four saved screens were visually inspected: complete sky/ground, legible protected overlay, NON-FLIGHT DIAGNOSTIC, altitude left and airspeed right NOT IMPLEMENTED. Renderer service pacing changed; vsync still limits visible cadence. Host tests independently vary actual presentation cadence and disable presentation entirely. Maximum observed stack usage across these runs is 34 hardware bytes and 108 software bytes; this is emulator observation only.

**Status: READY FOR REVIEW.** Review the focused owner modules, generated development contract, reset-only platform seam and retained evidence. No M1 commit, push, PR or merge was performed; no further milestone work is authorized by this handoff.

## Remaining boundaries

No physical timing/boot/runtime, D81, SD transfer/allocation, production ABI, production audio/storage, aircraft coefficients/gains, physics, mission/combat/AI or reserve borrowing. This small development text renderer does not establish the later Graphics pipeline budget. Snapshot rejection and frame pacing must remain presentation-only in future work. Review precedes any M1 publication or wider milestone work.
