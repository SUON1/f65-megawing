#ifndef R0FG1_GEOMETRY_FIXTURE_H
#define R0FG1_GEOMETRY_FIXTURE_H

#include <stdint.h>

// Actual bounded byte-record storage, not production face/vertex layouts.
// Claim, populate, consume into the scene CRC, then release on each attempt.
uint32_t r0fg1_geometry_fixture(uint16_t generation, uint16_t source_tick);

#endif
