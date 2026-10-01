#include <assert.h>
#include <stdint.h>
#include <stdio.h>

#include "successor_lifecycle.h"

// Independent bitwise oracle; it never calls the table implementation.
static uint32_t independent_update(uint32_t crc, const uint8_t *data,
                                   uint16_t length)
{
    for (uint16_t index = 0u; index < length; index++)
    {
        crc ^= data[index];
        for (uint8_t bit = 0u; bit < 8u; bit++)
        {
            uint32_t mask = 0u - (crc & 1u);
            crc = (crc >> 1u) ^ (mask & 0xedb88320u);
        }
    }
    return crc;
}

static uint32_t next_random(uint32_t *state)
{
    *state = *state * 1664525u + 1013904223u;
    return *state;
}

int main(void)
{
    static uint8_t data[65535];
    uint32_t random = 0x12345678u;
    uint32_t cases = 0u;
    const uint8_t known[] = "123456789";

    assert(r0fs_crc32(known, 9u) == 0xcbf43926u);
    assert(r0fs_crc32(NULL, 0u) == 0u);
    assert(r0fs_crc32_update(0x5a1234efu, NULL, 0u) == 0x5a1234efu);
    for (uint16_t seed = 0u; seed < 256u; seed++)
    {
        for (uint16_t byte = 0u; byte < 256u; byte++)
        {
            uint32_t crc = next_random(&random);
            data[0] = (uint8_t)byte;
            crc = (crc & 0xffffff00u) | seed;
            assert(r0fs_crc32_update(crc, data, 1u)
                   == independent_update(crc, data, 1u));
            cases++;
        }
    }
    for (uint32_t index = 0u; index < sizeof(data); index++)
    {
        data[index] = (uint8_t)(next_random(&random) >> 24u);
    }
    for (uint16_t trial = 0u; trial < 4096u; trial++)
    {
        uint16_t length = (uint16_t)(next_random(&random) & 1023u);
        uint16_t split = (uint16_t)(next_random(&random) % ((uint32_t)length + 1u));
        uint32_t seed = next_random(&random);
        uint32_t actual = r0fs_crc32_update(seed, data, split);
        actual = r0fs_crc32_update(actual, data + split, (uint16_t)(length - split));
        assert(actual == independent_update(seed, data, length));
        cases++;
    }
    const uint16_t lengths[] = {0u, 1u, 15u, 16u, 255u, 256u, 32767u, 65534u, 65535u};
    for (uint8_t index = 0u; index < sizeof(lengths) / sizeof(lengths[0]); index++)
    {
        uint16_t length = lengths[index];
        assert(r0fs_crc32(data, length)
               == ~independent_update(0xffffffffu, data, length));
        cases++;
    }
    printf("Independent CRC PASS: %lu cases, known vector, null empty, u16 boundary\n",
           (unsigned long)cases);
    return 0;
}
