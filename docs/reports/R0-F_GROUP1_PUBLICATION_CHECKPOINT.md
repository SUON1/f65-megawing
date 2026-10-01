# Group 1 preservation publication checkpoint — 2026-10-01

## Authority and boundary

The owner explicitly approved a reviewed checkpoint commit and push of the
current Group 1 work, labelled **local/Xemu validated; physical testing
pending**. This is preservation, not Group 1/R0-F acceptance, measured-limit
approval, a merge, an SD delivery or a physical run.

The [approved Build Intent](../plans/R0-F_GROUP1_BUILD_INTENT.md) and
[development workflow](../DEVELOPMENT_WORKFLOW.md) govern. Earlier frozen
records saying commit/push were not authorized remain accurate for their
original checkpoints; this later approval does not rewrite them.

## Exact preserved candidate

The latest tested target is the isolated version-7 candidate, not the earlier
root working source. Its complete 124-input build snapshot is retained at
`docs/evidence/r0f/group1/2026-10-01-capacity-summary/experiment/runtime-01/source-checkpoint/`,
with commands and input hashes in the adjacent `build.json`.

- PRG: adjacent `GROUP1.prg`, 37,517 bytes, SHA-256
  `c068cc532dc820845d8c0649b1c2ea7dfc0bda394b32f7c186088a04d0dc048b`.
- Exact carrier:
  `docs/evidence/r0f/group1/2026-10-01-capacity-summary/carrier/canonical/R0FG1P04.D81`,
  819,200 bytes, SHA-256
  `2519af02741197fb8851dccc26ab1379591d5340f1cae3b68cb243844c3730d4`.
- Resident end exclusive `$BFFD`, three bytes free; no expansion claim.
- Carrier state remains `XEMU_BOOT_VERIFIED`, not `TEST_ELIGIBLE`.

The frozen copies match their live build artifacts byte-for-byte. Publishing
them does not rebuild, relabel, rename, mount or retest the carrier. Source
commit fields in earlier build/evidence records identify their historical
base; the commit containing this report preserves the previously uncommitted
source snapshots. Historical source identities are not silently replaced.

## Publication scope

Include Group 1 source, private/generated contracts, memory ledger, controllers,
tests, plans/reports, retained Group 1 acquisition and trial evidence, and the
successor capture/IRQ dependencies needed by these sources. Preserve earlier
passing/failed source variants rather than overwrite them with the new variant.
The retained evidence snapshots contain the latest exact source even though its
live build directory is ignored by Git; `build/` remains transient/ignored.
The evidence-only `.gitattributes` disables text normalization so retained
monitor logs, source snapshots and binary captures round-trip byte-for-byte.

Do not publish the unrelated SD backup/mirror tools or reports, or the older
successor physical-photo/SD-delivery evidence directories in this checkpoint.
Those local files remain intact and outside the staged scope. Historical links
to that locally retained material are not evidence that it was published here.
No repository visibility change or physical acceptance is included.

## Preservation and validation

Fresh publication preflight establishes:

- Remote task branch and local HEAD agree at
  `9e2ffdb4786e4794119933a5edd4b1cf79f653f0`; fetched `origin/main` remains
  `ae2b397698cc7197d03349e57cd058b4fb9f3987`.
- Twelve frozen SHA-256 manifests verify all 7,511 entries: 5,726 predecessor
  entries and 1,785 current entries. All four original baseline PRGs, including
  `ec259fc7...`, remain unchanged.
- Passing input sets verify 93 root, 95 P02, 133 P03 and 134 P04 inputs.
  All 124 current frozen build inputs match their recorded hashes.
- `python3 -B -m unittest discover -s tools/diagnostics -p 'test_r0f_group1_*.py' -v`:
  47 tests PASS.
- `python3 -B tools/diagnostics/test_r0f_successor_capture.py`: seven tests PASS.

The [capacity/summary report](R0-F_GROUP1_CAPACITY_SUMMARY.md) records the prior
fit, native host, focused NTSC/PAL and four exact-carrier boot results. These
are retained observations, not newly executed target or hardware tests.
Frozen manifests and staged source bytes must remain identical during
publication; retained proof source is not restyled for this checkpoint.
Whitespace checks apply to the changed live source/documentation; historical
whitespace inside immutable evidence is preserved rather than normalized.

Registers/clobbers, CPU-visible/physical allocation, MAP/base-page, DMA,
timing/deadline and IRQ/NMI effects of this publication step: **none**.
Generated target layouts are preserved, not regenerated or changed.

## Next action

Keep the exact P04 target frozen. Separately approve SD delivery/carrier gates
and the bounded normal-workload physical Group 1 test, then independently
reduce the actual returned trace and review the result against the approved
scope. A missing case must be specifically identified against that scope.
Production renderer/model work, universal worst-case claims and Groups 2/3
are not automatically added to this checkpoint or to Group 1 implementation.
