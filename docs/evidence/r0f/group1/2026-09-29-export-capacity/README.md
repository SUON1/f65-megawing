# Group 1 terminal-export capacity qualification — 2026-09-29

This development-only probe exercises the admitted 327,680-byte trace limit
and the final unique chunk name. It is not the Group 1 workload, an exact-name
delivery carrier or physical MEGA65 evidence. The program is 28,294 bytes,
SHA-256 `13c8586c1ae94c6ca4ab98cd68bcc74f8d47c01090904d1e8a0fff088531db1f`.
The generated contract remains the only trace/staging geometry authority; the
probe length is a build parameter. Protected code/data ends at `$3006`, below
the `$4000` terminal staging start, and the resident image stays below `$C000`.

| Fresh disposable run | Mode | Actual post-run result |
| --- | --- | --- |
| `ntsc-01/G1MAX01.D81` | NTSC | Export status 4, error 0, `G1T00`–`G1T19` present. Independent extraction reconstructed all 327,680 ordered bytes, CRC32 `BDCC0FCA`; the actual result and returning `RSSTATE` validated. Post-run D81 SHA-256 `e12d3502d5df47b5e340d94e3b3200ed379c7eae55c93a193d5386056586dbcb`. |
| `pal-existing-last-01/G1MAX01.D81` | PAL | A pre-existing `G1T19` sentinel stayed byte-identical. The exporter wrote `G1T00`–`G1T18`, then stopped with status 5/error 3, 19 files counted and no success status. Independent extraction validated all preceding 311,296 bytes, the sentinel, result and returning `RSSTATE`. Post-run D81 SHA-256 `5ecc5fa113cfe692bf22b888556de7fc31bdf9dbff1b07b4fcfb1637c66a51b9`. |

Each D81 was freshly formatted and populated in one pinned-tool session in its
own directory; identical basenames here do not denote the same image. The
post-run images passed the independent directory/chain/BAM parser and pinned
tool extraction. Xemu was terminated at 180 seconds after the terminal halt;
memory status and actual D81 contents establish the results. No SD write,
physical run, tested-image overwrite, workload deadline or R0-F acceptance is
claimed.

`build.json` and each `build-identity.json` bind the binary to its inputs.
`source-inputs/` retains those exact source versions. The run folders retain
the full post-run D81s, extracted bytes, result, trace, logs and metadata;
`manifest.json` hashes the captured payloads. The one-byte-over-capacity
rejection is a separate subsequent case.
