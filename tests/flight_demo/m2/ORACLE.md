# Frozen PR1 oracle and cases

Authority: approved M2 plan D1–D6. Freeze before implementation tests.

Use Python Decimal at 60 significant digits. Compute sin/cos by independently
converged Taylor series using a literal high-precision pi; do not read the C
sine table or call target functions to obtain reference coefficients.
Quaternion q = q_yaw * q_pitch * q_roll (Hamilton scalar first), camera to NED.
Rotate world-minus-camera by q conjugate to obtain forward/right/down.
Clip segments by independent parametric interval intersection against the six
linear halfspaces X>=10, X<=40000, -X<=Y<=X, -2X<=5Z<=2X.
Project u=159.5+160Y/X, v=63.5+160Z/X. Raster reference is independent DDA;
compare point sets with Chebyshev distance <=1 pixel, numeric endpoints <=0.5.
No comparison to the C implementation itself as the expected value.

Cases: reset and all sign axes; yaw 0/90/180/270/359, pitch/roll -60/0/60;
camera envelope extrema and east offsets; explicit near/far and four viewport
crossings, behind/empty/degenerate segments; seeded random general segments
and points. Seed 650201, 2000 general segments and 1000 near-camera segments plus all 17 fixture segments
for each of 45 frozen camera combinations. Clip ambiguity only within the
approved near/far 1/1024-ft band; no non-finite/overflow success accepted.
Negative cases: invalid camera/fixture/revisions, world-range and raster-capacity
failure, and incomplete/stale/mismatched registration eligibility. Sentinel
outputs remain unchanged on failure. Horizon ray sign matches the same rotation.
Host M1 replay checks every authoritative tick with no geometry, normal geometry,
and intermittent/cancelled geometry; checkpoint remains DE675132.

PR1 does not activate a display or implement the PR2 renderer/keyboard driver.
