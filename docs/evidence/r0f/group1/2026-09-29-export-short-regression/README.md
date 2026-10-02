# Group 1 short export regression — 2026-09-29

After parameterizing the development probe, a fresh NTSC direct-PRG run
retested the original 33,025-byte case on `ntsc-01/G1EXP01.D81`. The rebuilt
program is 28,384 bytes, SHA-256
`042df1b84f3a4f11bb128ae03063e08138182c07dc346b7e44fe3f48fa403f48`.
Terminal status 4/error 0 reported three chunks. Independent post-run D81
extraction reconstructed all 33,025 bytes, CRC32 `F2CEE7CB`, and validated
the actual result and returning `RSSTATE`. Directory, chain, BAM and content
checks passed. Post-run D81 SHA-256:
`c1a730014c752bc9d45d830158734519f5dfd5dc9e097187b1d250c9239a76a1`.

This is development transport regression only, not a Group 1 workload,
exact-carrier, SD or physical result. The source/build identity, D81, extracted
bytes and logs are retained here; `manifest.json` hashes the captured payloads.
