"""Independent bigint arithmetic and native-reference equivalence, no target run."""
import ctypes as C
import itertools
import random
import sys

U8 = C.c_uint8
Wide = U8 * 8


class Job(C.Structure):
    _fields_ = [("a", U8 * 6), ("b", U8 * 6), ("product", U8 * 12),
                ("remainder", U8 * 7), ("quotient", U8 * 12), ("value", Wide),
                ("phase", U8), ("row", U8), ("bit", U8), ("negative", U8),
                ("shift", U8)]


class Point(C.Structure):
    _fields_ = [("v", C.c_int32 * 3)]


class Camera(C.Structure):
    _fields_ = [("position", Point), ("yaw", C.c_int16), ("pitch", C.c_int16),
                ("roll", C.c_int16), ("revision", C.c_uint32)]


class Line(C.Structure):
    _fields_ = [("x", C.c_int32 * 2), ("y", C.c_int32 * 2)]


def wide(value):
    return Wide.from_buffer_copy(value.to_bytes(8, "little", signed=True))


def integer(value, signed=False):
    return int.from_bytes(bytes(value), "little", signed=signed)


def rounded(numerator, denominator):
    quotient, remainder = divmod(abs(numerator), denominator)
    value = quotient + (2 * remainder >= denominator)
    return -value if numerator < 0 else value


def arithmetic(library):
    multiply = library.m2l_multiply
    multiply.argtypes = [C.POINTER(Job), Wide, Wide, U8]
    multiply.restype = U8
    service = library.m2l_service
    service.argtypes = [C.POINTER(Job)]
    service.restype = C.c_int8
    divide = library.m2l_divide
    divide.argtypes = [C.POINTER(Job), Wide]
    divide.restype = U8
    rng = random.Random(0x65A3)
    scale = 1 << 46
    values = [0, 1, -1, scale, -scale, scale + 8, -scale - 8,
              (1 << 47) - 1, -(1 << 47), 0x55AAFF00AA55, -0x7FFF00FFFF00]
    cases = list(itertools.product(values, repeat=2))
    cases += [(rng.randrange(-(1 << 47), 1 << 47),
               rng.randrange(-(1 << 47), 1 << 47)) for _ in range(3000)]
    cases += [(a, 1 << 45) for a in range(-65, 66)]
    cells = 0
    for a, b in cases:
        job = Job()
        assert multiply(C.byref(job), wide(a), wide(b), 255)
        partial = 0
        for row in range(6):
            assert service(C.byref(job)) == (row == 5)
            partial += ((abs(a) >> (8 * row)) & 255) * abs(b) << (8 * row)
            assert integer(job.product) == partial, (a, b, row, "carry")
            cells += 6
        assert integer(job.product) == abs(a * b)
        denominator = rng.choice([1, 2, scale, scale - 1, (1 << 46) - 1,
                                  rng.randrange(1, 1 << 46)])
        assert divide(C.byref(job), wide(denominator))
        expected = rounded(a * b, denominator)
        for bit in range(95, -1, -1):
            result = service(C.byref(job))
            prefix = abs(a * b) >> bit
            assert integer(job.quotient) >> bit == prefix // denominator
            if bit:
                assert result == 0
                assert integer(job.remainder) == prefix % denominator
            else:
                assert integer(job.remainder) == 2 * (abs(a * b) % denominator)
                fits = -(1 << 63) <= expected < (1 << 63)
                assert result == (1 if fits else -1), (a, b, denominator, expected)
                if fits:
                    assert integer(job.value, True) == expected
        job = Job()
        assert multiply(C.byref(job), wide(a), wide(b), 46)
        for _ in range(6):
            result = service(C.byref(job))
        assert result == 1 and integer(job.value, True) == rounded(a * b, scale)
    for invalid in [1 << 47, -(1 << 47) - 1, (1 << 63) - 1, -(1 << 63)]:
        assert not multiply(C.byref(Job()), wide(invalid), wide(1), 0)
    for denominator in [0, -1, 1 << 47]:
        assert not divide(C.byref(Job()), wide(denominator))
    job = Job()
    job.phase = 3
    assert service(C.byref(job)) == -1
    print(f"BIGINT PASS: {len(cases)} products/Q46/divisions; {cells} actual cells; "
          "every row carry and every division remainder/quotient; overflow/invalid fail closed")


def equivalence(candidate, reference):
    for library in [candidate, reference]:
        library.m2_transform.argtypes = [C.POINTER(Camera), C.POINTER(C.c_int64 * 9)]
        library.m2_project_segment.argtypes = [C.POINTER(Camera), C.POINTER(Point),
                                               C.POINTER(Point), C.POINTER(Line)]
        library.m2_project_segment.restype = C.c_int8
    rng = random.Random(0x65C4)
    cameras = [Camera(Point((C.c_int32 * 3)(n * 4096, e * 4096, -h * 4096)), y, p, r, 1)
               for n, e, h, y, p, r in itertools.product(
                   [-12000, 12000], [-6000, 6000], [10, 3000],
                   [0, 90, 179, 270, 359], [-60, 0, 60], [-60, 0, 60])]
    cameras += [Camera(Point((C.c_int32 * 3)(rng.randrange(-12000, 12001) * 4096,
                                            rng.randrange(-6000, 6001) * 4096,
                                            -rng.randrange(10, 3001) * 4096)),
                       rng.randrange(360), rng.randrange(-60, 61), rng.randrange(-60, 61), 1)
                for _ in range(1000)]
    projections = 0
    for camera in cameras:
        first = (C.c_int64 * 9)()
        last = (C.c_int64 * 9)()
        assert candidate.m2_transform(C.byref(camera), C.byref(first)) == 1
        assert reference.m2_transform(C.byref(camera), C.byref(last)) == 1
        assert bytes(first) == bytes(last), (tuple(first), tuple(last))
        for _ in range(3):
            points = [Point((C.c_int32 * 3)(*[rng.randrange(-65536 * 4096,
                                                          65536 * 4096 + 1)
                                            for _ in range(3)])) for _ in range(2)]
            a = Line.from_buffer_copy(b'\xA5' * C.sizeof(Line))
            b = Line.from_buffer_copy(bytes(a))
            x = candidate.m2_project_segment(C.byref(camera), C.byref(points[0]),
                                              C.byref(points[1]), C.byref(a))
            y = reference.m2_project_segment(C.byref(camera), C.byref(points[0]),
                                              C.byref(points[1]), C.byref(b))
            assert x == y and bytes(a) == bytes(b), (x, y, list(a.x), list(a.y), list(b.x), list(b.y))
            projections += 1
    print(f"NATIVE REFERENCE PASS: {len(cameras)} bit-exact Q46 transforms; "
          f"{projections} bit-exact Q24 clip/Q16 projections including unchanged empty outputs")


def camera_equivalence(candidate, reference):
    def fields(camera):
        return (tuple(camera.position.v), camera.yaw, camera.pitch, camera.roll, camera.revision)
    for library in [candidate, reference]:
        library.m2rb_camera_edges.argtypes = [C.POINTER(Camera), C.c_uint16]
        library.m2rb_camera_edges.restype = C.c_int8
    poses = [(-4500,0,300,0,-5,0,1), (-12000,-6000,10,359,-60,-60,1),
             (12000,6000,3000,0,60,60,1), (0,0,300,180,0,0,0xFFFFFFFF)]
    count = 0
    for n, e, h, yaw, pitch, roll, revision in poses:
        for edges in range(8192):
            a = Camera(Point((C.c_int32 * 3)(n*4096,e*4096,-h*4096)),
                       yaw,pitch,roll,revision)
            b = Camera.from_buffer_copy(bytes(a))
            x = candidate.m2rb_camera_edges(C.byref(a), edges)
            y = reference.m2rb_camera_edges(C.byref(b), edges)
            assert x == y and fields(a) == fields(b), (edges, x, y, fields(a), fields(b))
            count += 1
    print(f"CAMERA REFERENCE PASS: {count} edge-mask/pose combinations, clamps/reset/opposition/revision exhaustion")


if __name__ == "__main__":
    compact, native = map(C.CDLL, sys.argv[1:])
    arithmetic(compact)
    equivalence(compact, native)
    camera_equivalence(compact, native)
