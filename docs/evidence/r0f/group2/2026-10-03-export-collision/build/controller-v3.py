#!/usr/bin/env python3
"""Fresh R1/R2 control and bounded G2-L export-collision carrier; no SD writes.

MANDATORY D81 LOADABILITY GATE

Before creating, modifying, copying, renaming, packaging, mounting, testing, or releasing any D81, read and obey the repository-root file 00_D81_LOADABILITY_GATE.md.

The work must fail closed. A D81 may not be called final, test-ready, loadable, or delivered for physical testing until the exact artifact passes every applicable state in this order:

UNVERIFIED
-> HOST_STRUCTURALLY_VERIFIED
-> HOST_CONTENT_VERIFIED
-> XEMU_BOOT_VERIFIED
-> SD_COPY_VERIFIED
-> SD_CONTIGUITY_VERIFIED
-> PHYSICAL_CHOOSER_VERIFIED
-> TEST_ELIGIBLE

Never build a new test carrier by copying an existing D81 and reopening the copy in a second c1541 session to append files. Fresh-format the image and populate all files in one pinned-tool construction session.

ERROR CODE FF at the MEGA65 chooser is a hard chooser/attach-stage failure. Retire that tested copy and diagnose D81 construction, exact copied bytes, SD physical allocation, safe ejection, and platform identity before assigning a replacement. Do not patch, append to, rename, or re-test the failed copy and do not blame the program inside it.

A matching hash of the SD-card copy is necessary but not sufficient. The MEGA65 Freezer requires a disk-image file to occupy one contiguous FAT32 extent. A fragmented file can hash perfectly and still fail to mount with ERROR CODE FF. Do not submit a copied image to the physical chooser until an independent extent check reports exactly one extent.
"""
import argparse
import json
from pathlib import Path
import shutil

import r0f_group1_owner_recovery as codec
import r0f_group1_export_probe as probe
from r0f_group2_experiment import Experiment, verify_inputs
from r0f_group2_scratch import function
from r0f_group2_target_admission import ROOT, sha

BASE = ROOT / 'build/r0f/group2/copy-encoder/r2-b4wd7lrc'
runtime = probe.emulator
NAME = 'R0FG2L1.D81'
PREFIX = 'src/diagnostics/r0f/'


def write(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n')


def prepare():
    experiment=Experiment(BASE,'control')
    integration=experiment.source/PREFIX/'successor_integration.c'
    text=integration.read_text()
    needle='extern uint8_t r0fg2_queue_probe(r0fc_model *model);\nstatic volatile uint8_t group2_admission_result;\n'
    call='    group2_admission_result = r0fg2_queue_probe(&model);\n'
    if text.count(needle)!=1 or text.count(call)!=1:raise ValueError('Startup probe seam mismatch')
    integration.write_text(text.replace(needle,'').replace(call,''))
    platform=experiment.source/PREFIX/'combined_platform.c'
    text=platform.read_text()
    text=text.replace('R0-F COMBINED EXPERIMENT CF001 / F65BLK02','R0-F GROUP 2 CONTROL / R0FG2C1')
    platform.write_text(text)
    shutil.copyfile(Path(__file__),experiment.out/'controller.py')
    try:
        experiment.fit(excluded_sources=['tools/diagnostics/r0f_group2_queue_probe.c'])
        compiler=Path(experiment.report['commands'][0]['command'][0])
        # Inspect the unchanged terminal/context instruction boundaries at the
        # newly linked addresses. Runtime stack high-water stays a run gate.
        experiment.run('symbols',[str(compiler.parent/'llvm-nm'),str(experiment.out/'CANDIDATE.prg')+'.elf'])
        experiment.run('disassembly',[str(compiler.parent/'llvm-objdump'),'-d','--print-imm-hex',str(experiment.out/'CANDIDATE.prg')+'.elf'])
        symbols=(experiment.out/'symbols.txt').read_text()
        probe.validate_terminal((experiment.out/'disassembly.txt').read_text(),symbols)
        # Reuse exact R2 owner execution, not the P09 binaries or a copied PASS
        # attached to altered code. Match every tested definition and support.
        tested=(BASE/'actual_owners.h').read_text()
        for name,relative in [('cfcopy','combined_platform.c'),('cfput16','combined_platform.c'),
            ('cfput32','combined_platform.c'),('cfget32','combined_platform.c'),
            ('cfphysical_crc','combined_platform.c'),('cfrom_begin','combined_platform.c'),
            ('cfrom_restore','combined_platform.c'),('fixed_physical_copy','successor_integration.c'),
            ('dos_copy','successor_integration.c'),('dos_crc','successor_integration.c'),
            ('display_seed_staging','successor_integration.c'),('transfer','group1_transport.c'),
            ('validate_capsule','group1_transport.c'),('r0fg1_transport_init','group1_transport.c'),
            ('r0fg1_trace_write','group1_transport.c'),('r0fg1_trace_read','group1_transport.c'),
            ('r0fg1_transport_prepare','group1_transport.c')]:
            if function((experiment.source/PREFIX/relative).read_text(),name)!=function(tested,name):
                raise ValueError('Reused owner body mismatch: '+name)
        for relative in ('combined_model.c','successor_lifecycle.c','group1_export.c'):
            if sha(experiment.source/PREFIX/relative)!=sha(BASE/'source-inputs'/PREFIX/relative):
                raise ValueError('Support drift')
        if 'PASS: 1484' not in (BASE/'host-run.txt').read_text():raise ValueError('R2 host missing')
        if 'PASS: 256' not in (BASE/'encoder-host/1.txt').read_text():raise ValueError('R2 encoder proof missing')
        write(experiment.out/'host-admission.json',{'result':'PASS_REUSED_EXACT_OWNER_BODIES',
            'source':str(BASE),'ownerCases':1484,'encoderCases':256,
            'hostEvidenceSha256':sha(BASE/'host-run.txt'),
            'encoderEvidenceSha256':sha(BASE/'encoder-host/validation.json'),
            'terminalDisassembly':'PASS','capacityOrReserveChanged':False,
            'scope':'R1/R2 normal combined control; no Group 2 fault-case proof'})
    except Exception as error:
        experiment.report.update(result='FAIL',error=str(error))
    finally:
        experiment.finish([PREFIX+'successor_integration.c',PREFIX+'combined_platform.c'])
    return experiment.out


def checked(experiment):
    report=json.loads((experiment/'result.json').read_text())
    if report['result']!='FIT_PASS_NOT_EXECUTABLE':raise ValueError('Fit gate failed')
    verify_inputs(experiment/'source-inputs',report['inputs'])
    if sha(experiment/'CANDIDATE.prg')!=report['prgSha256']:raise ValueError('PRG drift')
    host=json.loads((experiment/'host-admission.json').read_text())
    if host['result']!='PASS_REUSED_EXACT_OWNER_BODIES':raise ValueError('Host gate missing')
    pin = experiment / 'controller-admission-v3.json'
    if not pin.exists():
        pin = experiment / 'controller-admission-v2.json'
    digest = json.loads(pin.read_text())['controllerSha256'] if pin.exists() else sha(experiment/'controller.py')
    verify_inputs(ROOT, {str(Path(__file__).relative_to(ROOT)):digest})
    if pin.exists():
        verify_inputs(ROOT, json.loads(pin.read_text()).get('supportInputs', {}))
    return report


def timing(experiment, directory, image, mode, autoload, initial_names, label):
    report=checked(experiment)
    runtime.PRG=experiment/'CANDIDATE.prg'
    runtime.SOURCE_BRANCH=runtime.git_text('branch','--show-current')
    write(directory/'build-identity.json',report)
    _,execution=runtime.run_xemu(directory,mode,image,'GROUP2_R1_R2_COMBINED_CONTROL',autoload,120)
    reduction,actual=codec.reduce_candidate_export(experiment/'source-inputs',directory,image,
        (experiment/'symbols.txt').read_text(),execution,initial_names,label)
    if (reduction['acquisition']!='PASS' or reduction['nominalTiming']!='WITHIN_OBSERVED_BOUNDS'
        or reduction['nominalDeadlineMisses'] or reduction['cohortsBelow20Hz'] or reduction['boundaryUncertain']):
        raise ValueError('Changed-control acquisition/timing gate failed')
    # Existing independent capacity reducer and its corruption tests operate on
    # the new trace only. Never rerun a P09 program or prior carrier.
    command=['python3','-B','tools/diagnostics/r0f_group1_capacity_check.py',
        '--trace',str(directory/'trace.bin'),'--out',str(directory/'capacity.json'),
        '--disassembly',str(experiment/'disassembly.txt'),'--symbols',str(experiment/'symbols.txt'),
        '--support-tools',str(ROOT/'tools/diagnostics')]
    import subprocess
    result=subprocess.run(command,cwd=experiment/'source-inputs',text=True,capture_output=True,timeout=60)
    write(directory/'capacity-command.json',{'command':command,'exitCode':result.returncode,
        'stdout':result.stdout,'stderr':result.stderr})
    result.check_returncode()
    memory=(directory/'memory.bin').read_bytes();symbols=(experiment/'symbols.txt').read_text()
    statuses={name:memory[probe.integration.symbol(symbols,'r0fg1_export_'+name)]
              for name in ('status','error','files')}
    if statuses!={'status':4,'error':0,'files':20}:raise ValueError('Terminal outcome incorrect')
    text_start=probe.integration.symbol(symbols,'r0fg1_operator_text')
    text_end=probe.integration.symbol(symbols,'r0fg1_operator_text_end')
    expected=b'\x93G1 EXPORT S:4 E:00 F:14\r4=OK 5=FAIL / E,F HEX\rREDUCE FOR TIMING\rNOT ACCEPTANCE\rRESET\r\0'
    if memory[text_start:text_end]!=expected:raise ValueError('Protected operator text mismatch')
    write(directory/'validation.json',{'result':'PASS','videoArgument':mode,
        'prgSha256':report['prgSha256'],'records':reduction['records'],
        'nominalTiming':reduction['nominalTiming'],'actualSave':'PASS','actualExport':'PASS',
        'capacity':'PASS','operatorText':'PASS','operatorScreenReview':'PENDING',
        'scope':'R1/R2 combined control; Group 2 fault cases remain open',
        'sd':'NOT RUN','physical':'NOT RUN'})
    checked(experiment)
    return actual


def focused(experiment, mode, attempt=1):
    prefix = 'ntsc' if mode=='1' else 'pal'
    suffix = '' if attempt == 1 else f'-{attempt:02d}'
    directory=experiment/(prefix+'-focused'+suffix)
    directory.mkdir(exist_ok=False)
    image=directory/'G2CTRL.D81'
    label='G2 CONTROL DEV'
    runtime.fresh_d81(directory,image,label,{'token':ROOT/'docs/evidence/r0f/successor/2026-09-21/TOKEN.prg'})
    timing(experiment,directory,image,mode,False,('token',),label)
    write(experiment/('focused-'+prefix+'-admission.json'),{'directory':str(directory),
        'validationSha256':sha(directory/'validation.json'),'prgSha256':checked(experiment)['prgSha256']})


def build_carrier(experiment):
    report=checked(experiment)
    for mode in ('ntsc','pal'):
        admission=json.loads((experiment/('focused-'+mode+'-admission.json')).read_text())
        directory=Path(admission['directory'])
        if sha(directory/'validation.json')!=admission['validationSha256']:raise ValueError('Focused record drift')
        gate=json.loads((directory/'validation.json').read_text())
        if gate['result']!='PASS' or gate['prgSha256']!=report['prgSha256']:raise ValueError('Focused gates missing')
    collision=json.loads((experiment/'export-collision/validation.json').read_text())
    if collision['result']!='PASS_EXPECTED_EXPORT_FAILURE' or collision['prgSha256']!=report['prgSha256']:raise ValueError('Exact control collision proof missing')
    directory=experiment/'carrier';directory.mkdir(exist_ok=False)
    canonical=directory/'canonical';canonical.mkdir()
    expected,loader=probe.carrier_contents(canonical,experiment/'CANDIDATE.prg',
        (experiment/'symbols.txt').read_text())
    expected['token']=ROOT/'docs/evidence/r0f/successor/2026-09-21/TOKEN.prg'
    # Existing first-chunk name is a safe on-disk stimulus. Never edit a tested
    # disk to add it; it belongs to this fresh single-session construction.
    expected['g1t00']=expected['token']
    image=canonical/NAME
    constructed=runtime.fresh_d81(canonical,image,NAME[:-4],expected)
    image.chmod(0o444)
    write(canonical/'host-gate.json',{'D81_STATE':'HOST_CONTENT_VERIFIED','D81_FILENAME':NAME,
        'D81_SHA256':constructed['sha256'],'D81_BYTES':819200,'label':NAME[:-4],
        'image':constructed,'build':report,**loader,'canonicalMountedWritable':False,
        'sourceBranch':runtime.git_text('branch','--show-current'),'sourceCommit':runtime.source_commit(),
        'case':'G2-L-EXPORT-COLLISION','programBuild':'R0FG2C1',
        'expectedOperator':{'status':5,'error':3,'files':0},
        'sd':'NOT RUN','physical':'NOT RUN','testEligible':False})
    print(image,flush=True)


def boot(experiment,mode,number):
    checked(experiment)
    carrier=experiment/'carrier';canonical=carrier/'canonical'
    if (carrier/'retirement.json').exists():raise ValueError('Carrier identity retired')
    gate=json.loads((canonical/'host-gate.json').read_text())
    if sha(canonical/NAME)!=gate['D81_SHA256']:raise ValueError('Canonical drift')
    run=('ntsc' if mode=='1' else 'pal')+f'-{number:02d}'
    directory=carrier/run;directory.mkdir(exist_ok=False)
    image=directory/NAME;shutil.copyfile(canonical/NAME,image);image.chmod(0o644)
    try:
        if sha(image)!=gate['D81_SHA256']:raise ValueError('Fresh exact-name copy drift')
        initial={e['name']:Path(gate['image']['extracted'][e['name']]).read_bytes()
                 for e in gate['image']['entries']}
        collision_result(experiment,directory,image,mode,True,initial,NAME[:-4])
        if sha(canonical/NAME)!=gate['D81_SHA256']:raise ValueError('Canonical changed')
        write(directory/'carrier-run.json',{'run':('ntsc' if mode=='1' else 'pal')+f'-{number}',
            'mountedD81Filename':NAME,'preRunD81Sha256':gate['D81_SHA256'],
            'postRunD81Sha256':sha(image),'validationSha256':sha(directory/'validation.json'),
            'result':'PASS_EXPECTED_EXPORT_FAILURE','autoload':True})
    except Exception as error:
        write(carrier/'retirement.json',{'result':'RETIRED_AFTER_LOCAL_GATE_FAILURE',
            'D81_FILENAME':NAME,'sha256':gate['D81_SHA256'],'run':run,'failure':str(error)})
        raise


def collision_result(experiment,directory,image,mode,autoload,initial,label):
    report=checked(experiment)
    write(directory/'build-identity.json',report)
    runtime.PRG=experiment/'CANDIDATE.prg'
    runtime.SOURCE_BRANCH=runtime.git_text('branch','--show-current')
    result,execution=runtime.run_xemu(directory,mode,image,'GROUP2_L_EXPORT_COLLISION',autoload,120)
    write(directory/'execution.json',execution)
    symbols=(experiment/'symbols.txt').read_text();memory=(directory/'memory.bin').read_bytes()
    observed={name:memory[probe.integration.symbol(symbols,'r0fg1_export_'+name)] for name in ('status','error','files')}
    if observed!={'status':5,'error':3,'files':0}:raise ValueError('Unexpected collision disposition')
    first=probe.integration.symbol(symbols,'r0fg1_operator_text')
    last=probe.integration.symbol(symbols,'r0fg1_operator_text_end')
    expected=b'\x93G1 EXPORT S:5 E:03 F:00\r4=OK 5=FAIL / E,F HEX\rREDUCE FOR TIMING\rNOT ACCEPTANCE\rRESET\r\0'
    if memory[first:last]!=expected:raise ValueError('Protected operator text mismatch')
    actual=probe.extract_actual(image,directory,[*initial,'rsstate'],label)
    for name,payload in initial.items():
        if actual[name]!=payload:raise ValueError('Preexisting file changed: '+name)
    import r0f_group1_reduce as core_oracle
    decoded=runtime.validate_success_result(result,(1600,3200),core_oracle.golden((1600,3200)))
    write(directory/'decoded-result.json',decoded)
    probe.validate_saved(actual['rsstate'],result,symbols)
    write(directory/'validation.json',{'result':'PASS_EXPECTED_EXPORT_FAILURE',
        'case':'G2-L-EXPORT-COLLISION','prgSha256':report['prgSha256'],
        'operator':observed,'operatorText':'PASS','operatorScreenReview':'PENDING',
        'preExistingFilesUnchanged':True,'actualReturningSave':'PASS',
        'lifecycleResult':'PASS_XEMU_MEMORY_ONLY','retries':0,
        'scope':'Export rejection/no-overwrite only; no exported trace or physical timing proof',
        'sd':'NOT RUN','physical':'NOT RUN'})
    checked(experiment)
    print('G2-L collision: rejected, no overwrite/retry, actual SAVE PASS',flush=True)


def collision(experiment):
    directory=experiment/'export-collision';directory.mkdir(exist_ok=False)
    image=directory/'G2COLL.D81';label='G2 COLLISION'
    token=ROOT/'docs/evidence/r0f/successor/2026-09-21/TOKEN.prg'
    runtime.fresh_d81(directory,image,label,{'token':token,'g1t00':token})
    collision_result(experiment,directory,image,'1',False,
                     {'token':token.read_bytes(),'g1t00':token.read_bytes()},label)


def finish_carrier(experiment):
    report=checked(experiment)
    carrier=experiment/'carrier';canonical=carrier/'canonical'
    if (carrier/'retirement.json').exists():raise ValueError('Carrier identity retired')
    gate=json.loads((canonical/'host-gate.json').read_text())
    if sha(canonical/NAME)!=gate['D81_SHA256']:raise ValueError('Canonical drift')
    runs=[]
    for mode in ('ntsc','pal'):
        for number in (1,2):
            directory=carrier/(mode+f'-{number:02d}')
            run=json.loads((directory/'carrier-run.json').read_text())
            execution=json.loads((directory/'execution.json').read_text())
            review=json.loads((directory/'operator-screen-review.json').read_text())
            validation=json.loads((directory/'validation.json').read_text())
            if (run['preRunD81Sha256']!=gate['D81_SHA256'] or run['mountedD81Filename']!=NAME
                or run['validationSha256']!=sha(directory/'validation.json')
                or run['result']!='PASS_EXPECTED_EXPORT_FAILURE' or not run['autoload']
                or '-autoload' not in execution['command'] or '-prg' in execution['command']
                or execution['videoMode']!=mode.upper()
                or validation['result']!='PASS_EXPECTED_EXPORT_FAILURE'
                or validation['prgSha256']!=report['prgSha256']
                or review['result']!='PASS_VISUALLY_REVIEWED'
                or review['observedLines'][0]!='G1 EXPORT S:5 E:03 F:00'
                or review['imageSha256']!=sha(directory/'screen.png')):
                raise ValueError('Exact boot/review gate missing: '+str(directory))
            runs.append({**run,'evidence':str(directory),
                         'screenSha256':review['imageSha256'],'execution':execution})
    lock=json.loads((ROOT/'toolchain/f65_toolchain.lock.json').read_text())
    builder=lock['r0d_d81_builder']
    validators=('tools/diagnostics/d81_foundation_compare.py',
                'tools/diagnostics/r0f_successor_emulator.py')
    write(canonical/'release.json',{
        'D81_STATE':'XEMU_BOOT_VERIFIED','D81_FILENAME':NAME,
        'D81_SHA256':gate['D81_SHA256'],'D81_BYTES':819200,
        'DISK_LABEL':NAME[:-4],'DISK_ID':runtime.CANONICAL_ID,'ENTRY_FILENAME':'AUTOBOOT.C65',
        'SOURCE_BRANCH':runtime.git_text('branch','--show-current'),
        'SOURCE_COMMIT':runtime.source_commit(),'UNCOMMITTED_SOURCE_FREEZE':True,
        'SOURCE_BUILD':str(experiment),'PROGRAM_SHA256':report['prgSha256'],
        'BUILDER_IDENTITY':{'path':builder['c1541_relative_path'],'version':builder['version'],
            'sha256':sha(ROOT/builder['c1541_relative_path']),'realdevice':'disabled'},
        'STRUCTURAL_VALIDATOR_IDENTITY':{path:sha(ROOT/path) for path in validators},
        'HOST_STRUCTURAL_RESULT':'PASS','HOST_CONTENT_RESULT':'PASS','XEMU_RESULT':'PASS',
        'XEMU_EVIDENCE':runs,'CASE':'G2-L-EXPORT-COLLISION',
        'SD_COPY_SHA256':None,'SD_FILESYSTEM':None,'SD_TRANSFER_METHOD':'OWNER_HELD',
        'SD_CONTIGUITY_RESULT':'NOT RUN','SD_EXTENT_COUNT':None,'SD_EXTENT_EVIDENCE':None,
        'SD_SAFE_EJECT_RESULT':'NOT RUN','PHYSICAL_CHOOSER_RESULT':'NOT RUN',
        'PHYSICAL_EVIDENCE':None,'TEST_ELIGIBLE':False,'GROUP2_COMPLETE':False})
    print(canonical/'release.json',flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('action',choices=('prepare','ntsc','pal','collision','carrier-build','boot','carrier-finish'))
    parser.add_argument('--experiment',type=Path)
    parser.add_argument('--mode',choices=('0','1'))
    parser.add_argument('--number',type=int,choices=(1,2))
    parser.add_argument('--attempt',type=int,choices=(1,2),default=1)
    args=parser.parse_args()
    if args.action=='prepare':prepare();return
    if args.experiment is None:parser.error('Exact experiment required')
    experiment=args.experiment.resolve()
    if args.action in ('ntsc','pal'):focused(experiment,'1' if args.action=='ntsc' else '0',args.attempt)
    elif args.action=='collision':collision(experiment)
    elif args.action=='carrier-build':build_carrier(experiment)
    elif args.action=='carrier-finish':finish_carrier(experiment)
    else:
        if args.mode is None or args.number is None:parser.error('Boot mode/number required')
        boot(experiment,args.mode,args.number)

if __name__=='__main__':
    main()
