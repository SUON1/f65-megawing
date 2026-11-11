"""Read-only cost gate and independent display-address reconstruction."""
import argparse
import json
from pathlib import Path
import re

from service_admission import verify_seal
from service_costs import Costs


WIDTH = 320
HEIGHT = 200
WORLD_CELLS = 640
COLUMNS = 40
MAP_BYTES = 2000
TILE_BYTES = 64
DYNAMIC = 0x0800
SOLID = 0xa800
GLYPH = 0xa880
BLANK = 0xf800
FOOTER_CELL = 960
STORE_BYTES = 63552


def tiles(pixels):
    return [bytes(pixels[y * WIDTH + x + dx + dy * WIDTH]
                  for dy in range(8) for dx in range(8))
            for y in range(0, HEIGHT, 8) for x in range(0, WIDTH, 8)]


def glyphs(source):
    data = source.split('static const uint8_t rows[][7] = {', 1)[1].split('};', 1)[0]
    rows = [list(map(int, re.findall(r'\d+', entry))) for entry in re.findall(r'\{([^}]+)\}', data)]
    if len(rows) != 41 or any(len(glyph) != 7 for glyph in rows) or any(rows[0]):
        raise ValueError('linked font source shape changed')
    output = {}
    for index, glyph in enumerate(rows[1:]):
        pixels = bytearray([1] * TILE_BYTES)
        for y, row in enumerate(glyph):
            for x in range(5):
                if row & (16 >> x):
                    pixels[8 * y + x + 1] = 4
        output[GLYPH + index * TILE_BYTES] = bytes(pixels)
    return output


def construct(base, source_tiles, library):
    store = bytearray(STORE_BYTES)
    for offset, content in library.items():
        store[offset:offset + TILE_BYTES] = content
    lookup = {content: offset for offset, content in library.items()}
    written = set()
    for cell, content in enumerate(source_tiles):
        if content in lookup:
            offset = lookup[content]
        elif cell < WORLD_CELLS:
            offset = DYNAMIC + cell * TILE_BYTES
            store[offset:offset + TILE_BYTES] = content
            written.add(offset)
        else:
            raise ValueError('telemetry glyph or footer has no exact immutable tile')
        if (cell >= FOOTER_CELL and offset != BLANK) or offset >= STORE_BYTES or offset % TILE_BYTES:
            raise ValueError('invalid local reference')
        char_id = (base + offset) // TILE_BYTES
        if char_id & ~0x1fff:
            raise ValueError('tile ID overlaps VIC-IV trim bits')
        store[2 * cell:2 * cell + 2] = char_id.to_bytes(2, 'little')
    return store, written


def reconstruct(base, store):
    """Independent scanout address calculation from the two bytes in each cell."""
    pixels = bytearray(WIDTH * HEIGHT)
    for cell in range(1000):
        lo, hi = store[2 * cell:2 * cell + 2]
        address = (lo + (hi & 31) * 256) << 6
        if hi & 224 or not base <= address < base + STORE_BYTES:
            raise ValueError('trim bits or cross-store reference')
        source = address - base
        x, y = cell % COLUMNS * 8, cell // COLUMNS * 8
        for row in range(8):
            start = (y + row) * WIDTH + x
            pixels[start:start + 8] = store[source + 8 * row:source + 8 * row + 8]
    return pixels


def estimate(root, references):
    packet = root / 'docs/evidence/flight-demo/2026-11-08-m2-bounded-service'
    verify_seal(packet / 'seal.json')
    host = next(packet.glob('host-*/host-frame.indices'))
    pixels = host.read_bytes()
    if len(pixels) != WIDTH * HEIGHT or not set(pixels) <= {1, 2, 3, 4}:
        raise ValueError('sealed host image changed')
    source_tiles = tiles(pixels)
    library = glyphs((root / 'src/graphics/m2_rebuild_text.c').read_text())
    library.update({BLANK: b'\x01' * TILE_BYTES, SOLID: b'\x02' * TILE_BYTES,
                    SOLID + TILE_BYTES: b'\x03' * TILE_BYTES})
    references_checked = {}
    for base in (0x20000, 0x30000):
        store, written = construct(base, source_tiles, library)
        if reconstruct(base, store) != pixels:
            raise ValueError('screen-map reconstruction differs from sealed reference')
        references_checked[hex(base)] = len(written)
    if set(references_checked.values()) != {48}:
        raise ValueError('default dynamic tile count changed')
    target = packet / 'target'
    model = Costs((target / 'UNADMITTED.prg').read_bytes(), (target / 'UNADMITTED.disassembly').read_text(),
                  (target / 'UNADMITTED.symbols').read_text(),
                  (references / 'xemu/cpu65_mega65_timings.h').read_bytes())
    delta_byte = model.minimum(0x269a, end=0x26d3)
    multiply_cell = model.minimum(0x29ce, end=0x2a19)
    body = sum(model.cycles(address) for address in model.instructions if 0x2c83 <= address <= 0x2ca2)
    div_bit = 7 * body
    qualified = json.loads((packet / 'qualification/result.json').read_text())['service']
    roles = qualified['roles']
    delta_calls = 9 * 2 * 3 * 3  # segments, endpoints, matrix rows and axes
    multiplications = 1290 * 6  # sealed host multiplication rows and six cells per row
    division_bits = qualified['division']['required_bits']
    arithmetic_only = delta_calls * 12 * 8 * delta_byte + multiplications * multiply_cell + division_bits * div_bit
    full_budget = qualified['maximum_frame_cycles_at_20hz']
    # The linked main calls exactly one input sample immediately before each
    # tick. It can enqueue only for that release. Stage 3 drains it before the
    # next sample. No handler or renderer path enqueues commands.
    tick = model.names['m1_tick']
    tick_core = model.upper(tick, loop_cap=2 * 21 + 4)
    terminals = {a for a in model.instructions if model.callee(a) == model.names['stop']}
    remaining_tick = model.upper(0x771e, omit_calls=frozenset({tick}),
                                 stop_at=frozenset(terminals | {0x7653}))
    overhead = qualified['batch_upper']
    tick_iteration = (tick_core + remaining_tick
                      + overhead['scheduler_cycles_including_clock_guard_dispatch_jsr']
                      + overhead['two_raster_irqs_and_one_nmi_cycles'])
    worst_tiles = min(WORLD_CELLS, 55 + 9 * 55)
    display_cycles = qualified['copy']['cycles_per_byte_minimum']
    return {
        'status': 'BLOCKED at integrated cost-estimate gate',
        'scope': 'read-only calculations and host representation model on the sealed default frame',
        'baseline_prg_sha256': json.loads((target / 'result.json').read_text())['prg']['sha256'],
        'target_executed': False, 'default_exact_reconstruction': references_checked,
        'display': {'map_bytes': MAP_BYTES, 'existing_reserved_bank_bytes_each': 65536,
                    'existing_used_extent_each': STORE_BYTES, 'dynamic_allocated_slots': WORLD_CELLS,
                    'affine_boundary_and_monotone_raster_demand_bound': worst_tiles,
                    'immutable_tiles_including_footer': len(library), 'additional_bitmap_bytes': 80,
                    'default_copied_bytes_using_existing_line_path': MAP_BYTES + 48 * TILE_BYTES + 96,
                    'default_copy_body_cycles_minimum': (MAP_BYTES + 48 * TILE_BYTES + 96) * display_cycles,
                    'conservative_copy_only_cardinality': MAP_BYTES + worst_tiles * TILE_BYTES + 9 * WIDTH,
                    'cost_boundary': 'per-byte cost is a lower bound; worst demand is an upper bound; their product is a sizing scenario, not observed cycles or a proved violation'},
        'numeric': {'mandatory_delta_calls': delta_calls, 'minimum_delta_byte_cycles': delta_byte,
                    'minimum_delta_body_cycles': delta_calls * 12 * 8 * delta_byte,
                    'mandatory_product_cells': multiplications, 'minimum_product_cell_cycles': multiply_cell,
                    'minimum_multiplication_cell_cycles': multiplications * multiply_cell,
                    'mandatory_division_bits': division_bits, 'minimum_division_bit_cycles': div_bit,
                    'minimum_division_shift_cycles': division_bits * div_bit,
                    'disjoint_arithmetic_body_minimum': arithmetic_only,
                    'previous_prepare_project_and_divider_minimum': roles['prepare']['minimum_total_cycles_excluding_separate_loops'] + roles['project']['minimum_total_cycles_excluding_separate_loops'] + division_bits * div_bit,
                    'normalized_division_structural_bit_bound': 7650,
                    'normalized_shift_only_budget_at_structural_bound': 7650 * div_bit},
        'integrated': {'frame_allowance_cycles': full_budget,
                       'previous_frame_minimum_cycles': qualified['minimum_complete_frame_cycles'],
                       'planning_allocation_cycles': {'exact_numerics': 800000, 'display_all_roles': 925000,
                                                      'five_ticks_and_scheduler': 300000},
                       'allocation_status': 'UNPROVEN for moving/cold, commit wait and exact five-tick bound',
                       'prior_tick_envelope_cycles': overhead['tick_iteration_upper_including_clock_and_interrupts'],
                       'restricted_queue_tick_envelope_cycles': tick_iteration,
                       'tick_limit_cycles': qualified['maximum_tick_cycles_at_100hz'],
                       'remaining_resident_before_code_after_bitmap': 656 - 80,
                       'actual_candidate_link': 'NOT BUILT; integrated estimate did not clear',
                       'same_camera_cache': 'Only a hit under the complete camera, fixture and numerical contract identity. Cold and changed poses still need the exact full computation.'},
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--references', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(estimate(Path(__file__).resolve().parents[3], args.references), indent=2))
