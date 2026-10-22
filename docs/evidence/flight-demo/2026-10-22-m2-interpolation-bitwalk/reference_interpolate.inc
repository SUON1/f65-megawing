static int64_t interpolate_delta(int64_t delta, int64_t numerator,
                                  int64_t denominator)
{
    uint64_t magnitude = (uint64_t)(delta < 0 ? -delta : delta);
    uint64_t divisor = (uint64_t)denominator;
    uint64_t fraction = (uint64_t)numerator;
    uint64_t quotient = 0u;
    uint64_t remainder = 0u;
    for (uint8_t bit = 64u; bit != 0u; --bit)
    {
        quotient *= 2u;
        remainder *= 2u;
        if (((magnitude >> (bit - 1u)) & 1u) != 0u)
        {
            remainder += fraction;
        }
        for (uint8_t subtraction = 0u; subtraction < 2u; ++subtraction)
        {
            if (remainder >= divisor)
            {
                remainder -= divisor;
                ++quotient;
            }
        }
    }
    if (remainder >= (divisor + 1u) / 2u)
    {
        ++quotient;
    }
    return delta < 0 ? -(int64_t)quotient : (int64_t)quotient;
}
