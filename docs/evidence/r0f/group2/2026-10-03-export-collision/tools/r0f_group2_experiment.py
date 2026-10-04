"""Fresh copied-source Group 2 experiments; shared hash, command and fit gates."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from r0f_group2_target_admission import ROOT, section_inventory, sha


def verify_inputs(source, inputs):
    for name, digest in inputs.items():
        if sha(source / name) != digest:
            raise ValueError('Source identity mismatch: ' + name)


class Experiment:
    def __init__(self, baseline, name):
        self.baseline_path = Path(baseline)
        self.baseline = json.loads((self.baseline_path / 'result.json').read_text())
        self.original = self.baseline_path / 'source-inputs'
        verify_inputs(self.original, self.baseline['inputs'])
        parent = ROOT / 'build/r0f/group2' / name
        parent.mkdir(parents=True, exist_ok=True)
        self.out = Path(tempfile.mkdtemp(prefix='trial-', dir=parent))
        self.source = self.out / 'source-inputs'
        shutil.copytree(self.original, self.source)
        self.report = {'result': 'FAIL', 'baseline': str(self.baseline_path),
                       'commands': [], 'targetExecuted': False, 'carrier': 'NOT BUILT'}

    def run(self, label, command, timeout=60):
        result = subprocess.run(command, cwd=self.source, capture_output=True,
                                text=True, timeout=timeout)
        (self.out / (label + '.txt')).write_text(result.stdout + result.stderr)
        self.report['commands'].append({'command': command, 'exitCode': result.returncode})
        result.check_returncode()

    def fit(self, extra_sources=(), excluded_sources=()):
        command = next(c['command'].copy() for c in self.baseline['commands']
                       if 'mos-mega65-clang' in c['command'][0])
        for name in excluded_sources:
            if command.count(name) != 1:
                raise ValueError('Excluded source missing or ambiguous: ' + name)
            command.remove(name)
        self.report['excludedSources'] = list(excluded_sources)
        compiler = Path(command[0])
        lock = json.loads((ROOT / 'toolchain/f65_toolchain.lock.json').read_text())
        if sha(compiler) != lock['llvm_mos']['compiler_sha256']:
            raise ValueError('Compiler identity mismatch')
        prg, mapping = self.out / 'CANDIDATE.prg', self.out / 'CANDIDATE.map'
        command[command.index('-o') + 1] = str(prg)
        command = ['-Wl,-Map,' + str(mapping) if c.startswith('-Wl,-Map,') else c
                   for c in command] + list(extra_sources)
        self.run('target-compile', command)
        sections = section_inventory(mapping.read_text())
        end = max(sections[k]['start'] + sections[k]['bytes'] for k in
                  ('.r0fs_protected', '.text', '.rodata', '.data', '.bss', '.noinit'))
        self.report.update(sections=sections, residentEndExclusive=end,
                           residentFreeBytes=0xc000-end,
                           addedBytes=end-self.baseline['residentEndExclusive'],
                           prgSha256=sha(prg))
        self.run('sizes', [str(compiler.parent / 'llvm-nm'), '--print-size',
                          '--size-sort', str(prg) + '.elf'])
        if sections['.r0fs_protected'] != self.baseline['sections']['.r0fs_protected']:
            raise ValueError('Protected region changed')
        self.report['result'] = 'FIT_PASS_NOT_EXECUTABLE' if end <= 0xc000 else 'FIT_FAIL'

    def finish(self, allowed_changes):
        self.report['inputs'] = {str(p.relative_to(self.source)): sha(p)
                                for p in sorted(self.source.rglob('*')) if p.is_file()}
        self.report['changedInputs'] = [k for k,v in self.report['inputs'].items()
                                       if self.baseline['inputs'].get(k) != v]
        verify_inputs(self.original, self.baseline['inputs'])
        self.report['baselineUnchanged'] = True
        if set(self.report['changedInputs']) != set(allowed_changes):
            self.report.update(result='FAIL', error='Unexpected changed inputs')
        (self.out / 'result.json').write_text(json.dumps(self.report, indent=2) + '\n')
        print(json.dumps({k: self.report.get(k) for k in
                         ('result', 'residentFreeBytes', 'addedBytes', 'error')}))
        print(self.out)
