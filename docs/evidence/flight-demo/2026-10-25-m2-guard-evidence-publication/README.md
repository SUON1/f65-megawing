# Accepted guard-test patch and host-evidence publication

25 October 2026. Founder acceptance is limited to the reported host-test scope.
The founder explicitly selected publication of the exact patch and sealed host
evidence only. Main does not contain the M2 minimum-renderer test or its
unapproved dependencies; this record does not activate that implementation.

- [Exact test patch](accepted-test-patch.json): join `lines` as UTF-8 to recover
  the original test-only unified diff. The JSON representation preserves all
  bytes, including diff context whitespace, without changing CI exceptions.
- [Original correction packet](accepted-host-evidence.tar.gz): a deterministic
  archive of the original ten sealed members plus their unchanged inventory.
  All members remain byte-identical. Historical WIP and review wording inside
  the archive retain their checkpoint meaning.
- [Identity and scope record](record.json): original packet, patch, source and
  host-log hashes; separately scoped development-candidate gate summary.
- [Preservation before](preservation-before.json) and
  [preservation result](preservation.json): existing worktrees and evidence.
- [Packaging verification](verification.json) and [new seal](inventory.json).

Run only the new read-only packaging check from the repository root:

```text
python3 -B docs/evidence/flight-demo/2026-10-25-m2-guard-evidence-publication/verify.py
```

It reads archive members in memory. It does not extract or execute the archived
test/checker, rerun the accepted 13 host tests, build/relink a target, or launch
Xemu. The archived checker depends on its historical development worktree and
is retained for provenance, not enabled as a main test.

The original correction inventory remains
`47c6fe4ed7a641c312e59563fa67a784d9b307612745cc4248d8870724eef116`;
the original runtime packet remains
`d5fce59c011225643d27d884454c7b7982e7a99dfbd4e1af598a4a4fb200a245`.
Original failed artifacts and all unrelated paths are preserved. No active
source, generated contract, memory ledger, hardware behavior or CI exception is
changed. [Publication report](../../../reports/M2_GUARD_EVIDENCE_PUBLICATION.md).
