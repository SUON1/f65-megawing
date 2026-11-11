// Private pinned-Xemu clock interpretation. No MMIO or public record layout.
#pragma once
#include <stdint.h>

#define M1_CLOCK_MODULUS UINT32_C(0xfffe0001)
#define M1_CLOCK_HALF_RANGE UINT32_C(0x80000000)

typedef struct
{
    uint32_t phase;
    uint32_t elapsed;
    uint8_t state; // 0: not initialized, 1: waiting for origin, 2: running.
    uint8_t fault;
} M1Clock;

static inline void m1_clock_reset(M1Clock *clock)
{
    clock->phase = 0u;
    clock->elapsed = 0u;
    clock->state = 1u;
    clock->fault = 0u;
}

// The caller must establish a gap below 2^31 native counts. A whole missed
// timer period aliases the same sample and cannot be detected here.
static inline uint32_t m1_clock_sample(M1Clock *clock, uint32_t raw,
                                      uint8_t sample_fault)
{
    if (clock->fault || sample_fault || (clock->state != 1u && clock->state != 2u))
    {
        clock->fault = 1u;
        return clock->elapsed;
    }
    uint32_t counters = ~raw;
    uint16_t a = (uint16_t)counters;
    uint16_t b = (uint16_t)(counters >> 16u);
    if (a == 0u || b == 0u)
    {
        clock->fault = 1u;
        return clock->elapsed;
    }
    uint32_t upper = (uint32_t)(65535u - b);
    uint32_t phase = (upper << 16u) - upper + (65535u - a);
    if (clock->state == 1u)
    {
        clock->phase = phase;
        clock->state = 2u;
        return clock->elapsed;
    }
    uint32_t delta = phase >= clock->phase ? phase - clock->phase
        : (M1_CLOCK_MODULUS - clock->phase) + phase;
    if (delta >= M1_CLOCK_HALF_RANGE)
    {
        clock->fault = 1u;
        return clock->elapsed;
    }
    clock->elapsed += delta;
    clock->phase = phase;
    return clock->elapsed;
}
