#ifndef R0FG1_POOL_OWNERS_H
#define R0FG1_POOL_OWNERS_H

#include "r0f_group1_pool.h"
#include <stdint.h>

// One foreground observation interval spanning returning storage.
// Encoding is field-wise private trace data, never native struct packing.
uint8_t r0fg1_owners_begin(void);
void r0fg1_owner_sample(uint8_t owner, uint16_t occupancy);
uint16_t r0fg1_owner_peak(uint8_t owner);
void r0fg1_owners_encode(uint8_t bytes[R0FG1_POOL_EPOCH_BYTES]);

#endif
