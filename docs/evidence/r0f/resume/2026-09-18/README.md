# RH001 returning-handoff evidence

Private standalone no-restart development proof; **not full R0-F acceptance,
not a physical result, not a hardware carrier**.

PRG SHA-256: `b856ad29b0ac06939083dd54140136d438037ce41c3f49f00163d6b2c52efcc9`.
Exact inputs are retained under `source-inputs/` and bound by `accounting.json`.
Build/map/symbols/disassembly and PRG/ELF are retained alongside the report.

| Run | Result CRC32 | Outcome |
|---|---|---|
| NTSC `xemu-1-1789768133106605000` | `32ECFBA6` | PASS |
| PAL `xemu-0-1789768137122746000` | `8B769569` | PASS |

Each run has zero faults, resumed state 05, storage phase 05, and tick 0022
(34 decimal). The original model continues after ROM reclaim/restoration,
LOAD/SAVE/reload and application context restoration. ROM, reserve, low-memory,
DOS-overlay and retained model integrity checks pass. The Java oracle checks
the actual `saved.prg` extracted after target SAVE, not only an expected blob,
and rejects 68 altered results/files. Screenshots were visually checked.
Different complete-result CRCs are expected because preserved entry-time
low-memory content varies; each run independently matches its before/after
integrity checks and the same tick-34 model golden `400B181F`.

Host admission/lockout tests: 16,842,752 checks with ASan/UBSan. Target startup
ordering, ROM-call allowlist, no relaxed long branches in the private wrapper,
linked ranges and compiler base-page ABI are checked by the build.

`host-gate.json` records each fresh single-session c1541 construction and
pre-boot content/structure checks. `evidence.json` records initial and final
disk hashes; SAVE intentionally changes the disposable image. Post-SAVE
structure and every extracted file are verified. Full writable D81/SD fixtures
remain in their original build run directories, not in this retained bundle.
No SD card or physical MEGA65 was used by RH001. Absolute build paths in logs
identify the original runs; retained equivalent result/file/screen artifacts
are in the `ntsc/` and `pal/` subdirectories.

Commands and scope: `docs/reports/R0-F_RESUME_HANDOFF.md`. Full workload/service
resumption, fault/repeated-transition matrix, physical evidence and owner
acceptance remain open. Existing CF001 hardware evidence is unchanged.
