// Foreground-only, canonical MEGA65 I/O. No MAP/B, CPU-port, interrupt-mask,
// DMA, callback or scheduler changes. The IRQ/NMI paths never use this file.
// The ordinary C ABI applies. The owner byte stays locked until reset on fault.
#include <string.h>

#include "wide_math.h"
#include "m1_platform.h"

#define MATH_STATUS 0xd70fu
#define MATH_BUSY_MASK 0xc0u
#define MATH_LEFT 0xd770u
#define MATH_RIGHT 0xd774u
#define MATH_PRODUCT 0xd778u
// Bytes 1..4 of the unsigned Q32.32 quotient give floor(left * 2^24 / right).
#define MATH_QUOTIENT_Q24 0xd769u
#define MATH_POLL_LIMIT 8u

#ifdef M2_MATH_HOST_BUS
uint8_t m2math_bus_read(uint16_t address);
void m2math_bus_write(uint16_t address, uint8_t value);
#define MATH_READ(address) m2math_bus_read((uint16_t)(address))
#define MATH_WRITE(address, value) m2math_bus_write((uint16_t)(address), (value))
#else
#define MATH_READ(address) (*(volatile uint8_t *)(uintptr_t)(address))
#define MATH_WRITE(address, value) (MATH_READ(address) = (value))
#endif

enum
{
    MATH_IDLE,
    MATH_ACTIVE,
    MATH_LOCKED
};

static uint8_t math_owner;

static uint8_t math_ready(void)
{
    for (uint8_t i = 0u; i < MATH_POLL_LIMIT; ++i)
    {
        if ((MATH_READ(MATH_STATUS) & MATH_BUSY_MASK) == 0u)
        {
            return 1u;
        }
    }
    return 0u;
}

static uint8_t math_transact(uint8_t *out, const uint8_t *left, const uint8_t *right,
                             uint8_t quotient)
{
    if (math_owner != MATH_IDLE || m1_platform_fault()
        || (MATH_READ(MATH_STATUS) & MATH_BUSY_MASK) != 0u)
    {
        math_owner = MATH_LOCKED;
        return 0u;
    }
    math_owner = MATH_ACTIVE;
    for (uint8_t i = 0u; i < 4u; ++i)
    {
        MATH_WRITE(MATH_LEFT + i, left[i]);
        MATH_WRITE(MATH_RIGHT + i, right[i]);
    }
    if (!math_ready())
    {
        math_owner = MATH_LOCKED;
        return 0u;
    }
    uint8_t result[8];
    uint8_t count = quotient ? 4u : 8u;
    if (quotient)
    {
        for (uint8_t i = 0u; i < 4u; ++i)
        {
            result[i] = MATH_READ(MATH_QUOTIENT_Q24 + i);
        }
    }
    else
    {
        for (uint8_t i = 0u; i < 8u; ++i)
        {
            result[i] = MATH_READ(MATH_PRODUCT + i);
        }
    }
    if (math_owner != MATH_ACTIVE || m1_platform_fault())
    {
        math_owner = MATH_LOCKED;
        return 0u;
    }
    memcpy(out, result, count);
    math_owner = MATH_IDLE;
    return 1u;
}

uint8_t m2rb_math_product(uint8_t out[8], const uint8_t left[4],
                         const uint8_t right[4])
{
    return math_transact(out, left, right, 0u);
}

uint8_t m2rb_math_q24(uint8_t out[4], const uint8_t left[4],
                     const uint8_t right[4])
{
    if ((right[3] & 128u) == 0u)
    {
        return 0u;
    }
    return math_transact(out, left, right, 1u);
}
