#include <assert.h>
#include <stdio.h>

#include "group1_scene.h"
#include "group1_pool_owners.h"
uint8_t cffault;

int main(void)
{
    r0fg1_presentation state;
    uint8_t pixels[R0FG1P_SCENE_BYTES];
    r0fg1_presentation_init(&state);
    assert(r0fg1_owners_begin());
    for (uint16_t tick = 1u; tick <= 3200u; tick++)
    {
        assert(r0fg1_view_request(&state,
            (uint8_t)((tick >> R0FG1P_VIEW_TICK_SHIFT) & 1u)));
        assert(r0fg1_scene_bind(&state, tick, (uint8_t)(tick & 1u)));
        assert(!state.ready);
        assert(r0fg1_scene_encode(&state, pixels));
        assert(!cffault);
        assert(state.building.anchor_count == R0FG1P_ANCHORS);
        assert(state.building.column_mask == R0FG1P_OCCLUSION_MASK);
        for (uint8_t index = 0u; index < sizeof(pixels); index++)
        {
            printf("%02X", pixels[index]);
        }
        puts("");
        assert(r0fg1_presentation_complete(&state, &state.building.key, 1u));
        assert(r0fg1_presentation_swap(&state));
        assert(state.displayed.key.source_tick == tick);
        assert(state.composition_view == state.requested_view);
    }
    assert(state.anchor_high == R0FG1P_ANCHORS);
    assert(state.occlusion_high == R0FG1P_OCCLUSION_COLUMNS);
    assert(state.anchor_drops == 6400u);
    assert(r0fg1_scene_bind(&state, 3201u, 1u));
    assert(r0fg1_view_request(&state, 0u));
    assert(r0fg1_scene_encode(&state, pixels));
    assert(r0fg1_presentation_complete(&state, &state.building.key, 1u));
    assert(!r0fg1_presentation_swap(&state));
    assert(state.displayed.key.source_tick == 3200u);
    r0fg1_presentation_cancel(&state);
    assert(r0fg1_scene_bind(&state, 3202u, 1u));
    assert(state.building.key.view == 0u);
    assert(state.displayed.key.view == 1u);
    puts("Scene owner cancellation/coherence PASS");
    return 0;
}
