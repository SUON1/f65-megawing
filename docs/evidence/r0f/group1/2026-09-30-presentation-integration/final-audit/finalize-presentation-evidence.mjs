import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import assert from 'node:assert/strict';

const root = '/Users/slice/Developer/f65-megawing';
const evidence = path.join(root, 'docs/evidence/r0f/group1');
const freeze = path.join(evidence, '2026-09-30-presentation-integration');
const carrier = path.join(root, 'build/r0f/group1/carriers/R0FG1P02');
const phase = process.argv[2];
assert(['prepare', 'seal'].includes(phase), 'choose prepare or seal');
assert(!fs.existsSync(path.join(freeze, 'sha256.json')), 'already frozen; never overwrite');
const read = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const checkHash = (file, expected) => assert.equal(sha(file), expected, file);
const copy = (source, destination) => {
  assert(destination.startsWith(`${freeze}/`), 'copy outside this new freeze');
  fs.mkdirSync(path.dirname(destination), { recursive: true });
  fs.cpSync(source, destination, { recursive: true, filter: file =>
    path.basename(file) !== 'disposable-sd.img' && path.basename(file) !== '__pycache__'
    && !file.endsWith('.pyc') });
};
const inputs = (base, hashes) => {
  for (const [file, expected] of Object.entries(hashes)) checkHash(path.join(base, file), expected);
  return Object.keys(hashes).length;
};
const commands = [];
const run = (program, args) => {
  const result = spawnSync(program, args, { cwd: root, encoding: 'utf8', timeout: 60000,
    maxBuffer: 4 * 1024 * 1024 });
  commands.push({ command: [program, ...args], exitCode: result.status,
    stdout: result.stdout, stderr: result.stderr });
  assert.equal(result.status, 0, `${program}: ${result.error ?? result.stderr}`);
  return result.stdout;
};
const stable = value => Array.isArray(value) ? value.map(stable) :
  value && typeof value === 'object' ? Object.fromEntries(Object.keys(value).sort()
    .map(key => [key, stable(value[key])])) : value;
const build = read(path.join(root, 'build/r0f/group1/integration/build.json'));
const gate = read(path.join(carrier, 'canonical/host-gate.json'));
const summary = read(path.join(carrier, 'carrier-summary.json'));
assert.equal(build.prgSha256, '25a18c23c750d0877103209fccd0114afe7cd30f31690731605b9687bfea94e1');
assert.equal(build.residentEndExclusive, 0xbfc5);
assert.equal(build.residentFreeBytes, 59);
assert.equal(gate.D81_SHA256, '60cea9c8dd51b0f2c199605e60574c0bebd7c758d5899fb9b1e7c2901f83e832');
assert.equal(gate.D81_STATE, 'XEMU_BOOT_VERIFIED');
assert.equal(summary.runs.length, 4);
assert.equal(summary.physical, 'NOT RUN');
assert.equal(summary.sd, 'NOT RUN');
assert.equal(summary.testEligible, false);
assert.equal(summary.fullGroup1Acceptance, false);
assert.equal(inputs(root, build.inputs), 93);
assert.equal(inputs(root, gate.inputs), 95);
assert.equal(inputs(path.join(freeze, 'source-inputs'), gate.inputs), 95);
checkHash(path.join(root, 'build/r0f/group1/integration/GROUP1.prg'), build.prgSha256);
checkHash(path.join(freeze, 'build/GROUP1.prg'), build.prgSha256);
checkHash(path.join(carrier, 'canonical/R0FG1P02.D81'), gate.D81_SHA256);
checkHash(path.join(freeze, 'carrier/R0FG1P02/canonical/R0FG1P02.D81'), gate.D81_SHA256);
assert.equal(fs.statSync(path.join(carrier, 'canonical/R0FG1P02.D81')).mode & 0o222, 0);

const preservation = [];
for (const name of ['2026-09-30-six-order-corrected-ntsc', '2026-09-30-six-order-ntsc-120s',
  '2026-09-30-six-order-pal-120s', '2026-09-30-presentation-core']) {
  const directory = path.join(evidence, name);
  const manifest = read(path.join(directory, 'sha256.json'));
  preservation.push({ freeze: name, verifiedFiles: inputs(directory, manifest.files),
    manifestSha256: sha(path.join(directory, 'sha256.json')) });
}
assert.equal(preservation.reduce((sum, row) => sum + row.verifiedFiles, 0), 248);
const baselines = {
  'build/r0f/group1/integration/preacq-trace-exact-f596-01/baseline-GROUP1.prg':
    'ec259fc7611d8bb5809d15f6c333f5b224df4c945a8e9ffca5b2402d8444cb30',
  'docs/evidence/r0f/group1/2026-09-30-six-order-corrected-ntsc/baseline/GROUP1.prg':
    '0d96a1b21eb36680b05689b659ac8c6f73cc2b61e647c060ab2f369c2bbfc244',
  'docs/evidence/r0f/group1/2026-09-30-six-order-corrected-ntsc/build/GROUP1.prg':
    'c249f4e4da972cdc0c5d0958a1a3a148387eb1ad4de602404c6b79fb7c79492b',
  'build/r0f/successor-integration/R0F-SUCCESSOR-INTEGRATION.prg':
    'cf605bd377ddcee2c72cdc4abfd20c3ae9eee350b7b78b36cbde8ff1adf8fc23',
  'build/r0f/group1/ordinary-preservation-final/R0F-SUCCESSOR-INTEGRATION.prg':
    'cf605bd377ddcee2c72cdc4abfd20c3ae9eee350b7b78b36cbde8ff1adf8fc23',
};
inputs(root, baselines);
for (const name of ['cache-refresh-probe', 'cache-refresh-negative-probe', 'pre-refresh-build']) {
  const snapshot = path.join(freeze, name);
  inputs(path.join(snapshot, 'source-inputs'), read(path.join(snapshot, 'build.json')).inputs);
}
const retired = read(path.join(freeze, 'retired-carrier/R0FG1P01/retirement.json'));
checkHash(path.join(freeze, 'retired-carrier/R0FG1P01/canonical/R0FG1P01.D81'), retired.canonicalSha256);
checkHash(path.join(freeze, 'retired-carrier/R0FG1P01/ntsc-01/R0FG1P01.D81'), retired.postRunSha256);

if (phase === 'prepare') {
  copy(path.join(carrier, 'pal-02'), path.join(freeze, 'carrier/R0FG1P02/pal-02'));
  copy(path.join(carrier, 'carrier-summary.json'), path.join(freeze, 'carrier/R0FG1P02/carrier-summary.json'));
  copy(path.join(carrier, 'canonical/host-gate.json'), path.join(freeze, 'carrier/R0FG1P02/canonical/host-gate.json'));
  const probe = path.join(root, 'build/r0f/group1/cache-refresh-collision-probe');
  const probeBuild = read(path.join(probe, 'build.json'));
  assert.equal(inputs(root, probeBuild.inputs), 77);
  copy(probe, path.join(freeze, 'cache-refresh-collision-probe'));
  for (const file of Object.keys(probeBuild.inputs)) copy(path.join(root, file),
    path.join(freeze, 'cache-refresh-collision-probe/source-inputs', file));
  assert.equal(inputs(path.join(freeze, 'cache-refresh-collision-probe/source-inputs'), probeBuild.inputs), 77);
  const collision = read(path.join(freeze, 'cache-refresh-collision-probe/pal-existing-01/export-validation.json'));
  assert.equal(collision.result, 'PASS');
  assert.equal(collision.status, 5);
  assert.equal(collision.error, 3);
  assert.equal(collision.actualFiles, 0);
  assert.equal(collision.existingFileUnchanged, true);
  assert.equal(collision.traceBytes, 0);
  assert.equal(collision.successorResult.fault, 0);
  assert.equal(collision.execution.videoMode, 'PAL');
  assert.equal(collision.execution.timedTerminationAfterSeconds, 60);
  const marker = 'cache-refresh-collision-probe/pal-existing-01/';
  checkHash(path.join(freeze, marker, 'actual/g1t00'), sha(path.join(freeze, marker, 'existing.prg')));
  assert.equal(fs.statSync(path.join(freeze, marker, 'actual/rsstate')).size, 34);
  for (const file of ['WORK_IN_PROGRESS.md', 'docs/reports/R0-F_GROUP1_PRESENTATION_INTEGRATION.md',
    'docs/plans/R0-F_GROUP1_MEASUREMENT_MATRIX.md', 'docs/reports/R0-F_GROUP1_PRESENTATION_CORE.md']) {
    copy(path.join(root, file), path.join(freeze, 'authority-checkpoint', file));
  }
  const host = run('python3', ['-B', '-m', 'unittest', 'discover', '-s', 'tools/diagnostics',
    '-p', 'test_r0f_group1_*.py', '-v']);
  assert.match(commands.at(-1).stderr + host, /Ran 30 tests/);
  run('git', ['diff', '--check']);
  const audit = path.join(freeze, 'final-audit');
  fs.mkdirSync(audit, { recursive: true });
  const runRows = [];
  const symbols = fs.readFileSync(path.join(root, 'build/r0f/group1/integration/symbols.txt'), 'utf8');
  const payload = `0x${symbols.match(/^([0-9a-f]+)\s+T\s+r0fsi_payload$/m)[1]}`;
  for (const runName of ['presentation-ntsc-04', 'presentation-pal-02', 'ntsc-01', 'ntsc-02', 'pal-01', 'pal-02']) {
    const isCarrier = !runName.startsWith('presentation');
    const directory = path.join(freeze, isCarrier ? 'carrier/R0FG1P02' : 'development', runName);
    const execution = read(path.join(directory, 'execution.json'));
    assert.equal(execution.status, 4);
    assert.equal(execution.error, 0);
    assert.equal(execution.files, 19);
    assert.equal(execution.timedTerminationAfterSeconds, 120);
    if (isCarrier) {
      const validation = read(path.join(directory, 'validation.json'));
      assert.equal(validation.result, 'PASS');
      assert.equal(validation.structureAndContent, 'PASS');
      assert.equal(validation.actualSave, 'PASS');
      assert(execution.command.includes('-autoload') && !execution.command.includes('-prg'));
      checkHash(path.join(directory, 'R0FG1P02.D81'), validation.postRunSha256);
      checkHash(path.join(directory, 'trace.bin'), validation.traceSha256);
      assert.equal(validation.canonicalSha256, gate.D81_SHA256);
      assert.equal(validation.prgSha256, build.prgSha256);
    } else {
      assert.equal(read(path.join(directory, 'build-identity.json')).prgSha256, build.prgSha256);
    }
    const output = path.join(audit, `${runName}-reduction.json`);
    run('python3', ['-B', 'tools/diagnostics/r0f_group1_reduce.py', path.join(directory, 'trace.bin'),
      '--saved', path.join(directory, 'saved.prg'), '--payload-address', payload, '--out', output]);
    const report = read(output);
    assert.deepEqual(stable(report), stable(read(path.join(directory, 'reduction.json'))));
    assert.equal(report.records, 3200);
    assert.equal(report.nominalDeadlineMisses, 0);
    assert.equal(report.boundaryUncertain, 0);
    assert.equal(report.cohortsBelow20Hz, 0);
    runRows.push({ run: runName, tier: isCarrier ? 'EXACT_NAME_XEMU_CARRIER' : 'DIRECT_XEMU',
      videoMode: execution.videoMode, traceSha256: sha(path.join(directory, 'trace.bin')),
      records: report.records, completePairs: report.worldEventsRetained,
      nominalMisses: 0, boundaryUncertain: 0, cohortsBelow20Hz: 0, result: 'PASS' });
    if (['presentation-ntsc-04', 'presentation-pal-02', 'ntsc-01'].includes(runName)) {
      const negative = run('python3', ['-B', 'tools/diagnostics/test_r0f_group1_reduce.py', path.join(directory, 'trace.bin')]);
      assert.match(negative, /rejected 30 corruption cases/);
    }
  }
  copy(path.join(root, 'build/r0f/group1/finalize-presentation-evidence.mjs'), path.join(audit, 'finalize-presentation-evidence.mjs'));
  const validation = { result: 'PASS', scope: 'Bounded private presentation integration, fit, fresh timing and local exact-carrier gates only',
    sourceCommit: run('git', ['rev-parse', 'HEAD']).trim(), sourceBranch: run('git', ['branch', '--show-current']).trim(),
    prgSha256: build.prgSha256, prgBytes: build.prgBytes, residentEndExclusive: build.residentEndExclusive,
    residentFreeBytes: 59, buildInputsVerified: 93, finalInputsVerified: 95,
    D81_FILENAME: gate.D81_FILENAME, D81_SHA256: gate.D81_SHA256, D81_STATE: gate.D81_STATE,
    canonicalMountedWritable: false, runs: runRows, hostTests: 30, corruptionCasesPerTrace: 30,
    corpus: read(path.join(freeze, 'host-scene/validation.json')), preservation, baselines,
    retiredCarrierPreserved: true, originalContextLifetimesUnchanged: true,
    probeInputsVerified: { normal: 73, initializeError: 73, collision: 77 }, collisionProbe: collision,
    commands, physical: 'NOT RUN', sd: 'NOT RUN', commit: 'NOT RUN', push: 'NOT RUN',
    fullGroup1Acceptance: false, fullR0FAcceptance: false, testEligible: false,
    remaining: ['Production projection/directional hysteresis/terrain-carrier registration',
      'Geometry/audio/sensor pool observations', 'Integrated near-capacity trace', 'Compact operator summary',
      'Whole ISR/entry latency and physical SI uncertainty', 'SD allocation/one extent and physical chooser/entry/runtime'] };
  fs.writeFileSync(path.join(freeze, 'validation.json'), `${JSON.stringify(validation, null, 2)}\n`, { flag: 'wx' });
  console.log('Final audit PASS; six exact reductions, 30 host tests, three 30-case mutation suites; ready to seal.');
} else {
  assert.equal(read(path.join(freeze, 'validation.json')).result, 'PASS');
  assert.equal(read(path.join(freeze, 'carrier/R0FG1P02/canonical/host-gate.json')).D81_STATE, 'XEMU_BOOT_VERIFIED');
  const files = {};
  const walk = directory => {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true }).sort((a,b) => a.name.localeCompare(b.name))) {
      const file = path.join(directory, entry.name);
      if (entry.isDirectory()) walk(file);
      else { assert(entry.isFile(), 'unexpected non-file'); files[path.relative(freeze, file)] = sha(file); }
    }
  };
  walk(freeze);
  const manifest = { scope: 'Immutable local Group 1 presentation integration evidence; not physical or full acceptance',
    algorithm: 'sha256', files };
  fs.writeFileSync(path.join(freeze, 'sha256.json'), `${JSON.stringify(manifest, null, 2)}\n`, { flag: 'wx' });
  const count = inputs(freeze, files);
  console.log(JSON.stringify({ result: 'PASS', frozenFiles: count, manifestSha256: sha(path.join(freeze, 'sha256.json')) }));
}
