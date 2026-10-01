#include "group1_pool.h"
#include "group1_pool_owners.h"

extern uint8_t cffault;
static r0fg1_pool_observation observations[R0FG1_POOL_COUNT];

// Initialization has its own register lifetime, separate from the lifecycle.
__attribute__((noinline))
uint8_t r0fg1_owners_begin(void)
{
    static const uint16_t capacities[R0FG1_POOL_COUNT] = R0FG1_POOL_CAPACITIES;
    for (uint8_t owner = 0u; owner < R0FG1_POOL_COUNT; owner++)
    {
        if (!r0fg1_pool_init(&observations[owner], capacities[owner])
            || !r0fg1_pool_sample(&observations[owner], 0u))
        {
            return 0u;
        }
    }
    return 1u;
}

void r0fg1_owner_sample(uint8_t owner, uint16_t occupancy)
{
    if (owner >= R0FG1_POOL_COUNT
        || !r0fg1_pool_sample(&observations[owner], occupancy))
    {
        if (!cffault)
        {
            cffault = R0FG1_POOL_FAULT;
        }
    }
}

uint16_t r0fg1_owner_peak(uint8_t owner)
{
    return owner < R0FG1_POOL_COUNT ? observations[owner].peak : 0u;
}

static void put16(uint8_t *bytes, uint16_t value)
{
    bytes[0] = (uint8_t)value;
    bytes[1] = (uint8_t)(value >> 8u);
}

void r0fg1_owners_encode(uint8_t bytes[R0FG1_POOL_EPOCH_BYTES])
{
    for (uint8_t owner = 0u; owner < R0FG1_POOL_COUNT; owner++)
    {
        const r0fg1_pool_observation *state = &observations[owner];
        put16(bytes + R0FG1_POOL_W_CAPACITY, state->capacity);
        put16(bytes + R0FG1_POOL_W_PEAK, state->peak);
        put16(bytes + R0FG1_POOL_W_SAMPLES, state->samples);
        put16(bytes + R0FG1_POOL_W_FULL_SAMPLES, state->full_samples);
        bytes += R0FG1_POOL_RECORD_BYTES;
    }
}
