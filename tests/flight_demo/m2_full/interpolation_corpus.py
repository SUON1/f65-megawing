"""Freeze I4's direct-helper corpus and independent integer expectations.

The explicit little-endian transport is private test data, not a public layout.
No C reference or bit-recurrence implementation supplies expected results.
"""
import hashlib
import json
from pathlib import Path
import random
import struct
import sys

LIMIT = 2**63 - 1
DENOMINATOR_LIMIT = (2**48 - 1) // 3
RECORD = struct.Struct('<qQQq')


def structured_sets():
    deltas = {0, -LIMIT, LIMIT}
    for bit in range(63):
        for magnitude in [2**bit - 1, 2**bit, 2**bit + 1]:
            if 0 <= magnitude <= LIMIT:
                deltas.update([magnitude, -magnitude])
    denominators = {1, 2, 3, 4, 5, DENOMINATOR_LIMIT - 1, DENOMINATOR_LIMIT}
    for bit in range(47):
        denominators.update(value for value in [2**bit - 1, 2**bit, 2**bit + 1]
                            if 1 <= value <= DENOMINATOR_LIMIT)
    return sorted(deltas), sorted(denominators)


def numerators(denominator):
    return sorted({value for value in [
        0, 1, denominator // 2 - 1, denominator // 2,
        (denominator + 1) // 2, denominator // 2 + 1,
        denominator - 1, denominator]
        if 0 <= value <= denominator})


def generate(output):
    deltas, denominators = structured_sets()
    assert len(deltas) == 373 and len(denominators) == 139
    counts = dict(structured=0, seeded=0)
    rounding = dict(exact=0, below_half=0, tie=0, above_half=0)
    with output.open('wb') as stream:
        def emit(kind, delta, numerator, denominator):
            assert -LIMIT <= delta <= LIMIT
            assert 1 <= denominator <= DENOMINATOR_LIMIT
            assert 0 <= numerator <= denominator
            quotient, remainder = divmod(abs(delta) * numerator, denominator)
            rounded = quotient + (2 * remainder >= denominator)
            expected = -rounded if delta < 0 else rounded
            assert expected == (1 if delta >= 0 else -1) * (
                (abs(delta) * numerator + denominator // 2) // denominator)
            category = ('exact' if remainder == 0 else 'below_half'
                        if 2 * remainder < denominator else 'tie'
                        if 2 * remainder == denominator else 'above_half')
            rounding[category] += 1
            stream.write(RECORD.pack(delta, numerator, denominator, expected))
            counts[kind] += 1

        for delta in deltas:
            for denominator in denominators:
                for numerator in numerators(denominator):
                    emit('structured', delta, numerator, denominator)
        rng = random.Random(650018)
        for _ in range(100000):
            delta = rng.randint(-LIMIT, LIMIT)
            denominator = rng.randint(1, DENOMINATOR_LIMIT)
            numerator = rng.randint(0, denominator)
            emit('seeded', delta, numerator, denominator)
    assert counts == dict(structured=357334, seeded=100000)
    sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    identity = dict(counts=counts, total=sum(counts.values()), rounding=rounding,
                    record_format=RECORD.format, record_bytes=RECORD.size,
                    bytes=output.stat().st_size, seed=650018,
                    draw_order=['delta', 'denominator', 'numerator'],
                    python=sys.version, corpus_sha256=sha(output),
                    generator_sha256=sha(Path(__file__)))
    output.with_suffix('.json').write_text(json.dumps(identity, indent=2) + '\n')
    print(json.dumps(identity, indent=2))


if __name__ == '__main__':
    generate(Path(sys.argv[1]))
