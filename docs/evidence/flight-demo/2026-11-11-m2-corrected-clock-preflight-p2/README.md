# CC3 publication-wait P2 evidence

Correction identity: `65AERO-M2-PREFLIGHT-WAIT-P2-1`.
See [P2 report](../../../reports/M2_CORRECTED_CLOCK_PREFLIGHT_WAIT_P2.md).

- `before.json` and `prior-*`: exact active identities and source/WIP before
  correction. The original 34-member packet and its seal remain unchanged.
- `run-1/`: 21 passing host tests, two expected mutation refusals, preflight
  refusal and exact final host source. Commands, exits and stdout/stderr retained.
- `mutation_probe.py`: stdout-only in-memory negative checks, no source edits.
- `historical-preservation.*`: unchanged original preservation checker output.
- `check_scope.py`, `static-*`: focused static and preservation evidence.
- `source-identities.json`, `host-tool.json`, `final-source.tar.gz`: final
  identities and host sources; no SDK binaries or ROMs.
- `seal.json`: final packet inventory, sizes and SHA-256 hashes.

The original preflight output is reproduced byte-for-byte, with exit 2 and
actual admission UNPROVEN. No target compiler, linker or runtime was invoked.
Tests use temporary fixtures; the mutation harness emits stdout only. Replays
must direct outputs to fresh locations outside every sealed packet.
