// Exercise the actual retained physical-copy validator against the extension.
// No platform registers, actual copy, DMA or target execution are involved.
#include <assert.h>
#include <stdint.h>
#include <stdio.h>

#include "combined_model.h"
#include "m2_extended_resident.h"

int main(void)
{
    uint32_t rejected = 0u;
    for (uint32_t address = M2RE_RESIDENT_START;
         address < M2RE_FORBIDDEN_MAP_END_EXCLUSIVE; ++address)
    {
        for (uint8_t reclaimed = 0u; reclaimed < 2u; ++reclaimed)
        {
            assert(!r0fc_range(address, 1u, 1u, reclaimed));
            assert(!r0fc_range(address, 255u, 1u, reclaimed));
            rejected += 2u;
        }
    }
    assert(!r0fc_range(0xffffffffUL, 255u, 1u, 1u));
    assert(!r0fc_range(R0FC_RESERVE, 1u, 1u, 1u));
    assert(r0fc_range(R0FC_STAGING, 255u, 1u, 0u));
    assert(r0fc_range(R0FC_BACKUP, 255u, 1u, 0u));
    printf("PASS: %lu resident/covering-block staging requests rejected; existing owners retained\n",
           (unsigned long)rejected);
    return 0;
}
