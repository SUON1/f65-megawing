// Diagnostics owns the requested presentation-only camera and its identity.
#pragma once
#include "m2_geometry.h"
#include "m2_rebuild_input.h"

void m2rb_camera_init(M2Camera *camera);
// -1 invalid/exhausted, 0 no change, 1 changed. Failure preserves the camera.
int8_t m2rb_camera_edges(M2Camera *camera, uint16_t edges);
uint8_t m2rb_camera_equal(const M2Camera *first, const M2Camera *last);
