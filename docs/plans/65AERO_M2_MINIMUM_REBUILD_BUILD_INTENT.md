# M2 minimum-renderer reimplementation — Build Intent

Identity: 65AERO-M2-MIN-REBUILD-1. Base: b044440fa98c2dfc91ec590668049610afc98a1e.
Founder authorizes a new implementation from verified main, preserving precision,
limits, historical evidence and unrelated paths, retaining fit failures and
stopping at READY FOR REVIEW. No banking, Xemu, D81, SD or physical testing.
The prior blocked import preflight remains unchanged historical evidence.

Owners: Environment retains all 17 fixture segments. Diagnostics owns the
mutable presentation-only camera; Input supplies semantic edges. CoreRuntime
and Presentation reuse the integrated 100 Hz/21-stage dispatcher and immutable
snapshot pool unchanged. Graphics owns captured generation, prepared geometry,
nine cached projected segments, raster continuation, telemetry and complete
publication. Platform owns hardware and typed physical copies.

Private profile: nine segments [0,1,2,3,4,5,7,11,15]; unchanged Q12/Q24/Q46/Q16,
camera limits, 320x128 logical world and 320x200 backing image, scaled inside
720x480 NTSC / 720x572 PAL. Preserve all public record layouts and FULL profile.
The new generated outer bundle declares composition revision 3; its inner
M2Registration retains the integrated public revision. No registered anchors,
ranked labels, physics or aircraft state. Both flight readings say NOT IMPLEMENTED.

Implementation: prepare one transform and project each selected segment once
per generation, then build background, cached runway and numeric telemetry
through eight bounded dispatch roles. A phase may invoke one existing bounded
geometry primitive; its target cost is UNPROVEN. No phase executes on target
unless its complete nonzero admitted bound fits before the next tick.
All target budgets stay zero. Host tests inject explicit synthetic grants;
they establish behavior, never target timing.

Hardware impact: reset-only startup normalizes both megabyte selectors and MAP,
EOM, B=$02, Z=0, E=1, CPU-port DDR=$2F/data=$35, MEGA65 I/O and page-1 stack
before dependent C accesses/BSS. No bank selection, temporary execution window,
DMA or new simulation clock. Platform uses the unchanged PF001 flat-copy
backend only behind checked display/Color-RAM classes and accounted $0222–$0229
scratch. Existing ROM-backup/clock seams remain explicit dependencies. IRQ/NMI
vectors and sticky faults must be resident; new startup/fault paths are charged.

Display writes are confined to existing stores [$020000,$02F840) and
[$030000,$03F840), immutable shared Color RAM [$0FF80000,$0FF807D0), declared
VIC-IV mode/pointer/scaling/palette registers and keyboard row selector.
Initialization keeps scanout disabled. Commit requires a safe prefetch window;
uncertainty is terminal. Registers/clobbers and restoration are documented in
the platform source. No inherited display or runtime acceptance is claimed.

Limits: resident [$2001,$8000), hardware stack [$0100,$0200), base page
[$0200,$0300), software stack [$C000,$D000), zero reserve, no other owner band.
Complete link includes real geometry, renderer/font, camera/input, core,
platform/runtime helpers and compiler scratch. Oversized images are quarantined
and normally launch into a disabled terminal path; they are never runtime-admitted.

Validation: generated-byte/schema/range checks; ASan/UBSan host rendering,
camera edges/extrema, common horizon, projection/cache counts, cancellation,
held snapshots, transfer/commit faults, exhaustion and per-tick replay.
Reuse the independent frozen 3857-case geometry and 841 near/far oracle.
Compile/link the complete mutable-camera target using the pinned LLVM-MOS
compiler and existing size flags; retain every command/log/output, exact source/
tool identities, sections, owner sizes, compiler scratch and stack limitations.
Preserve failures without automatic optimization or limit changes. No commit,
push, PR, merge or later banking task in this authorization.
