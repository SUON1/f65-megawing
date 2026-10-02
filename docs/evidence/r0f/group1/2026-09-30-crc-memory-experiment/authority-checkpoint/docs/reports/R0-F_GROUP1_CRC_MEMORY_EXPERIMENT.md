# Group 1 isolated CRC memory experiment and remaining fit boundary

2026-09-30 local continuation on `codex/r0f-successor-physical-exact-carrier`,
HEAD `9e2ffdb4786e4794119933a5edd4b1cf79f653f0`. The dirty tree, passing
builds, canonical carrier and prior evidence are preserved. No commit, push,
SD write or physical run.

## Outcome

The one isolated recovery variant replaces the Group 1 1024-byte CRC lookup
table with a generated 64-byte nibble table in a **copied source snapshot**.
Read-only data shrinks 960 bytes and code grows 92 bytes, recovering **868
resident bytes** without changing the public ABI, trace version or CRC values.
The runtime and dormant eight-observer API/state probe fit, host checks pass,
and one completed fresh NTSC acquisition passes behavior, actual SAVE/export
and nominal timing.

That recovery is **not sufficient for the next integration layer**. A cold
candidate initialization/sample/field-wise export adapter adds 308 bytes to
the dormant pool probe and exceeds the unchanged resident envelope by **66
bytes**, before actual owner hooks and trace-version integration. It is never
executed or admitted. No actual pool observations, fresh PAL timing or new
local carrier follow this failed gate.

| Exact build/probe | Resident end, exclusive | Space to $C000 | Disposition |
| --- | --- | --- | --- |
| Preserved passing presentation/export PRG | $BFC5 | 59 bytes free | Unchanged |
| Prior cold pool API + eight observers | $C272 | 626 bytes over | Retained, never executed |
| Nibble-CRC runtime | $BC61 | 927 bytes free | Host/static/focused NTSC pass |
| Nibble-CRC + cold pool API/state | $BF0E | 242 bytes free | Static fit only, never executed |
| Same + cold candidate adapter | $C042 | 66 bytes over | Fit FAIL, never executed |

The same API/state costs 685 bytes in both cold probes, including 64 bytes of
target-native observer state. Thus the recovery exceeds the original 626-byte
shortfall but does not cover this concrete 308-byte adapter, let alone real
owner hooks. This adapter is a cost sample, **not a mathematical lower bound
for all possible encodings or integrations**. Compile/link exit 0 does not
override the independent resident fit failure.

## Size inspection and selected experiment

The linked section inventory has 31888 bytes of text, 1442 bytes of read-only
data, 19 bytes of initialized data, 3243 bytes of BSS and 36 bytes of no-init
state, alongside the fixed 4250-byte protected range. The 1024-byte CRC table
dominates read-only data and has an exact independently checkable algorithmic
replacement. Live model, snapshot, presentation and transfer buffers are not
safe capacity cuts. Retained symbol-size output identifies larger foreground
code bodies as the next inspection area, rather than IRQ/storage critical
paths or claimed spare buffers.

The chosen experiment keeps reflected CRC-32/ISO-HDLC semantics and performs
two four-bit lookups per byte. Only these copied files change:

- `src/diagnostics/r0f/successor_lifecycle.c`: Group 1 nibble update; ordinary
  successor CRC path unchanged.
- `tools/diagnostics/r0f_group1_contract.py`: generate 16 four-bit entries.
- `interfaces/generated/r0f_group1_crc_table.inc`: generated experimental table.

All other copied inputs remain exact. The root versions of those three files
are **not changed**. The canonical generator/bindings stay byte-table based;
the copied generator produces the experimental include. Trace version 5,
generated public layouts, capacities and deadlines remain unchanged.

## Host and focused NTSC validation

The actual copied C CRC implementation passes strict-warning ASan/UBSan host
compilation and 69641 independent cases: known vector, empty/seed handling,
all byte/low-seed combinations, randomized streaming splits and u16 length
boundaries. The workload test passes stage/input/AI causality and 1025 streaming
lengths. Independent Python lineages remain `6B765FDB` at 1600 and `607348BD`
at 3200 ticks; sidecar remains `71A7DF9E` with 1600/640/320 runs. The full
Group 1 Python suite passes 41 tests, including fail-closed NTSC completion,
video-mode, export and timing gate checks. The cold adapter also passes an
isolated ASan/UBSan host test for initialization, sample rejection, unchanged
peer state, field-wise encoding and length/null guards; this is not owner proof.

The successfully executed PRG is 36755 bytes, SHA-256
`a4d4cd8de6415d7cfcefc695f46df3d7312586c7c0c423f371ac90da601b96e4`.
Pinned LLVM-MOS/static IRQ/terminal checks precede execution; the protected
range remains $2017-$30B1, end exclusive. A fresh disposable `G1DEV01.D81`
fixture uses direct PRG loading, **not an exact-name release-carrier gate**.
The completed attempt is `ntsc-03`, Xemu video argument `1`, NTSC, with a
120-second allowance. Its retained execution report records normal timed
termination and process return code 0.

- Export status 4/error 0; 19 closed chunks, 310436 trace bytes, 3200 records
  and 954 retained complete world pairs.
- Actual RSSTATE SAVE, independent image/BAM/chains/extraction, result/trace
  CRCs and full reduction pass.
- Both epochs: service-start masks FFFF and completed-order masks 3F.
- Nominal timing WITHIN_OBSERVED_BOUNDS: zero misses, zero uncertain cases and
  zero cohorts below the declared 20 Hz floor. All 30 corruption cases reject.
- Instrumented execution max/p95 rises from 6880/6816 to **7457/7424 CIA
  counts**; capture max rises from 705 to 1153. Hardware stack high-water is
  63 versus 61 bytes; software stack remains 118. This is measured cost, not
  a changed deadline or proof of uninstrumented/physical timing.
- IRQ read samples 894/910 have no nonzero interval. Pinned Xemu's 32-count
  timer batching remains a resolution boundary, not zero IRQ cost, whole-ISR
  cost or entry-latency proof. Physical SI uncertainty remains unresolved.

Trace SHA-256:
`f2929476d1e3a40b67046a7c22b612635b1814e737dbfeeb7a0a1fc8cafaaf89`.
Build metadata records static qualification time (`executed: false`); the
separate `ntsc-03/execution.json` and reduction establish this later execution.
The dormant pool and adapter artifacts remain genuinely unexecuted.

Two earlier fixtures remain retained and never reused: `ntsc-01` was aborted
after the incorrect video argument 0/PAL was identified (its name is not mode
evidence); `ntsc-02` used NTSC but the macOS sandbox prevented Xemu's normal
configuration write before program execution. Neither contributes acquisition
or timing proof. The fresh permission-approved retry uses only local emulator
configuration and disposable disk-image files, not an actual SD device.

## Commands and evidence

All commands below are relative to the repository root; exact compiler and
emulator commands and identities are retained in the build/host/execution JSON.
Preparation/build/attempt directories refuse overwrite. Do not rerun actions
against these retained identities.

```sh
python3 -B tools/diagnostics/r0f_group1_memory_experiment.py prepare
python3 -B tools/diagnostics/r0f_group1_memory_experiment.py host
python3 -B tools/diagnostics/r0f_group1_memory_experiment.py build
python3 -B tools/diagnostics/r0f_group1_memory_experiment.py run --attempt 3
python3 -B tools/diagnostics/test_r0f_group1_reduce.py build/r0f/group1/crc-recovery/nibble-01/ntsc-03/trace.bin
python3 -B tools/diagnostics/r0f_group1_memory_experiment.py adapter-fit
python3 -B -m unittest discover -s tools/diagnostics -p 'test_r0f_group1_*.py' -v
git diff --check
```

Successful host/static/runtime checks exit 0. `adapter-fit` also exits 0 after
recording fit FAIL, `executed: false`, `admitted: false`; no caller may treat
its command status as admission. Its PRG SHA-256 is
`1c97a7c3a4f90b175691631fc12eb9fa0709cfb187fd4a1f0a6fd20084e6fd30`.
The adapter is a standalone cold probe, has no owner connections, no admitted
wire ABI, and adds no resident output buffer.

New evidence is frozen separately under
`docs/evidence/r0f/group1/2026-09-30-crc-memory-experiment/`. It contains the
copied exact baseline and experimental inputs, maps/symbols/disassembly,
host/fit reports, successful and aborted fixture evidence, new test/probe
sources, authority checkpoint and preservation audit. Multi-gigabyte disposable
SD-image fixtures are excluded from the freeze, not deleted; the completed
execution report retains its fixture hash. The development D81s are retained.

The audit verifies all 1777 entries across the six preceding freezes, all 93
passing build inputs and 95 canonical-carrier inputs, passing/earlier PRGs,
the canonical P02 carrier and retired P01 canonical/post-run identities.
Passing PRG remains
`25a18c23c750d0877103209fccd0114afe7cd30f31690731605b9687bfea94e1`;
canonical P02 remains
`60cea9c8dd51b0f2c199605e60574c0bebd7c758d5899fb9b1e7c2901f83e832`,
XEMU_BOOT_VERIFIED only. Original `ec259fc7...`, corrected `0d96a1b...`,
six-order `c249f4e4...` and ordinary successor `cf605bd...` remain unchanged.

## Authority, effects and next action

The approved Group 1 Build Intent/export amendment, measurement matrix,
generated T02/T03/private contracts and memory ledgers govern. Navigation
reports and attached diagnostic material provide context, not new authority.
Programming principles and C readability rules apply to new local tools.

Ordinary compiler-managed registers/clobbers and C stack effects only; the
CRC alters CPU-visible ordinary code/read-only data and measured execution
time. No new physical memory allocation or public ABI change. MAP/base-page,
DMA policy, hardware registers, IRQ/NMI implementation and restoration rules
are unchanged. Resident fit still uses the original $C000 bound; no reserve,
capacity, stack-budget or deadline borrowing. The cold adapter has no runtime
hardware/IRQ effect because it is rejected before execution.

The requested one recovery experiment is complete, but pool integration is
blocked by fit. Recommended next owner-approved slice: inspect selective
foreground inlining/shared-helper code savings in the large linked bodies,
retain this passing nibble variant, and recover **more than 66 additional
bytes plus real hook/trace costs**. Do not select another CRC slowdown merely
to cross the 66-byte boundary: observed execution cost already increased.
An independently smaller adapter is an alternative, not a selected correction.
Neither option authorizes shrinking live pools, using reserved memory, relaxing
timing or relabeling fixture capacities as observed peaks.

Then require combined fit and independent host checks before actual owner
observations, fresh changed-build NTSC/PAL timing and a new local carrier.
Actual pool ownership/occupancy transitions must be bound to the applicable
bounded workload, not inferred from constant capacities or the synthetic host
corpus. Integrated near-capacity export and operator summary remain open.
No SD/physical eligibility, whole-ISR/physical timing, production engine proof,
full Group 1/R0-F acceptance, commit or push is claimed.
