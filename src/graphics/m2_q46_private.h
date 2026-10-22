// Exact Graphics-only Q46 product. Inputs have magnitude <= 2^46.
// Six 16-bit words retain the complete product; rounding is nearest/ties away.
#pragma once
#include <stdint.h>

static int64_t m2_multiply_q46(int64_t value, int64_t coefficient)
{
    uint64_t a = (uint64_t)(value < 0 ? -value : value);
    uint64_t b = (uint64_t)(coefficient < 0 ? -coefficient : coefficient);
    uint16_t a_words[3];
    uint16_t b_words[3];
    uint16_t product[6] = {0};
    for (uint8_t i = 0u; i < 3u; ++i)
    {
        a_words[i] = (uint16_t)a;
        b_words[i] = (uint16_t)b;
        a >>= 16u;
        b >>= 16u;
    }
    for (uint8_t i = 0u; i < 3u; ++i)
    {
        uint32_t carry = 0u;
        for (uint8_t j = 0u; j < 3u; ++j)
        {
            // (2^16-1)^2 + (2^16-1) + (2^16-1) = 2^32-1.
            uint32_t cell = (uint32_t)a_words[i] * b_words[j]
                + product[i + j] + carry;
            product[i + j] = (uint16_t)cell;
            carry = cell >> 16u;
#ifdef M2_Q46_OBSERVE
            // Test-only observation of actual cells/carries; absent on target.
            M2_Q46_OBSERVE(i, j, cell, carry, product);
#endif
        }
        product[i + 3u] = (uint16_t)carry;
    }
    uint64_t rounded = ((uint64_t)product[5] << 34u)
        | ((uint64_t)product[4] << 18u)
        | ((uint64_t)product[3] << 2u) | (product[2] >> 14u);
    // Bit 45 alone decides >= one half; lower bits remain in the full product.
    rounded += (product[2] >> 13u) & 1u;
    return (value < 0) != (coefficient < 0) ? -(int64_t)rounded : (int64_t)rounded;
}
