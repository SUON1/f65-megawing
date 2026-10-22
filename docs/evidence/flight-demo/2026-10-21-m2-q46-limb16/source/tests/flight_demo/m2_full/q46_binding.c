#include <stdint.h>
#include <string.h>

static uint16_t *observed_words;
static uint32_t *observed_cells;
static uint32_t *observed_carries;

static void observe(uint8_t i, uint8_t j, uint32_t cell, uint32_t carry,
                      const uint16_t product[6])
{
    if (observed_words != 0)
    {
        uint8_t step = (uint8_t)(i * 3u + j);
        memcpy(observed_words + step * 6u, product, 6u * sizeof(uint16_t));
        observed_cells[step] = cell;
        observed_carries[step] = carry;
    }
}
#define M2_Q46_OBSERVE(i, j, cell, carry, product) observe(i, j, cell, carry, product)
#include "m2_q46_private.h"

int64_t m2_test_q46(int64_t a, int64_t b)
{
    return m2_multiply_q46(a, b);
}

int64_t m2_test_q46_trace(int64_t a, int64_t b, uint16_t *words,
                          uint32_t *cells, uint32_t *carries)
{
    observed_words = words;
    observed_cells = cells;
    observed_carries = carries;
    int64_t result = m2_multiply_q46(a, b);
    observed_words = 0;
    return result;
}
