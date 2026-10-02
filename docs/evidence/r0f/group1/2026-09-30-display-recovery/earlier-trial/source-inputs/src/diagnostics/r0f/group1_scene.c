#include "group1_scene.h"
#include "group1_geometry_fixture.h"

static void put16(uint8_t *bytes, uint16_t value)
{
    bytes[0] = (uint8_t)value;
    bytes[1] = (uint8_t)(value >> 8u);
}

uint8_t r0fg1_scene_bind(r0fg1_presentation *state, uint16_t source_tick,
                        uint8_t buffer)
{
    r0fg1_presentation_key key;
    key.generation = (uint16_t)(state->swaps + 1u);
    key.source_tick = source_tick;
    key.view = state->requested_view;
    key.tier = r0fg1_lod_select(state->displayed_valid
        ? state->displayed.key.tier : 0u,
        (uint16_t)(8u + 2u * (source_tick & 3u)));
    key.buffer = buffer;
    return r0fg1_presentation_bind(state, &key,
                                   (int16_t)(40u + (source_tick & 3u)));
}

uint8_t r0fg1_scene_encode(r0fg1_presentation *state,
                          uint8_t pixels[R0FG1P_SCENE_BYTES])
{
    static const uint8_t priorities[R0FG1P_SCENE_CANDIDATES] = {
        3u, 2u, 1u, 1u, 0u, 0u,
    };
    const r0fg1_presentation_key *key = &state->building.key;
    uint8_t clip_codes = 0u;
    for (uint8_t index = 0u; index < R0FG1P_SCENE_CANDIDATES; index++)
    {
        r0fg1_anchor anchor;
        anchor.handle = index;
        anchor.x = (uint16_t)((key->source_tick & 63u) + index);
        anchor.y = (uint16_t)(20u + index);
        anchor.priority = priorities[index];
        if (r0fg1_anchor_add(state, key, &anchor) == R0FG1P_INVALID)
        {
            return 0u;
        }
    }
    for (uint8_t column = 0u; column < R0FG1P_OCCLUSION_COLUMNS; column++)
    {
        uint16_t depth = (uint16_t)(100u + column);
        uint16_t bottom = UINT16_MAX;
        if (!r0fg1_occlusion_column(state, key, column,
                (uint16_t)state->building.horizon, depth))
        {
            return 0u;
        }
        uint8_t code = r0fg1_occlusion_clip(state, key, column,
            column == 0u ? (uint16_t)(depth - 1u) : (uint16_t)(depth + 1u),
            column == 2u ? 50u : 10u, column == 3u ? 20u : 60u, &bottom);
        if (code == R0FG1P_INVALID)
        {
            return 0u;
        }
        put16(pixels + R0FG1P_S_VISIBLE_BOTTOMS + column * 2u, bottom);
        clip_codes |= (uint8_t)(code << (column * 2u));
    }
    const r0fg1_registration *work = &state->building;
    put16(pixels + R0FG1P_S_GENERATION, key->generation);
    put16(pixels + R0FG1P_S_SOURCE_TICK, key->source_tick);
    pixels[R0FG1P_S_VIEW] = key->view;
    pixels[R0FG1P_S_TIER] = key->tier;
    pixels[R0FG1P_S_BUFFER] = key->buffer;
    put16(pixels + R0FG1P_S_HORIZON, (uint16_t)work->horizon);
    pixels[R0FG1P_S_ANCHOR_COUNT] = work->anchor_count;
    for (uint8_t index = 0u; index < R0FG1P_ANCHORS; index++)
    {
        uint8_t *bytes = pixels + R0FG1P_S_ANCHORS
            + index * R0FG1P_ANCHOR_BYTES;
        const r0fg1_anchor *anchor = &work->anchors[index];
        put16(bytes, anchor->handle);
        put16(bytes + 2u, anchor->x);
        put16(bytes + 4u, anchor->y);
        bytes[6] = anchor->priority;
    }
    for (uint8_t column = 0u; column < R0FG1P_OCCLUSION_COLUMNS; column++)
    {
        uint8_t *bytes = pixels + R0FG1P_S_COLUMNS
            + column * R0FG1P_COLUMN_BYTES;
        put16(bytes, work->terrain_y[column]);
        put16(bytes + 2u, work->terrain_depth[column]);
    }
    pixels[R0FG1P_S_COLUMN_MASK] = work->column_mask;
    pixels[R0FG1P_S_COLUMN_COUNT] = work->column_count;
    pixels[R0FG1P_S_CLIP_CODES] = clip_codes;
    uint32_t geometry_crc = r0fg1_geometry_fixture(key->generation, key->source_tick);
    for (uint8_t index = 0u; index < 4u; index++)
    {
        pixels[R0FG1P_S_GEOMETRY_CRC + index] = (uint8_t)geometry_crc;
        geometry_crc >>= 8u;
    }
    return 1u;
}
