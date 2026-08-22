# DEC-012 — R0-C Save Medium and Recovery Policy

Status: **OPEN — human approval required before R0-C formal acceptance**.

| Candidate | Device/write protection | Recovery/testability | D81 impact and friction | R0-C recommendation |
|---|---|---|---|---|
| Same distribution D81 | Mount may be read-only or replaced; user media can be at risk | Fault injection is possible only on a sacrificial copy; content and saves contend for space | Simplest boot path, but couples distribution and mutable state | Not recommended for acceptance |
| Separate writable D81/image | Explicitly mount a sacrificial writable image; write protection and removal can be tested | Two-generation selection and every interruption point can be tested without risking the distribution image | Requires one additional image/mount action | **Recommended R0-C candidate** |
| Supported host storage | Depends on documented hardware/core service and host/device configuration | Cannot be admitted until the exact service, removal behavior, and transactional primitive are documented | Potentially convenient but higher configuration variance | Deferred pending documentation |

The recommendation is not a production selection. The owner must choose the
medium, supported physical configuration, recovery policy, and test media before
`R0C-SAVE-001`/`R0C-MEDIA-001` can pass on physical hardware. `DEC-015` remains
outside R0-C and is not decided here.

Required approval text: identify one medium/configuration, confirm sacrificial
media is acceptable, and approve recovery behavior after a failed/interrupted save.
