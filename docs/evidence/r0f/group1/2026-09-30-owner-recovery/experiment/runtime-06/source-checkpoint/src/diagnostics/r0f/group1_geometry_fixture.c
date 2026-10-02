#include "group1_geometry_fixture.h"
#include "group1_pool_owners.h"
#include "successor_lifecycle.h"

static uint8_t faces[R0FG1_POOL_FACES_CAPACITY];
static uint8_t vertices[R0FG1_POOL_VERTICES_CAPACITY];
static uint8_t spans[R0FG1_POOL_SPANS_CAPACITY];
static uint8_t buckets[R0FG1_POOL_BUCKETS_CAPACITY];
static uint8_t live[R0FG1_POOL_GEOMETRY_COUNT];

// Keep bounded fixture temporaries separate from the incremental display
// owner's much larger live state; measure the resulting call/timing cost.
__attribute__((noinline))
uint32_t r0fg1_geometry_fixture(uint16_t generation, uint16_t source_tick)
{
    static uint8_t *const buffers[R0FG1_POOL_GEOMETRY_COUNT] = {
        faces, vertices, spans, buckets,
    };
    static const uint8_t capacities[R0FG1_POOL_GEOMETRY_COUNT] = {
        R0FG1_POOL_FACES_CAPACITY, R0FG1_POOL_VERTICES_CAPACITY,
        R0FG1_POOL_SPANS_CAPACITY, R0FG1_POOL_BUCKETS_CAPACITY,
    };
    uint32_t crc = 0xfffffffful;
    uint8_t owner_offset = 0u;
    for (uint8_t owner = 0u; owner < R0FG1_POOL_GEOMETRY_COUNT; owner++)
    {
        // Reduce before adding: preserves even UINT16_MAX without 32-bit
        // division. With the unchanged fixture, the sum is at most 71.
        uint16_t period = (uint16_t)(capacities[owner] + 1u);
        uint16_t count = (uint16_t)(generation % period
            + owner_offset);
        while (count >= period)
        {
            count = (uint16_t)(count - period);
        }
        live[owner] = (uint8_t)count;
        r0fg1_owner_sample(owner, live[owner]);
        uint8_t value = (uint8_t)(source_tick + owner_offset);
        for (uint8_t index = 0u; index < live[owner]; index++)
        {
            buffers[owner][index] = value;
            value++;
        }
        crc = r0fs_crc32_update(crc, buffers[owner], live[owner]);
        live[owner] = 0u;
        r0fg1_owner_sample(owner, live[owner]);
        owner_offset = (uint8_t)(owner_offset + R0FG1_POOL_OFFSET_STRIDE);
    }
    return ~crc;
}
