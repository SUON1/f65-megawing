// Compile against the archived original geometry, before product replacement.
#include <assert.h>
#include <stdio.h>
#include "m2_q46_private.h"
#include M2_BASELINE_SOURCE

static uint64_t seed = 0x6500cafe12345678ULL;
static uint64_t random_bits(void)
{
    seed ^= seed << 13u;
    seed ^= seed >> 7u;
    seed ^= seed << 17u;
    return seed;
}

static unsigned cases;
static void check(int64_t a, int64_t b)
{
    assert(m2_multiply_q46(a, b) == multiply_rotation(a, b));
    ++cases;
}

int main(void)
{
    const int64_t scale = 1LL << 46u;
    const int64_t edges[] = {0, 1, -1, scale, -scale, scale - 1, 1 - scale,
        1LL << 45u, -(1LL << 45u), (1LL << 23u) - 1, 1LL << 23u,
        (1LL << 23u) + 1};
    for (unsigned i = 0u; i < sizeof(edges) / sizeof(edges[0]); ++i)
    {
        for (unsigned j = 0u; j < sizeof(edges) / sizeof(edges[0]); ++j)
        {
            check(edges[i], edges[j]);
        }
    }
    for (unsigned i = 0u; i <= 90u; ++i)
    {
        for (unsigned j = 0u; j <= 90u; ++j)
        {
            check(m2_sine_q46[i], m2_sine_q46[j]);
            check(-m2_sine_q46[i], m2_sine_q46[j]);
        }
    }
    for (unsigned i = 0u; i < 200000u; ++i)
    {
        int64_t a = (int64_t)(random_bits() % (uint64_t)(scale + 1));
        int64_t b = (int64_t)(random_bits() % (uint64_t)(scale + 1));
        if ((i & 1u) != 0u)
        {
            a = -a;
        }
        if ((i & 2u) != 0u)
        {
            b = -b;
        }
        check(a, b);
    }
    printf("PASS exact archived general-ratio equivalence: %u cases\n", cases);
    return 0;
}
