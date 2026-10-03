from pathlib import Path
import sys,shutil,difflib
sys.path.insert(0,'tools/diagnostics')
import r0f_group1_resume_recovery as r
base=Path('build/r0f/group1/terminal-recovery/status-02/source-inputs').resolve()
out=Path('build/r0f/group1/terminal-recovery/readiness-01').resolve();out.mkdir(exist_ok=False)
src=out/'source-inputs';shutil.copytree(base,src)
# Retain the capture integrity checks; retire broad markers in this new copy.
for name in ('group1_capture.c','group1_transport.c'):
 p=src/'src/diagnostics/r0f'/name;s=p.read_text()
 s=s.replace('    r0fg1_terminal_checkpoint();\n','')
 s='\n'.join(line for line in s.split('\n') if not any(tag in line for tag in ('// 6C:', '// 6D:', '// 6E:', '// 6F:')))
 p.write_text(s)
p=src/'src/diagnostics/r0f/group1_export.h';s=p.read_text();s=s.replace('uint8_t r0fg1_export_finish(','''// Pure terminal diagnostic: zero means admitted; 70-7B identify rejection.
// The existing boolean entry interface retains exactly its prior semantics.
uint8_t r0fg1_export_begin_diagnostic(r0fg1_export *export,
                                     const r0fg1_export_readiness *readiness);
uint8_t r0fg1_export_finish(''');p.write_text(s)
p=src/'src/diagnostics/r0f/group1_export.c';s=p.read_text();a=s.index('uint8_t r0fg1_export_begin(');b=s.index('uint8_t r0fg1_export_finish(',a)
s=s[:a]+'''uint8_t r0fg1_export_begin_diagnostic(r0fg1_export *export,
                                     const r0fg1_export_readiness *readiness)
{
    if (export == 0 || export->state != R0FG1X_S_FROZEN)
    {
        return 0x70u;
    }
    uint8_t reason = 0u;
    if (readiness == 0)
    {
        reason = 0x71u;
    }
'''+''.join('''    else if (readiness->%s != %su)
    {
        reason = 0x%02xu;
    }
'''%(field,expected,code) for field,expected,code in [('acquisition_stopped',1,0x72),('dma_empty',1,0x73),('display_stopped',1,0x74),('audio_stopped',1,0x75),('irq_masked',1,0x76),('rom_verified',1,0x77),('capsule_verified',1,0x78),('nmi_seen',0,0x79)])+'''    else if (export->bytes == 0u)
    {
        reason = 0x7au;
    }
    else if (export->bytes > R0FG1X_TRACE_CAPACITY)
    {
        reason = 0x7bu;
    }
    if (reason != 0u)
    {
        export->state = R0FG1X_S_FAILED;
        return reason;
    }
    // Consumed before storage, including when transport later fails.
    export->state = R0FG1X_S_EXPORTING;
    return 0u;
}

uint8_t r0fg1_export_begin(r0fg1_export *export,
                          const r0fg1_export_readiness *readiness)
{
    return (uint8_t)(r0fg1_export_begin_diagnostic(export, readiness) == 0u);
}

'''+s[b:];p.write_text(s)
p=src/'src/diagnostics/r0f/group1_transport.c';s=p.read_text().replace('    if (!r0fg1_export_begin(&export, &readiness))','''    uint8_t rejection = r0fg1_export_begin_diagnostic(&export, &readiness);
    if (rejection != 0u)''').replace('''    if (rejection != 0u)
    {
        return 0u;''','''    if (rejection != 0u)
    {
        r0fg1_export_status = rejection;
        return 0u;''');p.write_text(s)
p=src/'src/diagnostics/r0f/group1_transport.h';s=p.read_text();a=s.index('// Before terminal ownership');b=s.index('uint8_t r0fg1_transport_init',a);s=s[:a]+'''// Before entry: 6B is generic preparation; 70-7B are readiness rejections.
// The exporter takes ownership on successful terminal entry.
extern volatile uint8_t r0fg1_export_status;

'''+s[b:];p.write_text(s)
p=src/'src/platform/r0f/group1_terminal_export_45gs02.s';s=p.read_text().replace('// Pre-entry marker: 6B means DOS copy; C advances only after acquisition.','// Pre-entry marker: 6B means preparation; C records readiness rejection.');p.write_text(s)
p=src/'tools/diagnostics/r0f_group1_capture_owner_host_test.c';s=p.read_text().replace('assert(r0fg1_export_status == 0x6du);','assert(r0fg1_export_status == 0x6bu);').replace('    r0fg1_export_status++;\n','');p.write_text(s)
changed=[n for n,h in r.builder.inputs(src).items() if r.builder.inputs(base).get(n)!=h]
patch=''.join(''.join(difflib.unified_diff((base/n).read_text().splitlines(True),(src/n).read_text().splitlines(True),fromfile='a/'+n,tofile='b/'+n,n=0)) for n in changed)
(out/'readiness.patch').write_text(patch)
r.write(out/'preparation.json',{'baseline':str(base),'changed':changed,'patchSha256':r.sha(out/'readiness.patch')})
r.OUT=out;r.SOURCE=src
r.builder.build('runtime-01',source=src,out=out,predecessor=r.read(Path('build/r0f/group1/terminal-recovery/status-02/runtime-01/build.json')),terminal_validator=r.controller().snapshot_probe().validate_terminal)
shutil.copytree(src,out/'runtime-01/source-checkpoint')
print(r.read(out/'runtime-01/build.json')['fit'])
