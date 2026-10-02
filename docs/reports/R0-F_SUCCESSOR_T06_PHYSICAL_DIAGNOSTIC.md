# R0-F Successor T06 Physical Diagnostic Handoff

## 2026-09-22 retirement

The owner supplied physical chooser `ERROR CODE FF` for `R0FDIAG2.D81` after
manual copying. That SD copy is **INVALID — DO NOT USE**. The source bytes
still match their recorded identity, but this historical handoff is no longer
an instruction to transfer/test it. `r0f_t06_sd.sh` is disabled before any
media access. The new owner-formatted `R0FDIAG3.D81` is being examined and is
not filled or released. See [the examination report](D81_NATIVE_COMPARISON_2026-09-22.md).

## Outcome

The narrow T06 diagnostic successor is built and has passed the host structural,
host content, and exact-carrier Xemu gates. It remains a candidate awaiting SD
copy/contiguity verification and physical chooser/runtime evidence.

- Filename: `R0FDIAG2.D81`
- Bytes: `819200`
- SHA-256: `912df16828f1c60127e4fcdd8d545dfca0c2ad8fe6a24a64ae01b4ac280df17d`
- Disk label/ID: `R0F DIAG T06,65`
- Entry: `AUTOBOOT.C65 -> R0FSUCC`
- Target PRG bytes: `21921`
- Target PRG SHA-256: `3ce9aeb1029676465d47755145ec31d6b30ab2ca0c8ae95dc88e9703dd99446b`
- State: `XEMU_BOOT_VERIFIED`

`R0FDIAG1.D81` was retired before release because its first successful Xemu
runtime reached the diagnostic screen but the old evidence parser rejected the
new layout. That carrier was not copied to SD and must not be used.

## Diagnostic interpretation

The success predicate and execution order are unchanged. T06 only replaces the
aggregate final fallback `0x58` with the first specific unmet predicate when no
earlier fault already exists:

| Screen fault | Meaning |
| --- | --- |
| `00` | No fault |
| `5F` | Reserve CRC mismatch |
| `60` | Lifecycle did not reach completed state |
| `61` | NMI sticky flag set |
| `62` | Display service missing after resume |
| `63` | Audio service missing after resume |
| `64` | Input service missing after resume |
| `65` | IRQ service missing after resume |
| `66` | DMA service missing after resume |
| `67` | Resumed-service mask contains an unexpected value |
| `68` | Final tick is not `0042` |

The final screen also prints lifecycle state, tick, resumed-service mask, NMI
sticky value, reserve CRC before/after, and the result CRC32. Any nonzero fault
still ends in `SUCCESSOR LOCKOUT - NO ACCEPTANCE`.

## Validation evidence

- Lifecycle/continuation/fault host checks: `1,527,534`, PASS.
- RH001 exhaustive regression: `16,842,752` states, PASS.
- Target compile/link/static checks: PASS.
- Resident bytes/capacity/margin: `24097 / 40959 / 16862`.
- Protected resident end: `0x2B07`; resident high-water exclusive: `0x7E22`.
- Attic transition bytes: `5664`; reserve bytes: `0`.
- Fresh one-session D81 construction: PASS.
- Independent host structure and extracted-content hashes: PASS.
- Two NTSC plus two PAL exact-name boots: PASS.
- Each Xemu run: fault `00`, lifecycle `09`, tick `0042`, mask `1F`, NMI
  `00`, reserve CRCs `3C7D60D8`/`3C7D60D8`.

The first/last screenshots were visually inspected and the complete diagnostic
table is readable in both NTSC and PAL captures. The result CRC32 covers
captured machine context and is not a fixed golden value; each result
independently passed the Python reduction and Java oracle.

Retained evidence is under
`docs/evidence/r0f/successor/2026-09-21-recovery/R0FDIAG2/`.

## Hardware and contract impact

No public ABI, address range, MAP/base-page ownership, DMA behavior, 100 Hz
schedule/stage order, IRQ/NMI handling, or StorageService contract changed.
Only the private diagnostic fault classification and final screen changed.

## Exact next action

The first direct host-transfer attempt copied the correct 819,200 bytes but the
raw FAT32 audit found 22 physical extents. The helper stopped before the final
rename, removed its temporary staging file, and left the card mounted. This is
an SD allocation failure; it does not invalidate the host/Xemu-verified source
D81. Its full extent map is retained as `sd-attempt-1.json`.

Do not retry the ordinary host copy. Safely eject the card, insert it into the
MEGA65, and use the Freezer's `NEW D81 DD IMAGE` command to create a new blank
root-level slot named exactly `R0FDIAG2` (the Freezer supplies `.D81`). Do not
select or chooser-test that blank slot. Power down safely, return the card to
the Mac, and run from the repository root:

```sh
sudo tools/diagnostics/r0f_t06_sd.sh
```

The wrapper sees the matching root entry, proves it is an exact-size,
single-extent native slot, backs it up, fills its existing allocation in place,
rechecks the candidate hash and unchanged one-extent chain, and safely ejects.
It restores the original slot if any post-write gate fails. Do not use Finder
to create, copy, or rename the slot.

After the transfer passes, select exactly `R0FDIAG2.D81` on the MEGA65. Record
the final screen, especially `FAULT`, `STATE`, `TICK`, `MASK`, `NMI`, and both
reserve CRC values. SD, physical chooser, and physical runtime are not yet
claimed as PASS.
