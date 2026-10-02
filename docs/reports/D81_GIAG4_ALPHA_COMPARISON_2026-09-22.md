# GIAG4 failure versus the physical Alpha control

Status: read-only investigation; no replacement image and no SD writes.
Authority: owner failure report, existing workflow recovery intent, root
loadability gate failure handling. No target code, register/clobber, CPU or
physical memory, MAP/base-page, DMA, timing, IRQ/NMI or ABI changes apply.

The owner's first photo shows `R0FGIAG4.D81` selected with chooser FF. The
second shows `F65-R0A-PROOF.D81` in the MegaWing folder with its directory
readable, including AUTOBOOT.C65 and F65-R0A-PROOF. The owner reports that
Alpha works. Its historical physical pass is also documented in
`docs/evidence/r0a/R0A-D81-CONTAINER-FINDING.md`.

The GIAG4 tested copy is INVALID — DO NOT USE. Historical host/Xemu evidence
must not be relabeled as physical success. The prior handoff did not satisfy
the owner's requested working physical workflow.

## Live read-only findings

- `/Volumes/MEGA65FDISK/A. MegaWing/F65-R0A-PROOF.D81`: 819200 bytes,
  SHA-256 `40d95171389e3825793216ed54176084a87bad5bac630b942955c8b90668b3b4`.
- `/Volumes/MEGA65FDISK/R0FGIAG4.D81`: 819200 bytes,
  SHA-256 `90a819f49c5b6cb3bf66f71317c1f40e3cae3f4059fb422b46b05589e86915fa`.
  Its complete byte array equals the canonical build's byte array.
- Both pass `d81_foundation_compare.Image` geometry, directory, chain, BAM
  ownership/accounting parsing. This is host evidence, not mount proof.
- The 256-byte track-40/sector-0 headers differ only at offsets 4 through 11,
  containing disk labels. No other header byte differs.
- Alpha contains a 32-byte autoboot and 840-byte proof; GIAG4 contains a
  464-byte autoboot, 21921-byte successor and 34-byte token. File/directory/BAM
  differences exist; no causal conclusion is inferred from these sizes.
- Alpha's checked-in `tools/build/r0a.sh` and the successor builder both use
  fresh format and all payload writes in one `c1541` invocation. They name
  different executables. Current old-path binary SHA-256:
  `597907f1cad64d74f33f3631fb23a9d9b0e66445069333d4025e92f8f03b4e3c`.
  Current successor pinned binary SHA-256:
  `73235289aca30a7e2e8067e521bf604743156cc1d7499c888a3894d6e46fcb3c`.
  These are current local identities, not proof of the historical executable
  used to produce the on-card Alpha bytes. The difference merits investigation.
- The working long Alpha name disproves any claim that an eight-character
  basename is universally necessary for this chooser. The repository's
  conservative new-image naming rule is not a diagnosis of this failure.

The initial raw GIAG4 audit required local authentication. The owner then ran
it successfully: `build/r0f/2026-09-22-forensics/giag4-raw-audit.json` confirms
the exact canonical hash in **four extents**, of 49152, 253952, 155648 and
360448 bytes. This is a measured allocation-gate failure, distinct from
DIAG2's 13 extents. No card-wide defect is established.

## Next discriminating check

The allocation failure is now established. The owner explicitly approved a
new candidate via the qualified direct allocator, leaving existing files
untouched. New delivery identity is R0FHOST2.D81, with unchanged T06 payload
and repeated exact-name host/Xemu gates. Do not overwrite the Alpha control
or retest GIAG4; a physical pass remains required for the new delivery.
