import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';

const root = '/Users/slice/Developer/f65-megawing';
const evidence = path.join(root, 'docs/evidence/r0f/group1');
const output = path.join(evidence, '2026-09-30-pool-core');
const qualification = path.join(root, 'build/r0f/group1/pool-core');
assert(!fs.existsSync(path.join(output, 'sha256.json')), 'never modify an existing freeze');
const read = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const check = (file, digest) => assert.equal(sha(file), digest, file);
const copy = (file, destination) => {
  assert(destination.startsWith(`${output}/`));
  fs.mkdirSync(path.dirname(destination), { recursive: true });
  fs.cpSync(file, destination, { recursive: true,
    filter: file => path.basename(file) !== '__pycache__' && !file.endsWith('.pyc') });
};
const audited = [];
for (const name of ['2026-09-30-six-order-corrected-ntsc', '2026-09-30-six-order-ntsc-120s',
  '2026-09-30-six-order-pal-120s', '2026-09-30-presentation-core', '2026-09-30-presentation-integration']) {
  const directory = path.join(evidence, name);
  const manifest = read(path.join(directory, 'sha256.json'));
  for (const [file, digest] of Object.entries(manifest.files)) check(path.join(directory, file), digest);
  audited.push({ freeze: name, verifiedFiles: Object.keys(manifest.files).length,
    manifestSha256: sha(path.join(directory, 'sha256.json')) });
}
assert.equal(audited.reduce((total, item) => total + item.verifiedFiles, 0), 1637);
const base = read(path.join(root, 'build/r0f/group1/integration/build.json'));
const gate = read(path.join(root, 'build/r0f/group1/carriers/R0FG1P02/canonical/host-gate.json'));
check(path.join(root, 'build/r0f/group1/integration/GROUP1.prg'), base.prgSha256);
for (const [file, digest] of Object.entries(gate.inputs)) check(path.join(root, file), digest);
assert.equal(Object.keys(base.inputs).length, 93);
assert.equal(Object.keys(gate.inputs).length, 95);
assert.equal(gate.D81_STATE, 'XEMU_BOOT_VERIFIED');
check(path.join(root, 'build/r0f/group1/carriers/R0FG1P02/canonical/R0FG1P02.D81'), gate.D81_SHA256);
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
for (const [file, digest] of Object.entries(baselines)) check(path.join(root, file), digest);
const retired = read(path.join(root, 'build/r0f/group1/carriers/R0FG1P01/retirement.json'));
check(path.join(root, 'build/r0f/group1/carriers/R0FG1P01/canonical/R0FG1P01.D81'), retired.canonicalSha256);
check(path.join(root, 'build/r0f/group1/carriers/R0FG1P01/ntsc-01/R0FG1P01.D81'), retired.postRunSha256);
const qualified = read(path.join(qualification, 'validation.json'));
const fit = read(path.join(qualification, 'admission-probe-01/fit.json'));
assert.equal(qualified.result, 'PASS');
assert.equal(fit.fit, 'FAIL');
assert.equal(fit.residentEndExclusive, 0xc272);
assert.equal(fit.overflowBytes, 626);
assert.equal(fit.executed, false);
assert.equal(fit.admitted, false);
copy(qualification, path.join(output, 'qualification'));
for (const [file, digest] of Object.entries(fit.inputs)) {
  check(path.join(root, file), digest);
  copy(path.join(root, file), path.join(output, 'source-inputs', file));
}
const authority = ['AGENTS.md', 'CURRENT_STATE.md', 'WORK_IN_PROGRESS.md',
  'docs/DEVELOPMENT_WORKFLOW.md', 'docs/PROGRAMMING_PRINCIPLES.md', 'docs/CODE_STYLE_C.md',
  'docs/plans/R0-F_GROUP1_BUILD_INTENT.md', 'docs/plans/R0-F_GROUP1_MEASUREMENT_MATRIX.md',
  'docs/reports/R0-F_GROUP1_POOL_OBSERVATION_CORE.md', 'interfaces/r0f_successor_contract.json',
  'interfaces/r0f_successor_integration_contract.json', 'memory/r0f-successor-memory-ledger.json',
  'memory/r0f-successor-integration-memory-ledger.json', 'spec/manifests/spec-corpus.json'];
for (const file of authority) copy(path.join(root, file), path.join(output, 'authority-checkpoint', file));
const pdfs = ['spec/core/F65_65Aero_Engine_Runtime_and_Technical_Supplement_v1_HUMAN_APPROVED_CANDIDATE_DESIGN.pdf',
  'spec/subsystems/F-65_Megawing_Graphics_White_Paper_v2.1.pdf',
  'spec/subsystems/F-65_Megawing_Audio_Sound_Effects_and_Music_Engineering_White_Paper_v1.0_FINAL.pdf',
  'spec/subsystems/F-65_Megawing_SensorAndTrackEngine_Engineering_Model_Phase-3_v1.0.pdf'];
const pdfIdentities = Object.fromEntries(pdfs.map(file => [file, sha(path.join(root,file))]));
const commands = [];
for (const args of [['git', 'diff', '--check'], ['python3', '-B', '-m', 'unittest', 'discover',
  '-s', 'tools/diagnostics', '-p', 'test_r0f_group1_*.py', '-v']]) {
  const result = spawnSync(args[0], args.slice(1), { cwd: root, encoding: 'utf8', timeout: 60000 });
  assert.equal(result.status, 0, result.stderr);
  commands.push({ command: args, exitCode: result.status, stdout: result.stdout, stderr: result.stderr });
}
assert.match(commands.at(-1).stderr, /Ran 35 tests/);
const validation = { result: 'PASS_HOST_OBJECT_AND_PRESERVATION', sourceCommit: '9e2ffdb4786e4794119933a5edd4b1cf79f653f0',
  sourceBranch: 'codex/r0f-successor-physical-exact-carrier', dirtyTree: true,
  qualification: qualified, fitProbe: { fit: fit.fit, overflowBytes: fit.overflowBytes,
    admitted: false, executed: false, prgSha256: fit.prgSha256 }, commands,
  preservedPrgSha256: base.prgSha256, preservedInputs: 93, canonicalState: gate.D81_STATE,
  canonicalSha256: gate.D81_SHA256, baselines, priorManifests: audited, governingPdfs: pdfIdentities,
  newXemu: 'NOT RUN', newCarrier: 'NOT RUN', sd: 'NOT RUN', physical: 'NOT RUN',
  commit: 'NOT RUN', push: 'NOT RUN', integratedPoolEvidence: false,
  targetFitAdmitted: false, fullGroup1Acceptance: false, fullR0FAcceptance: false };
fs.writeFileSync(path.join(output, 'validation.json'), `${JSON.stringify(validation,null,2)}\n`, {flag:'wx'});
copy(path.join(root, 'build/r0f/group1/freeze-pool-evidence.mjs'), path.join(output, 'final-audit/freeze-pool-evidence.mjs'));
const files = {};
const walk = directory => {
  for (const entry of fs.readdirSync(directory, {withFileTypes:true}).sort((a,b)=>a.name.localeCompare(b.name))) {
    const file = path.join(directory,entry.name);
    if (entry.isDirectory()) walk(file);
    else { assert(entry.isFile()); files[path.relative(output,file)] = sha(file); }
  }
};
walk(output);
fs.writeFileSync(path.join(output,'sha256.json'), `${JSON.stringify({scope:'Isolated pool observation preparation; integration not admitted',algorithm:'sha256',files},null,2)}\n`, {flag:'wx'});
for(const [file,digest] of Object.entries(files)) check(path.join(output,file),digest);
console.log(JSON.stringify({result:'PASS',frozenFiles:Object.keys(files).length,priorFilesVerified:1637,
  preservedPrgSha256:base.prgSha256,fit:'FAIL',overflowBytes:626}));
