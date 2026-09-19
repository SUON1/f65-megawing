# R0-D Lessons for R0-E

Status: R0-D closure handoff. This document is operational guidance, not an
R0-E task admission, architecture change, or authorization to build an R0-E
D81.

## What changed the process

1. Treat the D81 as a separately tested release carrier. A successful target
   build or a `c1541 -list` result does not establish physical loadability.
2. Pin the exact `c1541` binary and reject its stderr. The former builder
   returned zero while emitting an OpenCBM dynamic-library failure, which made
   all carrier results inadmissible under the fail-closed gate.
3. Fresh-format each candidate and write every payload in one c1541 session.
   Never copy an older D81 or reopen it to append files.
4. Make raw structural checks and extracted-payload hash checks mandatory.
   The D81 size, a directory listing, and Xemu success are individually
   insufficient.
5. Keep the artifact identity immutable: host filename, disk label/ID,
   PETSCII directory names, byte length, payload hashes, whole-image hash,
   source commit, builder hash, and evidence must describe the same image.
6. A physical chooser `ERROR CODE FF` is a carrier failure. Preserve the
   failed identity and evidence, but diagnose the failing layer before issuing
   another D81. Matching logical bytes do not rule out fragmented FAT32
   allocation of the SD-card file.
7. Publish the source/evidence commit before Xemu; publish the Xemu evidence
   before physical testing. Reverify the remote commit before entering every
   later stage.
8. Require the SD-card copied-file hash, exactly one independently verified
   FAT32 physical extent, and successful safe eject, then a readable chooser
   directory before interpreting a program result. Capture the extent record,
   directory, and stable program identity.

## R0-E admission checklist

Before creating any R0-E D81, the next agent must receive an explicit R0-E
implementation prompt and create its own task admission/ExecPlan. That
admission must name:

- the exact payload list, on-disk PETSCII names, entry/bootstrap program, and
  expected stable screen or result block;
- disk label, disk ID, host filename, builder identity, and release-record
  location;
- host structural/content tests, Xemu objectives, SD-copy hash procedure, and
  physical chooser/function evidence;
- memory/ABI/ownership/timing impact and any relevant platform unknowns.

Only then may its builder fresh-format a new image. The R0-E image must not be
copied from, renamed from, or populated by reopening `F65R0D3.D81`.

## Reusable command sequence

The next agent should begin with the root D81 gate, then implement a
phase-owned non-interactive build that calls the locked `c1541` once to format
and write all phase-owned files. It must run the phase-owned structural and
content validators before requesting Xemu authorization. After Xemu passes,
the owner transfers the unchanged file under the same filename with
`tools/diagnostics/d81_sd_transfer.sh`. The transfer must produce a matching
SHA-256, one physical extent, and a successful safe eject before chooser
testing. The earlier `sync` plus `shasum` procedure is insufficient.

## R0-D reference identity

R0-D's successful carrier is only a process reference:

```text
F65R0D3.D81
SHA-256: 107c6a356b932e9ade875c24539d75b1b0a0078122a6a3910f524570aafec5ef
State: TEST_ELIGIBLE for the admitted R0-D proof only
Release record: docs/evidence/r0d/R0D-D81-D3-PHYSICAL-RELEASE.md
```

It is not an R0-E base image, template carrier, or payload source.
