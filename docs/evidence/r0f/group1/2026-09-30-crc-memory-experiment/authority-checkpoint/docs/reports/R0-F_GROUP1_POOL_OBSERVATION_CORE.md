# Group 1 isolated pool-observation core and target-fit boundary

2026-09-30 continuation of the approved Group 1 local Build Intent on
`codex/r0f-successor-physical-exact-carrier`, HEAD
`9e2ffdb4786e4794119933a5edd4b1cf79f653f0`. Dirty predecessor work and all
passing/failed evidence remain preserved. No SD, physical, commit or push action.

## Outcome

The pure owner-fed observation kernel passes host ASan/UBSan, **170335**
boundary transitions, two 65535-sample counter-boundary sequences and
**25600** independently checked observations across eight owners over 3200
host ticks. Empty, partial and full occupancy occur; peer/domain state remains
unchanged by another owner's samples. Five generated-contract tests and the
full **35-test** Group 1 host suite pass. Pinned LLVM-MOS object compilation
passes, including a separate target-native state-size probe.

This is preparation, **not integrated runtime pool coverage**. Eight target
observers require **64 bytes**, versus the current **59-byte** resident slack.
A separate cold retained-code/state link ends at **$C272**, growing 685 bytes
from $BFC5 and exceeding the $C000 envelope by **626 bytes**, before owner hooks
or trace transport. Compile/link exits 0 but the independent fit check reports
FAIL. That `FIT-ONLY.prg` is never executed or used in a carrier. No reserve,
stack, memory-map, workload, capacity or acceptance rule is relaxed.

## Authority and observation contract

The [Build Intent](../plans/R0-F_GROUP1_BUILD_INTENT.md), Main Concept v1.6
sections 15-17, generated T02/T03 contracts and ledgers, programming principles
and C readability rules govern. The PDF specification review narrowed this
slice to read-only observations, retaining the distinction between a fixture
capacity and an approved production limit:

- Candidate [Runtime v1](../../spec/core/F65_65Aero_Engine_Runtime_and_Technical_Supplement_v1_HUMAN_APPROVED_CANDIDATE_DESIGN.pdf)
  section 8.4 requires machine-readable geometry, audio and sensor high-water
  observations; it does not authorize an average as worst-phase evidence.
- [Graphics v2.1](../../spec/subsystems/F-65_Megawing_Graphics_White_Paper_v2.1.pdf)
  sections 16.2-16.5 retain measured geometry admission, fixed bounds and
  deterministic overflow; this observer chooses no renderer budget or policy.
- [Audio v1](../../spec/subsystems/F-65_Megawing_Audio_Sound_Effects_and_Music_Engineering_White_Paper_v1.0_FINAL.pdf)
  section 20 distinguishes channel/cache occupancy from voice stealing,
  preemption, external latency and underrun evidence. None of those latter
  claims is inferred here.
- [Sensor/Track v1](../../spec/subsystems/F-65_Megawing_SensorAndTrackEngine_Engineering_Model_Phase-3_v1.0.pdf)
  section 5 requires capacity-isolated 24-slot MEGA and RED domains. The
  recorder does not fuse knowledge, allocate tracks or access private arrays.

`interfaces/r0f_group1_pool_contract.json` owns the private fixture units,
capacities and input-stream parameter, generating `r0f_group1_pool.h`.
Geometry fixtures use 16 faces, 32 vertices, 32 spans and eight buckets; these
are test inputs, not measured production ceilings. Four PCM channels, a
255-byte cache fixture and two 24-slot domain fixtures exercise distinct units,
not physical PCM, actual audio scheduling/cache or real sensor allocation.

The generic observer owns only its caller-supplied native C state: immutable
interval capacity, observed peak, sample count and full-capacity sample count.
Owners supply occupancy after every relevant transition, including zero. No
capacity value is relabeled as an observed peak. Full occupancy is a fact,
not a universal acceptance failure/success. It does not allocate, release,
evict, steal, shed, schedule or modify authoritative simulation.

Invalid state, occupancy above capacity and sample-counter exhaustion return
failure without changing any state byte. Caller integration must fail evidence
acquisition on rejection; no saturation, dropped observation or automatic retry
is admitted. Initialization explicitly starts a new interval; the synthetic
3200-tick test does not reset at its midpoint. That host interval is not proof
of preservation across actual returning storage. Native sizeof is measured,
not a hand-authored public or serialized layout. Single foreground owner only;
no concurrency/IRQ atomicity guarantee.

## Validation and retained failure

```sh
python3 -B tools/diagnostics/r0f_group1_pool_build.py
python3 -B tools/diagnostics/r0f_group1_pool_fit.py --out build/r0f/group1/pool-core/admission-probe-01
python3 -B -m unittest discover -s tools/diagnostics -p 'test_r0f_group1_*.py' -v
git diff --check
```

Successful qualification and static probe commands exit 0; the fit report
itself is FAIL, `admitted: false`, `executed: false`. Exact compile commands,
inputs, tool pin, target object hashes, native-size symbols, actual C output
and independent Python comparisons are retained in
`build/r0f/group1/pool-core/validation.json` and the fit report.

The first host corpus correctly failed `missing empty/full pool pressure`:
its input progression aliased the MEGA fixture modulo 25 and never filled it.
The rejected output and exact fixture/validator sources remain in
`missing-pressure-01/`. Correcting the input to a generated per-owner offset
of a unit-stride progression covers every occupancy. The observer and its
validation requirements were not weakened.

Preserved integrated PRG:
`25a18c23c750d0877103209fccd0114afe7cd30f31690731605b9687bfea94e1`;
all 93 build inputs remain unchanged. The complete preceding 1389-file freeze
is reverified. Canonical `R0FG1P02.D81` remains
`60cea9c8dd51b0f2c199605e60574c0bebd7c758d5899fb9b1e7c2901f83e832`,
XEMU_BOOT_VERIFIED only; it is not rebuilt or retested. Earlier `ec259fc7...`,
`0d96a1b...`, `c249f4e4...`, ordinary successor and all prior manifests remain
unchanged. New evidence is frozen separately under
`docs/evidence/r0f/group1/2026-09-30-pool-core/`.

## Effects and next action

Ordinary compiler-managed C register/stack clobbers only. Caller-owned resident
state is charged by the target size probe; no physical allocation is admitted.
The new code is not linked into the running fixture, so hardware registers,
MAP/base-page, DMA, tick/deadline and IRQ/NMI effects are non-applicable to the
preserved build. The dormant fit artifact is rejected before execution.
Generated private fixture bindings are current; public interfaces unchanged.

Next recover resident space within the existing envelope, retaining exact old
inputs and proving behavior/timing for any changed PRG. The measured 626-byte
shortfall is a lower bound: real owner hooks and versioned transport add cost.
A bounded smaller CRC-table experiment is a possible memory/speed tradeoff,
not a selected correction or authorization to accept new deadline misses.
Then integrate actual owner observations, independent trace checks and fresh
NTSC/PAL timing before a new exact carrier. Do not substitute this synthetic
host corpus for that work. Integrated near-capacity trace, compact operator
summary, production geometry/projection/directional hysteresis, full audio and
sensor behavior, whole-ISR/entry latency, physical SI/SD/chooser/runtime gates
and owner acceptance remain open. No full Group 1 or R0-F acceptance is claimed.
