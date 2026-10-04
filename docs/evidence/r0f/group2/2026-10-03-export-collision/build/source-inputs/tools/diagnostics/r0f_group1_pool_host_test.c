#include <assert.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "group1_pool.h"
#include "r0f_group1_pool.h"
#include "r0f_group1_trace.h"

static uint32_t transition_cases;

static void rejects_unchanged(r0fg1_pool_observation *state, uint16_t used)
{
    r0fg1_pool_observation before = *state;
    assert(!r0fg1_pool_sample(state, used));
    assert(!memcmp(&before, state, sizeof(before)));
}

static void boundaries(void)
{
    assert(!r0fg1_pool_init(0, 1u));
    assert(!r0fg1_pool_sample(0, 0u));
    r0fg1_pool_observation state = {4u, 0u, 0u, 0u};
    r0fg1_pool_observation before = state;
    assert(!r0fg1_pool_init(&state, 0u));
    assert(!memcmp(&before, &state, sizeof(state)));

    const r0fg1_pool_observation corrupt[] = {
        {0u, 0u, 0u, 0u}, {4u, 5u, 1u, 0u},
        {4u, 0u, 1u, 2u}, {4u, 1u, 0u, 0u},
        {4u, 4u, 1u, 0u}, {4u, 3u, 1u, 1u}
    };
    for (uint8_t index = 0u; index < sizeof(corrupt) / sizeof(corrupt[0]); index++)
    {
        state = corrupt[index];
        rejects_unchanged(&state, 0u);
    }
    for (uint8_t pattern = 0u; pattern < 2u; pattern++)
    {
        assert(r0fg1_pool_init(&state, 1u));
        for (uint32_t sample = 0u; sample < UINT16_MAX; sample++)
        {
            uint16_t occupancy = pattern ? 1u : (uint16_t)(sample & 1u);
            assert(r0fg1_pool_sample(&state, occupancy));
        }
        assert(state.samples == UINT16_MAX);
        assert(state.full_samples == (pattern ? UINT16_MAX : 32767u));
        rejects_unchanged(&state, 1u);
    }

    const uint16_t sample_counts[] = {1u, UINT16_MAX - 1u, UINT16_MAX};
    for (uint16_t capacity = 1u; capacity <= 32u; capacity++)
    {
        for (uint16_t peak = 0u; peak <= capacity; peak++)
        {
            for (uint16_t used = 0u; used <= capacity + 1u; used++)
            {
                for (uint8_t index = 0u; index < 3u; index++)
                {
                    state = (r0fg1_pool_observation){capacity, peak,
                        sample_counts[index], peak == capacity ? 1u : 0u};
                    before = state;
                    uint8_t valid = used <= capacity && state.samples < UINT16_MAX;
                    assert(r0fg1_pool_sample(&state, used) == valid);
                    if (valid)
                    {
                        assert(state.capacity == capacity);
                        assert(state.peak == (used > peak ? used : peak));
                        assert(state.samples == before.samples + 1u);
                        assert(state.full_samples == before.full_samples
                            + (used == capacity ? 1u : 0u));
                    }
                    else
                    {
                        assert(!memcmp(&before, &state, sizeof(state)));
                    }
                    transition_cases++;
                }
            }
        }
    }
    for (uint32_t value = 0u; value <= UINT16_MAX; value++)
    {
        assert(r0fg1_pool_init(&state, UINT16_MAX));
        assert(r0fg1_pool_sample(&state, (uint16_t)value));
        assert(state.peak == value && state.samples == 1u);
        assert(state.full_samples == (value == UINT16_MAX ? 1u : 0u));
        transition_cases++;
        if (value != 0u)
        {
            assert(r0fg1_pool_init(&state, (uint16_t)value));
            assert(r0fg1_pool_sample(&state, (uint16_t)value));
            assert(state.peak == value && state.full_samples == 1u);
            if (value < UINT16_MAX)
            {
                rejects_unchanged(&state, (uint16_t)(value + 1u));
            }
            transition_cases++;
        }
    }
    printf("Boundary PASS: %" PRIu32 " transitions; two 65535-sample counter limits\n",
        transition_cases);
}

static void owner_sequences(void)
{
    const uint16_t capacities[R0FG1_POOL_COUNT] = R0FG1_POOL_CAPACITIES;
    r0fg1_pool_observation owners[R0FG1_POOL_COUNT];
    for (uint8_t pool = 0u; pool < R0FG1_POOL_COUNT; pool++)
    {
        assert(r0fg1_pool_init(&owners[pool], capacities[pool]));
    }
    // One continuous host interval. No reset at the storage-shaped midpoint.
    for (uint16_t tick = 1u; tick <= R0FG1_RECORDS; tick++)
    {
        for (uint8_t pool = 0u; pool < R0FG1_POOL_COUNT; pool++)
        {
            r0fg1_pool_observation before[R0FG1_POOL_COUNT];
            memcpy(before, owners, sizeof(owners));
            uint16_t occupancy = (uint16_t)(((uint32_t)tick
                + (uint32_t)pool * R0FG1_POOL_OFFSET_STRIDE)
                % ((uint32_t)capacities[pool] + 1u));
            assert(r0fg1_pool_sample(&owners[pool], occupancy));
            for (uint8_t peer = 0u; peer < R0FG1_POOL_COUNT; peer++)
            {
                if (peer != pool)
                {
                    assert(!memcmp(&owners[peer], &before[peer], sizeof(owners[peer])));
                }
            }
            printf("ROW %u %u %u %u %u %u\n", (unsigned)tick, (unsigned)pool,
                (unsigned)occupancy, (unsigned)owners[pool].peak,
                (unsigned)owners[pool].samples, (unsigned)owners[pool].full_samples);
        }
    }
}

int main(void)
{
    boundaries();
    owner_sequences();
    return 0;
}
