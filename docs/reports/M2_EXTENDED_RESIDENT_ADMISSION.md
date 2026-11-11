# M2 extended residency — measured admission checkpoint

**BLOCKED: development fit PASS; renderer service FAIL. PAL/NTSC Xemu NOT RUN.**

Identity `65AERO-M2-EXTRES-1`, from reviewed
`aed5bfb2014e8f3df28118668e5f24ded0ddad9e`, on
`codex/65aero-m2-extended-resident-admission`. Fetched main remains `9570f0a`.
No renderer optimization, banking, numeric change or further ceiling increase.

The [versioned private contract](../../interfaces/m2_extended_resident.json)
implements the founder's conditional development-only `$9000` decision.
Production stays `$8000`. The base profile, public ABI, Q12/Q24/Q46/Q16,
nine segments, camera, telemetry, immutable publication, 100Hz/21-stage order,
all other owners and protected reserve are unchanged. Runtime bank zero retains
ownership; this does not allocate a bank, borrow another owner's memory or
admit a production runtime.

## Implemented and measured

The generated development linker enforces end-exclusive `$9000` on actual
text/constants/data/BSS/scratch. Its ledger prohibits application MAP and any
covering `$8000–$9FFF` lease, including a request nominally starting at `$9000`.
The executable's initial PRG load is permitted; subsequent loader/staging use
of resident bytes is forbidden. Original production contracts and ledgers remain
byte-identical. Select this profile explicitly with `--profile extended`.

The new Platform-only startup fragment runs after canonical MAP/B, port, I/O,
page-1 hardware stack and software-SP initialization, before SDK BSS clearing.
It disables cartridge overlays, verifies port/ROM state, zeroes the actual
linked compiler scratch and sends failures to the closed stack-free terminal
sink. No DMA or new physical-copy backend is introduced.

| Allocation | Reviewed `aed5bfb` | Corrected extended link |
|---|---:|---:|
| Prefix | 22 | 22 |
| Text | 22,720 | 22,811 |
| Constants | 2,115 | 2,115 |
| Initialized data | 0 | 0 |
| BSS | 2,016 | 2,016 |
| Compiler static scratch | 53 | 53 |
| Alignment | 1 | 6 |
| Resident total | 26,927 | **27,023** |
| Development ceiling | not adopted | **28,671** |
| Development margin | — | **1,648** |
| Production deficit | 2,352 | **2,448** |
| Protected reserve use | 0 | **0** |

Resident extent is `[$2001,$8990)`. Text ends `$7932`, constants occupy
`[$7938,$817B)`, BSS `[$817B,$895B)` and scratch `[$895B,$8990)`.
Hardware/software stack envelopes remain 256/4096 bytes in their existing
ranges; they are not counted as unused resident margin or duplicated scratch.

Corrected [target packet](../evidence/flight-demo/2026-10-30-m2-extended-resident/target-1793405200824046000/result.json):
PRG **24,956 bytes**, SHA-256
`02430394f14144f944dfb52f53e3bb9491ac40250a0710eb92f898434a1d48b9`.
The unchanged pinned LLVM-MOS compiler, flags and 1,139-entry SDK identity were
verified before and after both links; SDK digest remains
`4166ea6e185bc8471593336e0ac691b784fb5c0a51f861a1c26463c1609bbfd4`.

Two complete links were made, with no intervening renderer/size experiment.
The [first image](../evidence/flight-demo/2026-10-30-m2-extended-resident/target-1793404701167257000/result.json)
fit but its new global-label long-relative startup branches landed one byte
early. The independent raw control-flow check rejected it before execution;
its PRG, source archive and [failure](../evidence/flight-demo/2026-10-30-m2-extended-resident/startup-failure-1/result.json)
remain sealed. Local labels force correct short branches in the corrected link.
Neither image has been executed.

## Qualification results

The [final qualification replay](../evidence/flight-demo/2026-10-30-m2-extended-resident/qualification-1793405443233721000/result.json)
establishes these distinct tiers:

| Gate | Actual result |
|---|---|
| Complete resident fit under the development contract | **PASS**, margin 1,648 |
| PRG/ELF payload equality, including above `$8000` | **PASS static**; 379 file-backed bytes above `$8000` |
| BSS/scratch initialization | **PASS static**; all 2,016 / 53 bytes accounted |
| Executable instructions above `$8000` | **None** in this exact image; no such execution claimed |
| Application MAP/ROM writer exclusion | **PASS static**; only canonical normalization sites |
| Staging rejection | **PASS host**; 131,068 requests against resident/covering block rejected |
| Canonical prefix, closed early sink, new startup branches/callsite | **PASS static** |
| Application stack, including helpers and IRQ plus one NMI | **PASS conditional static**, 44 hardware / 38 software bytes |
| Whole-program startup, privileged trap stack/restoration, arbitrary NMI entry | **UNPROVEN** |
| Renderer normal-world service | **FAIL** by necessary lower bound below |
| Eight per-operation WCETs, guard/clock/interrupt bounds, 100Hz target deadlines | **UNPROVEN**; no nonzero grant invented |
| Host ordered ticks, cancellation/fault/replay | **PASS**; checksum `DE675132` |
| PAL / NTSC direct-PRG Xemu | **NOT RUN / NOT RUN** |
| Actual runway/camera/telemetry/cadence/tick/fault observations | **NOT OBSERVED** |
| D81, SD or physical MEGA65 | **NOT RUN** |

Raw payload bytes match every allocated file-backed ELF section; BSS/scratch
are NOBITS and are not falsely described as loaded payload. An independent
decoder exercises the actual startup fragment for 15 cartridge entry states and
three invalid port/ROM states. It checks all scratch writes; the exact linked
BSS arguments, zeroing helper, actual BSS/main calls and fallthrough are pinned.
No inherited Xemu state or actual CPU visibility is inferred from this model.

The application graph covers 115 call entries and 11,130 reachable instructions,
21 explicit software-SP adjustments, compiler helpers, terminal paths, IRQ and
one NMI-over-IRQ. Maximum foreground hardware depth is 32; IRQ adds 8 and NMI
adds 4. Unknown/indirect transfers, recursion, partial-SP entries, unequal joins,
unbalanced returns, interrupt MAP/traps and all direct-page forms fail closed.
This is an application bound, **not whole-program admission**: the existing
CF001 `$D640` boot trap suspends into a separate Hypervisor mapping/stack. Its
exact internal stack/restoration and controlled entry/NMI preconditions remain
unproven. Repeated nested external NMI is outside the stated bound.

Application covering MAP/staging is prohibited. The existing privileged boot
trap is a suspended application, not an application window lease: bank-zero
bytes must remain intact and canonical state must return before resident access.
Pinned Xemu source shows save/restore mechanics, not an executed proof of this
executable. Official cartridge VHDL requires clearing `$D7FB.1` and forcing
`$D7FD.7/.6` inactive while retaining POWEREN; pinned Xemu does not model the
physical cartridge overlay. Source identities are in
[primary references](../evidence/flight-demo/2026-10-30-m2-extended-resident/primary-references.json).
ROM/emulator hashes were checked read-only; no ROM or SDK binary is published.

## Exact service failure and minimum correction

The retained 20Hz world floor is explicit in the approved PR2 Build Intent and
Phase 1 entry plan; the residency decision did not waive it.
The exact fresh linked `memcmp` equality loop consumes at least 55 pinned Xemu
fast cycles per byte. Every unchanged-camera background dispatch compares 18
pose bytes plus 4 revision bytes. A complete world needs 640 tiles × 8 dispatches:

`5,120 × 22 × 55 = 6,195,200 cycles ≥ 152.968 ms` at nominal 40.5MHz.

Only **2,025,000 cycles / 50ms** exist at 20Hz. Even with every other cost set
aside, this path caps throughput below **6.538Hz**. Calls, setup, taken branches,
painting, geometry, copies, raster, text, guard/clock, authoritative ticks and
interrupts all add positive cost. This is a rejection lower bound, not an
admitted worst-case operation budget or an observed cadence result.

The smallest compatible next task is one **bounded service-control correction**:
amortize checked camera/generation and dispatch bookkeeping across batches of
existing continuation steps, retain cancellation and complete-publication
barriers, yield before each authoritative tick, then prove complete frame cost
and all eight dispatch/guard/interrupt bounds. Do not merely skip validation,
use an unchecked revision token, raise the ceiling, alter arithmetic or waive
cadence. The background witness alone does not prove a proposed fix sufficient;
measure the whole composition. **No such change was started.** Exact privileged
boot/stack/entry proof must also close before any future Xemu launch.

## Retained checks and publication boundary

The corrected host packet passes 48 contract/verifier tests, ASan/UBSan scene,
camera, held-snapshot, cancellation/fault/exhaustion and replay checks, 16,588,800
exact horizon pixels, 6,453 continuation cancellation cutpoints, independent
3,857-case geometry and 841 near/far cases. Final verifier-only replay passes
15 focused regressions and ASan/UBSan staging checks. Independent review's
handler and boot-callsite guard corrections were replayed against the same PRG;
**no relink followed the corrected target**.

All 119 link inputs are archived. Five verifier/test paths subsequently received
the focused fail-closed corrections; these are not compiled target changes.
Their exact checked versions are identified in each qualification packet and
preserved separately. Every actual application/contract byte still matches the
corrected target. All C rendering/runtime inputs match reviewed `aed5bfb`.

Launch and all target/guard grants remain zero. No Xemu screenshot is supplied
as if executed; retained preview images are host previews only. Preserve the
old incomplete recovery evidence without reconstruction. Main, PR30/PR31,
historical packets, the eight other existing worktrees and 480 unrelated paths
are preserved. Push this focused development checkpoint; no PR or merge in this
task. WIP remains **BLOCKED** at admission.

Staged publication whitespace **FAILS** on nine empty-symbol rows in each of the
two sealed LLVM linker maps. Their SHA-256 identities are unchanged:
`5cb9f9e9f475ab9f56df689b0c2f492028ba1a10187226f86577e71d2b2335da`
(first image) and
`5606cb0b50af4b9e777220994e3195ef62af1d22334dc14d6426bfb6febaf1e5`
(corrected image). The earlier pre-stage publication result did not include
untracked map output; it remains sealed with that limitation. The separate
publication checkpoint records the actual staged failure. The existing CI
policy remains unchanged and requires explicit owner evidence-preservation
review before adding any exact-path exceptions. No exception was applied.
This pushed checkpoint is not CI-ready or an integration request. Historical
missing Git-worktree metadata remains **NOT VERIFIED**; no recovery claim is
promoted.
