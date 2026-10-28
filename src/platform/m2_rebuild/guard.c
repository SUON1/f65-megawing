#include <limits.h>

#include "guard.h"

uint8_t m2rb_guard(uint32_t now, uint32_t release,
                    uint32_t operation_bound, uint32_t guard_bound)
{
    if (operation_bound == 0u || guard_bound == 0u
        || operation_bound > UINT32_MAX - guard_bound)
    {
        return 0u;
    }
    uint32_t remaining = release - now;
    return (uint8_t)(remaining < 0x80000000UL
        && remaining > operation_bound + guard_bound);
}
