#ifndef R0FG1_SCENE_H
#define R0FG1_SCENE_H

#include "group1_presentation.h"

// Private deterministic scene behind the actual display owner. No hardware.
uint8_t r0fg1_scene_bind(r0fg1_presentation *state, uint16_t source_tick,
                        uint8_t buffer);
uint8_t r0fg1_scene_encode(r0fg1_presentation *state,
                          uint8_t pixels[R0FG1P_SCENE_BYTES]);

#endif
