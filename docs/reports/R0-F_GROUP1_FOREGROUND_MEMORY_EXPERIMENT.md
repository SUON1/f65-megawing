# Group 1 shared foreground bounds helper

2026-09-30 continuation of the approved local Group 1 Build Intent and the
owner-approved next isolated memory experiment. Branch
`codex/r0f-successor-physical-exact-carrier`, HEAD
`9e2ffdb4786e4794119933a5edd4b1cf79f653f0`; dirty predecessor work retained.

## Result

One shared instance of the existing pure `inside` bounds helper saves **163
additional resident bytes** from the qualified nibble-CRC build, or **1031
bytes total** from the preserved presentation PRG. Host checks and one fresh
complete NTSC acquisition pass. The previously overflowing cold pool adapter
now fits, with **97 bytes free**. That margin is not proof that actual owner
hooks and versioned trace integration fit.

| Build | Resident end, exclusive | Free to $C000 | Execution |
| --- | --- | --- | --- |
| Preserved presentation PRG | $BFC5 | 59 | Prior retained evidence |
| Qualified nibble-CRC predecessor | $BC61 | 927 | Prior retained NTSC |
| Shared-bounds runtime | $BBBE | 1090 | Fresh focused NTSC PASS |
| Shared-bounds + cold pool API/state/adapter | $BF9F | 97 | Never executed |

Runtime PRG: 36592 bytes, SHA-256
`acbabeeda80c96c59cfcb45b6f7ad5ce06e49e7e057b7075c772373228b06253`.
Cold fit PRG: 37521 bytes, SHA-256
`e35b86c56342d2d0438b78d54cc0b9e00b29964ed9c8182c9b509154c46d3924`.

## Change and contract impact

Only the copied `src/diagnostics/r0f/combined_model.c` changes relative to the
qualified nibble-CRC snapshot. A Group 1-only `noinline` attribute keeps one
copy of `inside`; disassembly has seven call sites to it. Its predicate,
arguments, admitted address ranges and caller checks are unchanged. The
runtime text section shrinks from 31980 to 31817 bytes. Data/BSS/no-init
sizes are unchanged; the protected $2017-$30B1 range remains exact.

The root target source and generated bindings are untouched. The experimental
64-byte CRC include remains the exact generated nibble predecessor; private
trace version 5 and all public layouts remain unchanged. No capacity or
deadline is relaxed, and no reserve is borrowed.

The Group 1 Build Intent, export amendment, measurement matrix, generated
T02/T03 contracts and resident/export memory ledgers govern. Ordinary C ABI
register/clobber and call-stack effects apply. There is no new physical
allocation, MAP/base-page operation, hardware register access or change to
DMA policy, IRQ/NMI code or restoration ownership. Foreground bounds checks
execute through a call now; fresh stack/timing observations are required.

## Validation

The copied C passes ASan/UBSan workload causality and independent lineage,
1025 streaming CRC lengths and 69641 independent CRC cases. Existing combined
model/snapshot/range/DMA checks pass, including all 4096 admitted DMA lengths,
255 copy-boundary lengths, rejection without mutation, 10000 input edge pairs
and 6092 exact ratio vectors. The standalone combined corpus checks the
unchanged helper logic; the Group 1 build/disassembly checks outlining and
the emulator exercises its actual target calling convention. The full
41-test Group 1 Python suite passes. Pinned target linking and static IRQ and
terminal boundaries pass for both builds; only the runtime PRG is executed.

Fresh NTSC fixture `ntsc-01/G1DEV01.D81` uses direct PRG loading, with video
argument `1` and a 120-second allowance. This is a development acquisition,
not an exact-name release-carrier gate. Actual SAVE, independent extraction,
image/BAM/file-chain checks, CRCs and reduction pass:

- Export status 4, error 0; 19 closed chunks, 310356 trace bytes, 3200 records
  and 949 complete world pairs.
- Both epochs have service-start masks FFFF and completed-order masks 3F.
- Nominal timing WITHIN_OBSERVED_BOUNDS; zero deadline misses, zero uncertain
  boundaries and zero cohorts below the existing 20 Hz floor.
- All 30 corruption cases reject, including mutations with repaired outer CRC.

| Observation | Nibble predecessor | Shared bounds |
| --- | --- | --- |
| Instrumented execution max/p95, CIA counts | 7457 / 7424 | 7489 / 7456 |
| Capture maximum, CIA counts | 1153 | 1153 |
| Hardware/software stack high-water, bytes | 63 / 118 | 67 / 120 |

The 32-count difference between observed execution maxima is not an isolated
measurement of helper-call cost: phase, scheduling and Xemu quantization also
affect the run. IRQ samples 916/911 again have no nonzero read interval. Pinned
Xemu's batching, whole-ISR/entry-latency limits and physical SI uncertainty
remain unchanged. These results are bounded emulator evidence.

Commands, from the repository root:

```sh
python3 -B tools/diagnostics/r0f_group1_foreground_experiment.py prepare
python3 -B tools/diagnostics/r0f_group1_foreground_experiment.py build
python3 -B tools/diagnostics/r0f_group1_foreground_experiment.py host
python3 -B tools/diagnostics/r0f_group1_foreground_experiment.py run
python3 -B -m unittest discover -s tools/diagnostics -p 'test_r0f_group1_*.py' -v
python3 -B tools/diagnostics/test_r0f_group1_reduce.py build/r0f/group1/foreground-recovery/shared-bounds-01/ntsc-01/trace.bin
git diff --check
```

All exit 0. The controller derives compiler commands from the qualified
predecessor, pins the compiler and guards source/PRG identity before execution.
Exact commands, outputs, maps, sizes and execution identities are retained.
Build metadata states `executed: false` at static-check time; the separate
runtime execution/reduction records establish the later NTSC run. The cold
adapter artifact remains unexecuted and carries no real owner observations.

## Preservation and next step

Evidence is frozen separately at
`docs/evidence/r0f/group1/2026-09-30-foreground-memory-experiment/`.
The audit verifies all 2016 entries across seven prior freezes, the 93 passing
build inputs, 95 canonical-carrier inputs, the nibble predecessor and earlier
passing PRGs, canonical P02 and retired P01 identities. The disposable emulator
SD image remains in the build directory and is excluded from the freeze;
its execution hash, actual D81, extracted files, memory and trace are retained.
No retained evidence identity is reused or overwritten.

The selected experiment is complete. The next authorized integration gate
is actual owner hooks and a versioned independent pool record, followed by
memory fit and host validation. The existing trace allocation has 508 bytes
of worst-case slack; a 64-byte pool record would leave 444, but its encoding
and owner code still consume resident space. Neither trace slack nor the
97-byte cold-link margin establishes that the complete integration fits.

The current scene owns anchors/occlusion columns rather than face/vertex/span/
bucket pools; the domain workload has scalar track arrays rather than a
track allocator. Actual bounded owner transitions must be implemented and
observed, not inferred from configured capacities or synthetic host peaks.
PCM/cache ownership is already in the platform path. These ownership bindings
and their full linked cost remain to be established before fresh integrated
NTSC/PAL timing and a new local carrier. The current recovery variant has
no fresh PAL or release-carrier proof. No SD writes, physical run, commit,
push, hardware readiness or full Group 1/R0-F acceptance is claimed.
