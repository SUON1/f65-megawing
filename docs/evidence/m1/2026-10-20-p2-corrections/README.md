# M1 P2 correction evidence

Status: READY FOR REVIEW, local and uncommitted. See the [correction report](../../../reports/M1_P2_CORRECTIONS.md). The original M1 packet and outputs remain unchanged.

`build.json` binds 56 source/tool/configuration inputs to the three development target profiles. `host.txt` records sanitizer-backed host checks; `admission.txt` records five admission tests, including mutation subtests. `verification.json` records independent generated-byte comparison, raw-artifact hash and symbol decoding, startup screen-code accounting, and preservation verification. `preservation-before.json` pins 417 files across historical M1 outputs/evidence/report and the 20 unrelated untracked entries. All still match.

| Run | Result | 600-tick checksum | Hardware / software stack bytes | Source manifest |
|---|---|---|---|---|
| [PAL replay](pal-replay/result.json) | PASS | DE675132 | 31 / 28 | boot-window-60s/build.json |
| [NTSC replay](ntsc-replay/result.json) | PASS | DE675132 | 31 / 28 | build.json |
| [PAL slow render](pal-slow-render/result.json) | PASS | DE675132 | 31 / 27 | build.json |
| [NTSC slow render](ntsc-slow-render/result.json) | PASS | DE675132 | 31 / 27 | build.json |

Each run includes its actual `screen.png`, visually inspected for complete sky/ground, readable counters, and altitude/airspeed marked NOT IMPLEMENTED. The displayed live checksum can differ from the saved 600-tick checkpoint because execution continues after the checkpoint.

The first PAL run used a 60-second emulator window. A subsequent NTSC attempt exhausted that window during emulator onboarding and never loaded M1; its FAIL result and screenshot are preserved in `ntsc-onboarding-failure/`. The runner was restored to 120 seconds and the build rerun before the remaining three successful runs. `boot-window-60s/` retains the exact earlier runner and build manifest. The target PRG bytes are identical across those manifests; only the runner timeout differs. The failed attempt is not runtime evidence and is not counted among the four passes.

Per-run result files pin the raw local log, screenshot, text screen and memory dump. Raw outputs remain under `build/flight-demo/m1-p2/`; ROM-bearing memory dumps are deliberately excluded from this packet. `inventory.json` hashes all other files in this packet. These are direct-PRG emulator results with isolated preferences and in-memory virtual boot media only: no D81, file-backed SD image, SD transfer/allocation, or physical testing. They establish neither physical acceptance nor flight behavior.
