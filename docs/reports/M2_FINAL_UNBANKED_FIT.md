# Final unbanked M2 fit investigation

Founder Build Intent: “M2 Final Unbanked Fit Investigation”, 30 October 2026.
Identity `65AERO-M2-COMMAND-1`; parent `d48c9ea884ea3dee1c7dcc90fa36891268b0dc14`.
Fresh remote verification: main `9570f0a`, PR30 branch `3573d716`, PR31 `d48c9ea`.
The parent is accepted development evidence, not admitted runtime. Its sealed
77-member packet and historical reports remain unchanged.

Selected single reduction: one checked fixed-command numerical continuation,
shared operand binding, exact field-copy/comparison descriptors and consolidated
four-coordinate raster validation. Keep the proven limb arithmetic and all
public Q12/Q24/Q46/Q16, geometry, camera, registration and pixel semantics.

Exact replaceable linked closure: numerical continuation/control 4,036;
registration 441; bundle validation 654; Graphics camera comparison 228;
Diagnostic camera comparison 305; raster begin 892: **6,556 bytes**.
The complete replacement must be **<=3,082 bytes**, including all new constants,
state, helpers, scratch and alignment, to close the **3,474-byte** deficit.

Independent read-only review supports one experiment with these explicit caps:

| Replacement allocation | Investigation cap |
| --- | ---: |
| VM/operand binding/sine/screen handlers | 1,300 |
| Immutable four-byte programs | 640 |
| Exact metadata/camera engine and descriptors | 500 |
| Checked raster initialization | 400 |
| State/scratch/alignment growth | 98 |
| **Total replacement** | **2,938** |
| **Projected recovery / remaining margin** | **3,618 / 144** |

These are design caps, not measured savings. The state-test branch chain itself
is only about 96 bytes; saving requires removing repeated operand/index setup
and result handling. Numeric-only replacement cannot close the deficit.
Do not alias away independent registration comparisons or replace them with
checksums. Every original field, raster bound, rounding and failure check stays.

Authority inspected: current manifest/Main v1.8/Runtime v1.2 candidate,
Graphics v2.1, Phase1/M2 intents, generated public records and owner ledgers,
programming/C standards, parent source, exact symbols/map/disassembly and tests.
Changes are Graphics-private C/control representation; public ABI, MAP/B,
CPU-port, DMA, IRQ/NMI handlers, physical ranges and authoritative timing stay
unchanged. Ordinary pinned compiler ABI applies. No assembly helper is assumed
free; none is selected initially. All target launch/service grants stay zero.

Validation: exact independent arithmetic/geometry/camera/rendering comparisons,
sanitizers, cancellation/replay/held/fault and interpreter fail-closed cases;
one source/tool-pinned complete link. If fit passes, prove startup/stack/service/
interrupt/display ownership before PAL/NTSC direct-PRG Xemu. If fit or safety
fails, retain it and stop. No second optimization or automatic contract change.

## Measured result — BLOCKED

Exactly one complete target link: compile/link PASS, resident fit **FAIL**.
No second link, new optimization, unsafe execution or integration attempt.

| Allocation | Accepted UNBANKED-1 | COMMAND-1 | Delta |
| --- | ---: | ---: | ---: |
| Text | 24,363 | 22,720 | -1,643 |
| Constants | 1,643 | 2,115 | +472 |
| BSS | 1,962 | 2,016 | +54 |
| Compiler scratch | 53 | 53 | 0 |
| Prefix | 22 | 22 | 0 |
| Alignment | 6 | 1 | -5 |
| **Resident** | **28,049** | **26,927** | **-1,122** |
| **Deficit against 24,575** | **3,474** | **2,352** | **-1,122** |

Resident end-exclusive `$8930`; initialized payload ends at `$811B`. Compiler
scratch is `$88FB–$892F`, 53 bytes. Renderer state is 1,217 target bytes
(+54); host size is 1,408, not target ABI/stack evidence. Hardware/software stack
envelopes remain 256 / 4,096 bytes, with actual maxima UNPROVEN. Zero reserve;
no physical owner change. The resident owner boundary is violated even though
there is no software-stack collision.

The exact [target packet](../evidence/flight-demo/2026-10-30-m2-final-unbanked-fit/target-1793382249042750000/result.json)
contains commands/exits, source archive, actual map/symbols/disassembly, section
allocation, PRG/ELF and complete 1,139-entry SDK identity. Pinned compiler,
objdump and flags unchanged; SDK unchanged before/after link. The builder's
`base=b044440` retains its ancestral check; actual parent/head is `d48c9ea`,
and tested uncommitted source is bound by its input hashes and source archive.

PRG **24,860 bytes**, SHA-256:
`5b3a93f3f6b6ca7d8c711bc74fe5b4d3895af79d5ca0104608fa3763c73426cc`.
Target seal SHA-256:
`26106670a262070a111656c160994bda42e6030955c04d2691b2b12e0e6033e5`.
The final checkpoint commit preserves those exact tested inputs without relink.

## What changed and why the estimate failed

Generated numerical control is 97 four-byte instructions (388 bytes) plus 64
constant bytes. One checked engine binds operands and resumes multiply/divide
units. It retains exact transform order, clipping, interpolation, projection
and horizon; no arithmetic kernel or numeric authority change.

Shared descriptors construct/compare all 127 semantic bundle bytes against the
independent prepared capture. Camera comparison excludes ABI padding. Raster
validation handles all four Q16 coordinates before cursor writes, preserving
rounding, capacity and unchanged-output-on-failure behavior. Context binding
is checked: copied active contexts and changed prepared/horizon addresses fail
closed until restarted. Flat coordinate layout has explicit compile guards.

Actual native code is decisive:

| Replaced code | Before | After | Delta |
| --- | ---: | ---: | ---: |
| Numerical continuation/control | 4,036 | 4,153 | +117 |
| Registration/bundle/camera comparisons | 1,628 | 451 | -1,177 |
| Raster begin/conversion | 959 | 579 | -380 |
| Prepare wrapper | 268 | 63 | -205 |
| Commit | 55 | 57 | +2 |

`m2_command_service` alone is 3,090 bytes; operand decoding is 245, binding 261,
and remaining wrappers/sine/control 557. Thus the native interpreter did not
meet its investigation cap. Data adds 472 constant bytes and 54 state bytes.
Required behavior remains reachable; native-wide helpers and public batch paths
are absent. This is a genuine complete-program fit failure, not stale symbol
retention or source-line accounting. No isolated assembly/helper saving is
credited. No further assembly or interpreter reduction was attempted.

## Validation and execution boundaries

Final [host packet](../evidence/flight-demo/2026-10-30-m2-final-unbanked-fit/host-1793382149793367000/result.json)
passes generated-byte checks, 37 contract/startup/SDK/closure/specialization tests,
ASan/UBSan full-frame/camera/held-snapshot/fault/exhaustion/replay tests, 3,857
frozen independent geometry cases and 841 near/far regressions. Unchanged
tolerances pass; deterministic replay remains `DE675132` across all schedules.
There are 16,588,800 exact horizon pixel comparisons, at most 479 preparation
services, and 6,453 actual numerical cancellation cutpoints. Those service
counts are not cycle bounds or throughput evidence.

Final [independent comparisons](../evidence/flight-demo/2026-10-30-m2-final-unbanked-fit/independent-1793382149789080000/run/result.json)
pass 3,252 bigint product/Q46/division cases, 117,072 actual multiplication cells,
every division remainder/quotient, 1,360 exact transforms, 4,080 exact clipped
projections, 32,768 camera mask/pose cases, and 4,121 exact raster lines /
483,691 pixels. Half-pixel boundaries and insufficient-capacity failures pass.

Final [focused sanitizer packet](../evidence/flight-demo/2026-10-30-m2-final-unbanked-fit/focused-1793382125713404000/result.json)
passes malformed opcode/PC/operand/constant-destination/branch/counter/return/
product/phase/alias/completion cases, active-copy/rebinding rejection and safe
restart, all 127 bundle field corruption cases, padding exclusion/read-only
comparison, invalid capture/store/completion modes and all four raster bounds.
All 2,048 independent telemetry rows also pass. Earlier successful development
checkpoints and their source identities remain retained; no failed packet is
edited or retroactively regraded.

| Gate | Result |
| --- | --- |
| Host/oracle behavior and precision | PASS at stated host scope |
| Complete target compile/link | PASS |
| Actual resident fit | **FAIL by 2,352** |
| Startup | UNPROVEN overall; linked prefix/closed sink static PASS only |
| Whole-program hardware/software stack | UNPROVEN |
| Renderer service, interrupts, guard and sustained cadence | UNPROVEN |
| Xemu PAL/NTSC | **NOT RUN** |
| Emulator visual/camera/tick/fault/cadence results | **NOT OBSERVED** |

Launch and all service/guard grants remain zero. Cardinalities include command
setup/finalization but do not claim cycles. Fit fails before further admission;
no safety checker was weakened. Source Platform/startup, public/generated
contracts, owner ledgers, Core/Input/Presentation and CI policies are unchanged.

Canonical reproduction entry is `commands_validate.py --tier host`,
`--tier independent`, `--tier focused`, or the create-once `--tier target --sdk
<absolute pinned SDK>`. No further target invocation is authorized here.

## Exact founder decision recommended

**Recommend a separate versioned, reset-only minimum-development residency
contract with end-exclusive `$9000`: 28,671 resident bytes.** This measured image
would have 1,744 bytes of headroom under that proposed ceiling, before any new
admission/enablement overhead. The smallest mathematical ceiling is 26,927;
that leaves no engineering margin. No ceiling increase is adopted or implemented
in this checkpoint.

The decision must explicitly amend the development-only `$8000` ceiling and
protect physical bank0 `$008000–$008FFF` / CPU `$8000–$8FFF` from every covering
temporary MAP or staging lease. Main §5.2 defines the temporary `$8000–$BFFF`
window; any covering 8KiB mapping of `$8000–$9FFF` must also be prohibited for
this profile. Do not treat `$9000–$9FFF` as independently remappable/free space.
This excludes reuse for loader/staging after the executable's own initial PRG
load; it does not forbid that initial load. Runtime retains bank0 ownership.

Preserve canonical MAP/B, existing stack envelopes, 100Hz/21stages, Q formats,
nine segments, camera, telemetry, immutable frames and zero reserve. No banking,
other-owner borrowing, production-map amendment or M3/M4 capacity claim.
Fresh boot/load, full stack, service/interrupt, physical-address/display and
owner evidence must precede exact PAL/NTSC Xemu. Proposed headroom is not runtime
or timing admission. Founder may reject the proposal; without a changed
development-runtime or presentation contract this task remains BLOCKED.

Stop this size-optimization sequence. Preserve and push the coherent successor
checkpoint only; PR30/PR31 and main remain unchanged. No integration or media/
hardware work follows automatically.
