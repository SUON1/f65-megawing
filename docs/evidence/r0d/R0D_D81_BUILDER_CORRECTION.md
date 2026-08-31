# R0-D D81 Builder Correction

## Incident

`F65R0D.D81` and `F65R0D2.D81` are permanently invalid after physical MEGA65
chooser `ERROR CODE FF` results. Review found an additional fail-closed
construction defect: the former pinned VICE `c1541` emitted
`OPENCBM: opening dynamic library libopencbm.dylib failed!` on stderr during
construction and validation. The root D81 gate requires any warning or error to
fail the build, even when the utility exit status is zero. Those old host checks
are retained only as diagnostic observations.

## Corrected builder identity

The R0-D builder is the repository-contained
`toolchain/vice-clean/bin/c1541`, SHA-256
`73235289aca30a7e2e8067e521bf604743156cc1d7499c888a3894d6e46fcb3c`.

- VICE source: 3.10, `vice-3.10.tar.gz`
- Source SHA-256:
  `8e5bac18cbcb9f192380ad3ef881f8790f5b75c41d7b3da65d831985d864d6d1`
- Configure control: `--disable-realdevice`
- Configure observation: `checking for OpenCBM support... no (realdevice disabled)`
- Standalone smoke check: `c1541 -version` prints `c1541 (VICE 3.10)` and
  writes zero stderr bytes.

The recorded build control is `--disable-realdevice`; the repository lock
records the exact builder binary and its source archive identity. That control,
the zero-stderr smoke check, and the clean D3 construction/output are the
admissibility evidence used by the gate.

## Enforced construction rule

`tools/build/r0d.sh` now uses this builder only and rejects a nonzero exit,
any stderr output, or any case-insensitive `warning`, `error`, `failed`,
`fatal`, `duplicate`, `truncat`, or `allocation` diagnostic in every c1541
construction/listing report. The Python structural/content gate independently
applies the same clean-output rule to its listing and extraction invocations.

`F65R0D3.D81` was formatted from scratch as `F65 R0-D3`, ID `65`, and written
with both payloads in one `c1541` invocation. It is 819,200 bytes, SHA-256
`107c6a356b932e9ade875c24539d75b1b0a0078122a6a3910f524570aafec5ef`, with
host structural/content verification PASS. It remains a candidate only; no
prior D81 was copied, patched, renamed, or reused.
