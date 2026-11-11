// Private M2 Platform seam. Only ordinary little-endian bytes cross it.
#pragma once
#include <stdint.h>

// Unsigned full 32 x 32 product. A fault returns zero without writing out.
uint8_t m2rb_math_product(uint8_t out[8], const uint8_t left[4],
                         const uint8_t right[4]);
// floor((left << 24) / right), for right >= 2^31. Same failure contract.
uint8_t m2rb_math_q24(uint8_t out[4], const uint8_t left[4],
                     const uint8_t right[4]);
