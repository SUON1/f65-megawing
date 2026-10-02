#include <stdint.h>

#include "group1_pool.h"
#include "r0f_group1_pool.h"

// Cold fit candidate only: no owner connections and no admitted trace version.
// These field-wise bytes estimate transport cost without using native packing.
// Never execute this object in a workload or release it as a wire ABI.
extern r0fg1_pool_observation r0fg1_pool_shape[R0FG1_POOL_COUNT];

uint8_t r0fg1_pool_probe_begin(void)
{
    static const uint16_t capacities[R0FG1_POOL_COUNT] = R0FG1_POOL_CAPACITIES;
    for (uint8_t owner = 0u; owner < R0FG1_POOL_COUNT; owner++)
    {
        if (!r0fg1_pool_init(&r0fg1_pool_shape[owner], capacities[owner]))
        {
            return 0u;
        }
    }
    return 1u;
}

uint8_t r0fg1_pool_probe_sample(uint8_t owner, uint16_t occupancy)
{
    if (owner >= R0FG1_POOL_COUNT)
    {
        return 0u;
    }
    return r0fg1_pool_sample(&r0fg1_pool_shape[owner], occupancy);
}

static void put16(uint8_t *bytes, uint16_t value)
{
    bytes[0] = (uint8_t)value;
    bytes[1] = (uint8_t)(value >> 8u);
}

uint8_t r0fg1_pool_probe_encode(uint8_t *bytes, uint16_t length)
{
    // Probe encoding only: four u16 fields per generated owner, no new buffer.
    if (bytes == 0 || length != R0FG1_POOL_COUNT * 4u * 2u)
    {
        return 0u;
    }
    for (uint8_t owner = 0u; owner < R0FG1_POOL_COUNT; owner++)
    {
        const r0fg1_pool_observation *state = &r0fg1_pool_shape[owner];
        put16(bytes, state->capacity);
        put16(bytes + 2u, state->peak);
        put16(bytes + 4u, state->samples);
        put16(bytes + 6u, state->full_samples);
        bytes += 4u * 2u;
    }
    return 1u;
}
