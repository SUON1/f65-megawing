#include "dispatch.h"

uint8_t m2_dispatch_allows(uint32_t now, uint32_t release,
                           uint32_t service_bound, uint32_t return_margin)
{
    uint32_t remaining = release - now;
    if (remaining == 0u || remaining >= 0x80000000ul
        || service_bound == 0u || return_margin == 0u
        || service_bound > UINT32_MAX - return_margin)
    {
        return 0u;
    }
    return (uint8_t)(remaining >= service_bound + return_margin);
}

void m2_dispatch_next(M2Dispatch *dispatch, uint32_t period_q16)
{
    uint32_t carry = (uint32_t)dispatch->fraction + (period_q16 & 65535u);
    dispatch->release += (period_q16 >> 16u) + (carry >> 16u);
    dispatch->fraction = (uint16_t)carry;
}
