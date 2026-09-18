# R0-F Step 3 audit — 2026-09-16

Status: **EXECUTED — STATIC GATE BLOCKED**. Native host tests and LLVM-MOS
compile/link pass. This review covers the existing bounded functional/raster
proxy. It does not complete the full R0-F measurement program or authorize
advancement to a new carrier.

## Finding requiring platform resolution

`R0F-STATIC-STARTUP-001`: the linked startup establishes B=$02 at $2025–$2027,
then `.init.250` calls KERNAL $FFD2 at $2035 before main. There is no intervening
B-save/B=$00/B-restore thunk. The R0-A B-register integration decision expressly
requires a separately proved thunk for KERNAL calls. Successful prior boot and
owner-reported runtime do not prove the missing calling-convention guarantees.
No ROM clobber or post-call interrupt behavior is inferred here.

The same listing shows stock startup SEI and writes to $00/$01/$D030. Previous
impact wording described only the private raster helper and incorrectly extended
its read-only/no-IRQ-change description to the entire linked program.

Resolve this startup path under the platform contract before passing Step 3.
Any target change needs its own build, ABI checks, fresh carrier identity, two
clean Xemu boots, and physical evidence under the root D81 gate. No target startup
fix or new wrapper was silently selected in this review.

## Corrections and validation

- Corrected the Step 2 completion claim: calibration is NOT PERFORMED; the full
  measurement contract and Java oracle remain incomplete. Source/static review
  is not formal architecture or owner acceptance.
- Corrected result-header, sample-order, false-pass-test, and register descriptions
  in the private contract. The 100 Hz field is unpaced model metadata. Cross-case
  execution order is not specified by the bitwise-AND C expression; within-case
  requested low-byte phases and payload positions are defined.
- Host validation now checks previously unchecked profile/snapshot metadata and
  reserved bytes. Both normal and timeout fixtures reject changes to every fixed
  byte with a recomputed valid checksum, explicit failed status, bad checksum,
  short record, and long record: 358 rejected mutations. Raw sample values 0 and
  255 remain valid observations. No elapsed-time threshold is invented.
- Accounting now includes `.basic_header`, `.noinit`, and empty direct-page
  sections, and checks nonempty linked-section bounds and overlaps. The existing
  107-byte compiler static stack is charged to the R0-F private ledger.
- Added `sh tools/build/r0f.sh audit`: build, ledger reconciliation, known startup
  ROM-call detection, retained Xemu result revalidation, and a machine-readable
  report. It exits 2 for the discovered startup conflict. It is a bounded check
  for this proof, not a general verifier of arbitrary assembly or ROM behavior.

## Inspected contracts and impact

Inspected the official record; frozen Architecture 1.4.1 and candidate 1.5.1
(MemoryAccessABI, memory ownership, timing, ABI and evidence requirements);
approved Read-First/AD-001/approval records; relevant Engine 0.2 ABI, memory,
build and acceptance sections; current `memory/` and `interfaces/` registries;
R0-A handoff and B-register decision; R0-F plan, stage control, test guide,
handoff/evidence map; target C, R0-A startup assembly, host mock, generator/build
script, lock, linked map/symbols/disassembly, and retained result blocks.

Changed this step: `interfaces/r0f_proof_contract.json`,
`memory/r0f-memory-ledger.json`, `tools/diagnostics/r0f_build.py`, R0-F plan/stage/
impact/handoff/evidence records, this report, and the official status index.
Pre-existing working-tree physical-evidence changes were preserved. No target
source, public ABI, preserved specification, pool, reserve, or ownership changed.

Registers: compiler C uses the pinned ABI, pseudo-registers and processor flags;
no new A/X/Y/Z/Q/B/P/SP preservation claim or handwritten wrapper. B entry is
$02; fini would restore $00 but main does not return. ROM-call clobbers are the
open finding. Logical compiler pseudo-registers remain $02–$21, addressed through
the relocated base page. Hardware stack $0100–$01FF and base page $0200–$02FF
retain their existing roles. No new MAP, DMA, IRQ/NMI or timing operation is
introduced; latency, dynamic stack high-water and production canonical state
remain unverified. Protected physical $050000–$05FFFF has no proof allocation.

| Linked storage | CPU range | Bytes |
|---|---|---:|
| BASIC header | $2001–$2016 | 22 |
| Code and runtime | $2017–$302D | 4119 |
| Read-only data | $302E–$3254 | 551 |
| Initialized data | empty | 0 |
| Snapshot BSS | $3255–$3314 | 192 |
| Compiler static stack (`.noinit`) | $3315–$337F | 107 |
| Total linked resident storage | $2001–$337F | 4991 |

Separate fixed result storage is $1900–$19FF (256 bytes); screen storage is
$0800–$0FCF (2000 bytes). Software stack top is $D000; a top address and static
allocation do not establish worst-case dynamic usage. The map's heap symbols
are linker markers, not evidence of a heap allocation or permitted heap use.
The main proof contains no storage calls; the pre-main ROM call remains separately
unresolved. R0-F remains a standalone proof overlay, not a production module-fit
or canonical runtime acceptance result.

## Commands and evidence identity

| Command/check | Result |
|---|---|
| `sh tools/build/r0f.sh build` | PASS; includes native C sanitizer and result-validator tests |
| `sh tools/build/r0f.sh audit` | Expected exit 2 / BLOCKED after host and compile/link PASS; startup conflict recorded |
| Stored `docs/evidence/r0f/xemu/evidence.json` result blocks with strengthened validator | PASS for both; no new emulator run |
| Generated header and target source diff against HEAD | Unchanged |
| `git diff --check` | PASS |

Current source base: `744920dd76d008fbc0ccce82e006cc0b647f477e` plus working-tree
inputs. Exact input/artifact hashes and current results are retained under
`docs/evidence/r0f/step3/2026-09-16/`. Prior `host/` and `xemu/` evidence was not
overwritten. Regenerated PRG/ELF/map/symbols/disassembly and reports are in
`build/r0f/`; the generated C header is byte-identical.

PRG: 4694 bytes, SHA-256
`510c2bfc8686f86b5fd934edd0b9863c0a176951a2871eaa0f990c8e0cec106e`, matching the
retained tested build. Historical carrier identity is F65R0F1.D81,
SHA-256 `9b539a14f08d671195ef71e54bbacb3eacd5258634f7a29396bf00a068cddd89`;
this audit did not create, modify, mount, copy, test or release any D81.

No fresh Xemu or physical run occurred. Java oracle implementation/execution,
calibrated independent-clock measurements, rolling deadlines, input/audio
latency, high-water, admitted DMA/IRQ instrumentation, full platform identity,
and owner acceptance remain outstanding. Step 3 cannot pass while the startup
contract conflict and full measurement prerequisites remain open.
