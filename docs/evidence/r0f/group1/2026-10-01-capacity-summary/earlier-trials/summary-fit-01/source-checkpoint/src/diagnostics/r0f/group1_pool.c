#include <stdint.h>

#include "group1_pool.h"

// Pure observations: no owner mutation, hardware, scheduling or allocator.
uint8_t r0fg1_pool_init(r0fg1_pool_observation *state, uint16_t capacity)
{
    if (state == 0 || capacity == 0u)
    {
        return 0u;
    }
    state->capacity = capacity;
    state->peak = 0u;
    state->samples = 0u;
    state->full_samples = 0u;
    return 1u;
}

// Let the pinned LTO compiler specialize the freshly initialized zero sample
// and the checked owner path; source-level rejection rules remain identical.
__attribute__((always_inline))
uint8_t r0fg1_pool_sample(r0fg1_pool_observation *state, uint16_t occupancy)
{
    if (state == 0 || state->capacity == 0u || occupancy > state->capacity
        || state->samples == UINT16_MAX
        || (state->samples == 0u && state->peak != 0u))
    {
        return 0u;
    }
    // Factor the same invariant by full/non-full history. A full history
    // requires peak == capacity; a non-full history requires peak < capacity.
    // full_samples <= samples is automatic when full_samples is zero.
    if (state->full_samples != 0u)
    {
        if (state->peak != state->capacity
            || state->full_samples > state->samples)
        {
            return 0u;
        }
    }
    else if (state->peak >= state->capacity)
    {
        return 0u;
    }
    if (occupancy > state->peak)
    {
        state->peak = occupancy;
    }
    state->samples++;
    if (occupancy == state->capacity)
    {
        state->full_samples++;
    }
    return 1u;
}
