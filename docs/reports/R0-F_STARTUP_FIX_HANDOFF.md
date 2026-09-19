# R0-F startup fix — 2026-09-17

Status: **STARTUP FIX STATIC PASS; TWO CLEAN XEMU BOOTS PASS; PHYSICAL RUNTIME
PHOTO OBSERVED; SD SAFE-EJECT CONFIRMATION OUTSTANDING**. This is a bounded correction to `R0F-STATIC-STARTUP-001`, not completion
of the full R0-F measurement program.

2026-09-17 physical update: owner transfer records prove the matching hash and
unchanged single FAT32 extent. The retained photo shows the new build banner,
functional PASS and all 80 acquisition samples valid. See
`docs/evidence/r0f/startup-fix/physical/R0F2-PHYSICAL-RUNTIME-2026-09-17.md`.
Delivery instructions below are historical for this completed load; safe-eject
completion was not included in the supplied output. Full R0-F remains open.

## Change and reason

Inspection of the pinned SDK's `commodore/lib/libc.a` member `char-conv.c.obj`
identified the `.init.250` `shift` initializer: `LDA #$0E; JSR __CHROUT`.
It ran after the existing R0-A startup set B=$02. The R0-A integration decision
does not admit KERNAL calls without a separately proved base-page thunk.

R0-F writes screen codes directly and uses no SDK text I/O. Its new private
linker fragment, `src/platform/r0f/startup.ld`, excludes `.init.250` from this
proof build. No ROM wrapper is introduced, no SDK installation is patched, and
the shared R0-A startup assembly is unchanged. This removes the need for the
unadmitted ROM call. The linked listing now goes from B=$02 setup through
software-stack/BSS initialization directly into main, with no direct ROM call
or jump anywhere in the executable. The host scanner has negative fixtures for
ROM calls and tail calls and a positive fixture for local calls/raster reads.
This check is not a general proof of arbitrary indirect calls or ROM behavior.

The screen adds `BUILD: F65R0F2 STARTUP FIX`. Functional logic, raster helper,
result schema/revision, and generated constants are unchanged. A fresh carrier
identity and separate `build/r0f/startup-fix/` outputs preserve F65R0F1.D81 and
all retained prior evidence. Packaging now requires the bounded static audit.

## Inspected requirements and impact

Inspected the official record, both architecture sources and MemoryAccessABI,
approved Read-First/AD-001/approval record, current interface and memory
registries, relevant Engine ABI/build/ledger requirements, R0-A B-register
decision, Step 3 report, R0-F source/build/validator, root D81 gate, pinned SDK
linker/startup/character-conversion implementation, and prior Xemu identity.

Registers: ordinary pinned C ABI and compiler pseudo-register use continue;
no new A/X/Y/Z/Q/B/P/SP contract. Existing startup sets B=$02, software-stack
top $D000, and masks IRQs with SEI. Main never returns; the linked fini's B=$00
and CLI path is not exercised. With the ROM initializer removed, the proof
does not claim active ROM IRQ service. No new MAP, DMA, IRQ/NMI, physical-memory
mapping, public ABI, reserve, or timing mechanism is introduced.

CPU writes remain screen $0800–$0FCF, result $1900–$19FF, inherited base page
$0200–$02FF, stack, and linked storage. Stock startup still writes $00/$01/$D030.
No allocation uses protected physical $050000–$05FFFF. Snapshot BSS is
$3278–$3337 (192 bytes); compiler static stack is $3338–$33A2 (107 bytes).
Dynamic stack high-water is still NOT MEASURED.

Linked accounting: BASIC header 22 bytes, text/runtime 4127, rodata 578, data 0,
BSS 192, compiler static stack 107; total 5026 resident bytes. Against F65R0F1,
text increases 8 bytes and rodata 27 bytes because the new banner exceeds the
5-byte initializer removal; BSS/static stack are unchanged. No cycle or deadline
claim follows from this size difference.

Changed paths: private linker fragment, diagnostic banner, private contract and
ledger, R0-F build/audit/Xemu runner, D81 validator, and R0-F control/evidence
records. Preserved specifications, public ABI, frozen memory ownership, shared
startup and R0-A–E target source remain unchanged. Existing working-tree changes
were preserved. No commit or push is included.

## Exact candidate and checks

- Candidate: `build/r0f/startup-fix/F65R0F2.D81`, 819200 bytes.
- SHA-256: `24fabf16d8c85e7767f7caf23183c67995886ce96d126d2085eb387aff548297`.
- Label/ID: `F65 R0-F2` / `65`; entry `AUTOBOOT.C65` loads `R0F-PROOF`.
- PRG: 4729 bytes, SHA-256
  `c1ff8943fd1c24857d1ddba7f6fb2c9919d61e5ab489b003f8a20d5ed31a02a1`.
- Source base: `744920dd76d008fbc0ccce82e006cc0b647f477e` plus exact working-tree
  input hashes in packaged `R0F-EVID.txt` and retained `build-accounting.json`.
- Prior F65R0F1.D81 remains unchanged at SHA-256
  `9b539a14f08d671195ef71e54bbacb3eacd5258634f7a29396bf00a068cddd89`.

`sh tools/build/r0f.sh audit`: PASS for bounded static/host scope, including
358 rejected corrupt result mutations, phase timeout injection, address/undefined
sanitizers, ROM-transfer scanner fixtures, map bounds/overlaps, and ledger
reconciliation. It does not pass the full measurement-contract gate.

`sh tools/build/r0f.sh package`: PASS, fresh format and all three payload writes
in one pinned c1541 invocation; independent structural/BAM/chain/free-block
and source-versus-extracted content checks passed. Repeating `package` returned
the expected exit 2 without modifying the existing carrier.

## Xemu environment incident and provenance

The first attempt failed before emulator memory/media initialization because
the sandbox denied `@mega65-template.cfg.TMP` in Xemu's preferences directory.
No memory dump or screenshot was produced. The old generic handler incorrectly
marked that missing dump as a carrier failure. `xemu-environment-review.json`
retains the original manifest, log hash and classification correction. The
original failure log and `carrier-failure.json` remain preserved.

The explicit `recover-xemu-preflight` command accepts only that exact recorded
permission failure, with no memory/media initialization or output, the original
host PASS records, and unchanged carrier hash. It does not recover any mount,
payload, filesystem, runtime, or chooser failure. Xemu's preference access was
then permitted, and retry output uses a fresh `xemu-permitted/` directory.
No image bytes were rebuilt, renamed, repaired or replaced for this retry.

The post-build runner gained environment-retry support. The exact runner used
to construct the payload is retained as `build-runner.py.txt`, hash
`c237379576d70e92b9ab57db52b49e6c0a62385821692f54a840c08e99192f27`.
The emulator evidence separately records the runner hash used for verification.
This avoids falsely attributing the immutable packaged record to a later tool edit.

## Fresh emulator evidence

Successful invocation (exit 0, permitted normal Xemu preference writes):

```sh
F65_XEMU_ATTEMPT=xemu-permitted \
F65_MEGA65_ROM='/Users/slice/Documents/Codex/f65-megawing/MEGA65.ROM' \
F65_MEGA65_SD_IMAGE='/Users/slice/Library/Application Support/xemu-lgb/mega65/mega65.img' \
sh tools/build/r0f.sh xemu
```

Two separate clean processes ran for 40 seconds each with disposable copies of
the initialized emulator SD image. The pinned Xemu and ROM hashes matched.
Both runs mounted the exact F65R0F2.D81 bytes, loaded the entry program, passed
the five functional case checks and all 80 acquisition bits, and displayed
`BUILD: F65R0F2 STARTUP FIX`. Both screenshots were visually inspected. Screen
and full 256-byte result records matched. Complete emulator memory dumps differ
and are not claimed identical. The carrier hash remained unchanged.

Retained evidence: `docs/evidence/r0f/startup-fix/`, including host/accounting/
static reports, map, symbols, disassembly, release manifest, emulator logs,
screenshots, result bytes and runner identities. Full memory dumps remain in
`build/r0f/startup-fix/xemu-permitted/`. `git diff --check` passes.

The headless emulator logged the same software-renderer fallback and startup
ROM/ETH/VIC warnings as the prior run; no mount/load/filesystem failure occurred.
Xemu cannot exercise the physical Freezer chooser. These are functional proxy
results, not hardware timing, DMA, IRQ, latency or measured-limit evidence.

## Outstanding R0 closure work

Physical retest of this fix requires a fresh, unused `F65R0F2.D81` root slot
created by MEGA65 Freezer, guarded in-place SD fill, exact hash, one unchanged
FAT32 extent and safe eject, then chooser/runtime evidence. No SD card was
mounted during this work; card-side filename availability is not yet verified.

After the owner creates that exact fresh slot and returns the card to macOS,
the delivery command is:

```sh
sudo tools/diagnostics/d81_sd_fill_mega65_slot.sh \
  build/r0f/startup-fix/F65R0F2.D81 /Volumes/MEGA65FDISK \
  24fabf16d8c85e7767f7caf23183c67995886ce96d126d2085eb387aff548297
```

Require matching hash, exactly one pre/post extent at the same offset and length,
and safe-eject PASS before moving to the hardware chooser. Do not replace the
old F65R0F1 slot, use Finder copy, or reuse an already-tested F65R0F2 slot.

Full R0-F still needs an admitted calibrated timebase and wrap handling;
independent 100 Hz/display phase sweep and rolling deadlines; actual input/audio
latency; snapshot/stack high-water and reserve evidence; separately admitted
DMA/IRQ instrumentation; complete physical platform identity; applicable Java
oracle evidence; and owner review. The full measurement contract remains open.
Prior bounded milestone acceptances/waivers retain their recorded scope.
The measured-limits revision is a separate human approval; Phase 1 and gameplay
remain closed. Coming development changes should consume this evidence as a
bounded baseline, not a full R0 pass.
