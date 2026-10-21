"""Fresh host/oracle and compile-only M2 PR1 evidence. Never executes a target."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time

from generate import generate
from stack_check import check

ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / 'toolchain/runtime/llvm-mos/bin'
PURE = ['src/environment/m2_fixture.c', 'src/graphics/m2_geometry.c',
        'interfaces/generated/m2_tables.c']
M1 = ['src/core/m1_runtime.c', 'src/input/m1_input.c', 'src/presentation/m1_snapshot.c']
INCLUDES = ['interfaces/generated', 'src/environment', 'src/graphics',
            'src/core', 'src/input', 'src/presentation']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build():
    data=generate()
    out=ROOT / ('build/flight-demo/m2-pr1-' + str(time.time_ns()))
    out.mkdir(parents=True)
    commands=[]

    def run(args, log):
        command=list(map(str,args));commands.append(command)
        result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
        (out/log).write_text(result.stdout+result.stderr)
        if result.returncode:
            raise RuntimeError(f'check failed; retained output: {out/log}')
        return result.stdout

    flags=['-std=c11','-Wall','-Wextra','-Wconversion','-Werror']
    includes=['-I'+p for p in INCLUDES]
    run([sys.executable,'-B','-m','unittest','discover','-s','tests/flight_demo/m2',
         '-p','test_*.py','-v'],'contract-tests.txt')
    run(['/usr/bin/clang',*flags,'-fsanitize=address,undefined',*includes,*PURE,*M1,
         'tests/flight_demo/m2/host.c','-o',out/'host'],'host-build.txt')
    host=run([out/'host'],'host.txt')
    run(['/usr/bin/clang',*flags,'-shared','-fPIC',*includes,*PURE,
         '-o',out/'geometry.dylib'],'oracle-build.txt')
    oracle=json.loads(run([sys.executable,'-B','tests/flight_demo/m2/oracle.py',
                          out/'geometry.dylib'],'oracle.json'))
    clipping=json.loads(run([sys.executable,'-B','tests/flight_demo/m2/clip_regressions.py',
                            out/'geometry.dylib'],'clip-regressions.json'))
    run([sys.executable,'-B','tests/flight_demo/m2/clip_regressions.py','--emit-c',
         out/'clip_vectors.h'],'clip-vectors.txt')
    run(['/usr/bin/clang',*flags,'-fsanitize=address,undefined',*includes,
         '-I'+str(out),*PURE,'tests/flight_demo/m2/clip_host.c',
         '-o',out/'clip-host'],'clip-host-build.txt')
    run([out/'clip-host'],'clip-host.txt')
    lock=json.loads((ROOT/'toolchain/f65_toolchain.lock.json').read_text())['llvm_mos']
    assert sha(TOOLS/'mos-mega65-clang')==lock['compiler_sha256']
    assert sha(TOOLS/'llvm-objdump')==lock['objdump_sha256']
    target=out/'M2.prg'
    # Disable indirect jump tables so the final stack CFG is fully enumerable.
    run([TOOLS/'mos-mega65-clang','-mcpu=mos45gs02','-mlto-zp=0','-Os',
         '-fno-jump-tables',*flags,*includes,*PURE,'tests/flight_demo/m2/target.c',
         '-Wl,-T,src/platform/r0f/startup.ld','-Wl,-Map,'+str(out/'M2.map'),
         '-o',target],'target-build.txt')
    disassembly=run([TOOLS/'llvm-objdump','-d',str(target)+'.elf'],'M2.disassembly')
    symbols=run([TOOLS/'llvm-nm','-S',str(target)+'.elf'],'M2.symbols')
    stack=check(disassembly)
    assert not re.search(r'\b(?:jsr|jmp)\s+\$[ef][0-9a-f]{3}\b',disassembly)
    assert not re.search(r'\b(?:cfentry|cfcopy|r0f_pf_enter|m1_platform_)',symbols)
    mapping=(out/'M2.map').read_text();sections={}
    for name in ('.text','.rodata','.data','.bss','.noinit'):
        found=re.search(r'^\s*([0-9a-f]+)\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+'+re.escape(name)+r'$',mapping,re.M)
        start,size=[int(x,16) for x in found.groups()]
        assert not size or data['memory']['resident_start']<=start<start+size<=data['memory']['resident_end_exclusive']
        sections[name]={'start':start,'bytes':size}
    assert '__stack = ' + hex(data['memory']['software_stack_end_exclusive']) in mapping
    stack['compiler_static_stack_bytes']=sections['.noinit']['bytes']
    assert '(.noinit..Lstatic_stack)' in mapping
    # Ensure optimizer retained the actual outputs, including the full raster.
    owners={name:{'address':int(addr,16),'bytes':int(size,16)}
            for addr,size,name in re.findall(r'^([0-9a-f]+) ([0-9a-f]+) [BbDd] (m2_probe_\w+)$',symbols,re.M)}
    assert owners['m2_probe_pixels']['bytes']==data['constants']['raster_points']*4
    assert owners['m2_probe_record']['bytes']>0 and owners['m2_probe_surface']['bytes']>0
    paths=set(PURE+M1+['interfaces/m2_pr1.json','interfaces/generated/m2_pr1.h',
              'memory/m2-pr1-ledger.json','src/environment/m2_fixture.h','src/graphics/m2_geometry.h',
              'src/graphics/m2_raster_private.h','src/graphics/m2_prepared_private.h',
              'src/platform/r0f/startup.ld','toolchain/f65_toolchain.lock.json',
              'interfaces/generated/m1_development.h','src/core/m1_runtime.h',
              'src/input/m1_input.h','src/presentation/m1_snapshot.h'])
    for directory in ('tools/flight_demo/m2','tests/flight_demo/m2'):
        paths.update(str(p.relative_to(ROOT)) for p in (ROOT/directory).iterdir() if p.is_file())
    report={'identity':data['identity'],'base':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
            'commands':commands,'host':host.strip(),'oracle':oracle,'clipping_regressions':clipping,'sections':sections,'owner_symbols':owners,
            'stack':stack,'target_sha256':sha(target),'target_bytes':target.stat().st_size,
            'inputs':{p:sha(ROOT/p) for p in sorted(paths)},
            'compiler_sha256':sha(TOOLS/'mos-mega65-clang'),'objdump_sha256':sha(TOOLS/'llvm-objdump'),
            'clang_sha256':sha(Path('/usr/bin/clang')),
            'target_execution':'NOT RUN; SDK-linked probe is not platform-admitted',
            'pr2_xemu_d81_sd_physical':'NOT RUN','reserve_allocation':0}
    (out/'build.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'output':str(out),'status':'PASS host/oracle/target compile-link-static','stack':stack,
                      'sections':sections,'oracle':oracle},indent=2))


if __name__=='__main__':build()
