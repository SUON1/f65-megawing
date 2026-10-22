"""Independent Python integer product/rounding, without fixed-width overflow."""
import ctypes
import json
import random
import sys

library = ctypes.CDLL(sys.argv[1])
function = library.m2_test_q46
function.argtypes = [ctypes.c_int64, ctypes.c_int64]
function.restype = ctypes.c_int64
scale = 1 << 46
rng = random.Random(650046)
cases = [(a, b) for a in [0, 1, -1, scale, -scale, scale - 1, 1 - scale]
         for b in [0, 1, -1, scale, -scale, scale - 1, 1 - scale]]
# Exercise both sides of exact half ties for every split-limb boundary.
for shift in range(47):
    for offset in [-1, 0, 1]:
        a = (1 << shift) + offset
        if 0 <= a <= scale:
            for b in [1 << 45, (1 << 45) - 1, (1 << 45) + 1]:
                cases.extend([(a, b), (-a, b), (a, -b), (-a, -b)])
cases.extend((rng.randint(-scale, scale), rng.randint(-scale, scale))
             for _ in range(100000))
for a, b in cases:
    product = a * b
    magnitude = (abs(product) + scale // 2) // scale
    expected = -magnitude if product < 0 else magnitude
    actual = function(a, b)
    assert actual == expected, (a, b, expected, actual)
print(json.dumps({'status': 'PASS', 'cases': len(cases),
                  'oracle': 'Python unbounded exact product, nearest/ties away',
                  'seed': 650046}))
