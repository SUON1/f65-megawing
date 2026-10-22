// Pure deadline policy; bounds and clock units must come from actual admission.
#pragma once
#include <stdint.h>

typedef struct
{
    uint32_t release;
    uint16_t fraction;
} M2Dispatch;

uint8_t m2_dispatch_allows(uint32_t now, uint32_t release,
                           uint32_t service_bound, uint32_t return_margin);
void m2_dispatch_next(M2Dispatch *dispatch, uint32_t period_q16);
