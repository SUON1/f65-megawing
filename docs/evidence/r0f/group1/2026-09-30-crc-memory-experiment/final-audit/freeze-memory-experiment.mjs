import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';

const root = '/Users/slice/Developer/f65-megawing';
const evidence = path.join(root, 'docs/evidence/r0f/group1');
const experiment = path.join(root, 'build/r0f/group1/crc-recovery/nibble-01');
const output = path.join(evidence, '2026-09-30-crc-memory-experiment');
const auditOutput = path.join(experiment, 'final-audit');
assert(!fs.existsSync(output), 'never overwrite a retained evidence identity');
assert(!fs.existsSync(auditOutput), 'never overwrite final audit artifacts');
const read = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const check = (file, digest) => assert.equal(sha(file), digest, file);
const freezes = ['2026-09-30-six-order-corrected-ntsc', '2026-09-30-six-order-ntsc-120s',
  '2026-09-30-six-order-pal-120s', '2026-09-30-presentation-core',
  '2026-09-30-presentation-integration', '2026-09-30-pool-core'];
const baselines = {
  'build/r0f/group1/integration/preacq-trace-exact-f596-01/baseline-GROUP1.prg':
    'ec259fc7611d8bb5809d15f6c333f5b224df4c945a8e9ffca5b2402d8444cb30',
  'docs/evidence/r0f/group1/2026-09-30-six-order-corrected-ntsc/baseline/GROUP1.prg':
    '0d96a1b21eb36680b05689b659ac8c6f73cc2b61e647c060ab2f369c2bbfc244',
  'docs/evidence/r0f/group1/2026-09-30-six-order-corrected-ntsc/build/GROUP1.prg':
    'c249f4e4da972cdc0c5d0958a1a3a148387eb1ad4de602404c6b79fb7c79492b',
  'build/r0f/successor-integration/R0F-SUCCESSOR-INTEGRATION.prg':
    'cf605bd377ddcee2c72cdc4abfd20c3ae9eee350b7b78b36cbde8ff1adf8fc23',
};
const base = read(path.join(root, 'build/r0f/group1/integration/build.json'));
const carrier = read(path.join(root, 'build/r0f/group1/carriers/R0FG1P02/canonical/host-gate.json'));
const prepared = read(path.join(experiment, 'preparation.json'));
const fit = read(path.join(experiment, 'fit.json'));
const adapter = read(path.join(experiment, 'adapter-fit/fit.json'));
const host = read(path.join(experiment, 'host.json'));
const execution = read(path.join(experiment, 'ntsc-03/execution.json'));
const reduction = read(path.join(experiment, 'ntsc-03/reduction.json'));
const commands = [];
function execute(args, cwd = root) {
  const result = spawnSync(args[0], args.slice(1), { cwd, encoding: 'utf8', timeout: 60000 });
  assert.equal(result.status, 0, result.stderr || String(result.error));
  commands.push({ command: args, cwd, exitCode: result.status,
    stdout: result.stdout, stderr: result.stderr });
  return result.stdout + result.stderr;
}
function preservation() {
  const manifests = freezes.map(name => {
    const directory = path.join(evidence, name);
    const manifest = read(path.join(directory, 'sha256.json'));
    for (const [file, digest] of Object.entries(manifest.files)) check(path.join(directory, file), digest);
    return { freeze: name, verifiedFiles: Object.keys(manifest.files).length,
      manifestSha256: sha(path.join(directory, 'sha256.json')) };
  });
  assert.equal(manifests.reduce((total, item) => total + item.verifiedFiles, 0), 1777);
  assert.equal(Object.keys(base.inputs).length, 93);
  assert.equal(Object.keys(carrier.inputs).length, 95);
  for (const inputs of [base.inputs, carrier.inputs, prepared.originalInputs]) {
    for (const [file, digest] of Object.entries(inputs)) check(path.join(root, file), digest);
  }
  check(path.join(root, 'build/r0f/group1/integration/GROUP1.prg'), base.prgSha256);
  assert.equal(base.prgSha256, '25a18c23c750d0877103209fccd0114afe7cd30f31690731605b9687bfea94e1');
  assert.equal(carrier.D81_STATE, 'XEMU_BOOT_VERIFIED');
  check(path.join(root, 'build/r0f/group1/carriers/R0FG1P02/canonical/R0FG1P02.D81'), carrier.D81_SHA256);
  assert.equal(carrier.D81_SHA256, prepared.carrierSha256);
  for (const [file, digest] of Object.entries(baselines)) check(path.join(root, file), digest);
  const retired = read(path.join(root, 'build/r0f/group1/carriers/R0FG1P01/retirement.json'));
  check(path.join(root, 'build/r0f/group1/carriers/R0FG1P01/canonical/R0FG1P01.D81'), retired.canonicalSha256);
  check(path.join(root, 'build/r0f/group1/carriers/R0FG1P01/ntsc-01/R0FG1P01.D81'), retired.postRunSha256);
  assert.deepEqual(prepared.baseline, base);
  const changes = Object.entries(prepared.originalInputs)
    .filter(([file, digest]) => sha(path.join(experiment, 'source-inputs', file)) !== digest)
    .map(([file]) => file).sort();
  assert.deepEqual(changes, prepared.allowedExperimentalChanges.slice().sort());
  assert.equal(changes.length, 3);
  for (const report of [fit.runtime, fit['pool-fit'], adapter, host]) {
    const inputs = report.snapshotInputs ?? report.inputs;
    for (const [file, digest] of Object.entries(inputs)) check(path.join(experiment, 'source-inputs', file), digest);
  }
  for (const [label, report] of Object.entries(fit)) {
    check(path.join(experiment, label, 'GROUP1.prg'), report.prgSha256);
    assert.deepEqual(report.sections['.r0fs_protected'], base.sections['.r0fs_protected']);
  }
  check(path.join(experiment, 'adapter-fit/FIT-ONLY.prg'), adapter.prgSha256);
  check(adapter.source, adapter.sourceSha256);
  check(path.join(root, 'tools/diagnostics/r0f_group1_crc_host_test.c'), host.crcTestSha256);
  const poolQualification = read(path.join(root, 'build/r0f/group1/pool-core/validation.json'));
  assert.equal(poolQualification.result, 'PASS');
  for (const [file, digest] of Object.entries(poolQualification.inputs)) check(path.join(root, file), digest);
  assert.equal(execute(['git', 'rev-parse', 'HEAD']).trim(), '9e2ffdb4786e4794119933a5edd4b1cf79f653f0');
  assert.equal(execute(['git', 'branch', '--show-current']).trim(), 'codex/r0f-successor-physical-exact-carrier');
  return { manifests, unchangedBaselineInputs: 93, unchangedCarrierInputs: 95, changes,
    baselineSha256: base.prgSha256, carrierSha256: carrier.D81_SHA256, baselines, retired };
}
const before = preservation();
assert.equal(fit.runtime.fit, 'PASS');
assert.equal(fit.runtime.residentEndExclusive, 0xbc61);
assert.equal(fit.runtime.residentRecoveredBytes, 868);
assert.equal(fit['pool-fit'].fit, 'PASS');
assert.equal(fit['pool-fit'].residentEndExclusive, 0xbf0e);
assert.equal(adapter.fit, 'FAIL');
assert.equal(adapter.residentEndExclusive, 0xc042);
assert.equal(adapter.overflowBytes, 66);
assert.equal(adapter.adapterGrowthBytes, 308);
assert.equal(adapter.executed, false);
assert.equal(adapter.admitted, false);
assert.equal(host.result, 'PASS');
assert.equal(execution.videoArgument, '1');
assert.equal(execution.videoMode, 'NTSC');
assert.equal(execution.status, 4);
assert.equal(execution.error, 0);
assert.equal(execution.files, 19);
assert.equal(execution.timedTerminationAfterSeconds, 120);
assert.equal(reduction.acquisition, 'PASS');
assert.equal(reduction.records, 3200);
assert.equal(reduction.nominalTiming, 'WITHIN_OBSERVED_BOUNDS');
assert.equal(reduction.nominalDeadlineMisses, 0);
assert.equal(reduction.boundaryUncertain, 0);
assert.equal(reduction.cohortsBelow20Hz, 0);
assert.equal(reduction.worldEventsRetained, 954);
assert.equal(fs.statSync(path.join(experiment, 'ntsc-03/trace.bin')).size, 310436);
check(path.join(experiment, 'ntsc-03/trace.bin'), 'f2929476d1e3a40b67046a7c22b612635b1814e737dbfeeb7a0a1fc8cafaaf89');
const timingBaseline = read(path.join(evidence, '2026-09-30-presentation-integration/development/presentation-ntsc-04/reduction.json'));
assert.equal(timingBaseline.instrumentedExecutionCounts.max, 6880);
assert.equal(timingBaseline.instrumentedExecutionCounts.p95, 6816);
fs.mkdirSync(auditOutput);
for (const [label, original, expected] of [
  ['workload-host-test', host.command, /1025 streaming CRC lengths PASS/],
  ['crc-host-test', host.crcCommand, /69641 cases/],
]) {
  const command = original.slice();
  const binary = path.join(auditOutput, label);
  command[command.indexOf('-o') + 1] = binary;
  execute(command, path.join(experiment, 'source-inputs'));
  assert.match(execute([binary]), expected);
}
const adapterBinary = path.join(auditOutput, 'adapter-host-test');
execute(['/usr/bin/clang', '-std=c11', '-Wall', '-Wextra', '-Wconversion', '-Werror',
  '-fsanitize=address,undefined', '-Iinterfaces/generated', '-Isrc/diagnostics/r0f',
  'src/diagnostics/r0f/group1_pool.c', 'tools/diagnostics/r0f_group1_pool_shape.c',
  'tools/diagnostics/r0f_group1_pool_adapter_probe.c', 'tools/diagnostics/r0f_group1_pool_adapter_host_test.c',
  '-o', adapterBinary]);
assert.match(execute([adapterBinary]), /Cold adapter host PASS/);
assert.match(execute(['python3', '-B', '-m', 'unittest', 'discover', '-s', 'tools/diagnostics',
  '-p', 'test_r0f_group1_*.py', '-v']), /Ran 41 tests/);
assert.match(execute(['python3', '-B', 'tools/diagnostics/test_r0f_group1_reduce.py',
  path.join(experiment, 'ntsc-03/trace.bin')]), /rejected 30 corruption cases/);
execute(['git', 'diff', '--check']);
const nm = path.join(path.dirname(base.commands[0][0]), 'llvm-nm');
for (const [label, bytes] of [['baseline', 1024], ['runtime', 64]]) {
  const symbols = execute([nm, '--print-size', '--size-sort', path.join(experiment, label, 'GROUP1.prg.elf')]);
  fs.writeFileSync(path.join(auditOutput, `${label}-size-breakdown.txt`), symbols, { flag: 'wx' });
  const table = symbols.split('\n').find(line => line.endsWith('r0fs_crc32_update.crc_table'));
  assert(table, 'CRC table symbol missing');
  assert.equal(parseInt(table.trim().split(/\s+/)[1], 16), bytes);
}
const after = preservation();
assert.deepEqual(after, before);
execute(['git', 'status', '--short']);
const excluded = ['ntsc-01', 'ntsc-02', 'ntsc-03'].map(name => ({
  path: `${name}/disposable-sd.img`, bytes: fs.statSync(path.join(experiment, name, 'disposable-sd.img')).size,
  exclusionReason: 'Disposable multi-gigabyte emulator fixture; retained in build, not deleted',
  recordedExecutionSha256: name === 'ntsc-03' ? execution.disposableSdSha256 : null,
  rehashedInThisFreeze: false,
}));
fs.mkdirSync(output);
function copy(file, destination) {
  assert(destination.startsWith(`${output}/`));
  fs.mkdirSync(path.dirname(destination), { recursive: true });
  fs.cpSync(file, destination, { recursive: true, filter: source =>
    path.basename(source) !== '__pycache__' && !source.endsWith('.pyc') &&
    path.basename(source) !== 'disposable-sd.img' });
}
copy(experiment, path.join(output, 'experiment'));
const tools = ['r0f_group1_memory_experiment.py', 'test_r0f_group1_memory_experiment.py',
  'r0f_group1_crc_host_test.c', 'r0f_group1_pool_adapter_probe.c', 'r0f_group1_pool_adapter_host_test.c'];
for (const file of tools) copy(path.join(root, 'tools/diagnostics', file), path.join(output, 'experiment-tools', file));
const authority = ['AGENTS.md', 'CURRENT_STATE.md', 'WORK_IN_PROGRESS.md',
  'docs/DEVELOPMENT_WORKFLOW.md', 'docs/PROGRAMMING_PRINCIPLES.md', 'docs/CODE_STYLE_C.md',
  '00_D81_LOADABILITY_GATE.md', 'docs/D81_WORKFLOW.md',
  'docs/plans/R0-F_GROUP1_BUILD_INTENT.md', 'docs/plans/R0-F_GROUP1_EXPORT_AMENDMENT.md',
  'docs/plans/R0-F_GROUP1_MEASUREMENT_MATRIX.md',
  'docs/reports/R0-F_GROUP1_CRC_MEMORY_EXPERIMENT.md',
  'docs/reports/R0-F_GROUP1_POOL_OBSERVATION_CORE.md',
  'docs/reports/R0-F_GROUP1_SERVICE_PHASE_DIAGNOSTIC.md'];
for (const file of authority) copy(path.join(root, file), path.join(output, 'authority-checkpoint', file));
copy(path.join(root, 'build/r0f/group1/freeze-memory-experiment.mjs'), path.join(output, 'final-audit/freeze-memory-experiment.mjs'));
const validation = {
  result: 'PASS_ISOLATED_RECOVERY_AND_PRESERVATION_POOL_ADAPTER_FIT_FAIL',
  sourceCommit: '9e2ffdb4786e4794119933a5edd4b1cf79f653f0',
  sourceBranch: 'codex/r0f-successor-physical-exact-carrier', dirtyTree: true,
  before, after, commands, fit, adapterFit: adapter, host,
  ntsc: { execution, reduction }, timingBaselineIdentity:
    '2026-09-30-presentation-integration/development/presentation-ntsc-04/reduction.json',
  excludedFiles: excluded, runtimeSha256: fit.runtime.prgSha256,
  finalHarnessAddedAfterAcquisition: 'Completion gate, unit checks and cold adapter action; executed source/PRG unchanged',
  actualPoolObservations: 'NOT RUN', freshPal: 'NOT RUN', newCarrier: 'NOT RUN',
  sd: 'NOT RUN', physical: 'NOT RUN', commit: 'NOT RUN', push: 'NOT RUN',
  fullGroup1Acceptance: false, fullR0FAcceptance: false,
};
fs.writeFileSync(path.join(output, 'validation.json'), `${JSON.stringify(validation, null, 2)}\n`, { flag: 'wx' });
const files = {};
function walk(directory) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
    const file = path.join(directory, entry.name);
    if (entry.isDirectory()) walk(file);
    else { assert(entry.isFile(), 'unexpected evidence symlink'); files[path.relative(output, file)] = sha(file); }
  }
}
walk(output);
const manifest = path.join(output, 'sha256.json');
fs.writeFileSync(manifest, `${JSON.stringify({
  scope: 'One isolated nibble-CRC recovery; focused NTSC pass; pool adapter fit FAIL, no integration admission',
  algorithm: 'sha256', files,
}, null, 2)}\n`, { flag: 'wx' });
for (const [file, digest] of Object.entries(files)) check(path.join(output, file), digest);
assert.deepEqual(preservation(), before);
console.log(JSON.stringify({ result: 'PASS_PRESERVATION_AND_ISOLATED_EXPERIMENT',
  frozenFiles: Object.keys(files).length, manifestSha256: sha(manifest), priorFilesVerified: 1777,
  residentRecoveredBytes: 868, poolAdapterFit: 'FAIL', overflowBytes: 66,
  actualPoolObservations: 'NOT RUN', freshPal: 'NOT RUN', newCarrier: 'NOT RUN' }));
