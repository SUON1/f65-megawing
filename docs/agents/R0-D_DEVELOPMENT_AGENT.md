# R0-D Development Agent Record

R0-D is limited to protected-workload calibration and instrumentation. It owns
the proof-only 21-stage fixture, independent-clock counters, generated counter
records, and diagnostic target result block. It does not own a renderer, audio
engine, flight/sensor/weapon/AI implementation, CoreRuntime, public ABI,
memory-map selection, or measured-limit selection.

The R0-D target result block is diagnostic-only at `$1860-$18DF`. It must not
use the protected staging, audio, DMA-list, reserve, or measured-limits ranges.
All target exits retain canonical platform state through the existing startup
and ABI infrastructure.
