// Environment owns the canonical synthetic runway, in Q12 feet.
#pragma once
#include "m2_pr1.h"

uint8_t m2_fixture_segment(uint32_t revision, uint8_t index,
                           M2Point *first, M2Point *last);
uint8_t m2_surface_query(uint32_t revision, const M2Point *point,
                         M2Surface *surface);
uint8_t m2_point_valid(const M2Point *point);
