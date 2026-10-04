# L3 owner-supplied SD allocation audit

2026-10-04. Supplements the original L3 qualification without changing its
release, manifest or retained observations.

The owner supplied the read-only inspector's printed file array after running
`d81_fat32_audit.py /Volumes/MEGA65FDISK R0FG2L3.D81` in their CLI, with a fresh
temporary JSON destination. [Retained fields](owner-supplied-files.json) are a
transcription of that supplied array, not the complete inspector report. The
temporary report path, device metadata and inspector hash were not supplied;
do not infer them from earlier card observations. Copy method was not reconfirmed.

Exact name/short name, 819200 bytes and SHA-256 match the canonical L3 release.
The single extent starts at logical offset zero and covers all 819200 bytes.
Canonical size/hash were independently rechecked without execution or mutation.
This establishes owner-reported SD byte/allocation PASS for the exact L3 copy,
not complete card health, safe ejection, physical loadability or runtime PASS.

**Next gates:** safely eject and record success; select only R0FG2L3.D81 on
MEGA65, photograph its chooser identity, confirm attach/readable directory and
ordinary AUTOBOOT.C65 entry. Stop on an attach or entry error. Once entry passes,
let that one run finish and photograph the full readable terminal and border.
Expected deliberate rejection: red border, `G1 EXPORT S:5 E:03 F:00`. Do not
reset/reload/retry. Power down safely and return the card for a fresh host
snapshot and read-only payload/SAVE checks under the
[one-run procedure](../../../../../plans/R0-F_GROUP2_HARDWARE_TEST.md).

Safe eject, chooser/entry, terminal observation and actual returned-card checks
are pending. TEST_ELIGIBLE and GROUP2_COMPLETE remain false. The two required
photos and actual configuration identities (or explicit UNKNOWN) remain needed.
Physical call-stage, attempt-count, full lifecycle and timing proof are outside
this carrier's observable evidence. Historical Group 2 allocation remains
unrecovered; broader suite completion, measured limits and publication remain
separate. Preserve L2, P09 and all historical carriers unchanged.

Authority: Group 2 Build Intent, D81 gate and D81 workflow. This is evidence-only:
register/clobber, CPU-visible/physical memory, MAP/base-page, DMA,
timing/deadline and IRQ/NMI changes are non-applicable. No generated artifact or
target implementation was changed, and no card write, execution, commit or push
was performed by the agent. SHA256SUMS covers this supplemental directory only.
