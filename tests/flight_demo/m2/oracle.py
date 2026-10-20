"""Independent Decimal quaternion/interval oracle; ctypes loads the C under test."""
import ctypes as C
from decimal import Decimal as D, getcontext
from functools import lru_cache
import json
from pathlib import Path
import random
import re
import sys

getcontext().prec = 60
ROOT = Path(__file__).resolve().parents[3]
DATA = json.loads((ROOT / 'interfaces/m2_pr1.json').read_text())
K = DATA['constants']
TYPES = {'int64_t': C.c_int64, 'int32_t': C.c_int32, 'uint32_t': C.c_uint32,
         'int16_t': C.c_int16, 'uint16_t': C.c_uint16, 'uint8_t': C.c_uint8}
for name, fields in DATA['records'].items():
    members = []
    for field, kind in fields:
        match = re.fullmatch(r'(\w+)(?:\[(\d+)\])?', field)
        ctype = TYPES[kind]
        members.append((match[1], ctype * int(match[2]) if match[2] else ctype))
    TYPES[name] = type(name, (C.Structure,), {'_fields_': members})
Point, Camera, Line, Pixel = [TYPES[x] for x in ('M2Point', 'M2Camera', 'M2Line', 'M2Pixel')]
PI = D('3.141592653589793238462643383279502884197169399375105820974944592')


def sin(x):
    term = total = x
    for n in range(1, 100):
        term *= -x*x / D((2*n)*(2*n+1))
        total += term
        if abs(term) < D('1e-55'):
            return total
    raise AssertionError('oracle convergence')


def cos(x):
    return sin(PI/2-x)


def product(a, b):
    w,x,y,z = a
    v,i,j,k = b
    return (w*v-x*i-y*j-z*k, w*i+x*v+y*k-z*j,
            w*j-x*k+y*v+z*i, w*k+x*j-y*i+z*v)


@lru_cache(None)
def quaternion(yaw, pitch, roll):
    y,p,r = [D(a)*PI/360 for a in (yaw,pitch,roll)]
    return product(product((cos(y),D(0),D(0),sin(y)),
                           (cos(p),D(0),sin(p),D(0))),
                   (cos(r),sin(r),D(0),D(0)))


def rotate(q, v):
    return product(product(q,(D(0),*v)),(q[0],-q[1],-q[2],-q[3]))[1:]


def camera_point(camera, point):
    q = quaternion(camera.yaw,camera.pitch,camera.roll)
    return rotate((q[0],-q[1],-q[2],-q[3]),
                  tuple(D(point.v[i]-camera.position.v[i])/K['position_scale'] for i in range(3)))


def distances(p):
    x,y,z=p
    return (x-K['near_ft'],K['far_ft']-x,x+y,x-y,2*x+5*z,2*x-5*z)


def reference(camera, a, b):
    a,b=camera_point(camera,a),camera_point(camera,b)
    low, high = D(0), D(1)
    for av,bv in zip(distances(a),distances(b)):
        slope=bv-av
        if slope==0:
            if av<0:return None
        elif slope>0:low=max(low,-av/slope)
        else:high=min(high,-av/slope)
    if low>high:return None
    points=[tuple(a[i]+t*(b[i]-a[i]) for i in range(3)) for t in (low,high)]
    return [(D('159.5')+160*p[1]/p[0],D('63.5')+160*p[2]/p[0]) for p in points]


def point(values):
    p=Point()
    for i,v in enumerate(values):p.v[i]=round(D(str(v))*K['position_scale'])
    return p


def camera(position=(-4500,0,-300), angles=(0,-5,0)):
    c=Camera();c.position=point(position);c.yaw,c.pitch,c.roll=angles;c.revision=1
    return c


def dda(points):
    endpoints=[(max(0,min(319,int(x+D('.5')))),max(0,min(127,int(y+D('.5'))))) for x,y in points]
    (x,y),(u,v)=endpoints;n=max(abs(u-x),abs(v-y))
    if n==0:return {(x,y)}
    return {(round(x+(u-x)*i/n),round(y+(v-y)*i/n)) for i in range(n+1)}


def run(library):
    lib=C.CDLL(str(library))
    lib.m2_project_segment.argtypes=[C.POINTER(Camera),C.POINTER(Point),C.POINTER(Point),C.POINTER(Line)]
    lib.m2_project_segment.restype=C.c_int8
    lib.m2_fixture_segment.argtypes=[C.c_uint32,C.c_uint8,C.POINTER(Point),C.POINTER(Point)]
    lib.m2_raster_line.argtypes=[C.POINTER(Line),C.POINTER(Pixel),C.c_uint16,C.POINTER(C.c_uint16)]
    lib.m2_ground_sample.argtypes=[C.POINTER(Camera),C.c_uint16,C.c_uint16]
    lib.m2_ground_sample.restype=C.c_int8
    rng=random.Random(650201);cases=[]
    fixture=[]
    # Expected coordinates computed from the authoring dimensions, never C output.
    length,width=K['runway_half_length_ft'],K['runway_half_width_ft']
    corners=[(-length,-width,0),(-length,width,0),(length,width,0),(length,-width,0)]
    expected=[(corners[i],corners[(i+1)%4]) for i in range(4)]
    expected += [((n,-width,0),(n,width,0)) for n in (-K['threshold_north_ft'],K['threshold_north_ft'])]
    expected += [((n-K['mark_half_length_ft'],0,0),(n+K['mark_half_length_ft'],0,0))
                 for n in range(K['mark_first_ft'],K['mark_last_ft']+1,K['mark_step_ft'])]
    for i,(av,bv) in enumerate(expected):
        a,b=Point(),Point();assert lib.m2_fixture_segment(1,i,C.byref(a),C.byref(b))==1
        assert list(a.v)==list(point(av).v) and list(b.v)==list(point(bv).v)
        fixture.append((a,b))
    cameras=[camera(angles=(y,p,r)) for y in (0,90,180,270,359) for p in (-60,0,60) for r in (-60,0,60)]
    cameras += [camera(),camera((-12000,-6000,-10)),camera((12000,6000,-3000)),camera((-4500,500,-300)),camera((-4500,-500,-300))]
    for c in cameras:
        cases.extend((c,a,b) for a,b in fixture)
        q=quaternion(c.yaw,c.pitch,c.roll)
        for x,y in [(0,0),(319,0),(0,127),(319,127),(160,64)]:
            down=rotate(q,(D(160),D(x)-D('159.5'),D(y)-D('63.5')))[2]
            assert lib.m2_ground_sample(C.byref(c),x,y)==int(down>D('1e-40'))
    for _ in range(2000):
        c=camera((rng.randint(-12000,12000),rng.randint(-6000,6000),-rng.randint(10,3000)),
                 (rng.randrange(360),rng.randint(-60,60),rng.randint(-60,60)))
        cases.append((c,point([rng.randint(-60000,60000) for _ in range(3)]),point([rng.randint(-60000,60000) for _ in range(3)])))
    # Small camera-space segments near the divide boundary amplify precision
    # errors that distant runway fixtures cannot reveal. Convert through the
    # independent quaternion, then quantize only the declared world input.
    for _ in range(1000):
        c=camera(angles=(rng.randrange(360),rng.randint(-60,60),rng.randint(-60,60)))
        q=quaternion(c.yaw,c.pitch,c.roll)
        endpoints=[]
        for end in range(2):
            local=(D(rng.randint(500,3000))/100,D(rng.randint(-3000,3000))/100,
                   D(rng.randint(-1500,1500))/100)
            world=rotate(q,local)
            endpoints.append(point([world[i]+D(c.position.v[i])/4096 for i in range(3)]))
        cases.append((c,*endpoints))
    c=camera((0,0,-10),(0,0,0))
    for av,bv in [((0,0,-10),(100,0,-10)),((39999,0,-10),(40001,0,-10)),
                  ((100,-200,-10),(100,200,-10)),((100,0,-110),(100,0,90)),
                  ((-10,0,-10),(-1,0,-10)),((10,0,-10),(10,0,-10)),
                  ((100,0,-10),(100,0,-10))]:cases.append((c,point(av),point(bv)))
    maximum=D(0);visible=0;raster_points=0
    for index,(c,a,b) in enumerate(cases):
        ref=reference(c,a,b);line=Line();C.memset(C.byref(line),0x55,C.sizeof(line));before=bytes(line)
        status=lib.m2_project_segment(C.byref(c),C.byref(a),C.byref(b),C.byref(line))
        assert status==int(ref is not None),(index,status,ref)
        if ref is None:
            assert bytes(line)==before
            continue
        visible+=1
        for i in range(2):
            error=max(abs(D(line.x[i])/65536-ref[i][0]),abs(D(line.y[i])/65536-ref[i][1]))
            maximum=max(maximum,error)
            assert error<=D('.5'),(index,error)
        pixels=(Pixel*320)();count=C.c_uint16()
        assert lib.m2_raster_line(C.byref(line),pixels,320,C.byref(count))==1
        actual={(pixels[i].x,pixels[i].y) for i in range(count.value)}
        wanted=dda(ref)
        for left,right in ((actual,wanted),(wanted,actual)):
            assert all(any((x+dx,y+dy) in right for dx in (-1,0,1) for dy in (-1,0,1)) for x,y in left),index
        raster_points+=count.value
    result={'oracle':'Decimal 60-digit independent quaternion and parametric clipping',
            'cases':len(cases),'visible':visible,'raster_points':raster_points,
            'max_projection_error_pixels':str(maximum),'projection_limit':0.5,'raster_limit_pixels':1,'status':'PASS'}
    print(json.dumps(result,indent=2))


if __name__=='__main__':run(Path(sys.argv[1]))
