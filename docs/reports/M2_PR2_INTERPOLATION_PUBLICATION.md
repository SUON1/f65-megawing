# Bounded interpolation and verifier publication

The founder approved the bounded interpolation result and the BIT/CLV verifier
fix after read-only reviews, then authorized commit, push, PR, merge after
checks, verification of main and stop. This record defines the narrower
publication independently of the reconstructed renderer development tree.
Historical pending/failed/stop wording in preserved documents continues to
describe the original checkpoint; no old record is relabeled.

The only active target production change is the exact reviewed private
`interpolate_delta` function in `src/graphics/m2_geometry.c`: select the current
unsigned magnitude's high bit and advance it once after the two subtraction
tests. All 64 iterations, recurrence, sign restoration, rounding and narrowing
remain unchanged. The approved host checker adds exactly BIT/CLV recognition,
with its six regression methods and shared fixture helpers. No other active
production function, header, public/generated record or memory ledger changes.

Publication includes the direct-helper corpus/comparator, approved planning and
reconstruction documents, three reports and all three original immutable
packets: initial failed checker gate, bounded verifier correction and resumed
single composed relink. Renderer/cache/dispatch code and private prepared-owner
comparison remain preserved in the development checkout and archived source
snapshots, outside main's active source tree. No full composition is rebuilt
during publication.

One exact-path SHA-256 whitespace exception preserves the original font
snapshot copy in the interpolation packet. The exception has changed-byte
rejection coverage, and an unlisted neighboring path remains subject to normal
whitespace checks. No directory-wide or binary/media exception is added.

[Fresh publication validation](../evidence/flight-demo/2026-10-22-m2-interpolation-publication/README.md)
passes all 457,334 direct old/new/independent-integer comparisons with 29,269,376
bit-state checks, frozen 799,886 projection cases plus 34 contract checks,
3,857 independent Decimal cases, 841 near/far/reversed clipping regressions,
sanitized replay, 11 contract/verifier tests and 15 static-hygiene fixture tests.
Both regenerated corpora retain their reviewed exact hashes. The fresh
standalone target PRG is byte-identical to the reviewed probe:
`622ff2318cdf7cee9cd3be721fabb118a56cf0929eb0fb58debcad6cd53fb88d`.
Its sections and stack result match: 20 hardware bytes including entry return,
zero dynamic software bytes, 487 resident compiler-scratch bytes and resident
end `$629F`. These standalone bounds do not admit the full renderer.

The [retained composed result](M2_PR2_INTERPOLATION_RELINK_RESULT.md) saves
385 resident bytes: 34,149 → 33,764, with interpolation 1,605 → 1,257 text bytes,
31-byte shift helper and one-byte SDK constant removed, and five alignment
bytes recovered. It still exceeds `$8000` by **9,189 bytes**, ending at `$A3E5`.
Resident compiler scratch remains 200 bytes, charged once. Projection-closure
stack analysis passes at 24 hardware / 8 dynamic software bytes, unchanged;
whole-program proof remains unsupported at CLD in both artifacts. Structural
instruction bounds establish no cycle WCET or 100 Hz service admission.
These are exact retained-composition measurements, not a complete renderer
built from the narrower publication tree.

All earlier evidence inventories and bytes, original checkout path sets,
75 retained raw files and 20 unrelated entries remain exact. Generated
contracts and memory ledgers match the verified baseline. Packet hashes,
source-scope, links, JSON/Python/shell syntax and static-hygiene checks complete
local publication validation; exact-head PR CI and integrated-main CI are
separate publication gates.

No ABI/layout, precision, memory ownership/limit, reserve, hardware register,
MAP/base-page, DMA, IRQ/NMI or admitted service-budget change. Full resident
fit, whole-program stack/ABI/timing and runtime/display admission remain open.
No additional optimization, Xemu, D81, SD or physical testing is authorized.
Verify merged main, then stop.
