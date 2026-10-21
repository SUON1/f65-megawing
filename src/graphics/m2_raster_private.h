// Graphics implementation workspace only: not serialized, a public ABI or
// registration state. The integration probe allocates it to measure real size.
#pragma once
#include <stdint.h>

struct M2RasterCursor
{
    int16_t x;
    int16_t y;
    int16_t dx;
    int16_t dy;
    int16_t step_x;
    int16_t step_y;
    int16_t error;
    uint16_t remaining;
};
