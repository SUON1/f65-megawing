# Group 1 service-order stress: retained failed development runs

These are **failed local diagnostic runs**, not a Group 1 pass or a physical
carrier. The six deterministic display/input/audio permutations were tried
inside the sixteen existing release cohorts. The private version-4 trace
header also recorded sixteen pre-release start bins per service and epoch.

`phase-ntsc-01` stopped before target execution because sandboxed Xemu could
not create its configuration template. Runs `phase-ntsc-02` through `06` used
fresh disposable development D81s. They reached tick 3200 and the original
result reached stage 127, but terminal export correctly locked out with fault
107 and zero exported files because the IRQ body-read probe raised its error
flag. There is **no validated Group 1 trace** from these runs. Resident phase
masks became `FFFF` for each of input, audio and display in both epochs, and
both order masks became `3F`, but these are observations inside invalid
acquisitions and do not earn phase-coverage PASS.

The diagnostic variants distinguished a bounded CIA reader exhaustion from an
out-of-range interval. The flag was `3` in the later runs, indicating a
positive computed IRQ body interval above 65535 counts. A first-failure
operand capture remained zero after termination and did not explain the
counter behavior. No observed interval was silently discarded or reclassified.

The narrower fixed-order, phase-bin variant timed out at 180 seconds
(`phase-ntsc-07`) and 360 seconds (`phase-ntsc-08`) before recording its first
tick. It showed no target fault or IRQ probe error. The screen still held the
earlier ROM-backup-verification message, but the live IRQ count had advanced
10,458 and 21,248 respectively, so that message does **not** establish that
ROM verification itself was still running. The exact stall point remains
unresolved. In a fresh development image on the same host, the previously
validated PRG `ec259fc7...` (`baseline-ntsc-01`) reached stage 127, fault 00,
and ticks 1600 to 3200 under the original 180-second wait; its 512-byte
result and CRC passed the independent host success validator. This separates
the new binary's failure from a general Xemu startup outage.

Built PRGs, run metadata, logs, memories, results, screens and disposable
D81s are retained here. `source/` freezes the last six-order diagnostic source;
the fixed-order variants retain their exact PRGs and build-input hashes, but
their full source trees were not frozen before the rollback. `sha256.json` pins
every retained file. The 4 GiB disposable SD fixtures are omitted; these were
host Xemu fixtures, not physical SD copies.

The active branch subsequently restored all touched target/trace source from
the prior passing Group 1 source freeze and rebuilt the exact `ec259fc7...`
PRG. Independent-service phase coverage remains open. No SD card write or
physical test was performed.
