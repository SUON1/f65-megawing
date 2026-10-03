# P06 returned-card verification — 2026-10-02

The owner returned the card. Live diskutil identity matched removable FAT32
UUID `83FFC12E-67E1-307F-91AD-E584C2E01E87`, currently `disk4s1`.
The mounted `R0FG1P06.D81` was read into a host-only snapshot and compared
again after extraction. No card writes, unmount, eject or raw extent audit
were performed. The card is left mounted.

Independent chain/BAM parsing and pinned c1541 extraction agree on exactly
four closed files: AUTOBOOT.C65, R0FSUCC, TOKEN and RSSTATE. Original payload
hashes match P06. Actual 34-byte RSSTATE loads at $3063 and its 32 data bytes
match the independent host model at tick 1600, checksum `6B765FDB`, using
the declared checksum/index encoding. These bytes came from the returned card.

**No G1Txx chunks exist.** No actual terminal 512-byte result or complete
physical trace is available for independent workload/model/timing reduction.
No full-result Java-oracle PASS is claimed. The photograph remains bounded
physical evidence of tick 3200 and all five resumed-service bits, followed
by terminal preparation failure 6B. Group 1 acceptance remains ungranted.

Returned D81 SHA-256:
`6401290b6ae86abb3147d943419403e00b834941656e4685cdc98b9838e7a0f2`.
Actual RSSTATE SHA-256:
`7d2f63b8e8e970bb35c351174fae1ca365245f14acf35db0d3cf9016ba8ba5bd`.
See [verification.json](verification.json) and [post-disk.json](post-disk.json).
The original photo-observation manifest remains unchanged; this addendum has
its own manifest. P06 stays retired. Explicit photo-filename confirmation and
physical video/platform identities remain unrecorded.

Next work: isolate which terminal preparation guard rejected before changing
or building a fresh candidate. Do not bypass trace CRC/readback or transport
checks. No target correction or retest was performed as part of card analysis.
