// Exact private record field operations; never a new public record layout.
#pragma once
#include "m2_pr1.h"

struct M2RebuildRenderer;
uint8_t m2_camera_same(const M2Camera *first, const M2Camera *last);
// compare=0 constructs; compare=1 verifies without writing; other modes fail.
uint8_t m2_bundle_fields(struct M2RebuildRenderer *renderer, uint8_t compare);
