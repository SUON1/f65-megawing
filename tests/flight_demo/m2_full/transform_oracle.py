"""Independent full-integer matrix equations; never interpret candidate descriptors."""
import ctypes
import json
from pathlib import Path
import random
import re
import sys

ROOT = Path(__file__).resolve().parents[3]
scale = json.loads((ROOT / 'interfaces/m2_pr1.json').read_text())['constants']['rotation_scale']
table = [int(x) for x in re.findall(r'(-?\d+)LL',
                                  (ROOT / 'interfaces/generated/m2_tables.c').read_text())]
assert len(table) == 91
library = ctypes.CDLL(sys.argv[1])
function = library.m2_test_transform
function.argtypes = [ctypes.c_int16, ctypes.c_int16, ctypes.c_int16,
                     ctypes.POINTER(ctypes.c_int64)]
function.restype = ctypes.c_uint8
ties = negative_products = wide_products = cancellations = exact_cancellations = extrema = 0


def sine(angle):
    angle %= 360
    negative = angle > 180
    if negative:
        angle -= 180
    if angle > 90:
        angle = 180 - angle
    return -table[angle] if negative else table[angle]


def rounded_product(a, b):
    global ties, negative_products, wide_products
    product = a * b
    ties += int(abs(product) % scale == scale // 2)
    negative_products += int(product < 0)
    wide_products += int(abs(product) > (1 << 64) - 1)
    value = (abs(product) + scale // 2) // scale
    return -value if product < 0 else value


def reference(yaw, pitch, roll):
    global cancellations, exact_cancellations, extrema
    sy, cy = sine(yaw), sine(yaw + 90)
    sp, cp = sine(pitch), sine(pitch + 90)
    sr, cr = sine(roll), sine(roll + 90)
    r = rounded_product
    srsp, crsp = r(sr, sp), r(cr, sp)
    # Each element is a mathematical equation, with each product rounded before
    # summation. Deliberately independent of the implementation's operation table.
    terms = [(r(cp, cy),), (r(cp, sy),), (-sp,),
             (r(srsp, cy), -r(cr, sy)), (r(srsp, sy), r(cr, cy)),
             (r(sr, cp),), (r(crsp, cy), r(sr, sy)),
             (r(crsp, sy), -r(sr, cy)), (r(cr, cp),)]
    result = [sum(values) for values in terms]
    cancellations += sum(len(t) == 2 and t[0] * t[1] < 0 for t in terms)
    exact_cancellations += sum(len(t) == 2 and t[0] != 0 and sum(t) == 0 for t in terms)
    extrema += sum(abs(value) == scale for value in result)
    assert all(-scale <= value <= scale for value in result)
    return result


edges = [-60, -59, -45, -30, -1, 0, 1, 30, 45, 59, 60]
cases = [(yaw, pitch, roll) for yaw in range(360) for pitch in edges for roll in edges]
rng = random.Random(650014)
cases += [(rng.randrange(360), rng.randint(-60, 60), rng.randint(-60, 60))
          for _ in range(20000)]
actual = (ctypes.c_int64 * 9)()
for angles in cases:
    expected = reference(*angles)
    assert function(*angles, actual) == 1
    assert list(actual) == expected, (angles, expected, list(actual))
assert ties and negative_products and wide_products and cancellations and extrema
print(json.dumps({'status': 'PASS', 'cases': len(cases), 'seed': 650014,
                  'oracle': 'unbounded integer staged matrix equations; canonical sine inputs',
                  'rounding_ties': ties, 'negative_products': negative_products,
                  'products_above_64_bits': wide_products,
                  'opposite_sign_term_cancellations': cancellations,
                  'exact_nonzero_term_cancellations': exact_cancellations,
                  'coefficient_extrema': extrema}))
