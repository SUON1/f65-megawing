# R0FHOST1 physical run 1 — retained failure evidence

Status: **D81 carrier/loadability PASS; successor runtime FAIL; retain evidence.**

The owner ran the newly delivered root-level `R0FHOST1.D81` on the MEGA65
immediately after the transfer helper reported the exact pre-run SHA-256
`3721dff9b84cfb7842cc154f6885861e0c7cbd3c3408c8ecec190bf6b405d461`,
one 819,200-byte FAT32 extent at device offset 111,132,672, and safe eject.
Program execution proves that the chooser attached the carrier and that the
entry path loaded. The earlier `ERROR CODE FF` loadability failure is not
present for this carrier.

Photo 1 shows the running program at `VERIFYING IMMUTABLE ROM BACKUP - DO NOT
PRESS RESTORE`. The owner reported very brief graphics/video-like activity and
sound. Those are consistent with the diagnostic's display and audio stress
workloads, but the photos do not establish cadence, content, acoustic path or
performance.

Photo 2 is a fail-closed result, not a pass:

| Display field | Hex | Meaning |
|---|---:|---|
| Fault | `58` | decimal 88; aggregate final completion predicate failed |
| Lifecycle | `0A` | `LOCKOUT` |
| Tick | `0042` | 66; the 33 pre-storage and 33 post-storage ticks completed |
| Result CRC32 | `20452538` | target-displayed CRC; not independently reduced |

The target reached the final completion evaluation with no earlier displayed
fault, then `lockout(88)` changed the lifecycle to `LOCKOUT`. Source inspection
shows that fault 88 combines measured-reserve equality, lifecycle/NMI/fault and
required resumed-service-mask checks, plus the 66-tick total. The display does
not expose the reserve CRCs, service mask or individual counters, so this
evidence cannot truthfully identify the exact failed subpredicate.

This failure is after D81 attachment and program execution. It does not reopen
the corrected host-created contiguous-transfer result. It does block successor
physical-runtime PASS and full R0-F acceptance. Do not rerun this exact tested
copy: the storage phase writes `RSSTATE`, so its post-run D81 bytes may differ
from the pre-run artifact even when operation is expected.

The narrow next diagnostic should preserve this result and assign distinct
fail-closed codes (or a result page) for reserve mismatch, resumed-service mask,
NMI/state and tick predicates. That requires a separately authorized target
diagnostic revision, fresh D81 identity, and repetition of every D81 gate.

No target source, D81, SD card or existing evidence was modified during this
intake. The two supplied photos and the exact staging/final SD reports are
retained unchanged beside this review. Registers/clobbers, CPU-visible and
physical memory, MAP/base-page, DMA, timing/deadline and IRQ/NMI behavior are
unchanged by this evidence-only intake.
