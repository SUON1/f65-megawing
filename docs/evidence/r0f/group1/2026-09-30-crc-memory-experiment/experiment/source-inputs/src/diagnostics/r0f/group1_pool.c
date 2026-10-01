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

uint8_t r0fg1_pool_sample(r0fg1_pool_observation *state, uint16_t occupancy)
{
    if (state == 0 || state->capacity == 0u || occupancy > state->capacity
        || state->peak > state->capacity || state->samples == UINT16_MAX
        || state->full_samples > state->samples
        || (state->samples == 0u && state->peak != 0u)
        || ((state->peak == state->capacity) != (state->full_samples != 0u)))
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
