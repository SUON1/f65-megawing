# P07 readiness diagnostic — 2026-10-03

The owner authorized a bounded local diagnostic with “Execute” after P07's
physical `6F/0A/0C80/1F/00` failure and returned-card verification. Two copied-
source variants compile/link but both fail resident fit. Neither executed;
no P08 carrier exists. The initial two-attempt limit is reached.

| Variant | Resident exclusive end | Over limit | PRG bytes |
| --- | --- | --- | --- |
| readiness-01, named predicates | $C012 | 18 bytes | 37538 |
| readiness-02, asserted-layout loop | $C02C | 44 bytes | 37564 |

First PRG SHA-256:
`16c326461d852a59513acf136cae86017b164773c42e5a2960a4f142f21078e4`.
Second PRG SHA-256:
`1b3eb192ccf56bb6642c2f1c905bf410f503aa7d43426fcdf9e720d95c63bb7f`.

## Authority and scope

Inspected repository state/WIP/workflow, programming and C standards, Group 1
Build Intent and export amendment, the qualified P07 private export policy,
transport/capture source and generated bounds, build/validation tooling and
physical evidence. Remote main remains c27d89787d1d5c4472e24262e0181c47943d46be;
branch is codex/r0f-group1-resume-clock. No publication is included.

Each variant is isolated under
`build/r0f/group1/terminal-recovery/readiness-01/` or `readiness-02/`.
The original P07 source, PRG, canonical image, physical records and failed
carriers remain unchanged. Root target source and CURRENT_STATE are unchanged.

The diagnostic retains all readiness conditions, order, byte bounds and policy
state transitions. A pure private diagnostic function returns zero for entry
or the first rejection code; the existing boolean interface wraps it. The
transport stores a nonzero rejection in the existing protected status byte.
Prior broad marker increments are removed only from these new copies.
No new allocation, public/generated ABI, capacity or reserve changes occur.

Unexecuted code meanings: 6B generic preparation; 70 invalid policy state or
null export; 71 null readiness; 72 acquisition; 73 DMA; 74 display; 75 audio;
76 IRQ mask; 77 ROM; 78 capsule; 79 NMI; 7A empty export; 7B capacity overflow.
These codes have no new physical observation and must not be applied to P07.

The second variant traverses the private readiness object's unsigned-character
representation, with compile-time assertions for every offset and total size.
It preserves the first-seven-equal-one/last-equal-zero comparisons. The target
compiler emits a larger result than the first variant; source brevity did not
reduce resident size.

Registers/clobbers are ordinary compiler-managed C state. CPU-visible status
storage is the existing $2F98 byte. Physical allocations, MAP/base-page, DMA,
clock/deadline and IRQ/NMI policies are unchanged. No additional hardware
register reads or writes are introduced. Reporting remains outside acquisition.

## Validation and preservation

The preparation scripts invoke the existing pinned owner-integration builder
with the P07 predecessor and matching terminal validator. Both compiler/link
runs complete; protected IRQ/terminal static checks pass; resident fit fails.
The exact compiler commands, inputs, PRGs, symbols and local artifact hashes
are retained. No full host admission, Xemu, D81 construction, SD access or
physical execution follows either failed fit.

A separate pure-policy differential test compares each actual candidate
against the extracted original P07 boolean implementation. Each passes
**2,624,256 comparisons** under Clang AddressSanitizer/UndefinedBehaviorSanitizer,
covering every byte-valued policy state, each field's 256 values, five length
boundaries, null pointers and combined invalid readiness fields. Acceptance,
policy state transitions, untouched byte count/CRC and exact first-rejection
codes agree. This is policy evidence only; hardware and capsule edges are
not exercised by this test and target admission remains blocked.

Preparation commands:
`python3 -B /private/tmp/prepare-readiness-diagnostic.py` and
`python3 -B /private/tmp/prepare-readiness-02.py`.
Policy comparison: `python3 -B /private/tmp/verify-readiness-policy.py`.
Copies are retained in the evidence packet; these scripts refuse existing
output directories and are provenance, not instructions to replay this work.

The frozen [evidence packet](../evidence/r0f/group1/2026-10-03-readiness-diagnostic/README.md)
contains both patches/changed sources, build records/PRGs and host tests.
Original P07 source supplies unchanged files, identified by each exact input
manifest. Patch replay, source identities, generated identities, predecessor
manifests, packet hashes and whitespace are checked at closeout.

## Disposition

BLOCKED on resident fit. P07's actual returning SAVE remains valid; its physical
terminal-readiness failure is not corrected or further localized. Group 1
acceptance and Group 2 progression remain pending. The next local task is a
size-focused review of terminal reporting: the smaller attempted variant needs
at least 18 bytes recovered without removing integrity predicates or borrowing
reserves. Review before another bounded implementation attempt. No new card
run is ready, and P07 must remain retired.
