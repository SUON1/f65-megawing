# Group 1 compact readiness reporting — 2026-10-03

Local fit, host and emulator gates pass. P08 is XEMU_BOOT_VERIFIED only;
SD and physical execution are NOT RUN. See the
[report](../../../../reports/R0-F_GROUP1_READINESS_COMPACT.md).

Two shorter failure-screen strings save 22 resident bytes, allowing the
named readiness diagnostic to fit at $BFFC with four bytes free. Every
integrity predicate remains; native differential policy and extracted
transport tests pass. Focused NTSC/PAL, collision preservation and four
fresh exact-name P08 boots pass. Physical P07's inner cause remains unknown.

This packet preserves the source, PRG and build identities, host checks,
actual exported traces/SAVEs/chunks, screenshots, carrier records and tools.
Large disposable SD/memory images and whitespace-bearing original files
remain unchanged at paths/hashes indexed in local-artifacts.json. The
first readiness attempts remain in their separate failed-fit packet.
No prior freeze is rewritten. Do not rerun retired P07/P06/P05 carriers.
