from pathlib import Path
import sys,shutil,difflib
sys.path.insert(0,'tools/diagnostics')
import r0f_group1_resume_recovery as r
base=Path('build/r0f/group1/terminal-recovery/status-02/source-inputs').resolve()
out=Path('build/r0f/group1/terminal-recovery/readiness-02').resolve();out.mkdir(exist_ok=False)
src=out/'source-inputs';shutil.copytree(Path('build/r0f/group1/terminal-recovery/readiness-01/source-inputs'),src)
p=src/'src/diagnostics/r0f/group1_export.c';s=p.read_text();s=s.replace('#include "group1_export.h"','#include <stddef.h>\n\n#include "group1_export.h"\n\n// This private readiness object is inspected as bytes only after proving\n// every member offset. No public or generated layout is duplicated.\n'+ '\n'.join('_Static_assert(offsetof(r0fg1_export_readiness, %s) == %du,\n               "readiness byte layout");'%(field,i) for i,field in enumerate(('acquisition_stopped','dma_empty','display_stopped','audio_stopped','irq_masked','rom_verified','capsule_verified','nmi_seen')))+'\n_Static_assert(sizeof(r0fg1_export_readiness) == 8u, "readiness size");')
a=s.index('    else if (readiness->acquisition_stopped');b=s.index('    if (reason != 0u)',a)
s=s[:a]+'''    else
    {
        // Unsigned-character access to object representation is permitted C.
        // Check every readiness field in the original short-circuit order.
        const unsigned char *fields = (const unsigned char *)readiness;
        for (uint8_t index = 0u; index < 8u; index++)
        {
            uint8_t expected = index == 7u ? 0u : 1u;
            if (fields[index] != expected)
            {
                reason = (uint8_t)(0x72u + index);
                break;
            }
        }
        if (reason == 0u)
        {
            if (export->bytes == 0u)
            {
                reason = 0x7au;
            }
            else if (export->bytes > R0FG1X_TRACE_CAPACITY)
            {
                reason = 0x7bu;
            }
        }
    }
'''+s[b:];p.write_text(s)
old=r.builder.inputs(base);changed=[n for n,h in r.builder.inputs(src).items() if old.get(n)!=h]
patch=''.join(''.join(difflib.unified_diff((base/n).read_text().splitlines(True),(src/n).read_text().splitlines(True),fromfile='a/'+n,tofile='b/'+n,n=0)) for n in changed)
(out/'readiness.patch').write_text(patch)
r.write(out/'preparation.json',{'baseline':str(base),'changed':changed,'patchSha256':r.sha(out/'readiness.patch')})
r.OUT=out;r.SOURCE=src
r.builder.build('runtime-01',source=src,out=out,predecessor=r.read(Path('build/r0f/group1/terminal-recovery/status-02/runtime-01/build.json')),terminal_validator=r.controller().snapshot_probe().validate_terminal)
shutil.copytree(src,out/'runtime-01/source-checkpoint')
print(r.read(out/'runtime-01/build.json')['fit'])
