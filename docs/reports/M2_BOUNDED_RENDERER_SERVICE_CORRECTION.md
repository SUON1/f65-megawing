# M2 bounded renderer service correction

`65AERO-M2-EXTRES-1-SERVICE1` is **M2 BLOCKED**. This is the single correction and complete link authorized from `53ea27cbcd145be625c6e6602eac1f232e41b0cc`, with main `9570f0ab427121a4e8f042041a14c89aaaeff9e2` as an ancestor. The 20 Hz frame requirement fails before charging the 100 Hz simulation. [Sealed qualification](../evidence/flight-demo/2026-11-08-m2-bounded-service/qualification/result.json)

| Gate | Result |
| --- | --- |
| Extended resident fit | **PASS** at 28,015 / 28,671 bytes, margin 656 and zero protected reserve |
| Production resident fit | **FAIL** by 3,440 bytes at the 24,575-byte ceiling |
| Startup and visibility | Linked prefix, load, BSS, scratch and application MAP checks **PASS**. Fresh BASIC/SYS entry and live firmware identity **UNPROVEN** |
| Stack | Application plus one IRQ and one nested NMI **PASS** statically at 44 hardware and 38 software bytes. Built-in trap path uses 3 separate private stack bytes. Whole-program entry/interrupt conditions **UNPROVEN** |
| Renderer service | **FAIL**. At least 12,626,832 cycles / 311.774 ms for a complete default-view frame at 40.5 MHz. Allowed 2,025,000 cycles / 50 ms before simulation |
| PAL and NTSC Xemu | **NOT RUN**. Visuals, runtime cadence, tick continuity and target faults **NOT OBSERVED** |

## Source and linked image

Graphics captures the validated camera and generation at BEGIN. Each ordinary batch charges a positive cost per existing continuation, with one complete camera and generation validation at entry and another on safe exit. BEGIN and COMMIT run separately. COMMIT validates all registration fields, rechecks coherence before selecting the completed store and latches the matching record without yielding. A pose change with the same revision cancels the hidden frame. Invalid ownership and generations, hardware faults and overflow enter the terminal path. Insufficient credit yields with private work intact. No snapshot slot is held across a batch. The nine canonical segments are prepared once per generation with the existing precision and command sequence.

Main alone drives camera writes, snapshot-producing ticks and renderer calls. The linked handlers write only raster acknowledge `$D019`, IRQ bookkeeping `$8776`, `$8777`, `$877B`, `$877C`, and sticky NMI `$8775`. They have no C calls, compiler direct-page access, MAP or trap. Platform copy checks its own physical destination and near source. It keeps the PF001 scratch at `$0222–$0229` separate from the handlers. The exact budget inequality is `Σ step_cost ≤ release − now − fixed_guard_cost − 1`, with `uint16_t` saturation and each positive cost charged before work. Native grants, guard grant and launch are zero in BSS with no enabling writer. Camera validation, eligibility, budget arithmetic and atomic publication checks remain in the linked closure.

| Bank-zero resident component | Previous bytes | SERVICE1 bytes | Change |
| --- | ---: | ---: | ---: |
| BASIC header | 22 | 22 | 0 |
| `.text` | 22,811 | 23,821 | +1,010 |
| Alignment | 6 | 4 | −2 |
| `.rodata` | 2,115 | 2,115 | 0 |
| `.data` | 0 | 0 | 0 |
| `.bss` | 2,016 | 2,000 | −16 |
| Compiler `.noinit` | 53 | 53 | 0 |
| **Total** | **27,023** | **28,015** | **+992** |

The PRG is 25,964 bytes including its two-byte load address. SHA-256 `567a7b0425598ffc049d4b82bcd8bdd82c09d7aef6bcd8523ac1063cdda4fbdd`. Its payload is `$2001–$856A`, with 1,387 bytes of read-only data above `$8000`. Executable `.text` ends before `$8000`. BSS `$856B–$8D3A` and scratch `$8D3B–$8D6F` are zeroed after normalization. The hardware stack envelope is `$0100–$01FF` and the software stack envelope is `$C000–$CFFF`. Other owner allocations, the generated public contracts and the production ceiling are preserved. The pinned SDK digest and compiler flags match the prior link. The target source archive verifies all 120 archived build-input identities. [PRG](../evidence/flight-demo/2026-11-08-m2-bounded-service/target/UNADMITTED.prg) · [Link accounting](../evidence/flight-demo/2026-11-08-m2-bounded-service/target/result.json) · [Target seal](../evidence/flight-demo/2026-11-08-m2-bounded-service/target/seal.json)

## Service accounting

The default-camera host witness reaches a complete frame. Its role counts, 3,456 divider bits and 96 runway pixel writes follow the same linked control flow and exact numerical kernels. The minimums allow optimistic branches, subtract the separately charged copy and divider loop bodies, and omit the cost of outer role calls and scheduling. The CPU envelopes include callees and returns. They deliberately overbound loop paths, including paths that cannot all occur in one call. They are too loose to admit deadlines or assign native-clock budgets. [Host witness](../evidence/flight-demo/2026-11-08-m2-bounded-service/host-1794156888511030000/host.txt) · [Static service records](../evidence/flight-demo/2026-11-08-m2-bounded-service/qualification/result.json) · [Pinned Xemu opcode timing](https://github.com/lgblgblgb/xemu/blob/40dfef0d1d5f56be2469492715c12bdb32c75b67/xemu/cpu65_mega65_timings.h)

| Role | Complete-frame calls | Minimum cycles per call, excluding separate loop bodies | Conservative CPU cycles per call |
| --- | ---: | ---: | ---: |
| BEGIN | 1 | 82 | 20,261 |
| PREPARE | 585 | 44 | 1,103,542 |
| PROJECT | 5,868 | 168 | 603,024 |
| BACKGROUND | 5,120 | 1,703 | 16,582 |
| COPY | 960 | 105 | 41,421 |
| LINE | 115 | 20 | 42,233 |
| TEXT | 320 | 325 | 62,854,144 |
| COMMIT | 1 | 150 | 504,041 |

The painter charges at least 293 cycles for row setup, including the linked 16-bit tile-index division, eight pixels at at least 170 cycles each, and 50 cycles of exit work. This gives 8,719,360 cycles / 215.293 ms across BACKGROUND. The 61,536 required physical writes consume at least 1,599,936 cycles in the flat-copy loop. The required seven-byte remainder shift per division bit adds at least 1,088,640 cycles. Transfer and remainder loops alone require 2,688,576 cycles / 66.385 ms. Summing their disjoint work with all eight role minimums gives 12,626,832 cycles / 311.774 ms. It excludes the positive overheads below and allows at most 3.2075 Hz even before that work. Five authoritative 100 Hz ticks must also fit in the 50 ms interval.

A full equal camera check costs at least 1,514 cycles in the linked comparison, including the two successful `memcmp` calls and returns. It is bounded by 1,908 CPU cycles. Ordinary batches call it twice and a successful COMMIT calls it three times. The old linked image did 5,120 full checks during BACKGROUND alone. The new code charges per batch, so the batch count depends on admitted linked costs and clock slack. The 932 host test batches use synthetic mixed-cost credits and establish behavior only.

| Fixed or per-step accounting | Conservative CPU cycles |
| --- | ---: |
| `m1_platform_now`, including at most 32 coherent samples | 6,111 |
| Deadline guard | 522 |
| Main poll, guard and outer dispatch call through next poll | 6,981 |
| Dispatch entry and exit with coherence and return | 9,343 |
| Ordinary per-step bookkeeping, call, role selection and fault probe | 359 plus role envelope |
| Application IRQ / NMI, each including 7-cycle entry and RTI | 101 / 26 |
| Fixed batch cost with up to two raster IRQs and one NMI | 16,552 |
| `m2rb_io_commit`, including readback and return | 304 |
| Normal tick path including input, release update, clock and interrupt allowance | 864,989 |

The IRQ allowance covers a pending raster IRQ and one new raster IRQ in a 10 ms interval. The NMI term assumes a single edge followed by a terminal fault. A `JSR` and `RTS` each cost five cycles under the pinned fast-mode table. The conservative tick envelope exceeds the 405,000-cycle period and establishes no deadline admission. A usable guard would also require PAL/NTSC native-clock conversion, sample age, raster prefetch and commit-window bounds. A late NMI may follow physical selection of a complete validated frame. Fault latching remains terminal and there is no target observation of that interleaving. The whole-frame lower bound establishes failure independently of any tightening of these envelopes. [Pinned Xemu CPU and interrupt accounting](https://github.com/lgblgblgb/xemu/blob/40dfef0d1d5f56be2469492715c12bdb32c75b67/xemu/cpu65.c)

## Startup and CF001

The independent raw-image replay verified the BASIC payload and canonical prefix order, the stack-free early terminal loop, all 2,000 BSS bytes and 53 scratch bytes, 15 cartridge input cases and three fail-closed visibility cases. It matched the PRG to ELF load sections and found three MAP instructions used for canonical normalization. Application code uses no covering MAP window. Pinned Xemu injects the contiguous `$2001` payload into main RAM at READY and issues RUN. Static proofs apply once the expected entry bytes are CPU-visible. [Pinned direct-PRG loader](https://github.com/lgblgblgb/xemu/blob/40dfef0d1d5f56be2469492715c12bdb32c75b67/targets/mega65/inject.c)

The linked CF001 wrapper at `$2225` saves P/X/Y/Z/B, masks IRQ, and requests trap 0 at `$222E` with `A=$70` and a following `NOP`. The current contract supplies canonical MAP, B `$02`, DDR/data `$2F/$35`, page-one stack and VIC-IV I/O. The ROM backup and readback precede the transition. The independently fetched Xemu source and exact installed emulator match a 16,384-byte built-in HICKUP array at file offset 631,104. Its SHA-256 is `21f5b58549c61a886bfcdd4e73e3200b2c36790b8ba21ad6bbdaa59fefb8e7a4`. Exact path `$8000 → $8C04 → $8CC3 → $8216 → $A224 → $8219` ends at the `$D67F` leave write. This path flips ROM protection bit 2, reports A and carry, and unmaps the SD buffer via command `$82` with no media transfer. [Pinned trap I/O](https://github.com/lgblgblgb/xemu/blob/40dfef0d1d5f56be2469492715c12bdb32c75b67/targets/mega65/io_mapper.c) · [Pinned HICKUP bytes](https://github.com/lgblgblgb/xemu/blob/40dfef0d1d5f56be2469492715c12bdb32c75b67/targets/mega65/memcontent.c) · [Pinned buffer command](https://github.com/lgblgblgb/xemu/blob/40dfef0d1d5f56be2469492715c12bdb32c75b67/targets/mega65/sdcard.c)

The privileged path runs in a private window with B `$BF` and stack at `$BEFF`. Its 3-byte hardware-stack peak is one return address and one saved accumulator. Xemu defers IRQ and NMI service while privileged. The path stores to saved A/P and the feature, unmap and leave registers. It leaves user RAM, application SP, D030 and cartridge registers intact. Xemu restores the saved CPU/MAP/port/I/O/DMA-list context, and the app wrapper restores its saved P/X/Y/Z/B. The app rejects a bad carry, B or ROM-protection result before starting its clock. Other return invariants depend on the pinned trap behavior. Fresh ROM entry before vector installation, pending/queued NMI or traps, and the running HICKUP identity after boot remain unobserved. [Pinned Xemu transition](https://github.com/lgblgblgb/xemu/blob/40dfef0d1d5f56be2469492715c12bdb32c75b67/targets/mega65/hypervisor.c) · [Pinned memory visibility rules](https://github.com/lgblgblgb/xemu/blob/40dfef0d1d5f56be2469492715c12bdb32c75b67/targets/mega65/memory_mapper.c)

The smallest startup evidence still needed is a separately authorized boot-only trace, with workload disabled, on the pinned ROM and emulator under fresh PAL and NTSC configurations. Capture HICKUP and pending NMI before SYS, then MAP/B, CPU ports, ROM/cartridge state, stack, resident bytes and the terminal fault outcome immediately before and after CF001. Full runtime admission remains blocked by service independently of this trace.

## Verification and preservation

- Host ASan/UBSan and contract checks passed, including 932 mixed-cost and same-revision camera batch cases, 6,453 numerical cutpoint cancellations, held snapshots, fault/exhaustion tests, 16,588,800 exact horizon pixels and replay `DE675132`. The Decimal geometry oracle passed 3,857 cases and 841 near/far cases. [Host commands and results](../evidence/flight-demo/2026-11-08-m2-bounded-service/host-1794156888511030000/result.json)
- Independent checks passed 3,252 arithmetic cases and 117,072 carry cells, 1,360 transforms, 4,080 clip/projection comparisons, 32,768 camera cases and 4,121 raster lines. [Independent results](../evidence/flight-demo/2026-11-08-m2-bounded-service/independent-1794156948965229000/run/bigint-native-oracle.txt)
- One complete target link passed the static fit gate using `python3 -B tools/flight_demo/m2_rebuild/commands_validate.py --tier target --profile extended-service --sdk /Users/slice/Developer/f65-megawing/toolchain/runtime/llvm-mos`. The checker replay deliberately exits 1 after reporting service FAIL. All 15 startup/stack verifier regressions and 16 static CI policy tests passed. [Exact commands](../evidence/flight-demo/2026-11-08-m2-bounded-service/qualification/commands.json)
- The original 109 sealed members and 480 unrelated paths matched by size and SHA-256. Six available historical checkouts matched HEAD and status. Two missing temporary checkouts remain **NOT VERIFIED at the Git-worktree tier**. The new linker map is stored losslessly, with raw SHA-256 `9aa0df5cd052fddf3dbbd0a2ebd18a48f165cf1285424b5c027fd027c7c7a4b7`. Focused hygiene against `53ea27c` passed. Main-range hygiene produced byte-identical failure output before and after the correction, covering 18 lines in the two sealed maps and 19 lines in the historical hygiene transcript. Those files retain their original bytes. [Preservation record](../evidence/flight-demo/2026-11-08-m2-bounded-service/qualification/preservation.json) · [Prior checkpoint failure](../evidence/flight-demo/2026-10-30-m2-extended-resident/publication.json)

The minimum next implementation task is a single measured throughput correction for exact numeric preparation/projection and hidden-store construction. The painter alone exceeds 50 ms, and the numeric path plus flat copies exceeds it independently. Require a linked complete-frame recovery of more than 10,601,832 cycles plus all scheduling costs. Keep the existing pixel, numeric, ownership, publication and authoritative timing contracts as acceptance criteria. Further renderer work awaits founder review.
