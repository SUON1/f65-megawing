# M2 PR1 clipping P2 correction

**READY FOR REVIEW.** Founder-authorized correction on `codex/65aero-m2-pr1-geometry`, still based on main `2acd30c21a4be0996cd1a2dd3ce74da6deb6c84d`. The [approved M2 intent](../plans/65AERO_M2_REGISTERED_RUNWAY_CAMERA_BUILD_INTENT.md) and its unchanged acceptance limits govern. This corrects the numeric P2 found after the [original PR1 report](M2_PR1_GEOMETRY.md); that report, its evidence, original oracle description and all prior build outputs are preserved. This report supersedes their numeric representation, current validation and memory accounting only.

## Correction and contract effects

[Graphics](../../src/graphics/m2_geometry.c) previously rounded transformed coordinates to Q12 before clipping. Nearly parallel crossings amplified that rounding into a 2.419677-pixel error in the reported case. Keeping Q24 coordinates fixed that case, but the new far-plane cases also exposed insufficient Q30 angular precision. The final correction retains **Q24 private camera/clip coordinates and Q46 rotation coefficients** through all six planes. It does not raise the 0.5-pixel projection or 1-pixel raster limits.

[Development schema](../../interfaces/m2_pr1.json) is versioned `65AERO-M2-PR1-2`; projection revision is 2. Public point/camera position inputs remain Q12 feet, the approved fixture/camera envelopes are unchanged, and Environment remains the sole geometry owner. The generated M2Transform uses nine int64 Q46 coefficients; the target registration record grows from 83 to 119 bytes. This is a versioned development record, not a production ABI amendment. The generated quarter-wave sine table has 91 int64 entries (728 bytes), replacing the previous full-circle Q30 table. [Generator](../../tools/flight_demo/m2/generate.py) admission pins the updated source before writing; generated header, table and ledger match regeneration exactly.

All new arithmetic remains pure C. No Platform/R0 dependency, physical allocation, MAP/base-page operation, DMA, IRQ/NMI behavior, persistent state or display activation is added. Scheduling and authoritative checksum code are unchanged. The SDK-linked probe remains compile-only and is not admitted for execution.

## Numeric and work bounds

The public input bounds limit the world-minus-camera norm below 126000 ft. Q24 camera components therefore stay below about 2.12×10^12; a segment delta stays below about 4.24×10^12. Rotation coefficients are Q46 (scale 2^46). Directly multiplying either pair could overflow int64, so `interpolate_delta` evaluates the rounded product/ratio by a fixed 64-step quotient/remainder recurrence, with at most two subtracts per step. It never forms the full product. The same helper handles signed rotation products and clip interpolation. Admitted fractions have magnitude at most one; quotient magnitude is bounded by the input delta/value. Remainders stay below the divisor after each step, and the temporary remainder is below three divisors, below 2^48. No data-dependent loop, floating-point target arithmetic or dynamic allocation is introduced.

After clipping, forward distance is at most 40000 ft plus Q24 rounding; horizontal component is at most that distance. The direct Q16 projection numerator is bounded near 40000×2^24×160×2^16 = 7.037×10^18, below INT64_MAX, including rounding bias. Output narrows only to the declared Q16 screen coordinates. Record and horizon computation use the same higher-precision generated transform.

The arithmetic is more expensive than before. Six clip planes, three coordinates per intersection, 64 fixed recurrence steps, and the existing 320-sample line cap remain finite. No target timing or renderer throughput claim is made. PR2 still needs its own integrated-fit and bounded-service evidence.

## Checks and exact results

Command: `python3 -B tools/flight_demo/m2/build.py`.
Final output: `build/flight-demo/m2-pr1-1792539681412609000/`.
[New evidence packet](../evidence/flight-demo/2026-10-20-m2-pr1-clipping-p2/README.md).

| Check | Actual result |
|---|---|
| Five contract tests | PASS, including generated consistency, admission drift, nested constant software-stack adjustments and rejection of unbalanced/unknown writes |
| Original ASan/UBSan host checks | PASS; negative/registration/replay checks retain per-tick equality and checkpoint `DE675132` |
| Original independent Decimal suite | PASS: 3857 cases; max endpoint error 0.000021225 pixel; raster distance ≤1 pixel |
| New near/far regressions | PASS: 841 cases, both endpoint orders, five yaw angles, seven pitch/roll combinations and six shallow crossing depths at both planes |
| Reported P2 case | Error reduced from 2.419677 to **0.000092739 pixel** |
| Worst new regression | **0.035136325 pixel**, under 0.5; independent bidirectional raster comparison ≤1 pixel |
| New ASan/UBSan regression runner | PASS on all 841 independently authored public-input/expected-output vectors |
| Target compile/link/map/disassembly | PASS; current standalone resident end `$7466`, no reserve use |
| Identity/preservation | 28 current source/tool/configuration input hashes verified; 568 pre-correction file fingerprints unchanged; all 20 unrelated entries preserved |

[Regression description](../../tests/flight_demo/m2/CLIP_REGRESSIONS.md) and [independent generator/checker](../../tests/flight_demo/m2/clip_regressions.py) retain exact input construction and tolerances. Decimal expectations are computed from the quantized public Q12 inputs, never from target C. The native sanitizer runner uses a generated host-only vector header; its one-Q16-unit serialization allowance does not relax the strict Decimal comparison. The cases inside the approved ambiguity band also satisfy the strict projection threshold; no ambiguity waiver was needed.

The first full correction build (`m2-pr1-1792539600993544000`) stopped at the existing static gate because the widened arithmetic introduced software-stack adjustments. Those logs/artifacts remain retained. The gate was extended to recognize only the compiler's explicit constant 16-bit adjustment sequence, propagate software depth through the call CFG, reject unequal joins/unbalanced returns/unknown SP writes, and check the envelope. It was not bypassed. Earlier exploratory Q24/Q30 far-plane failures informed the Q46 correction and are not counted as passes.

### Linked memory and stack

| Section | Bytes | Start |
|---|---:|---:|
| Text/runtime support | 18892 | `$2017` |
| Read-only data | 737 | `$69E8` |
| Initialized data | 22 | `$6CC9` |
| BSS | 1456 | `$6CDF` |
| Compiler static scratch | 471 | `$728F` |

Resident end `$7466` leaves 2970 bytes below `$8000` in this standalone probe. There is a 5-byte linker alignment gap before read-only data; it is included in the resident extent. PRG is 19680 bytes, SHA-256 `4b338b0d745900532416a40ad3e9732ca412ddb009ff3a85546a9f1c14a0e15c`.

The checked probe call graph uses at most **25 hardware-stack bytes** including main's entry return and **16 dynamic software-stack bytes** (two nested 8-byte frames). The **471-byte static compiler scratch** is separately charged in resident .noinit. These replace the earlier probe's 22/0/275-byte figures; none is an exercised target high-water measurement. The existing SDK startup/register caveats and unadmitted runtime ABI remain unchanged. PR2 integration fit is still unproven.

## Stop

Review the clipping correction, new regressions, generated record revision and refreshed accounting. Original evidence remains historically truthful for its tested cases; its earlier READY status does not override the later P2 finding. No PR2, target execution, Xemu, D81, SD or physical testing was performed. No commit, push, PR creation or merge. Stop at READY FOR REVIEW.
