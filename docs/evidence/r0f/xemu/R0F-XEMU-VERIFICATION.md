# R0-F two-clean-boot verification — 2026-09-05

State: **XEMU_BOOT_VERIFIED**, not SD-verified or physical-test eligible.

Exact carrier: `F65R0F1.D81`, 819,200 bytes, SHA-256
`9b539a14f08d671195ef71e54bbacb3eacd5258634f7a29396bf00a068cddd89`.
Source inputs are retained in `../host/build-accounting.json` and committed
in `8b2da49`. No target source, ABI, memory allocation, wrapper, timing code,
payload, D81 content, or filename changed during this verification.

The owner supplied the other project location:
`/Users/slice/Documents/Codex/f65-megawing/F65_OFFICIAL_RECORD.md`.
That record describes older R0-A authority and was not substituted for the
current workspace's R0-F governing records. Read-only inspection located the
ROM and emulator in that project, and prior boot logs identified the initialized
SD image. ROM and emulator matched the current lock exactly.

Command (exit 0):

```sh
F65_MEGA65_ROM='/Users/slice/Documents/Codex/f65-megawing/MEGA65.ROM' \
F65_MEGA65_SD_IMAGE='/Users/slice/Library/Application Support/xemu-lgb/mega65/mega65.img' \
sh tools/build/r0f.sh xemu
```

The runner started two separate Xemu processes, each with a fresh disposable
copy of the initialized emulator SD image. It did not copy or alter the D81,
touch physical media, or write to the original emulator SD image. Temporary
SD copies were removed by the runner after each boot. ROM remains external
and is not included in source control.

Both boots reached the stable `R0F1 REV1` banner. Five functional case records
and checksum checks passed; all 80 acquisition-validity bits were set. Result
blocks and screen hashes matched between boots. Both screenshots were visually
inspected. Raw modulo raster samples are observations, not timing thresholds.

Runner/validator SHA-256:
`812a199542702c3bf0c4b1b0e3b4ac191cfcbc661e5dbdcaf5e38d08e4851f5e`.
Default configuration was read before the run and contained comments only;
its post-run SHA-256 is
`edf0822a32fe8c6ce3d285cf43a69f2535be4ac410c33d0e61c7d53528dbadfc`.
Full effective startup/version/profile information is in the boot logs.

`evidence.json` retains exact arguments, emulator/ROM/SD/image hashes, all 256
result bytes for each boot, and memory/screen/screenshot hashes. Screen text
and screenshots are retained beside it, along with both boot logs. Full
384-KiB memory dumps remain under `build/r0f/xemu/`. Both headless runs logged
an accelerated-SDL-renderer creation error but continued to completed execution
and valid captured screens; this is not a media-mount failure. ROM/ETH/VIC/FDC
startup warnings were also present. Neither boot had a mount/load/filesystem
failure. No physical chooser was exercised.

The next permitted step is the gated native-slot SD delivery workflow.
First confirm `F65R0F1.D81` is unused on the physical card, then create that
exact fresh root slot in Freezer with `NEW D81 DD IMAGE`. Never overwrite or
rename an existing tested identity. Transfer only with the approved slot-fill
helper, proving exact hash, one unchanged raw FAT32 extent, and safe eject.
No SD, chooser, physical timing, DMA, IRQ, latency, high-water, platform-identity
or full R0-F acceptance claim is made by these emulator results.
