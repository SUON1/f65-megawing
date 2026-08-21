# F-65 R0-B Development Agent

## Authority and scope

This record governs bounded Phase 0 R0-B proof work on branch
`codex/r0-b-development`, based on accepted R0-A commit
`1ab5b62928d0e725c8dcf48e8a17783a525503b6`.

AD-001 authorizes R0-B proof development.  Architecture 1.5.1, Gameplay 0.2,
and Engine 0.2 remain candidates.  This work must not select a production
display mode, renderer tier, input profile, audio format, palette, or
presentation cadence.

## Owning proof modules

| Module | Owns | Does not own |
|---|---|---|
| Graphics proof harness | synthetic scene, incomplete/complete store state | simulation or production rendering |
| Platform/VIC-IV proof service | documented display setup and measured display behavior | canonical platform ABI changes |
| Core proof DMA service | range validation and immutable proof job records | production DMA manager semantics |
| Input proof harness | raw samples and proof edge accumulator | control feel or flight control |
| Audio proof harness | proof SID/PCM presentation state and priority records | final audio format/content |
| Diagnostics/host tools | generated contracts, independent oracle, evidence | target-defined expected results |

## Required invariants

- The CPU base page remains `$0200-$02FF`; the R0-A C runtime keeps `B=$02`.
- The CPU stack remains `$0100-$01FF`.  MAP, `$01`, and interrupt return
  state must return to the R0-A canonical state.
- Ordinary C pointers are not physical MEGA65 pointers.
- Only complete stores are display candidates; the prior complete store remains
  visible while a new store is incomplete or abandoned.
- The `$058000-$05FFFF` measured-limits reserve is untouched.
- No gameplay, flight, radar, systems, weapons, AI, mission, campaign, or
  production resource implementation is admitted.

## Unknowns and escalation rule

R0-A did not verify shared MAP, DMA, IRQ, Q-register, hardware-math, stack,
or hardware-identity behavior beyond its scoped base-page/pointer proof.
VIC-IV/FCM, DMAgic, SID/audio, CIA/input, raster, and IRQ code may be added
only after an official reference identifies the exact behavior and a smallest
R0-B-specific test records it.  Never infer a shared Platform ABI fact from a
candidate proof.  Record blocked work as `NOT_APPLICABLE_UNTIL_GATE: <gate> —
<reason>`.

## Evidence states

`PASS` means the named test actually passed in the named environment. `NOT RUN`
is not pass. Xemu evidence is distinct from physical-MEGA65 evidence. R0-B can
be implementation-complete before physical evidence is returned; it cannot be
evidence-passed or hardware-passed without owner-reviewed results from the
exact D81.
