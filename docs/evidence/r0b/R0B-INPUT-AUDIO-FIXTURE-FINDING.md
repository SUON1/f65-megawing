# R0-B Input and Audio Fixture Finding

Status: partial target fixture evidence; no physical input or audio-latency claim.

## Input fixture

The independent Java oracle emits the expected consumed-edge count for the
10,000-transition `R0B-INPUT-PROFILE-001` corpus. The target counterpart in
`src/input/r0b/input_fixture.c` repeats the specified transition recipe and
compares its accumulator result to the generated expectation. The successful
target result is `R0B-IN-001` (fixture accumulator), while `R0B-IN-002` is the
host corpus evidence.

This does **not** exercise CIA, keyboard, joystick, a context binding, or a
physical latency path. Those remain target and owner-test work. No final input
profile is selected.

## Audio fixture

`src/audio/r0b/audio_fixture.c` has a bounded presentation-priority model:
priority zero is selected before priorities one and two at each model service
opportunity. It also configures a continuous SID voice proxy through the pinned
LLVM-MOS MEGA65 SID header. `R0B-AUD-003` means the model passed; it does not
mean the audible warning latency or preemption latency was measured.

The Xemu run is headless with a dummy audio backend, so it cannot be retained
as an audible-output capture. PCM/DMA is explicitly
`NOT_APPLICABLE_UNTIL_GATE: verified DMA audio path`.
