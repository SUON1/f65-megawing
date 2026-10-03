#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "group1_pool.h"
#include "r0f_group1_pool.h"

extern r0fg1_pool_observation r0fg1_pool_shape[R0FG1_POOL_COUNT];
uint8_t r0fg1_pool_probe_begin(void);
uint8_t r0fg1_pool_probe_sample(uint8_t owner, uint16_t occupancy);
uint8_t r0fg1_pool_probe_encode(uint8_t *bytes, uint16_t length);

static uint16_t read16(const uint8_t *bytes)
{
    return (uint16_t)((uint16_t)bytes[0] | (uint16_t)bytes[1] << 8u);
}

int main(void)
{
    static const uint16_t capacities[R0FG1_POOL_COUNT] = R0FG1_POOL_CAPACITIES;
    uint8_t bytes[66];
    r0fg1_pool_observation original[R0FG1_POOL_COUNT];
    assert(r0fg1_pool_probe_begin());
    for (uint8_t owner = 0u; owner < R0FG1_POOL_COUNT; owner++)
    {
        assert(r0fg1_pool_probe_sample(owner, 0u));
        assert(r0fg1_pool_probe_sample(owner, capacities[owner]));
        assert(r0fg1_pool_probe_sample(owner, (uint16_t)(capacities[owner] / 2u)));
    }
    memcpy(original, r0fg1_pool_shape, sizeof(original));
    assert(!r0fg1_pool_probe_sample(R0FG1_POOL_COUNT, 0u));
    assert(!r0fg1_pool_probe_sample(0u, (uint16_t)(capacities[0] + 1u)));
    assert(memcmp(original, r0fg1_pool_shape, sizeof(original)) == 0);
    memset(bytes, 0xa5, sizeof(bytes));
    assert(!r0fg1_pool_probe_encode(NULL, 64u));
    assert(!r0fg1_pool_probe_encode(bytes + 1u, 63u));
    assert(!r0fg1_pool_probe_encode(bytes + 1u, 65u));
    for (uint8_t index = 0u; index < sizeof(bytes); index++)
    {
        assert(bytes[index] == 0xa5u);
    }
    assert(r0fg1_pool_probe_encode(bytes + 1u, 64u));
    assert(bytes[0] == 0xa5u && bytes[65] == 0xa5u);
    for (uint8_t owner = 0u; owner < R0FG1_POOL_COUNT; owner++)
    {
        const uint8_t *row = bytes + 1u + owner * 8u;
        assert(read16(row) == capacities[owner]);
        assert(read16(row + 2u) == capacities[owner]);
        assert(read16(row + 4u) == 3u);
        assert(read16(row + 6u) == 1u);
    }
    assert(memcmp(original, r0fg1_pool_shape, sizeof(original)) == 0);
    puts("Cold adapter host PASS: initialization, peer state, field-wise encoding and invalid input guards");
    return 0;
}
