// Graphics-private exact integers. Public Q12/Q24/Q46/Q16 records are unchanged.
#pragma once
#include <stdint.h>

typedef uint8_t M2Wide[8];

typedef struct
{
    uint8_t a[6];
    uint8_t b[6];
    uint8_t product[12];
    uint8_t remainder[7];
    uint8_t quotient[12];
    M2Wide value;
    uint8_t phase;
    uint8_t row;
    uint8_t bit;
    uint8_t negative;
    uint8_t shift;
} M2LimbJob;

void m2w_i32(M2Wide out, int32_t value);
void m2w_add(M2Wide out, const M2Wide a, const M2Wide b, uint8_t subtract);
void m2w_negate(uint8_t *value, uint8_t count);
void m2w_double(M2Wide value);
int8_t m2w_compare(const M2Wide a, const M2Wide b);
uint8_t m2w_positive(const M2Wide value);
uint8_t m2w_narrow(const M2Wide value, int32_t *out);
// Inputs must be signed48, but the complete product is retained in 96 bits.
// shift=255 retains that product for a subsequent divide; otherwise rounds it.
uint8_t m2l_multiply(M2LimbJob *job, const M2Wide a, const M2Wide b,
                      uint8_t shift);
uint8_t m2l_divide(M2LimbJob *job, const M2Wide denominator);
// One six-cell multiplication row or one restoring-division bit. -1 is fault.
int8_t m2l_service(M2LimbJob *job);
