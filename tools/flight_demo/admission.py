"""Admission for this fixed M1 development profile, not a configurable runtime."""
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def validate(data, root=ROOT):
    # These are explicit scope restrictions, not alternative runtime settings.
    fixed = {'identity': '65AERO-M1-DEV-2', 'tick_hz': 100, 'stages': 21,
             'queue_capacity': 8, 'snapshot_slots': 3, 'columns': 80, 'rows': 25,
             'render_rows_per_service': 1}
    for key, value in fixed.items():
        if type(data.get(key)) is not type(value) or data[key] != value:
            raise ValueError('Unsupported M1 profile: ' + key)
    header = (root / 'interfaces/generated/r0f_combined.h').read_text()
    retained = {k: int(v) for k, v in re.findall(r'^#define (R0FC_\w+) (\d+)u[l]?$', header, re.M)}
    memory = data['memory']
    # Existing CF001 range admission, ROM backup and one-byte bank switching
    # are intentionally fixed. Reject drift rather than changing retained code.
    expected = {
        'display_a': retained['R0FC_ROM'],
        'display_b': retained['R0FC_ROM'] + retained['R0FC_ROM_BYTES'] // 2,
        'color': retained['R0FC_COLOR'], 'rom_backup': retained['R0FC_BACKUP'],
        'rom_backup_bytes': retained['R0FC_ROM_BYTES'],
        'resident_start': 0x2001, 'resident_end_exclusive': 0x8000,
        'software_stack_start': 0xc000, 'software_stack_end_exclusive': 0xd000,
        'hardware_stack_start': 0x100, 'hardware_stack_end_exclusive': 0x200,
        'base_page_start': 0x200, 'base_page_end_exclusive': 0x300,
        'platform_result_start': retained['R0FC_RESULT'],
        'platform_result_end_exclusive': retained['R0FC_RESULT'] + retained['R0FC_RESULT_BYTES'],
        'reserve_start': retained['R0FC_RESERVE'],
        'reserve_end_exclusive': retained['R0FC_RESERVE'] + retained['R0FC_RESERVE_BYTES']}
    if memory != expected:
        raise ValueError('M1 allocation conflicts with admitted CF001/platform profile')
    init = data['inherited_initialization']
    source = root / init['source']
    if init['source'] != 'src/diagnostics/r0f/combined_platform.c' or hashlib.sha256(source.read_bytes()).hexdigest() != init['source_sha256']:
        raise ValueError('Retained initialization source changed; reinspection required')
    function = source.read_text().split('uint8_t cfrom_begin(void)', 1)[1].split('uint8_t cfrom_restore', 1)[0]
    row, message = re.search(r'cfline\((\d+)u,"([^"]+)"\)', function).groups()
    start = 0x800 + 80 * int(row)
    if init['start'] != start or init['end_exclusive'] != start + min(80, len(message)):
        raise ValueError('Retained startup screen write is not fully accounted')
    return data
