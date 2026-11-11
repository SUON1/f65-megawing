#include <limits.h>

#include "guard.h"

uint16_t m2rb_guard(uint32_t now, uint32_t release,
                     uint32_t operation_bound, uint32_t guard_bound)
{
    if (operation_bound == 0u || operation_bound > UINT16_MAX || guard_bound == 0u
        || operation_bound > UINT32_MAX - guard_bound)
    {
        return 0u;
    }
    uint32_t remaining = release - now;
    if (remaining >= 0x80000000UL || remaining <= operation_bound + guard_bound)
    {
        return 0u;
    }
    // Preserve a strict margin even when the batch spends its full grant.
    uint32_t spendable = remaining - guard_bound - 1u;
    return spendable > UINT16_MAX ? UINT16_MAX : (uint16_t)spendable;
}
