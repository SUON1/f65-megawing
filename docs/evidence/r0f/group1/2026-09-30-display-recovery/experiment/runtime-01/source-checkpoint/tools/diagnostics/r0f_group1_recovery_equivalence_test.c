#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "group1_geometry_fixture.h"
#include "group1_pool.h"
#include "group1_pool_owners.h"

uint8_t cffault;
uint8_t reference_sample(r0fg1_pool_observation *state, uint16_t occupancy);

static uint32_t crc_byte(uint32_t crc, uint8_t value)
{
    crc ^= value;
    for (unsigned bit = 0u; bit < 8u; bit++)
    {
        crc = (crc >> 1u) ^ ((crc & 1u) ? 0xedb88320u : 0u);
    }
    return crc;
}

static uint16_t word(const uint8_t *bytes)
{
    return (uint16_t)(bytes[0] | (uint16_t)bytes[1] << 8u);
}

int main(void)
{
    static const uint16_t values[] = {
        0u, 1u, 7u, 8u, 15u, 16u, 24u, 32u, 255u, 256u, 65534u, 65535u,
    };
    uint32_t cases = 0u;
    for (unsigned c = 0u; c < 12u; c++)
    for (unsigned p = 0u; p < 12u; p++)
    for (unsigned s = 0u; s < 12u; s++)
    for (unsigned f = 0u; f < 12u; f++)
    for (unsigned o = 0u; o < 12u; o++)
    {
        r0fg1_pool_observation original = {values[c], values[p], values[s], values[f]};
        r0fg1_pool_observation revised = original;
        assert(reference_sample(&original, values[o])
            == r0fg1_pool_sample(&revised, values[o]));
        assert(memcmp(&original, &revised, sizeof(original)) == 0);
        cases++;
    }
    assert(reference_sample(0, 0u) == r0fg1_pool_sample(0, 0u));
    static const uint16_t capacities[R0FG1_POOL_COUNT] = R0FG1_POOL_CAPACITIES;
    uint16_t samples[4], full[4], peak[4];
    for (uint32_t generation = 0u; generation <= UINT16_MAX; generation++)
    {
        if (generation % 16384u == 0u)
        {
            assert(r0fg1_owners_begin());
            for (unsigned owner = 0u; owner < 4u; owner++)
            {
                samples[owner] = 1u;
                full[owner] = peak[owner] = 0u;
            }
        }
        uint16_t source = (uint16_t)(generation * 193u + 17u);
        uint32_t crc = 0xffffffffu;
        for (unsigned owner = 0u; owner < 4u; owner++)
        {
            // Independent original wide formula, deliberately not optimized.
            uint16_t count = (uint16_t)((generation
                + owner * R0FG1_POOL_OFFSET_STRIDE) % (capacities[owner] + 1u));
            for (unsigned index = 0u; index < count; index++)
            {
                crc = crc_byte(crc, (uint8_t)(source
                    + owner * R0FG1_POOL_OFFSET_STRIDE + index));
            }
            samples[owner] += 2u;
            full[owner] += count == capacities[owner] ? 1u : 0u;
            if (count > peak[owner])
            {
                peak[owner] = count;
            }
        }
        assert(r0fg1_geometry_fixture((uint16_t)generation, source) == ~crc);
        assert(!cffault);
        uint8_t bytes[R0FG1_POOL_EPOCH_BYTES];
        r0fg1_owners_encode(bytes);
        for (unsigned owner = 0u; owner < 4u; owner++)
        {
            const uint8_t *row = bytes + owner * R0FG1_POOL_RECORD_BYTES;
            assert(word(row + R0FG1_POOL_W_CAPACITY) == capacities[owner]);
            assert(word(row + R0FG1_POOL_W_PEAK) == peak[owner]);
            assert(word(row + R0FG1_POOL_W_SAMPLES) == samples[owner]);
            assert(word(row + R0FG1_POOL_W_FULL_SAMPLES) == full[owner]);
        }
    }
    printf("Observer equivalence PASS: %u boundary-state combinations plus null; "
           "all 65536 generations, actual geometry CRC and counters PASS\n", (unsigned)cases);
    return 0;
}
