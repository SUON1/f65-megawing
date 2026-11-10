"""Independent integer checks for the Platform-backed Graphics arithmetic."""
import ctypes as C
import itertools
import random
import sys

from limb_oracle import U8, Wide, equivalence, integer, rounded, wide


class Job(C.Structure):
    _fields_ = [("a", U8 * 6), ("b", U8 * 6), ("product", U8 * 18),
                ("quotient", U8 * 12), ("value", Wide), ("phase", U8),
                ("row", U8), ("bit", U8), ("negative", U8), ("shift", U8)]


def arithmetic(lib):
    multiply = lib.m2l_multiply
    multiply.argtypes, multiply.restype = [C.POINTER(Job), Wide, Wide, U8], U8
    divide = lib.m2l_divide
    divide.argtypes, divide.restype = [C.POINTER(Job), Wide], U8
    service = lib.m2l_service
    service.argtypes, service.restype = [C.POINTER(Job)], C.c_int8
    transactions = lib.m2math_transactions
    transactions.restype = C.c_uint
    rng = random.Random(0x65A024)
    scale = 1 << 46
    extrema = [0, 1, -1, scale, -scale, scale + 1, -scale - 1,
               (1 << 47) - 1, -(1 << 47), 0x55AAFF00AA55, -0x7FFF00FFFF00]
    pairs = list(itertools.product(extrema, repeat=2))
    pairs += [(rng.randrange(-(1 << 47), 1 << 47),
               rng.randrange(-(1 << 47), 1 << 47)) for _ in range(6000)]
    pairs += [(n, 1 << 45) for n in range(-65, 66)]
    digit_counts = [0] * 5
    corrections = {-1: 0, 0: 0, 1: 0}
    saturated = 0
    overflows = 0
    rounding_ties = 0

    def verify_division(job, numerator, denominator):
        nonlocal saturated, overflows, rounding_ties
        assert divide(C.byref(job), wide(denominator))
        shift = 48 - denominator.bit_length()
        norm = denominator << shift
        dividend = abs(numerator) << shift
        assert integer(job.b) == norm and integer(job.product) == dividend
        expected = rounded(numerator, denominator)
        fits = -(1 << 63) <= expected < (1 << 63)
        overflows += not fits
        rounding_ties += 2 * (abs(numerator) % denominator) == denominator
        index = max(0, ((abs(numerator) // denominator).bit_length() - 1) // 24)
        assert job.bit == index
        digit_counts[index + 1] += 1
        for digit in range(index, -1, -1):
            offset = digit * 3
            current = integer(job.product[offset:offset + 9])
            prefix = dividend >> (24 * digit)
            actual, remainder = divmod(current, norm)
            estimate = ((current >> 40) << 24) // (norm >> 16)
            saturated += estimate == (1 << 24)
            estimate = min(estimate, (1 << 24) - 1)
            corrections[actual - estimate] += 1
            prior = transactions()
            status = service(C.byref(job))
            assert transactions() - prior == 3
            assert integer(job.quotient) >> (24 * digit) == prefix // norm
            if digit:
                assert status == 0 and integer(job.product[offset:offset + 9]) == remainder
            else:
                assert integer(job.product[:9]) == 2 * remainder
                assert status == (1 if fits else -1), (numerator, denominator, expected)
                if fits:
                    assert integer(job.value, True) == expected

    for a, b in pairs:
        job = Job()
        assert multiply(C.byref(job), wide(a), wide(b), 255)
        partial = 0
        for row in range(4):
            def part(value, high):
                return (abs(value) >> (32 * high)) & 0xffffffff
            first, second = row & 1, row >> 1
            partial += part(a, first) * part(b, second) << (32 * (first + second))
            prior = transactions()
            assert service(C.byref(job)) == (row == 3)
            assert transactions() - prior == 1
            assert integer(job.product) == partial, (a, b, row, "carry")
        assert integer(job.product) == abs(a * b)
        denominator = rng.choice([1, 2, 3, 256, 257, 65537, scale, scale - 1,
                                  rng.randrange(1, 1 << 47)])
        verify_division(job, a * b, denominator)
        for shift in [0, 46]:
            assert multiply(C.byref(job), wide(a), wide(b), shift)
            expected = rounded(a * b, 1 << shift)
            for _ in range(4):
                status = service(C.byref(job))
            fits = -(1 << 63) <= expected < (1 << 63)
            assert status == (1 if fits else -1)
            if fits:
                assert integer(job.value, True) == expected

    # Exercise exact and almost-next-digit quotients around the hardware
    # estimate boundaries, plus both signed64 rounding/narrowing extrema.
    focused = []
    for shift in range(1, 48):
        for divisor in [(1 << shift) - 1, 1 << (shift - 1),
                        min((1 << shift) - 1, (1 << (shift - 1)) + 313)]:
            for q in [1, 17, 0xffff, 0xfffffe, 0xffffff, 0x1000001]:
                for rem in {0, divisor // 2, divisor - 1}:
                    focused.append((q * divisor + rem, divisor))
    for n in [1 << 63, (1 << 63) - 1, (1 << 63) + 1]:
        for rem in [-1, 0, 1, 2]:
            focused.extend(((2 * n + rem, 2), (-(2 * n + rem), 2)))
    for numerator, denominator in focused:
        job = Job()
        job.product[:12] = abs(numerator).to_bytes(12, "little")
        job.negative = int(numerator < 0)
        verify_division(job, numerator, denominator)

    for invalid in [1 << 47, -(1 << 47) - 1, (1 << 63) - 1, -(1 << 63)]:
        assert not multiply(C.byref(Job()), wide(invalid), wide(1), 0)
    for denominator in [0, -1, 1 << 47]:
        assert not divide(C.byref(Job()), wide(denominator))
    assert not multiply(C.byref(Job()), wide(0), wide(0), 45)
    for phase, row, digit in [(1, 4, 0), (2, 0, 4), (3, 0, 0), (255, 0, 0)]:
        job = Job(phase=phase, row=row, bit=digit)
        assert service(C.byref(job)) == -1
    assert all(corrections.values()) and saturated and rounding_ties and overflows
    assert all(digit_counts[1:])
    print(f"BIGINT PASS {len(pairs)} products with all four carry states and Q46 outputs, "
          f"{len(pairs) + len(focused)} divisions with every quotient digit and remainder")
    print(f"digits={digit_counts[1:]} estimate corrections={corrections} saturated={saturated} "
          f"division rounding ties={rounding_ties} overflow={overflows}")


if __name__ == "__main__":
    candidate, reference = map(C.CDLL, sys.argv[1:])
    arithmetic(candidate)
    equivalence(candidate, reference)
