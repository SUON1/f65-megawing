from pathlib import Path
import sys,subprocess,json
sys.path.insert(0,'tools/diagnostics')
from r0f_group1_resume_validate import function
base=Path('build/r0f/group1/terminal-recovery/status-02/source-inputs')
original=function((base/'src/diagnostics/r0f/group1_export.c').read_text(),'uint8_t r0fg1_export_begin(').replace('r0fg1_export_begin(', 'baseline_begin(')
text='''#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "group1_export.h"
'''+original+'''
static unsigned long cases;
static void check(uint8_t state, uint32_t bytes, r0fg1_export_readiness *readiness)
{
    r0fg1_export before = {.state=state, .bytes=bytes, .acquisition_crc=0x12345678u};
    r0fg1_export old=before, current=before, diagnostic=before;
    uint8_t expected=baseline_begin(&old,readiness);
    assert(r0fg1_export_begin(&current,readiness)==expected);
    uint8_t reason=r0fg1_export_begin_diagnostic(&diagnostic,readiness);
    assert((reason==0u)==expected);
    assert(old.state==current.state && old.state==diagnostic.state);
    assert(current.bytes==bytes && diagnostic.bytes==bytes);
    assert(current.acquisition_crc==before.acquisition_crc);
    assert(diagnostic.acquisition_crc==before.acquisition_crc);
    if (state != R0FG1X_S_FROZEN) assert(reason==0x70u);
    else if (!readiness) assert(reason==0x71u);
    else
    {
        uint8_t wanted=0u;
        const unsigned char *fields=(const unsigned char *)readiness;
        for (unsigned i=0;i<8;i++)
        {
            if (fields[i]!=(i==7?0u:1u)) {wanted=(uint8_t)(0x72u+i);break;}
        }
        if (!wanted && !bytes) wanted=0x7au;
        if (!wanted && bytes>R0FG1X_TRACE_CAPACITY) wanted=0x7bu;
        assert(reason==wanted);
    }
    cases++;
}
int main(void)
{
    const uint32_t lengths[]={0,1,R0FG1X_TRACE_CAPACITY,R0FG1X_TRACE_CAPACITY+1,UINT32_MAX};
    r0fg1_export_readiness valid={1,1,1,1,1,1,1,0};
    assert(!baseline_begin(0,&valid));assert(!r0fg1_export_begin(0,&valid));
    assert(r0fg1_export_begin_diagnostic(0,&valid)==0x70u);
    for (unsigned state=0;state<256;state++)
    for (unsigned size=0;size<5;size++)
    {
        check((uint8_t)state,lengths[size],0);
        check((uint8_t)state,lengths[size],&valid);
        for (unsigned field=0;field<8;field++)
        for (unsigned value=0;value<256;value++)
        {
            r0fg1_export_readiness ready=valid;
            ((unsigned char *)&ready)[field]=(unsigned char)value;
            check((uint8_t)state,lengths[size],&ready);
        }
    }
    for (unsigned mask=0;mask<256;mask++)
    {
        r0fg1_export_readiness ready=valid;
        for (unsigned i=0;i<8;i++) if (mask&(1u<<i)) ((unsigned char *)&ready)[i]^=1u;
        check(R0FG1X_S_FROZEN,1,&ready);
    }
    printf("%lu policy comparisons and first-rejection cases PASS\\n",cases);
}
'''
for number in ('01','02'):
 out=Path('build/r0f/group1/terminal-recovery/readiness-'+number).resolve()
 src=out/'source-inputs';host=out/'policy-equivalence';host.mkdir(exist_ok=False)
 (host/'policy-test.c').write_text(text)
 command=['/usr/bin/clang','-std=c11','-Wall','-Wextra','-Wconversion','-Werror','-fsanitize=address,undefined','-I'+str(src/'interfaces/generated'),'-I'+str(src/'src/diagnostics/r0f'),str(host/'policy-test.c'),str(src/'src/diagnostics/r0f/group1_export.c'),'-o',str(host/'policy-test')]
 logs=[]
 for label,cmd in [('compile',command),('run',[str(host/'policy-test')])]:
  r=subprocess.run(cmd,capture_output=True,text=True,timeout=60);(host/(label+'.txt')).write_text(r.stdout+r.stderr);logs.append({'command':cmd,'exitCode':r.returncode});r.check_returncode()
 (host/'validation.json').write_text(json.dumps({'result':'PASS','scope':'Pure policy equivalence only; target fit FAIL; no execution admission','commands':logs},indent=2)+'\n')
 print(number,(host/'run.txt').read_text().strip())
