#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "group1_presentation.h"

static uint32_t permutations;
static uint32_t clipping_cases;

static void envelope(r0fg1_presentation *state,
                      const r0fg1_presentation_key *key)
{
    for (uint8_t column = 0u; column < R0FG1P_OCCLUSION_COLUMNS; column++)
    {
        assert(r0fg1_occlusion_column(state, key, column, 4u, 1u));
    }
}

static void test_coherence(void)
{
    r0fg1_presentation state;
    r0fg1_presentation_init(&state);
    r0fg1_presentation_key key = {1u, 10u, 0u, 0u, 0u};
    r0fg1_anchor cue = {50u, 12u, 3u, 0u};
    assert(!r0fg1_view_request(&state, R0FG1P_VIEWS));
    assert(r0fg1_presentation_bind(&state, &key, -3));
    assert(!r0fg1_presentation_bind(&state, &key, -3));
    assert(!r0fg1_presentation_swap(&state));
    assert(!r0fg1_presentation_complete(&state, &key, 1u));
    assert(!r0fg1_occlusion_column(&state, &key,
                                  R0FG1P_OCCLUSION_COLUMNS, 4u, 1u));
    envelope(&state, &key);
    assert(state.occlusion_high == R0FG1P_OCCLUSION_COLUMNS);
    envelope(&state, &key);
    assert(state.building.column_count == R0FG1P_OCCLUSION_COLUMNS);
    assert(r0fg1_anchor_add(&state, &key, &cue) == R0FG1P_RETAINED);
    assert(!r0fg1_presentation_complete(&state, &key, 0u));
    assert(!r0fg1_presentation_complete(&state, &key, 2u));

    for (uint8_t field = 0u; field < 5u; field++)
    {
        r0fg1_presentation_key wrong = key;
        r0fg1_anchor other_cue = {51u, 13u, 3u, 0u};
        switch (field)
        {
            case 0u:
                wrong.generation++;
                break;
            case 1u:
                wrong.source_tick++;
                break;
            case 2u:
                wrong.view++;
                break;
            case 3u:
                wrong.tier++;
                break;
            default:
                wrong.buffer++;
                break;
        }
        uint16_t bottom = 999u;
        assert(!r0fg1_presentation_complete(&state, &wrong, 1u));
        assert(!r0fg1_anchor_add(&state, &wrong, &other_cue));
        assert(!r0fg1_occlusion_column(&state, &wrong, 0u, 4u, 1u));
        assert(!r0fg1_occlusion_clip(&state, &wrong, 0u, 2u, 0u, 7u, &bottom));
        assert(bottom == 999u);
    }
    assert(r0fg1_presentation_complete(&state, &key, 1u));
    assert(!r0fg1_occlusion_column(&state, &key, 0u, 7u, 1u));
    assert(!r0fg1_anchor_add(&state, &key, &cue));
    assert(r0fg1_view_request(&state, 1u));
    assert(!r0fg1_presentation_swap(&state));
    assert(!state.displayed_valid);
    assert(r0fg1_view_request(&state, 0u));
    assert(r0fg1_presentation_swap(&state));
    assert(state.displayed_valid && state.composition_view == 0u);
    assert(state.displayed.key.generation == 1u);
    assert(state.displayed.key.source_tick == 10u);
    assert(state.displayed.horizon == -3);
    assert(state.displayed.anchors[0].handle == cue.handle);
    assert(state.displayed.anchors[0].x == cue.x);
    assert(state.displayed.anchors[0].y == cue.y);
    assert(!r0fg1_presentation_bind(&state, &key, 7));

    r0fg1_registration old_display;
    memcpy(&old_display, &state.displayed, sizeof(old_display));
    key = (r0fg1_presentation_key){2u, 11u, 0u, 0u, 1u};
    assert(r0fg1_presentation_bind(&state, &key, 7));
    assert(r0fg1_view_request(&state, 1u));
    assert(state.building.key.view == 0u && state.building.key.tier == 0u);
    assert(r0fg1_lod_select(0u, UINT16_MAX) == 1u);
    assert(state.building.key.tier == 0u);
    assert(!r0fg1_presentation_swap(&state));
    envelope(&state, &key);
    assert(r0fg1_presentation_complete(&state, &key, 1u));
    assert(!r0fg1_presentation_swap(&state));
    assert(!memcmp(&old_display, &state.displayed, sizeof(old_display)));
    assert(state.composition_view == 0u);
    r0fg1_presentation_cancel(&state);
    assert(!memcmp(&old_display, &state.displayed, sizeof(old_display)));

    key = (r0fg1_presentation_key){3u, 14u, 1u, 1u, 1u};
    assert(r0fg1_presentation_bind(&state, &key, 9));
    envelope(&state, &key);
    assert(r0fg1_anchor_add(&state, &key, &cue) == R0FG1P_RETAINED);
    assert(r0fg1_presentation_complete(&state, &key, 1u));
    assert(r0fg1_presentation_swap(&state));
    assert(state.displayed.key.generation == 3u);
    assert(state.displayed.key.source_tick == 14u);
    assert(state.displayed.key.view == 1u && state.composition_view == 1u);
    assert(state.displayed.key.tier == 1u && state.displayed.key.buffer == 1u);
    assert(state.displayed.horizon == 9 && state.completions == 3u);
    assert(state.swaps == 2u);

    const r0fg1_presentation_key invalid[] = {
        {0u, 15u, 1u, 1u, 0u}, {4u, 0u, 1u, 1u, 0u},
        {3u, 15u, 1u, 1u, 0u}, {4u, 13u, 1u, 1u, 0u},
        {4u, 15u, 0u, 1u, 0u}, {4u, 15u, 1u, 2u, 0u},
        {4u, 15u, 1u, 1u, 1u}, {4u, 15u, 1u, 1u, 2u}
    };
    for (uint8_t index = 0u; index < sizeof(invalid) / sizeof(invalid[0]); index++)
    {
        assert(!r0fg1_presentation_bind(&state, &invalid[index], 0));
    }
}

static int anchor_order(const void *first, const void *second)
{
    const r0fg1_anchor *a = first;
    const r0fg1_anchor *b = second;
    if (a->priority != b->priority)
    {
        return a->priority < b->priority ? -1 : 1;
    }
    return a->handle < b->handle ? -1 : a->handle > b->handle;
}

static void anchor_permutations(r0fg1_anchor *cues, uint8_t start)
{
    if (start == 6u)
    {
        r0fg1_anchor ranked[6];
        memcpy(ranked, cues, sizeof(ranked));
        qsort(ranked, 6u, sizeof(ranked[0]), anchor_order);
        r0fg1_presentation state;
        r0fg1_presentation_init(&state);
        r0fg1_presentation_key key = {1u, 1u, 0u, 0u, 0u};
        assert(r0fg1_presentation_bind(&state, &key, 0));
        for (uint8_t index = 0u; index < 6u; index++)
        {
            assert(r0fg1_anchor_add(&state, &key, &cues[index]) != R0FG1P_INVALID);
        }
        assert(state.anchor_high == R0FG1P_ANCHORS && state.anchor_drops == 2u);
        for (uint8_t index = 0u; index < R0FG1P_ANCHORS; index++)
        {
            assert(state.building.anchors[index].handle == ranked[index].handle);
            assert(state.building.anchors[index].x == ranked[index].x);
            assert(state.building.anchors[index].y == ranked[index].y);
            assert(state.building.anchors[index].priority == ranked[index].priority);
        }
        assert(!r0fg1_anchor_add(&state, &key, &ranked[0]));
        r0fg1_anchor wrong_priority = {99u, 0u, 0u, R0FG1P_ANCHOR_PRIORITIES};
        assert(!r0fg1_anchor_add(&state, &key, &wrong_priority));
        state.anchor_drops = UINT16_MAX;
        assert(!r0fg1_anchor_add(&state, &key, &ranked[5]));
        assert(state.anchor_drops == UINT16_MAX);
        permutations++;
        return;
    }
    for (uint8_t index = start; index < 6u; index++)
    {
        r0fg1_anchor temporary = cues[start];
        cues[start] = cues[index];
        cues[index] = temporary;
        anchor_permutations(cues, (uint8_t)(start + 1u));
        temporary = cues[start];
        cues[start] = cues[index];
        cues[index] = temporary;
    }
}

static void test_clipping(void)
{
    r0fg1_presentation state;
    r0fg1_presentation_init(&state);
    r0fg1_presentation_key key = {1u, 1u, 0u, 0u, 0u};
    assert(r0fg1_presentation_bind(&state, &key, 0));
    uint16_t visible_bottom = 999u;
    assert(!r0fg1_occlusion_clip(&state, &key, 0u, 2u, 0u, 7u, &visible_bottom));
    assert(visible_bottom == 999u);
    for (uint16_t ridge = 0u; ridge < 8u; ridge++)
    {
        for (uint16_t ridge_depth = 0u; ridge_depth < 3u; ridge_depth++)
        {
            assert(r0fg1_occlusion_column(&state, &key, 0u, ridge, ridge_depth));
            for (uint16_t depth = 0u; depth < 3u; depth++)
            {
                for (uint16_t top = 0u; top < 8u; top++)
                {
                    for (uint16_t bottom = top; bottom < 8u; bottom++)
                    {
                        // Independent fragment enumeration, not the target's
                        // closed-form boundary calculation.
                        uint16_t visible = 0u, last = 999u;
                        for (uint16_t y = top; y <= bottom; y++)
                        {
                            if (depth <= ridge_depth || y < ridge)
                            {
                                visible++;
                                last = y;
                            }
                        }
                        visible_bottom = 999u;
                        uint8_t result = r0fg1_occlusion_clip(
                            &state, &key, 0u, depth, top, bottom, &visible_bottom);
                        uint8_t expected = visible == 0u ? R0FG1P_HIDDEN
                            : visible == bottom - top + 1u ? R0FG1P_UNCLIPPED
                            : R0FG1P_CLIPPED;
                        assert(result == expected);
                        assert(visible_bottom == last);
                        clipping_cases++;
                    }
                }
            }
        }
    }
    assert(!r0fg1_occlusion_clip(&state, &key, 0u, 0u, 8u, 7u, &visible_bottom));
    assert(!r0fg1_occlusion_clip(&state, &key,
                                R0FG1P_OCCLUSION_COLUMNS, 0u, 0u, 7u,
                                &visible_bottom));
    assert(r0fg1_occlusion_column(&state, &key, 0u, UINT16_MAX, 1u));
    assert(r0fg1_occlusion_clip(&state, &key, 0u, 2u, 0u, UINT16_MAX,
                               &visible_bottom) == R0FG1P_CLIPPED);
    assert(visible_bottom == UINT16_MAX - 1u);
    assert(r0fg1_occlusion_column(&state, &key, 0u, 0u, 1u));
    assert(r0fg1_occlusion_clip(&state, &key, 0u, 2u, 0u, UINT16_MAX,
                               &visible_bottom) == R0FG1P_HIDDEN);
}

static void test_lod_and_overflow(void)
{
    for (uint8_t previous = 0u; previous < R0FG1P_TIERS; previous++)
    {
        for (uint32_t pixels = 0u; pixels <= UINT16_MAX; pixels++)
        {
            uint8_t expected = previous;
            if (previous == 0u && pixels >= R0FG1P_LOD_ENTER_PIXELS)
            {
                expected = 1u;
            }
            if (previous == 1u && pixels <= R0FG1P_LOD_EXIT_PIXELS)
            {
                expected = 0u;
            }
            assert(r0fg1_lod_select(previous, (uint16_t)pixels) == expected);
        }
    }
    assert(r0fg1_lod_select(2u, 10u) == R0FG1P_INVALID_TIER);
    uint8_t chosen = 0u;
    for (uint16_t repeat = 0u; repeat < 100u; repeat++)
    {
        chosen = r0fg1_lod_select(chosen, 11u);
        assert(chosen == 0u);
        chosen = r0fg1_lod_select(chosen, 12u);
        assert(chosen == 1u);
        chosen = r0fg1_lod_select(chosen, 9u);
        assert(chosen == 1u);
        chosen = r0fg1_lod_select(chosen, 8u);
        assert(chosen == 0u);
    }
    r0fg1_presentation state;
    r0fg1_presentation_init(&state);
    r0fg1_presentation_key key = {1u, 1u, 0u, 0u, 0u};
    assert(r0fg1_presentation_bind(&state, &key, 0));
    envelope(&state, &key);
    state.completions = UINT16_MAX;
    assert(!r0fg1_presentation_complete(&state, &key, 1u));
    assert(!state.ready);
    state.completions = 0u;
    assert(r0fg1_presentation_complete(&state, &key, 1u));
    state.swaps = UINT16_MAX;
    assert(!r0fg1_presentation_swap(&state));
    assert(!state.displayed_valid && state.swaps == UINT16_MAX);
}

int main(void)
{
    assert(R0FG1P_ANCHORS == 4u);
    test_coherence();
    r0fg1_anchor cues[6] = {
        {10u, 10u, 1u, 3u}, {11u, 11u, 2u, 3u}, {12u, 12u, 3u, 3u},
        {13u, 13u, 4u, 3u}, {50u, 50u, 5u, 0u}, {60u, 60u, 6u, 1u}
    };
    anchor_permutations(cues, 0u);
    test_clipping();
    test_lod_and_overflow();
    printf("Presentation coherence/overflow PASS; anchors %u permutations; "
           "occlusion %u cases; LOD 131072 comparisons\n",
           (unsigned int)permutations, (unsigned int)clipping_cases);
    printf("Host native state %u bytes; not target-linked memory accounting\n",
           (unsigned int)sizeof(r0fg1_presentation));
    return 0;
}
