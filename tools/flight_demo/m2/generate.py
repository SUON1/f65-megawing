"""Generate fixed, development-only M2 math contracts; no M1 writes."""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
# Admission binds the reviewed authoring source; edits require explicit re-admission.
APPROVED_SHA = '4832867688dc11c98cf816ae00254778f82a69dfb2b13af0e63d5db7ce36cda6'


def generate(root=ROOT, destination=None):
    source = root / 'interfaces/m2_pr1.json'
    raw = source.read_bytes()
    if hashlib.sha256(raw).hexdigest() != APPROVED_SHA:
        raise ValueError('M2 source differs from the admitted PR1 profile')
    data = json.loads(raw)
    dest = destination or root
    header = ['// Generated M2 PR1 development records; not a production ABI.',
              '#pragma once', '#include <stdint.h>', '// Source SHA256: ' + APPROVED_SHA]
    for k, v in data['constants'].items():
        header.append(f"#define M2_{k.upper()} ({v}{'LL' if abs(v) > 2147483647 else 'L'})")
    divisor = math.gcd(data['constants']['height'], 2 * data['constants']['focal'])
    header += [f"#define M2_VERTICAL_NUM ({data['constants']['height'] // divisor}L)",
               f"#define M2_VERTICAL_DEN ({2 * data['constants']['focal'] // divisor}L)"]
    for name, fields in data['records'].items():
        header += ['typedef struct', '{']
        header += [f'    {kind} {name};' for name, kind in fields]
        header += [f'}} {name};']
    header += ['extern const int64_t m2_sine_q46[91];']
    table = ['// Generated integer-degree rotation coefficients.', '#include "m2_pr1.h"',
             'const int64_t m2_sine_q46[91] =', '{']
    values = [round(math.sin(math.radians(i)) * data['constants']['rotation_scale']) for i in range(91)]
    for i in range(0, 91, 6):
        table.append('    ' + ', '.join(str(v) + 'LL' for v in values[i:i+6]) + ',')
    table += ['};']
    ledger = {'identity': data['identity'], 'source_sha256': APPROVED_SHA,
              'ranges': data['memory'], 'physical_allocations': [], 'dma_lists': [],
              'reserve_allocation': 0, 'status': 'compile/link-only PR1; no target execution',
              'owners': {'fixture': 'Environment', 'transform_clipping_registration': 'Graphics',
                         'camera': 'caller-owned diagnostic presentation state'},
              'runtime_abi_admission': 'NONE: SDK-linked compile-only probe, logical rc0..rc31 at $0002..$0021; no executed B/MAP contract. The base-page range is reserved for later reviewed integration, not used or tested here.',
              'numeric': 'public positions signed Q12 feet; private clipping signed Q24 feet; rotations signed Q46; screen signed Q16 pixels; widened int64 intermediates',
              'stack': 'no recursion or dynamic allocation; static compiler accounting in build evidence; no exercised target high-water'}
    for path, text in [('interfaces/generated/m2_pr1.h', '\n'.join(header)+'\n'),
                       ('interfaces/generated/m2_tables.c', '\n'.join(table)+'\n'),
                       ('memory/m2-pr1-ledger.json', json.dumps(ledger, indent=2)+'\n')]:
        p = dest / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    return data


if __name__ == '__main__':
    generate()
