# Owner physical terminal photograph

2026-10-04. The owner's original JPEG is retained byte-for-byte as
[terminal-photo.jpg](terminal-photo.jpg), with identity and transcription in
[observation.json](observation.json). The readable text and visible red border
match the deliberately expected G2-L-EXPORT-COLLISION terminal disposition:

```text
G1 EXPORT S:5 E:03 F:00
4=OK 5=FAIL / E,F HEX
REDUCE FOR TIMING
NOT ACCEPTANCE
RESET
```

The photo was supplied during the L3 hardware handoff; it does not show the
carrier filename, chooser or build identity. Exact R0FG2L3.D81 chooser/entry,
safe ejection and one-run/no-restart confirmations are pending. Physical video
mode/core/HYPPO/ROM/Freezer identities remain UNKNOWN, not emulator-derived.
Do not label this photo alone as carrier loadability, TEST_ELIGIBLE or completed
physical fault-behavior proof.

Next: power down safely without reset/reload, return the card, retain a fresh
host-only snapshot and perform read-only original-payload/SAVE checks with
L3's canonical release. Preserve the chooser photo if already captured; never
rerun the carrier to fill a photographic gap. Follow the
[one-run procedure](../../../../../plans/R0-F_GROUP2_HARDWARE_TEST.md).
Files/photos do not establish physical call-stage, attempt count, full lifecycle
or timing. Group 2 remains unfinished and publication remains held.

This evidence-only addition follows the Group 2 Build Intent, D81 gate/workflow
and hardware procedure. Register/clobber, CPU-visible/physical memory,
MAP/base-page, DMA, timing/deadline and IRQ/NMI effects are non-applicable.
No target/generated artifact, historical carrier or original L3 release was
changed. SHA256SUMS covers this supplemental directory only.
