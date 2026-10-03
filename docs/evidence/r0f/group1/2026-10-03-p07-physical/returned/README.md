# P07 returned-card verification — 2026-10-03

Live mounted volume identity matched removable FAT32 UUID
83FFC12E-67E1-307F-91AD-E584C2E01E87, currently disk4s1. The mounted
R0FG1P07.D81 was copied into a host-only snapshot and compared again after
extraction. No card write, filesystem repair/check, raw allocation audit,
unmount or eject was performed. The card remains mounted.

Independent chain/BAM parsing and hash-pinned c1541 extraction agree on four
closed entries: AUTOBOOT.C65, R0FSUCC, TOKEN and RSSTATE. All three original
payloads match canonical P07, including its exact 37518-byte PRG.
Actual 34-byte RSSTATE loads at $3063; its 32 payload bytes exactly match
checksum 6B765FDB from the independent tick-1600 model in the qualified
copied-source tooling and the declared checksum/index encoding. Physical
bytes came from the card, not from an emulator output.

No G1Txx trace exists. No actual 512-byte terminal result, complete physical
trace reduction or timing PASS is available. The photographed 6F rejection
still leaves the individual readiness predicate unknown. Group 1 acceptance
and Group 2 progression remain pending. Preserve P07 without rerunning it.

Returned D81 SHA-256:
`6c1879eb32bd42eb5eee1c8cf80f5f786113ce8fa9b6b2785a8d883acb73af41`.
Actual SAVE SHA-256:
`7d2f63b8e8e970bb35c351174fae1ca365245f14acf35db0d3cf9016ba8ba5bd`.
The full D81 snapshot is retained locally at
`build/r0f/group1/carriers/R0FG1P07/returned-01/R0FG1P07.D81`;
this packet retains both extractions, structure and verification records.
The changed D81 hash reflects the added SAVE; original payloads did not drift.

This is a separately manifested addendum; the initial photo packet and all
prior frozen evidence remain unchanged. Only off-card records and WIP change.
Target registers/clobbers, memory allocation, MAP/base-page, DMA, deadlines,
IRQ/NMI and generated/public interfaces are unchanged/non-applicable.
