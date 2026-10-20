"""Adversarial near/far crossings, independent Decimal oracle, unchanged bars."""
import ctypes as C
from decimal import Decimal as D
import json
from pathlib import Path
import sys

import oracle as o


def cases():
    c=o.camera((0,0,-10),(1,0,0));a=o.Point();b=o.Point()
    a.v[:]=[41303,-19762,-40960];b.v[:]=[40605,21192,-40960]
    result=[('reported-P2',c,a,b)]
    for plane in (10,40000):
        for yaw in (1,17,45,89,137):
            for pitch,roll in ((0,0),(-60,0),(60,0),(0,-60),(0,60),(-60,60),(60,-60)):
                c=o.camera((0,0,-10),(yaw,pitch,roll));q=o.quaternion(yaw,pitch,roll)
                for epsilon in ('.0001','.0003','.001','.002','.01','.1'):
                    points=[]
                    for sign in (-1,1):
                        rotated=o.rotate(q,(D(plane)+sign*D(epsilon),D(sign)*D(plane)/2,D(0)))
                        points.append(o.point([rotated[i]+D(c.position.v[i])/4096 for i in range(3)]))
                    label=f'{plane}-yaw{yaw}-pitch{pitch}-roll{roll}-epsilon{epsilon}'
                    result.extend([(label,c,*points),(label+'-reversed',c,*reversed(points))])
    return result


def run(library):
    lib=C.CDLL(str(library))
    lib.m2_project_segment.argtypes=[C.POINTER(o.Camera),C.POINTER(o.Point),C.POINTER(o.Point),C.POINTER(o.Line)]
    lib.m2_project_segment.restype=C.c_int8
    lib.m2_raster_line.argtypes=[C.POINTER(o.Line),C.POINTER(o.Pixel),C.c_uint16,C.POINTER(C.c_uint16)]
    worst=D(0);worst_case=None;failures=[];results=[]
    for label,c,a,b in cases():
        ref=o.reference(c,a,b);line=o.Line()
        status=lib.m2_project_segment(C.byref(c),C.byref(a),C.byref(b),C.byref(line))
        error=None
        if status!=int(ref is not None):failures.append((label,'classification'))
        elif ref is not None:
            error=max(abs(D(value)/65536-ref[i][axis])
                      for i in range(2) for axis,value in enumerate((line.x[i],line.y[i])))
            if error>worst:worst,worst_case=error,label
            if error>D('.5'):failures.append((label,str(error)))
            pixels=(o.Pixel*320)();count=C.c_uint16()
            assert lib.m2_raster_line(C.byref(line),pixels,320,C.byref(count))==1
            actual={(pixels[i].x,pixels[i].y) for i in range(count.value)}
            expected=o.dda(ref)
            for left,right in ((actual,expected),(expected,actual)):
                if not all(any((x+dx,y+dy) in right for dx in (-1,0,1) for dy in (-1,0,1)) for x,y in left):
                    failures.append((label,'raster distance exceeds one pixel'))
        results.append({'case':label,'error_pixels':str(error) if error is not None else None})
    report={'cases':len(results),'max_error_pixels':str(worst),'worst_case':worst_case,
            'failures':failures,'status':'FAIL' if failures else 'PASS','results':results}
    print(json.dumps(report,indent=2))
    return not failures


def emit_c(path):
    # Freeze exact public Q12 inputs and independently calculated expectations
    # for the native sanitizer runner; do not derive expected values from C.
    lines=['// Generated host-only regression vectors from Decimal oracle.',
           'static const ClipCase clip_cases[] =', '{']
    for label,c,a,b in cases():
        ref=o.reference(c,a,b)
        camera='{{{'+','.join(str(v)+'L' for v in c.position.v)+'}},'+f'{c.yaw},{c.pitch},{c.roll},1u'+'}'
        endpoints=['{{'+','.join(str(v)+'L' for v in p.v)+'}}' for p in (a,b)]
        expected='{{0,0},{0,0}}' if ref is None else ('{{'+','.join(str(round(p[0]*65536))+'L' for p in ref)+'},{'+','.join(str(round(p[1]*65536))+'L' for p in ref)+'}}')
        lines.append('    {'+','.join([camera,*endpoints,expected,str(int(ref is not None))])+'},')
    lines.append('};')
    path.write_text('\n'.join(lines)+'\n')


if __name__=='__main__':
    if sys.argv[1]=='--emit-c':emit_c(Path(sys.argv[2]))
    else:sys.exit(0 if run(Path(sys.argv[1])) else 1)
