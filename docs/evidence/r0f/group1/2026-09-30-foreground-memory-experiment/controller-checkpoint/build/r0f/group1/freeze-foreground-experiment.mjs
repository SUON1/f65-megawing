import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';

const root = '/Users/slice/Developer/f65-megawing';
const evidence = path.join(root, 'docs/evidence/r0f/group1');
const experiment = path.join(root, 'build/r0f/group1/foreground-recovery/shared-bounds-01');
const output = path.join(evidence, '2026-09-30-foreground-memory-experiment');
assert(!fs.existsSync(output), 'never overwrite retained evidence');
const read = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const check = (file, expected) => assert.equal(sha(file), expected, file);
const preceding = read(path.join(evidence, '2026-09-30-crc-memory-experiment/validation.json'));
const freezeNames = [...preceding.before.manifests.map(item => item.freeze), '2026-09-30-crc-memory-experiment'];
const preparation = read(path.join(experiment, 'preparation.json'));
const fit = read(path.join(experiment, 'fit.json'));
const host = read(path.join(experiment, 'host.json'));
const execution = read(path.join(experiment, 'ntsc-01/execution.json'));
const reduction = read(path.join(experiment, 'ntsc-01/reduction.json'));
function preservation() {
  const manifests = freezeNames.map(name => {
    const directory = path.join(evidence, name), manifest = read(path.join(directory, 'sha256.json'));
    for (const [file, digest] of Object.entries(manifest.files)) check(path.join(directory, file), digest);
    return { name, files: Object.keys(manifest.files).length, manifestSha256: sha(path.join(directory, 'sha256.json')) };
  });
  assert.equal(manifests.reduce((sum, item) => sum + item.files, 0), 2016);
  const base = read(path.join(root, 'build/r0f/group1/integration/build.json'));
  const carrier = read(path.join(root, 'build/r0f/group1/carriers/R0FG1P02/canonical/host-gate.json'));
  assert.equal(Object.keys(base.inputs).length, 93);
  assert.equal(Object.keys(carrier.inputs).length, 95);
  for (const inputs of [base.inputs, carrier.inputs]) {
    for (const [file, digest] of Object.entries(inputs)) check(path.join(root, file), digest);
  }
  check(path.join(root, 'build/r0f/group1/integration/GROUP1.prg'), preceding.before.baselineSha256);
  check(path.join(root, 'build/r0f/group1/carriers/R0FG1P02/canonical/R0FG1P02.D81'), preceding.before.carrierSha256);
  for (const [file, digest] of Object.entries(preceding.before.baselines)) check(path.join(root, file), digest);
  const retired = preceding.before.retired;
  check(path.join(root, 'build/r0f/group1/carriers/R0FG1P01/canonical/R0FG1P01.D81'), retired.canonicalSha256);
  check(path.join(root, 'build/r0f/group1/carriers/R0FG1P01/ntsc-01/R0FG1P01.D81'), retired.postRunSha256);
  check(path.join(root, 'build/r0f/group1/crc-recovery/nibble-01/runtime/GROUP1.prg'), preparation.predecessor.prgSha256);
  for (const [file, digest] of Object.entries(preparation.predecessor.inputs)) {
    check(path.join(root, 'build/r0f/group1/crc-recovery/nibble-01/source-inputs', file), digest);
  }
  check(path.join(root, 'tools/diagnostics/r0f_group1_foreground_experiment.py'), preparation.controllerSha256);
  const changed = Object.entries(preparation.inputs).filter(([file, digest]) =>
    sha(path.join(experiment, 'source-inputs', file)) !== digest).map(([file]) => file);
  assert.deepEqual(changed, ['src/diagnostics/r0f/combined_model.c']);
  for (const report of [fit.runtime, fit['adapter-fit'], host]) {
    for (const [file, digest] of Object.entries(report.inputs)) check(path.join(experiment, 'source-inputs', file), digest);
  }
  for (const [label, report] of Object.entries(fit)) check(path.join(experiment, label, 'GROUP1.prg'), report.prgSha256);
  return { manifests, basePrg: base.prgSha256, baseInputs: 93,
    carrier: carrier.D81_SHA256, carrierInputs: 95, nibblePrg: preparation.predecessor.prgSha256, changed };
}
const before = preservation();
assert.equal(host.result, 'PASS');
assert.equal(fit.runtime.fit, 'PASS');
assert.equal(fit.runtime.residentEndExclusive, 0xbbbe);
assert.equal(fit['adapter-fit'].fit, 'PASS');
assert.equal(fit['adapter-fit'].residentEndExclusive, 0xbf9f);
assert.equal(fit['adapter-fit'].executed, false);
assert.equal(fit['adapter-fit'].actualPoolObservations, false);
assert.equal(execution.videoMode, 'NTSC');
assert.equal(execution.videoArgument, '1');
assert.equal(execution.status, 4);
assert.equal(execution.error, 0);
assert.equal(execution.files, 19);
assert.equal(reduction.acquisition, 'PASS');
assert.equal(reduction.nominalTiming, 'WITHIN_OBSERVED_BOUNDS');
assert.equal(reduction.records, 3200);
assert.equal(reduction.nominalDeadlineMisses, 0);
assert.equal(reduction.boundaryUncertain, 0);
assert.equal(reduction.cohortsBelow20Hz, 0);
const commands = [];
function execute(args, expected = 0) {
  const result = spawnSync(args[0], args.slice(1), { cwd: root, encoding: 'utf8', timeout: 60000 });
  assert.equal(result.status, expected, result.stderr || String(result.error));
  commands.push({ command: args, exitCode: result.status, stdout: result.stdout, stderr: result.stderr });
  return result.stdout + result.stderr;
}
assert.equal(execute(['git', 'rev-parse', 'HEAD']).trim(), '9e2ffdb4786e4794119933a5edd4b1cf79f653f0');
assert.equal(execute(['git', 'branch', '--show-current']).trim(), 'codex/r0f-successor-physical-exact-carrier');
assert.match(execute(['python3', '-B', 'tools/diagnostics/test_r0f_group1_reduce.py',
  path.join(experiment, 'ntsc-01/trace.bin')]), /rejected 30 corruption cases/);
execute(['git', 'diff', '--check']);
execute(['git', 'diff', '--no-index', '--',
  path.join(root, 'build/r0f/group1/crc-recovery/nibble-01/source-inputs/src/diagnostics/r0f/combined_model.c'),
  path.join(experiment, 'source-inputs/src/diagnostics/r0f/combined_model.c')], 1);
const after = preservation();
assert.deepEqual(after, before);
fs.mkdirSync(output);
function copy(file, destination) {
  assert(destination.startsWith(`${output}/`));
  fs.mkdirSync(path.dirname(destination), { recursive: true });
  fs.cpSync(file, destination, { recursive: true, filter: source =>
    path.basename(source) !== 'disposable-sd.img' && path.basename(source) !== '__pycache__' && !source.endsWith('.pyc') });
}
copy(experiment, path.join(output, 'experiment'));
for (const file of ['tools/diagnostics/r0f_group1_foreground_experiment.py',
  'tools/diagnostics/r0f_group1_memory_experiment.py',
  'build/r0f/group1/freeze-foreground-experiment.mjs']) {
  copy(path.join(root, file), path.join(output, 'controller-checkpoint', file));
}
for (const file of ['AGENTS.md', 'CURRENT_STATE.md', 'WORK_IN_PROGRESS.md',
  'docs/DEVELOPMENT_WORKFLOW.md', 'docs/PROGRAMMING_PRINCIPLES.md', 'docs/CODE_STYLE_C.md',
  '00_D81_LOADABILITY_GATE.md', 'docs/D81_WORKFLOW.md',
  'docs/plans/R0-F_GROUP1_BUILD_INTENT.md', 'docs/plans/R0-F_GROUP1_EXPORT_AMENDMENT.md',
  'docs/plans/R0-F_GROUP1_MEASUREMENT_MATRIX.md',
  'docs/reports/R0-F_GROUP1_FOREGROUND_MEMORY_EXPERIMENT.md']) {
  copy(path.join(root, file), path.join(output, 'authority-checkpoint', file));
}
const validation = { result: 'PASS_ISOLATED_SHARED_BOUNDS_EXPERIMENT', before, after, commands,
  host, fit, execution, reduction, traceSha256: sha(path.join(experiment, 'ntsc-01/trace.bin')),
  hostUnitSuite: { command: ['python3', '-B', '-m', 'unittest', 'discover', '-s',
    'tools/diagnostics', '-p', 'test_r0f_group1_*.py', '-v'], exitCode: 0, tests: 41,
    evidence: 'Successful command output in this task before freeze; not rerun for capture' },
  excludedFixture: { path: 'experiment/ntsc-01/disposable-sd.img',
    recordedExecutionSha256: execution.disposableSdSha256, rehashedDuringFreeze: false,
    reason: 'Disposable multi-gigabyte emulator fixture retained in build, not deleted' },
  actualPoolObservations: 'NOT RUN', fullPoolIntegrationFit: 'NOT VERIFIED',
  freshPal: 'NOT RUN', newCarrier: 'NOT RUN', sd: 'NOT RUN', physical: 'NOT RUN',
  commit: 'NOT RUN', push: 'NOT RUN', fullGroup1Acceptance: false, fullR0FAcceptance: false };
fs.writeFileSync(path.join(output, 'validation.json'), `${JSON.stringify(validation, null, 2)}\n`, { flag: 'wx' });
const files = {};
function walk(directory) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
    const file = path.join(directory, entry.name);
    if (entry.isDirectory()) walk(file);
    else { assert(entry.isFile()); files[path.relative(output, file)] = sha(file); }
  }
}
walk(output);
const manifest = path.join(output, 'sha256.json');
fs.writeFileSync(manifest, `${JSON.stringify({ scope: 'One isolated shared bounds variant; cold adapter fits; focused NTSC passes; actual pool integration remains open',
  algorithm: 'sha256', files }, null, 2)}\n`, { flag: 'wx' });
for (const [file, digest] of Object.entries(files)) check(path.join(output, file), digest);
assert.deepEqual(preservation(), before);
console.log(JSON.stringify({ result: 'PASS', frozenFiles: Object.keys(files).length,
  priorFilesVerified: 2016, manifestSha256: sha(manifest), recoveredBytes: 163,
  totalRecoveredBytes: 1031, coldAdapterFreeBytes: 97, actualPoolIntegration: 'NOT VERIFIED' }));
