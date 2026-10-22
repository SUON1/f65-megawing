// Exact Graphics-only Q46 product. Inputs have magnitude <= 2^46.
// Five limb products avoid a 94-bit intermediate and preserve ties-away rounding.
#pragma once
#include <stdint.h>

static int64_t m2_multiply_q46(int64_t value, int64_t coefficient)
{
    const uint64_t mask = (1ULL << 23u) - 1u;
    uint64_t a = (uint64_t)(value < 0 ? -value : value);
    uint64_t b = (uint64_t)(coefficient < 0 ? -coefficient : coefficient);
    uint64_t a_low = a & mask;
    uint64_t b_low = b & mask;
    uint64_t a_high = a >> 23u;
    uint64_t b_high = b >> 23u;
    uint64_t cross = a_low * b_high + a_high * b_low;
    uint64_t low = a_low * b_low + ((cross & mask) << 23u) + (1ULL << 45u);
    uint64_t rounded = a_high * b_high + (cross >> 23u) + (low >> 46u);
    return (value < 0) != (coefficient < 0) ? -(int64_t)rounded : (int64_t)rounded;
}
