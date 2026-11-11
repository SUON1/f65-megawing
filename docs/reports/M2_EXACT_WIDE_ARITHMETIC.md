# M2 exact wide arithmetic

`65AERO-M2-EXACT-WIDE-1` is a private compile-only option on
`codex/65aero-m2-exact-wide-arithmetic`, based on
`5ccfe124b53af6a755819d6ae4da3fc1ded0de02`. The founder approved the bounded
arithmetic backend and its proof. The existing `M2LimbJob` call sites, command
interpreter, camera, renderer, display stores, public ABI, generated contracts
and 100 Hz / 21-stage timeline are retained. `M2_EXACT_WIDE` selects the new
private implementation. With the option absent, the portable byte-limb
implementation is unchanged. The launch and all operation/guard grants
remain zero. [Throughput baseline](M2_THROUGHPUT_ARCHITECTURE_CORRECTION.md)

## Platform transaction and ownership

The only owners of the new I/O sites are the foreground
`m2rb_math_product` and `m2rb_math_q24` call paths through `math_transact`
and `math_ready`. Under canonical MEGA65 I/O, the CPU status register is
`$D70F` and the math window is `$D768–$D77F`. Their physical Fast I/O
aliases are `$0FFD370F` and `$0FFD3768–$0FFD377F`. The gateway reads the
status, writes `$D770–$D777`, and reads either the full eight-byte product
at `$D778–$D77F` or quotient bytes 1–4 at `$D769–$D76C`. Graphics passes
ordinary little-endian operands and receives ordinary bytes. The ordinary
LLVM-MOS C ABI applies. The transaction preserves canonical MAP/B,
CPU DDR/data, ROM/I/O visibility and interrupt masks. It submits no DMA,
calls no firmware, and yields only after it has returned.
[Platform registry](../../interfaces/f65_platform_abi.json5) ·
[MEGA65 I/O map](https://github.com/MEGA65/mega65-core/blob/development/iomap.txt) ·
[Pinned mapper](https://github.com/lgblgblgb/xemu/blob/40dfef0d1d5f56be2469492715c12bdb32c75b67/targets/mega65/memory_mapper.c)

A BSS owner byte starts idle at reset. A pre-existing Platform fault or
busy status rejects entry and locks subsequent calls until reset. After
acquisition, the gateway writes four operand pairs and reads status up
to eight times. It copies its staged output only after readiness, an
active-owner check and a second Platform fault check. A timeout or
re-entry returns failure with caller output unchanged and latches
lockout. An invalid quotient denominator is rejected before acquiring
the device. The existing NMI handler may interrupt the gateway and sets
the sticky Platform fault without accessing the math unit. If it arrives
after the last gateway fault check, the next Graphics continuation
boundary observes the fault before frame publication. The IRQ only
acknowledges the raster interrupt and updates its counters.
[Gateway](../../src/platform/m2_rebuild/wide_math.c) ·
[Graphics fault boundary](../../src/graphics/m2_rebuild.c)

The raw link audit covered 12,309 application instructions including
the reset prefix, and 30 IRQ/NMI instructions. It found two status-read
sites and four indexed operand/result sites. The latter derive from
bounded offsets on explicit I/O constants, with the ordinary C ABI
invariant `Z=0`. The two PF001 physical-indirect instructions are
reachable only through the checked CF001 copy and M2 display/color
adapter. Their physical ranges are disjoint from the Fast I/O window.
The other variable I/O addresses are the CF001 startup message and
identity reads, VIC register pairs and palette writes. Their source
bounds also exclude the math window. No interrupt calls a C helper,
changes MAP or reaches a math-register site. The sole privileged trap
occurs during startup, before the arithmetic path. Ownership is proved
for this linked application under its existing canonical entry
conditions. An external concurrent master and physical accelerator
latency require separate qualification.
[Linked audit](../evidence/flight-demo/2026-11-09-m2-exact-wide/qualification/result.json)

## Exact arithmetic

For signed48 inputs, take each magnitude before splitting it into a
low 32-bit and high 16-bit word. The four unsigned hardware products
are placed at bit offsets 0, 32, 32 and 64 with carry. Each cumulative
sum is bounded by the full product, which fits in the retained 96 bits.
The same finish routine applies sign, ties-away Q46 rounding and
signed64 narrowing. A raw product stays exact until the divide starts.

For division use radix `B=2^24`. Shift the positive divisor and raw
dividend by the same amount so the divisor `V` has its top bit at bit 47.
This takes at most 47 bits and leaves the dividend in its 18-byte
workspace. In each digit let `U` be the 72-bit window with
`0 <= U < B*V`. Write `V = 2^16*(v+f)`, where
`v >= 2^31` and `0 <= f < 1`. Let `T = floor(U/(2^16*B))`.
The estimator is `floor(T*B/v)`, saturated to `B-1`. The pinned math
quotient returns `floor(T*2^32/v)`, so shifting its result right eight
bits gives that integer estimator exactly.
[Pinned math semantics](https://github.com/lgblgblgb/xemu/blob/40dfef0d1d5f56be2469492715c12bdb32c75b67/targets/mega65/io_mapper.c)

`U/V` can exceed `T*B/v` by less than `B/v` because the omitted
lower portion of `U/2^16` is below `B`. In the opposite direction
discarding `f` changes the ratio by less than `B*f/v`. Both quantities
are at most `1/128`, so the integer digit differs by at most one.
Saturation cannot increase the error because the true digit is below
`B`. The backend subtracts the full estimated-digit product using two
exact partial products. Their sum fits in 72 bits, so at most one
subtraction wraps and the combined borrow is exact. It then adds back
`V` or subtracts `V` once, as needed, and requires
`0 <= remainder < V` before storing the digit. The next window
inherits that remainder and is strictly below `B*V`. Comparing
`2*remainder` with `V` gives the original rounding decision because
both were scaled equally. Overflow is checked before Graphics can
consume the narrowed value.
[Exact implementation](../../src/graphics/m2_limb.c)

A clip interpolation multiplies a signed48 coordinate delta by
`d_in/(d_in-d_out)` with `d_in >= 0 > d_out`. Its quotient magnitude
is at most `2^47`. In perspective division the signed48 component is
multiplied by `160*65536 < 2^24` and divided by forward distance at
least `10*2^24 > 2^27`, giving magnitude below `2^44`. Both need at
most two radix-24 digits. The generic signed48 product/division
operation supports up to four digits. Nine segments allow at most
162 clip interpolations and 36 perspective divisions per captured
generation. The counts include all six planes and all three axes for
each possible cut, plus two projected coordinates for each endpoint.
[Generated command sequence](../../src/graphics/m2_commands.inc) ·
[Numerical envelope and allocation](M2_THROUGHPUT_ARCHITECTURE_CORRECTION.md)

## Linked timing and memory

The static verifier binds the exact PRG, listing, symbols and target
seal. It validates raw branch targets and uses the pinned fast-mode
opcode table with taken-branch charges. Each reachable loop in the
arithmetic closure has an explicit cap witnessed against the linked
instructions. The expanded control-flow graph counts the longest
allowed path through every loop and direct callee, including the timeout
and failure returns. The bounds permit branch combinations that may be
mutually infeasible for particular operands. They apply to instruction
cycles in the pinned model. Accelerator and bus wall-clock timing on
physical hardware is unproven.
[Pinned opcode costs](https://github.com/lgblgblgb/xemu/blob/40dfef0d1d5f56be2469492715c12bdb32c75b67/xemu/cpu65_mega65_timings.h) ·
[Cycle and ownership verifier](../../tools/flight_demo/m2_rebuild/wide_static.py)

| Linked operation | Conservative CPU cycles |
| --- | ---: |
| Product transaction, including caller JSR | 1,392 |
| Quotient-estimate transaction, including caller JSR | 1,302 |
| Two-digit clip or perspective division, including setup, rounding and caller JSRs | 32,760 |
| The same division with raw numerator multiplication and command wrappers | 82,880 |
| Largest single arithmetic command and wrapper | 17,480 |
| Clock sample and guard, including caller JSRs | 4,910 |
| One raster IRQ / one NMI, including entry | 101 / 26 |

For 198 divisions the division-only envelope is 6,486,480 cycles. The
envelope including numerator products and command wrappers is 16,410,240
cycles. These envelopes exclude transforms, DELTA, scheduler/dispatch,
interrupts, display and commit. The division-only envelope exceeds the
800,000-cycle numerical planning allocation.

The sealed cold default-camera workload records 860 multiplication steps
and 36 division digits. Each division digit adds two product transactions
and one quotient estimate. Mandatory operand writes, result reads and
staging copies cost at least `932 × 852 + 36 × 588 = 815,232` cycles.
The 162 `DELTA` commands each double eight bytes 12 times. At 97 cycles
per byte, those loop bodies add at least `162 × 12 × 8 × 97 = 1,508,544`
cycles. These disjoint counts omit taken-branch penalties, display work
and simulation ticks.
[Sealed host workload](../evidence/flight-demo/2026-11-09-m2-exact-wide/host/host.txt) ·
[Linked disassembly](../evidence/flight-demo/2026-11-09-m2-exact-wide/target/UNADMITTED.disassembly)

**Static 20 Hz service FAIL.** The cold frame requires at least
**2,323,776 cycles** in the pinned instruction model, **298,776 cycles**
over the **2,025,000-cycle** frame budget at 40.5 MHz. Elapsed frame time
remains unmeasured. [Development timing contract](../../interfaces/m2_extended_resident.json)

The pinned LLVM-MOS link produced the complete disabled renderer
composition. The development assertion still applies. The link used
`--noinhibit-exec` to retain the over-limit output for inspection. LLD
reported the BSS and scratch violations, and the independent fit gate
returned failure. The exclusive resident end is `$92F3`. The last
668 bytes of BSS and all 87 scratch bytes are beyond the approved
`$9000` boundary. The gateway uses one BSS owner byte. Its automatic
staging and spills are charged through the actual linked compiler
allocation. Protected reserve use is zero.
[Link result and source/tool identities](../evidence/flight-demo/2026-11-09-m2-exact-wide/target/result.json)

| Resident component | SERVICE1 baseline | Exact wide candidate | Change |
| --- | ---: | ---: | ---: |
| Text | 23,821 | 25,197 | +1,376 |
| Read-only data | 2,115 | 2,116 | +1 |
| Initialized data | 0 | 0 | 0 |
| BSS | 2,000 | 2,000 | 0 |
| Compiler scratch | 53 | 87 | +34 |
| BASIC header and alignment | 26 | 26 | 0 |
| Total resident | 28,015 | 29,426 | +1,411 |
| Development margin against 28,671 | 656 | **−755** | −1,411 |

The application stack bound is 44 hardware and 38 software bytes,
including the existing interrupt envelope of one IRQ with one
nonrecursive NMI. Static BSS/scratch ordering and application MAP checks
passed. Fresh-entry and privileged runtime admission for this image
remain unproven. The earlier boot-only Xemu evidence belongs to a
different image. [Application qualification](../evidence/flight-demo/2026-11-09-m2-exact-wide/qualification/result.json)

## Checks and disposition

- Host checks passed with 6,252 full products and every partial carry,
  8,772 divisions and every quotient digit and remainder, both correction
  directions, 30 saturated estimates, 496 rounding ties and 4,092
  signed division overflows. The native comparison matched 1,360
  transforms and 4,080 projections. The independent Decimal and
  841-case near/far suites also passed.
- ASan/UBSan passed for all six gateway cases and the integrated host
  frame/cache/camera/horizon, cancellation, held snapshot, fault, guard
  and replay checks. Replay checksum `DE675132`. The exact commands,
  outputs and host artifacts are sealed. [Host evidence](../evidence/flight-demo/2026-11-09-m2-exact-wide/host/result.json)
- The copy-range predicate rejected all 1,424 math-alias cases. The
  verifier rejected a different PRG, a different timing table, an IRQ
  math access and a missing poll-loop witness. The prior SERVICE1
  cycle report replayed exactly. Default-backend preprocessed source
  matched after removing blank lines. The 57 contract tests and 16 CI
  policy tests passed. The 188 historical seal members and all 480
  unrelated original-checkout paths matched their recorded identities.
  Two unavailable historical checkouts remain unverified at the
  Git-worktree tier.
  [Preservation and final checks](../evidence/flight-demo/2026-11-09-m2-exact-wide/checks/result.json)
- The complete PRG is 27,341 bytes, SHA-256
  `7fdcea61387c0e6b7ae92310725966ac6c0e29e82e8ba1c9a6be77335af76aad`.
  `wide_validate.py host` captures the host suite, `wide_validate.py target`
  reproduces the link and reports the failed fit, and `wide_static.py`
  replays the arithmetic and ownership proofs on the sealed target.
  [Exact PRG](../evidence/flight-demo/2026-11-09-m2-exact-wide/target/UNADMITTED.prg)

**READY FOR REVIEW.** Math register ownership and the clipping-division
instruction bound are established at the static application tier.
The cold frame fails the static 20 Hz service gate. The linked image
independently fails resident fit by 755 bytes. Runtime admission remains
unproven. Tile integration, Xemu, D81, SD and physical testing were
outside this checkpoint.
