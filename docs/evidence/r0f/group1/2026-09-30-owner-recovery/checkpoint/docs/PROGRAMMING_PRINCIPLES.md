# Programming principles

These rules apply immediately to new and materially changed program, build,
validation and test code, including R0 diagnostics. They apply across C,
assembly, Python and Java. R0's test purpose is not an exemption.

## DRY: Don't Repeat Yourself

- Give each rule, layout, numeric contract and piece of knowledge one
  authoritative home. Generate language bindings from the governing contract.
- Extract shared behavior when it represents the same responsibility and must
  change together. Call that implementation rather than copying it.
- Similar-looking code with different ownership, failure rules or lifetimes
  need not share an abstraction. Do not couple independent responsibilities
  merely to reduce line count.
- Independent validation must remain independent: share the declared wire
  format and inputs where appropriate, but do not make an oracle call the
  implementation it is supposed to check. Independent calculation is
  deliberate verification, not accidental duplication.

## ETC: Easy to Change

- Put each likely change behind a small, named boundary with explicit inputs,
  outputs and side effects. Prefer a local edit over synchronized edits in
  unrelated files.
- Keep configuration and generated constants separate from algorithms.
- Prefer plain control flow, bounded data and narrow interfaces. Avoid hidden
  global mode switches, copied build pipelines and speculative frameworks.
- Test observable requirements, failure behavior and boundaries. Tests should
  support safe changes without depending unnecessarily on internal structure.
- Record the reason for hardware-specific constraints and optimizations. Easy
  to change does not mean relaxing an admitted timing or restoration contract.

## Orthogonality

- Separate workload, timing measurement, evidence encoding, transport and
  acceptance evaluation. A transport failure must not rewrite acquisition
  results; a timing result must not silently change the workload.
- Separate pure policy/arithmetic from hardware access and orchestration.
  Keep hardware register, memory and lifecycle ownership explicit.
- Avoid unrelated side effects. Changing presentation must not change model
  state, checksum, scheduling semantics or storage ownership.
- Use dependency direction deliberately: low-level primitives do not select
  test cases, and validators do not depend on UI or SD delivery operations.

## Review and scope

For each change, check whether knowledge was duplicated, whether the next
reasonable change stays local, and whether unrelated behavior remains
independent. Apply these rules while doing the authorized work; do not defer
them until production development.

Preserve retained proof source and evidence. Do not mass-refactor historical
code solely to apply this guide. Governing contracts and generated layouts
remain authoritative. C-specific naming, formatting and readability rules
are in [CODE_STYLE_C.md](CODE_STYLE_C.md).
