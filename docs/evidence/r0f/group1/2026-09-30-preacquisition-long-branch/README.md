# Group 1 pre-acquisition long-branch trace

This is a local Xemu diagnostic and correction proof, not a carrier, SD or
physical result and not Group 1 acceptance. Main Concept v1.6 §§4.6 and
17.5–17.7, the approved Group 1 Build Intent and measurement matrix, and the
generated private trace/export contracts govern.

## Exact cause

The retained fixed-order phase PRG
`f5963ae5197f034bcb3e024de4d803a07fd693ce700bf1f9f594b1b34b6b33e5`
was observed without rebuilding it through pinned Xemu's Unix-domain serial
monitor. The first pause landed in the raster IRQ at `$2DB0`. Single stepping
then established this exact path:

- `$3298`: relaxed `BEQ16`, bytes `F3 86 00`;
- taken destination in Xemu: `$3320`, one byte before the intended `RTS` at
  `$3321`;
- `$3320`: byte `B0`, the high address byte of the preceding indexed store,
  decoded as `BCS +$60` because carry was set;
- `$3382`: execution continued into non-entry bytes and reached `BRK` at
  `$3384`, re-entering the IRQ handler.

The zero-epoch IRQ fast path is used while initial `cfcalibrate(0)` waits for
display frames. Recursive BRK/IRQ execution therefore prevented calibration
from completing and made the apparent stall layout-sensitive. This is the same
pinned-assembler relaxed 16-bit branch defect already documented for RH001;
it is not a phase-bin arithmetic failure.

## Correction and direct proof

`src/platform/r0f/group1_irq_45gs02.s` now uses an in-range `BNE` followed by
the inactive-path `RTS`. `tools/diagnostics/r0f_group1_integration.py` rejects
all 65CE02 16-bit branch opcodes inside the private Group 1 IRQ probe.

For a layout-neutral proof, the retained failing PRG was copied and only file
positions 4762–4764 (one-based) changed from `F3 86 00` to `D0 01 60`. The
corrected diagnostic PRG is
`cca0ecb91a2d5378333482ebf706b16b9d513eb01953511119b96298d178460a`.
It reached the terminal loop in less than one minute with export status 4,
error 0, 20 chunks, target fault 0 and 3200 records.

Pinned `c1541` extraction and the independent BAM/chain parser passed. The
retained version-4 reducer was narrowed only to the known fixed-order boundary:
all six service phase masks must be `FFFF`, while both deliberately absent
service-order masks must be `00`. The complete trace and actual SAVE then
passed acquisition, lineage, CRC, timing, cadence, stack and workload checks:
zero nominal deadline misses, zero cohorts below 20 Hz and 975 retained world
events. This does not establish six-order coverage.

The normal corrected Group 1 build is 36,473 bytes with SHA-256
`0d96a1b21eb36680b05689b659ac8c6f73cc2b61e647c060ab2f369c2bbfc244`.
It differs from the preserved passing `ec259fc7...` baseline at exactly those
three bytes. The ordinary successor PRG remains byte-identical at
`cf605bd377ddcee2c72cdc4abfd20c3ae9eee350b7b78b36cbde8ff1adf8fc23`.

No PAL run, six-order rerun, exact-name carrier gate, SD write, physical run,
commit or push was performed.
