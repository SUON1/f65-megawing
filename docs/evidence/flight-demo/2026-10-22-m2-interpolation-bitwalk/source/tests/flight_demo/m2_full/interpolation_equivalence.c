// Direct old/new helper and independent integer-result comparison.
// The separate bit-state invariant supports the unchanged recurrence proof.
#include <assert.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>

#include "m2_geometry.c"

#define interpolate_delta m2_reference_interpolate_delta
#include "reference_interpolate.inc"
#undef interpolate_delta

static uint64_t read_u64(const unsigned char *bytes)
{
    uint64_t value = 0u;
    for (uint8_t byte = 0u; byte < 8u; ++byte)
    {
        value |= (uint64_t)bytes[byte] << (8u * byte);
    }
    return value;
}

static int64_t read_i64(const unsigned char *bytes)
{
    uint64_t value = read_u64(bytes);
    return value <= INT64_MAX ? (int64_t)value
        : -1 - (int64_t)(UINT64_MAX - value);
}

static void bit_state(uint64_t magnitude)
{
    uint64_t working = magnitude;
    for (uint8_t step = 0u; step < 64u; ++step)
    {
        assert(working == (magnitude << step));
        assert((working >> 63u)
            == ((magnitude >> (63u - step)) & UINT64_C(1)));
        working <<= 1u;
    }
    assert(working == 0u);
}

int main(int argc, char **argv)
{
    assert(argc == 2);
    FILE *stream = fopen(argv[1], "rb");
    assert(stream != 0);
    unsigned char record[32];
    uint64_t count = 0u;
    uint64_t negative = 0u;
    size_t bytes;
    while ((bytes = fread(record, 1u, sizeof(record), stream)) != 0u)
    {
        assert(bytes == sizeof(record));
        int64_t delta = read_i64(record);
        uint64_t numerator = read_u64(record + 8u);
        uint64_t denominator = read_u64(record + 16u);
        int64_t expected = read_i64(record + 24u);
        assert(delta != INT64_MIN);
        assert(denominator >= 1u && denominator <= ((UINT64_C(1) << 48u) - 1u) / 3u);
        assert(numerator <= denominator);
        int64_t original = m2_reference_interpolate_delta(
            delta, (int64_t)numerator, (int64_t)denominator);
        int64_t candidate = interpolate_delta(
            delta, (int64_t)numerator, (int64_t)denominator);
        assert(original == expected && candidate == expected);
        bit_state((uint64_t)(delta < 0 ? -delta : delta));
        negative += (uint64_t)(delta < 0);
        ++count;
    }
    assert(!ferror(stream) && fclose(stream) == 0);
    assert(count == UINT64_C(457334));
    printf("PASS %" PRIu64 " direct old/new/integer-oracle cases; "
           "%" PRIu64 " negative; %" PRIu64 " bit-state steps\n",
           count, negative, count * 64u);
    return EXIT_SUCCESS;
}
