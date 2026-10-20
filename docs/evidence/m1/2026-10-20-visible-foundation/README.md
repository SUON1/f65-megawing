# M1 review evidence — 20 October 2026

`build.json` pins the complete build inputs and target identities; `host.txt` records the sanitizer-backed host result. The four result/screenshot pairs are the final exact-PRG PAL/NTSC runs, including changed renderer service pacing. All four passed at checkpoint tick 600 with checksum `DE675132`.

Raw logs, memory dumps, target maps/symbols/disassembly and PRGs remain in the local `build/flight-demo/m1/` paths named by the results. Full dumps may include owner ROM bytes and must not be published. Early unsuccessful attempts are preserved locally and are not substituted for these final results. No D81, SD transfer or physical testing was performed.

`inventory.json` pins all retained files in this directory except itself. See the [M1 contract and handoff](../../../reports/M1_VISIBLE_FOUNDATION.md) for scope, actual accounting, commands and limits. No production or physical acceptance is implied.
