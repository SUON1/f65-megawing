#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "group1_pool_owners.h"
#include "group1_geometry_fixture.h"

uint8_t cffault;

static void output(const char *name)
{
    uint8_t bytes[R0FG1_POOL_EPOCH_BYTES];
    r0fg1_owners_encode(bytes);
    printf("%s ", name);
    for (unsigned index = 0u; index < sizeof(bytes); index++)
    {
        printf("%02X", bytes[index]);
    }
    puts("");
}

int main(void)
{
    uint8_t before[R0FG1_POOL_EPOCH_BYTES], after[R0FG1_POOL_EPOCH_BYTES];
    assert(r0fg1_owners_begin());
    output("initial");
    for (uint16_t generation = 1u; generation <= 3200u; generation++)
    {
        uint16_t source = (uint16_t)(generation * 17u);
        uint32_t crc = r0fg1_geometry_fixture(generation, source);
        assert(!cffault);
        printf("geometry %u %u %08X\n", generation, source, (unsigned)crc);
        if (generation == 1600u || generation == 3200u)
        {
            output("checkpoint");
        }
    }
    printf("geometry 65535 65535 %08X\n",
           (unsigned)r0fg1_geometry_fixture(UINT16_MAX, UINT16_MAX));
    r0fg1_owners_encode(before);
    r0fg1_owner_sample(R0FG1_POOL_COUNT, 0u);
    assert(cffault == R0FG1_POOL_FAULT);
    r0fg1_owners_encode(after);
    assert(memcmp(before, after, sizeof(before)) == 0);
    cffault = 87u;
    r0fg1_owner_sample(R0FG1_POOL_FACES, R0FG1_POOL_FACES_CAPACITY + 1u);
    assert(cffault == 87u);
    r0fg1_owners_encode(after);
    assert(memcmp(before, after, sizeof(before)) == 0);
    cffault = 0u;
    assert(r0fg1_owners_begin());
    for (uint32_t sample = 1u; sample < UINT16_MAX; sample++)
    {
        r0fg1_owner_sample(R0FG1_POOL_FACES, R0FG1_POOL_FACES_CAPACITY);
    }
    assert(!cffault);
    r0fg1_owners_encode(before);
    r0fg1_owner_sample(R0FG1_POOL_FACES, 0u);
    assert(cffault == R0FG1_POOL_FAULT);
    r0fg1_owners_encode(after);
    assert(memcmp(before, after, sizeof(before)) == 0);
    puts("owner bounds, first fault, overflow and immutable peers PASS");
    return 0;
}
