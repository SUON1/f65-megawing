"""Generate the isolated M1 development records and allocation ledger."""
import hashlib
import json
from admission import validate
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def generate():
    source = ROOT / 'interfaces/m1_development.json'
    data = validate(json.loads(source.read_text()), ROOT)
    header = ['// Generated from interfaces/m1_development.json; do not edit.',
              '#pragma once', '#include <stdint.h>',
              '// Source SHA-256: ' + hashlib.sha256(source.read_bytes()).hexdigest()]
    for key, value in data.items():
        if isinstance(value, int):
            header.append(f'#define M1_{key.upper()} {value}u')
    for key, value in data['memory'].items():
        header.append(f'#define M1_{key.upper()} {value}ul')
    for name, fields in data['records'].items():
        header += ['typedef struct', '{']
        header += [f'    {kind} {field};' for field, kind in fields]
        header += [f'}} {name};']
    (ROOT / 'interfaces/generated/m1_development.h').write_text('\n'.join(header) + '\n')
    memory = data['memory']
    ledger = {'identity': data['identity'], 'status': 'development allocation; actual linked sizes in build report',
              'ranges': data['memory'], 'display_bytes_each': data['columns'] * data['rows'],
              'hardware_stack': [memory['hardware_stack_start'], memory['hardware_stack_end_exclusive']],
              'base_page': [memory['base_page_start'], memory['base_page_end_exclusive']],
              'proof_platform_result': [memory['platform_result_start'], memory['platform_result_end_exclusive']],
              'reserve_allocation': 0,
              'inherited_initialization': data['inherited_initialization'],
              'owners': data['owners'],
              'dma_lists': [],
              'state': 'Core/input/snapshot/render owner objects linked in resident bank 0; charged by symbols, not full production state',
              'stack': str(memory['software_stack_end_exclusive'] - memory['software_stack_start']) + '-byte software envelope; dynamic high-water required, not inferred from allocation'}
    (ROOT / 'memory/m1-development-ledger.json').write_text(json.dumps(ledger, indent=2) + '\n')


if __name__ == '__main__':
    generate()
