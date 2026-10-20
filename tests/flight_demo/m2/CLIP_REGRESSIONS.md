# M2 PR1 clipping correction regressions

The original ORACLE.md remains preserved. This adds the exact reported P2 case
(camera NED 0,0,-10 ft; yaw 1 degree; world Q12 endpoints 41303,-19762,-40960
and 40605,21192,-40960), plus near and far crossings at depths 10 and 40000 ft.

For each plane: yaw 1/17/45/89/137 degrees; pitch/roll (0,0), (-60,0), (60,0),
(0,-60), (0,60), (-60,60), (60,-60); endpoint depth offsets ±0.0001, ±0.0003,
±0.001, ±0.002, ±0.01 and ±0.1 ft; transverse offsets ±half the plane depth.
Reverse each segment as a separate case. Total: 841. Decimal quaternion rotation
constructs public Q12 world inputs; the independent reference recomputes from
those quantized inputs. It never uses C output as an expected value.

Classification must match and endpoint error must remain <=0.5 logical pixel,
even for this suite's cases inside the permitted ambiguity band. Independent
DDA comparison retains <=1 pixel bidirectional raster distance. A generated
host-only C vector header feeds the same public inputs and independently rounded
reference endpoints to the ASan/UBSan runner. Its serialization adds at most
one Q16 unit to the endpoint threshold; the Decimal comparison remains strict.
No new accepted tolerance, display behavior or target execution is introduced.
