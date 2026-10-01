# Group 1 workload/timing integration checkpoint

Local host, target and direct-PRG Xemu evidence; **not a delivery carrier,
physical result, full Group 1 acceptance or R0-F completion**.

The same final PRG ran in NTSC (`ntsc-04`) and PAL (`pal-02`):
37,394 bytes, SHA-256
`bd6f75d4eb5829d76640bf81ed307cf55b64b00db950a6a822dce981ef93c516`.
Each run contains 3200 ticks, 1600 before returning storage and 1600 afterward.
The actual exported trace and RSSTATE were independently extracted and
validated. Header version 2 retains every world swap in a bounded event log.

| Observation | NTSC | PAL |
| --- | ---: | ---: |
| Raw trace bytes | 315780 | 314620 |
| Retained world events | 976 | 831 |
| Nominal deadline misses / uncertain boundaries | 0 / 0 | 0 / 0 |
| Cohorts below the 20 Hz floor | 0 | 0 |
| Observed nominal complete-world cadence | 29.06–30.12 Hz | 24.11–25.12 Hz |
| Instrumented tick p95 / max, CIA counts | 7648 / 8065 | 7392 / 8352 |
| Maximum capture cost, CIA counts | 673 | 705 |
| Exercised hardware/software stack high-water | 72 / 88 bytes | 72 / 88 bytes |

The ratio is nominal, not traceable SI calibration. Targets of 25/30 Hz are
not substituted for the existing 20 Hz floor. Physical clock uncertainty and
universal worst-case performance are not established here. See each run's
`reduction-final.json` for all cohorts, overlapping windows and distributions.

`manifest.json` pins retained binaries, maps, raw bytes, reports and source
inputs. Post-run D81s are disposable development images, never canonical
delivery artifacts. They were loaded using direct PRG injection, not the
exact-carrier boot route. No physical SD was accessed.

The initial version-1 run (`build/r0f/group1/integration/ntsc-01`) is retained
locally with 32 nominal misses and low-cadence observations. A measured CRC
optimization reduced capture cost. Later version-1 runs validated timing but
could omit intermediate world ages when two swaps occurred between records;
version 2 corrects that capture gap. Earlier runs are not substituted for the
two final runs retained here.

Commands, changes, limits and next work are recorded in
[the integration report](../../../../reports/R0-F_GROUP1_INTEGRATION.md).
