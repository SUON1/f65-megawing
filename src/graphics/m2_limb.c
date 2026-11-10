// Little-endian byte loops prevent repeated native wide-expression expansion.
// No global scratch, heap, recursion or public representation change.
#include <string.h>

#include "m2_limb.h"
#ifdef M2_EXACT_WIDE
#include "../platform/m2_rebuild/wide_math.h"
#endif

void m2w_i32(M2Wide out, int32_t value)
{
    uint32_t bits = (uint32_t)value;
    for (uint8_t i = 0u; i < 8u; ++i)
    {
        out[i] = i < 4u ? (uint8_t)bits : (value < 0 ? 255u : 0u);
        bits >>= 8u;
    }
}

void m2w_negate(uint8_t *value, uint8_t count)
{
    uint16_t carry = 1u;
    for (uint8_t i = 0u; i < count; ++i)
    {
        carry += (uint8_t)~value[i];
        value[i] = (uint8_t)carry;
        carry >>= 8u;
    }
}

void m2w_add(M2Wide out, const M2Wide a, const M2Wide b, uint8_t subtract)
{
    uint16_t carry = subtract;
    for (uint8_t i = 0u; i < 8u; ++i)
    {
        carry += (uint16_t)a[i] + (subtract ? (uint8_t)~b[i] : b[i]);
        out[i] = (uint8_t)carry;
        carry >>= 8u;
    }
}

void m2w_double(M2Wide value)
{
    m2w_add(value, value, value, 0u);
}

int8_t m2w_compare(const M2Wide a, const M2Wide b)
{
    if ((a[7] ^ b[7]) & 128u)
    {
        return a[7] & 128u ? -1 : 1;
    }
    for (uint8_t i = 8u; i != 0u; --i)
    {
        if (a[i - 1u] != b[i - 1u])
        {
            return a[i - 1u] < b[i - 1u] ? -1 : 1;
        }
    }
    return 0;
}

uint8_t m2w_positive(const M2Wide value)
{
    M2Wide zero = {0};
    return (uint8_t)(m2w_compare(value, zero) > 0);
}

uint8_t m2w_narrow(const M2Wide value, int32_t *out)
{
    uint8_t sign = value[3] & 128u ? 255u : 0u;
    for (uint8_t i = 4u; i < 8u; ++i)
    {
        if (value[i] != sign)
        {
            return 0u;
        }
    }
    uint32_t bits = 0u;
    for (uint8_t i = 4u; i != 0u; --i)
    {
        bits = (bits << 8u) | value[i - 1u];
    }
    memcpy(out, &bits, sizeof(bits));
    return 1u;
}

static uint8_t magnitude(uint8_t out[6], const M2Wide value)
{
    uint8_t sign = value[5] & 128u ? 255u : 0u;
    if (value[6] != sign || value[7] != sign)
    {
        return 0u;
    }
    memcpy(out, value, 6u);
    if (sign != 0u)
    {
        m2w_negate(out, 6u);
    }
    return 1u;
}

uint8_t m2l_multiply(M2LimbJob *job, const M2Wide a, const M2Wide b,
                      uint8_t shift)
{
    job->phase = 255u;
    if ((shift != 0u && shift != 46u && shift != 255u)
        || !magnitude(job->a, a) || !magnitude(job->b, b))
    {
        return 0u;
    }
    memset(job->product, 0, sizeof(job->product));
    job->negative = (uint8_t)(((a[7] ^ b[7]) & 128u) != 0u);
    job->row = 0u;
    job->shift = shift;
    job->phase = 1u;
    return 1u;
}

static uint8_t finish(M2LimbJob *job, const uint8_t *source, uint8_t round)
{
    uint8_t shift_bytes = (uint8_t)(job->shift / 8u);
    uint8_t shift_bits = (uint8_t)(job->shift % 8u);
    uint16_t carry = round;
    for (uint8_t i = 0u; i < 12u; ++i)
    {
        uint8_t index = (uint8_t)(i + shift_bytes);
        uint16_t cell = index < 12u ? source[index] : 0u;
        if (index + 1u < 12u)
        {
            cell |= (uint16_t)source[index + 1u] << 8u;
        }
        carry += (uint8_t)(cell >> shift_bits);
        if (i < 8u)
        {
            job->value[i] = (uint8_t)carry;
        }
        else if ((uint8_t)carry != 0u)
        {
            return 0u;
        }
        carry >>= 8u;
    }
    if (carry)
    {
        return 0u;
    }
    if (job->value[7] & 128u)
    {
        if (!job->negative || job->value[7] != 128u)
        {
            return 0u;
        }
        for (uint8_t i = 0u; i < 7u; ++i)
        {
            if (job->value[i] != 0u)
            {
                return 0u;
            }
        }
    }
    if (job->negative)
    {
        m2w_negate(job->value, 8u);
    }
    job->phase = 0u;
    return 1u;
}

#ifndef M2_EXACT_WIDE
uint8_t m2l_divide(M2LimbJob *job, const M2Wide denominator)
{
    job->phase = 255u;
    if (!m2w_positive(denominator) || !magnitude(job->b, denominator))
    {
        return 0u;
    }
    memset(job->remainder, 0, sizeof(job->remainder));
    memset(job->quotient, 0, sizeof(job->quotient));
    job->bit = 96u;
    job->shift = 0u;
    job->phase = 2u;
    return 1u;
}

static uint8_t remainder_ge(const M2LimbJob *job)
{
    if (job->remainder[6] != 0u)
    {
        return 1u;
    }
    for (uint8_t i = 6u; i != 0u; --i)
    {
        if (job->remainder[i - 1u] != job->b[i - 1u])
        {
            return (uint8_t)(job->remainder[i - 1u] > job->b[i - 1u]);
        }
    }
    return 1u;
}

static void remainder_double(M2LimbJob *job, uint8_t carry)
{
    for (uint8_t i = 0u; i < 7u; ++i)
    {
        uint16_t cell = (uint16_t)((uint16_t)job->remainder[i] * 2u + carry);
        job->remainder[i] = (uint8_t)cell;
        carry = (uint8_t)(cell >> 8u);
    }
}

int8_t m2l_service(M2LimbJob *job)
{
    if (job->phase > 2u)
    {
        return -1;
    }
    if (job->phase == 1u)
    {
        uint16_t carry = 0u;
        uint8_t i = job->row;
        for (uint8_t j = 0u; j < 6u; ++j)
        {
            // 255*255 + 255 + 255 = 65535: full cell and carry are exact.
            uint16_t cell = (uint16_t)((uint16_t)job->a[i] * job->b[j]
                + job->product[i + j] + carry);
            job->product[i + j] = (uint8_t)cell;
            carry = cell >> 8u;
        }
        job->product[i + 6u] = (uint8_t)carry;
        if (++job->row == 6u)
        {
            if (job->shift == 255u)
            {
                job->phase = 0u;
            }
            else
            {
                uint8_t round = job->shift == 46u
                    ? (uint8_t)((job->product[5] >> 5u) & 1u) : 0u;
                if (!finish(job, job->product, round))
                {
                    job->phase = 255u;
                }
            }
        }
    }
    else if (job->phase == 2u)
    {
        --job->bit;
        uint8_t byte = (uint8_t)(job->bit / 8u);
        uint8_t bit = (uint8_t)(job->bit % 8u);
        remainder_double(job, (uint8_t)((job->product[byte] >> bit) & 1u));
        if (remainder_ge(job))
        {
            uint16_t carry = 1u;
            for (uint8_t i = 0u; i < 7u; ++i)
            {
                carry += (uint16_t)job->remainder[i]
                    + (i < 6u ? (uint8_t)~job->b[i] : 255u);
                job->remainder[i] = (uint8_t)carry;
                carry >>= 8u;
            }
            job->quotient[byte] |= (uint8_t)(1u << bit);
        }
        if (job->bit == 0u)
        {
            remainder_double(job, 0u);
            if (!finish(job, job->quotient, remainder_ge(job)))
            {
                job->phase = 255u;
            }
        }
    }
    return job->phase == 255u ? -1 : (int8_t)(job->phase == 0u);
}
#else

// Each normalized radix-2^24 step works on a 72-bit window. The divisor
// always has 48 bits with its high bit set. All buffers are Graphics-owned.
#define DIGIT_BYTES 3u
#define DIVISOR_BYTES 6u
#define WINDOW_BYTES 9u

static uint8_t finish_multiply(M2LimbJob *job)
{
    if (job->shift == 255u)
    {
        job->phase = 0u;
        return 1u;
    }
    uint8_t round = job->shift == 46u
        ? (uint8_t)((job->product[5] >> 5u) & 1u) : 0u;
    return finish(job, job->product, round);
}

// Carry out is one for unsigned subtraction without borrow.
static uint8_t accumulate(uint8_t *out, uint8_t width, const uint8_t *part,
                          uint8_t count, uint8_t subtract)
{
    uint16_t carry = subtract;
    for (uint8_t i = 0u; i < width; ++i)
    {
        uint8_t byte = i < count ? part[i] : 0u;
        if (subtract)
        {
            byte = (uint8_t)~byte;
        }
        carry += (uint16_t)out[i] + byte;
        out[i] = (uint8_t)carry;
        carry >>= 8u;
    }
    return (uint8_t)carry;
}

static uint8_t multiply_part(M2LimbJob *job)
{
    uint8_t left_high = (uint8_t)(job->row & 1u);
    uint8_t right_high = (uint8_t)(job->row >> 1u);
    uint8_t left[4] = {0};
    uint8_t right[4] = {0};
    memcpy(left, job->a + 4u * left_high, left_high ? 2u : 4u);
    memcpy(right, job->b + 4u * right_high, right_high ? 2u : 4u);
    uint8_t part[8];
    if (!m2rb_math_product(part, left, right))
    {
        return 0u;
    }
    uint8_t offset = (uint8_t)(4u * (left_high + right_high));
    uint8_t width = (uint8_t)(12u - offset);
    if (width == 4u && (part[4] | part[5] | part[6] | part[7]) != 0u)
    {
        return 0u;
    }
    return (uint8_t)!accumulate(job->product + offset, width, part, 8u, 0u);
}

// Shift from high to low so input and output may occupy the same storage.
// The caller supplies a leading zero byte whenever there could be a carry.
static void normalize(uint8_t *bytes, uint8_t count, uint8_t whole, uint8_t bits)
{
    uint8_t i = (uint8_t)(count - 1u);
    uint16_t shifted = (uint16_t)((uint16_t)bytes[i] << bits);
    while (i != 0u)
    {
        uint16_t lower = (uint16_t)((uint16_t)bytes[i - 1u] << bits);
        bytes[i + whole] = (uint8_t)(shifted | (lower >> 8u));
        shifted = lower;
        --i;
    }
    bytes[whole] = (uint8_t)shifted;
    memset(bytes, 0, whole);
}

static uint8_t remainder_ge(const uint8_t *window, const uint8_t *divisor)
{
    if ((window[6] | window[7] | window[8]) != 0u)
    {
        return 1u;
    }
    for (uint8_t i = DIVISOR_BYTES; i != 0u; --i)
    {
        if (window[i - 1u] != divisor[i - 1u])
        {
            return (uint8_t)(window[i - 1u] > divisor[i - 1u]);
        }
    }
    return 1u;
}

uint8_t m2l_divide(M2LimbJob *job, const M2Wide denominator)
{
    job->phase = 255u;
    if (!m2w_positive(denominator) || !magnitude(job->b, denominator))
    {
        return 0u;
    }
    uint8_t used = DIVISOR_BYTES;
    while (job->b[used - 1u] == 0u)
    {
        --used;
    }
    uint8_t top = job->b[used - 1u];
    uint8_t bits = 0u;
    while ((top & 128u) == 0u)
    {
        top = (uint8_t)(top << 1u);
        ++bits;
    }
    uint8_t whole = (uint8_t)(DIVISOR_BYTES - used);
    normalize(job->b, used, whole, bits);
    memset(job->product + 12u, 0, 6u);
    normalize(job->product, 13u, whole, bits);
    memset(job->quotient, 0, sizeof(job->quotient));
    // At most four quotient digits for a 96-bit product. Leading zero
    // windows require no math transactions. The last digit handles zero.
    job->bit = 3u;
    while (job->bit != 0u
           && !remainder_ge(job->product + job->bit * DIGIT_BYTES, job->b))
    {
        --job->bit;
    }
    job->shift = 0u;
    job->phase = 2u;
    return 1u;
}

static uint8_t subtract_product(uint8_t *window, const uint8_t *digit,
                                const uint8_t *divisor, uint8_t *borrow)
{
    uint8_t part[8];
    uint8_t high[4] = {divisor[4], divisor[5], 0u, 0u};
    if (!m2rb_math_product(part, digit, divisor))
    {
        return 0u;
    }
    uint8_t low_carry = accumulate(window, WINDOW_BYTES, part, 8u, 1u);
    if (!m2rb_math_product(part, digit, high))
    {
        return 0u;
    }
    uint8_t high_carry = accumulate(window + 4u, 5u, part, 5u, 1u);
    *borrow = (uint8_t)!(low_carry & high_carry);
    return 1u;
}

static uint8_t divide_digit(M2LimbJob *job, uint8_t offset)
{
    uint8_t *window = job->product + offset;
    uint8_t digit[4];
    if (!m2rb_math_q24(digit, window + 5u, job->b + 2u) || digit[3] > 1u)
    {
        return 0u;
    }
    if (digit[3] != 0u)
    {
        memset(digit, 255, DIGIT_BYTES);
        digit[3] = 0u;
    }
    uint8_t borrow;
    if (!subtract_product(window, digit, job->b, &borrow))
    {
        return 0u;
    }
    // The estimate differs by at most one. Check the correction and the
    // resulting remainder before exposing any quotient digit to the caller.
    static const uint8_t one[1] = {1u};
    if (borrow)
    {
        if (!accumulate(window, WINDOW_BYTES, job->b, DIVISOR_BYTES, 0u)
            || !accumulate(digit, DIGIT_BYTES, one, 1u, 1u))
        {
            return 0u;
        }
    }
    else if (remainder_ge(window, job->b))
    {
        if (!accumulate(window, WINDOW_BYTES, job->b, DIVISOR_BYTES, 1u)
            || accumulate(digit, DIGIT_BYTES, one, 1u, 0u))
        {
            return 0u;
        }
    }
    if (remainder_ge(window, job->b))
    {
        return 0u;
    }
    memcpy(job->quotient + offset, digit, DIGIT_BYTES);
    return 1u;
}

int8_t m2l_service(M2LimbJob *job)
{
    uint8_t ok = 0u;
    if (job->phase == 0u)
    {
        return 1;
    }
    if (job->phase == 1u && job->row < 4u)
    {
        ok = multiply_part(job);
        if (ok && ++job->row == 4u)
        {
            ok = finish_multiply(job);
        }
    }
    else if (job->phase == 2u && job->bit < 4u)
    {
        ok = divide_digit(job, (uint8_t)(job->bit * DIGIT_BYTES));
        if (ok && job->bit == 0u)
        {
            // The remainder occupies only six bytes after correction.
            job->product[6] = accumulate(job->product, DIVISOR_BYTES,
                                        job->product, DIVISOR_BYTES, 0u);
            ok = finish(job, job->quotient, remainder_ge(job->product, job->b));
        }
        else if (ok)
        {
            --job->bit;
        }
    }
    if (!ok)
    {
        job->phase = 255u;
        return -1;
    }
    return (int8_t)(job->phase == 0u);
}
#endif
