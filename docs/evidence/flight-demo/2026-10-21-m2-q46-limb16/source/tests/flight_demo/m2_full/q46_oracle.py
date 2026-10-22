"""Independent Python integer product/rounding, without fixed-width overflow."""
import ctypes
import json
import random
import sys

library = ctypes.CDLL(sys.argv[1])
function = library.m2_test_q46
function.argtypes = [ctypes.c_int64, ctypes.c_int64]
function.restype = ctypes.c_int64
trace = library.m2_test_q46_trace
trace.argtypes = [ctypes.c_int64, ctypes.c_int64,
                  ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(ctypes.c_uint32),
                  ctypes.POINTER(ctypes.c_uint32)]
trace.restype = ctypes.c_int64
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
# Carry chains and full products above 64 bits, including each signed extreme.
limb_edges = [0, 1, 65534, 65535, 65536, 65537, (1 << 32) - 1,
              1 << 32, (1 << 32) + 1, scale - 1, scale]
for a in limb_edges:
    for b in limb_edges:
        cases.extend([(a, b), (-a, b), (a, -b), (-a, -b)])
carry_steps = 0
nonzero_carries = 0
max_cell = 0
words = (ctypes.c_uint16 * 54)()
cells = (ctypes.c_uint32 * 9)()
carries = (ctypes.c_uint32 * 9)()
for a, b in cases:
    product = a * b
    magnitude = (abs(product) + scale // 2) // scale
    expected = -magnitude if product < 0 else magnitude
    actual = function(a, b)
    assert actual == expected, (a, b, expected, actual)
    assert trace(a, b, words, cells, carries) == expected
    aa, bb = abs(a), abs(b)
    for i in range(3):
        for j in range(3):
            step = i * 3 + j
            state = sum(int(words[step * 6 + k]) << (16 * k) for k in range(6))
            # Independent full-integer partial product, not a fixed-width carry model.
            prior_rows = (aa & ((1 << (16 * i)) - 1)) * bb
            a_word = (aa >> (16 * i)) & 65535
            partial_row = a_word * (bb & ((1 << (16 * (j + 1))) - 1)) << (16 * i)
            expected_partial = prior_rows + partial_row
            assert state + (int(carries[step]) << (16 * (i + j + 1))) == expected_partial
            assert words[step * 6 + i + j] == cells[step] & 65535
            assert carries[step] == cells[step] >> 16
            assert 0 <= cells[step] <= 0xffffffff and carries[step] <= 65535
            carry_steps += 1
            nonzero_carries += int(carries[step] != 0)
            max_cell = max(max_cell, cells[step])
print(json.dumps({'status': 'PASS', 'cases': len(cases),
                  'oracle': 'Python unbounded exact product, nearest/ties away',
                  'seed': 650046, 'carry_steps': carry_steps,
                  'nonzero_carries': nonzero_carries, 'largest_observed_cell': max_cell,
                  'universal_cell_bound': (65535 * 65535 + 65535 + 65535),
                  'domain': 'both magnitudes <= 2^46; no out-of-contract int64 extrema admitted'}))
