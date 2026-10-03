#include <stdint.h>
#include <string.h>

#include "group1_presentation.h"

// Foreground-only bounded policy. The future display owner must call complete
// only after pixel/DMA completion and apply the matching VIC store separately.
static uint8_t same_key(const r0fg1_presentation_key *first,
                        const r0fg1_presentation_key *second)
{
    return first->generation == second->generation
        && first->source_tick == second->source_tick
        && first->view == second->view && first->tier == second->tier
        && first->buffer == second->buffer;
}

static uint8_t editable(const r0fg1_presentation *state,
                        const r0fg1_presentation_key *key)
{
    return state->busy && !state->ready && same_key(&state->building.key, key);
}

void r0fg1_presentation_init(r0fg1_presentation *state)
{
    memset(state, 0, sizeof(*state));
}

uint8_t r0fg1_view_request(r0fg1_presentation *state, uint8_t view)
{
    if (view >= R0FG1P_VIEWS)
    {
        return 0u;
    }
    state->requested_view = view;
    return 1u;
}

uint8_t r0fg1_presentation_bind(r0fg1_presentation *state,
                               const r0fg1_presentation_key *key,
                               int16_t horizon)
{
    if (state->busy || key->generation == 0u || key->source_tick == 0u
        || key->view != state->requested_view || key->view >= R0FG1P_VIEWS
        || key->tier >= R0FG1P_TIERS || key->buffer >= R0FG1P_BUFFERS
        || (state->displayed_valid
            && (key->buffer == state->displayed.key.buffer
                || key->generation <= state->displayed.key.generation
                || key->source_tick < state->displayed.key.source_tick)))
    {
        return 0u;
    }
    state->building.key = *key;
    state->building.horizon = horizon;
    state->building.anchor_count = 0u;
    state->building.column_mask = 0u;
    state->building.column_count = 0u;
    state->busy = 1u;
    state->ready = 0u;
    return 1u;
}

uint8_t r0fg1_anchor_add(r0fg1_presentation *state,
                        const r0fg1_presentation_key *key,
                        const r0fg1_anchor *anchor)
{
    r0fg1_registration *work = &state->building;
    if (!editable(state, key) || anchor->priority >= R0FG1P_ANCHOR_PRIORITIES)
    {
        return R0FG1P_INVALID;
    }
    uint8_t position = 0u;
    for (uint8_t index = 0u; index < work->anchor_count; index++)
    {
        const r0fg1_anchor *existing = &work->anchors[index];
        if (existing->handle == anchor->handle)
        {
            return R0FG1P_INVALID;
        }
        if (existing->priority < anchor->priority
            || (existing->priority == anchor->priority
                && existing->handle < anchor->handle))
        {
            position++;
        }
    }
    if (work->anchor_count == R0FG1P_ANCHORS)
    {
        if (state->anchor_drops == UINT16_MAX)
        {
            return R0FG1P_INVALID;
        }
        state->anchor_drops++;
        if (position == R0FG1P_ANCHORS)
        {
            return R0FG1P_DROPPED;
        }
    }
    else
    {
        work->anchor_count++;
        if (work->anchor_count > state->anchor_high)
        {
            state->anchor_high = work->anchor_count;
        }
    }
    for (uint8_t index = (uint8_t)(work->anchor_count - 1u);
         index > position; index--)
    {
        work->anchors[index] = work->anchors[index - 1u];
    }
    work->anchors[position] = *anchor;
    return R0FG1P_RETAINED;
}

uint8_t r0fg1_occlusion_column(r0fg1_presentation *state,
                              const r0fg1_presentation_key *key,
                              uint8_t column, uint16_t ridge_y,
                              uint16_t ridge_depth)
{
    if (!editable(state, key) || column >= R0FG1P_OCCLUSION_COLUMNS)
    {
        return 0u;
    }
    r0fg1_registration *work = &state->building;
    uint8_t bit = (uint8_t)(1u << column);
    if (!(work->column_mask & bit))
    {
        work->column_count++;
        if (work->column_count > state->occlusion_high)
        {
            state->occlusion_high = work->column_count;
        }
    }
    work->column_mask |= bit;
    work->terrain_y[column] = ridge_y;
    work->terrain_depth[column] = ridge_depth;
    return 1u;
}

uint8_t r0fg1_occlusion_clip(const r0fg1_presentation *state,
                            const r0fg1_presentation_key *key, uint8_t column,
                            uint16_t depth, uint16_t top, uint16_t bottom,
                            uint16_t *visible_bottom)
{
    if (!editable(state, key) || column >= R0FG1P_OCCLUSION_COLUMNS
        || !(state->building.column_mask & (uint8_t)(1u << column))
        || top > bottom)
    {
        return R0FG1P_INVALID;
    }
    uint16_t ridge = state->building.terrain_y[column];
    if (depth > state->building.terrain_depth[column] && bottom >= ridge)
    {
        if (top >= ridge)
        {
            return R0FG1P_HIDDEN;
        }
        *visible_bottom = (uint16_t)(ridge - 1u);
        return R0FG1P_CLIPPED;
    }
    *visible_bottom = bottom;
    return R0FG1P_UNCLIPPED;
}

uint8_t r0fg1_presentation_complete(r0fg1_presentation *state,
                                   const r0fg1_presentation_key *key,
                                   uint8_t buffer_complete)
{
    if (!editable(state, key) || buffer_complete != 1u
        || state->building.column_mask != R0FG1P_OCCLUSION_MASK
        || state->completions == UINT16_MAX)
    {
        return 0u;
    }
    state->ready = 1u;
    state->completions++;
    return 1u;
}

uint8_t r0fg1_presentation_swap(r0fg1_presentation *state)
{
    if (!state->busy || !state->ready || state->swaps == UINT16_MAX
        || state->building.key.view != state->requested_view)
    {
        return 0u;
    }
    // One owner, no interrupt readers: logical publication, not an assertion
    // that this C structure assignment is instruction-atomic on 45GS02.
    state->displayed = state->building;
    state->composition_view = state->displayed.key.view;
    state->displayed_valid = 1u;
    state->busy = 0u;
    state->ready = 0u;
    state->swaps++;
    return 1u;
}

void r0fg1_presentation_cancel(r0fg1_presentation *state)
{
    state->busy = 0u;
    state->ready = 0u;
}

// Pinned MOS inlining miscompiles the zero-size exit path: STZ followed by
// BNE reuses NZ from LDX #1. Keep this pure boundary out of that caller fold.
__attribute__((noinline))
uint8_t r0fg1_lod_select(uint8_t previous_tier, uint16_t pixels)
{
    if (previous_tier >= R0FG1P_TIERS)
    {
        return R0FG1P_INVALID_TIER;
    }
    if (pixels >= R0FG1P_LOD_ENTER_PIXELS)
    {
        return 1u;
    }
    if (pixels <= R0FG1P_LOD_EXIT_PIXELS)
    {
        return 0u;
    }
    return previous_tier;
}
