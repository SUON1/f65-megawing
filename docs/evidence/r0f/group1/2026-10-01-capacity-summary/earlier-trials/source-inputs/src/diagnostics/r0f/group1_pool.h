#ifndef R0FG1_POOL_H
#define R0FG1_POOL_H

#include <stdint.h>

// Caller-owned observation only; no pool storage or allocation policy.
// Native C state, not a public/serialized layout. Single foreground owner.
typedef struct
{
    uint16_t capacity;
    uint16_t peak;
    uint16_t samples;
    uint16_t full_samples;
} r0fg1_pool_observation;

// Explicitly start a new observation interval. Zero capacity is invalid.
uint8_t r0fg1_pool_init(r0fg1_pool_observation *state, uint16_t capacity);

// Observe an owner-supplied count. Invalid evidence leaves state unchanged.
// The caller must fail acquisition on zero; no retry/saturation is implied.
uint8_t r0fg1_pool_sample(r0fg1_pool_observation *state, uint16_t occupancy);

#endif
