"""Freeze the approved projection cohort as explicit little-endian test data.

The test record is a private transport, not a public C structure layout.
Canonical/analytic cases consume no random draws. No retries or filtering.
"""
import hashlib
import itertools
import json
from pathlib import Path
import random
import struct
import sys

ROOT = Path(__file__).resolve().parents[3]
C = json.loads((ROOT / 'interfaces/m2_pr1.json').read_text())['constants']
SCALE = C['position_scale']
RECORD = struct.Struct('<6iI6iI')


def point(north, east, down=0):
    return [int(v * SCALE) for v in (north, east, down)]


def segments():
    length, width = C['runway_half_length_ft'], C['runway_half_width_ft']
    corners = [(-length, -width), (-length, width),
               (length, width), (length, -width)]
    for i in range(4):
        yield point(*corners[i]), point(*corners[(i + 1) % 4])
    for n in [-C['threshold_north_ft'], C['threshold_north_ft']]:
        yield point(n, -width), point(n, width)
    for center in range(C['mark_first_ft'], C['mark_last_ft'] + 1, C['mark_step_ft']):
        yield (point(center - C['mark_half_length_ft'], 0),
               point(center + C['mark_half_length_ft'], 0))


def generate(out):
    counts = dict(canonical=0, seeded=0, analytic=0)
    with out.open('wb') as stream:
        def emit(kind, camera, a, b, same=0):
            stream.write(RECORD.pack(*camera, *a, *b, same))
            counts[kind] += 1

        fixture = list(segments())
        assert len(fixture) == C['segment_count'] == 17
        for yaw, pitch, roll in itertools.product(
                range(360), [-60, -30, -1, 0, 1, 30, 60],
                [-60, -30, -1, 0, 1, 30, 60]):
            camera = [*point(-4500, 0, -300), yaw, pitch, roll, 1]
            for a, b in fixture:
                emit('canonical', camera, a, b)
                emit('canonical', camera, b, a)
        rng = random.Random(650017)
        world = C['world_limit_ft'] * SCALE
        for _ in range(100000):
            camera = [rng.randint(-C['north_limit_ft'] * SCALE, C['north_limit_ft'] * SCALE),
                      rng.randint(-C['east_limit_ft'] * SCALE, C['east_limit_ft'] * SCALE),
                      rng.randint(-C['height_max_ft'] * SCALE, -C['height_min_ft'] * SCALE),
                      rng.randint(0, 359),
                      rng.randint(-C['tilt_limit_deg'], C['tilt_limit_deg']),
                      rng.randint(-C['tilt_limit_deg'], C['tilt_limit_deg']),
                      rng.randint(1, 2**32 - 1)]
            a = [rng.randint(-world, world) for _ in range(3)]
            b = [rng.randint(-world, world) for _ in range(3)]
            emit('seeded', camera, a, b)
            emit('seeded', camera, b, a)
        camera = [*point(0, 0, -10), 0, 0, 0, 1]
        planes = [(point(C['near_ft'], 0), point(C['near_ft'], 1), 0),
                  (point(C['far_ft'], 0), point(C['far_ft'], 1), 0),
                  (point(100, -100), point(110, -110), 1),
                  (point(100, 100), point(110, 110), 1),
                  (point(100, 0, -40), point(110, 0, -44), 2),
                  (point(100, 0, 40), point(110, 0, 44), 2)]
        for a, b, axis in planes:
            a[2] += camera[2]
            b[2] += camera[2]
            for da, db in itertools.product([-1, 0, 1], repeat=2):
                first, last = a.copy(), b.copy()
                first[axis] += da
                last[axis] += db
                emit('analytic', camera, first, last)
                emit('analytic', camera, last, first)
            for offset in [-1, 0, 1]:
                first = a.copy()
                first[axis] += offset
                emit('analytic', camera, first, first, same=1)
    assert counts == dict(canonical=599760, seeded=200000, analytic=126)
    sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    identity = dict(counts=counts, total=sum(counts.values()), bytes=out.stat().st_size,
                    record_format=RECORD.format, seed=650017, python=sys.version,
                    corpus_sha256=sha(out), generator_sha256=sha(Path(__file__)),
                    contract_sha256=sha(ROOT / 'interfaces/m2_pr1.json'),
                    fixture_sha256=sha(ROOT / 'src/environment/m2_fixture.c'))
    out.with_suffix('.json').write_text(json.dumps(identity, indent=2) + '\n')
    print(json.dumps(identity, indent=2))


if __name__ == '__main__':
    generate(Path(sys.argv[1]))
