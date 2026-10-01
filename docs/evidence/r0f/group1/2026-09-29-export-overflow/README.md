# Group 1 one-byte-over-capacity export rejection — 2026-09-29

The development probe requested 327,681 trace bytes, exactly one beyond the
generated 327,680-byte capacity. Its target PRG is 28,339 bytes, SHA-256
`631084c71d4639942e0f6be86ed1e95a8dca5f1f45f42c5b1054d0fa28dc1433`.
It linked with protected terminal code/data below `$4000` and all resident
sections below `$C000`.

On a fresh disposable `ntsc-01/G1OVR01.D81`, NTSC Xemu completed the ordinary
66-tick/result/returning-SAVE path, then rejected trace preparation at the
boundary. The result has stage 127, tick 66, fault 107, lifecycle 10 and a
valid CRC. Export permit, terminal status, error and file count are all zero.
The actual post-run D81 contains only `TOKEN` and `RSSTATE`; independent
directory/chain/BAM and extracted-content checks passed. Post-run D81 SHA-256:
`a6487f090f98bf8d1974dd29be4668cbdecf55b986948410e482cb1dbdd359eb`.

`build.json`, `source-inputs/`, run logs, result, post-run D81 and extracted
bytes retain the exact evidence. `manifest.json` hashes the captured payloads.
This tests the development transport boundary only. It does not establish
Group 1 workload timing, exact-carrier delivery, SD allocation, physical
execution or R0-F acceptance. No tested disk was overwritten.
