// Little-endian byte loops prevent repeated native wide-expression expansion.
// No hardware, global scratch, heap, recursion or public representation change.
#include <string.h>

#include "m2_limb.h"

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
