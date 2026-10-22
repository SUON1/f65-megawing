// Diagnostics owns requested camera; commands are semantic press edges.
#pragma once
#include "m2_pr1.h"

enum M2CameraCommand
{
    M2_NORTH_PLUS = 1u, M2_NORTH_MINUS = 2u,
    M2_EAST_PLUS = 4u, M2_EAST_MINUS = 8u,
    M2_HEIGHT_PLUS = 16u, M2_HEIGHT_MINUS = 32u,
    M2_YAW_PLUS = 64u, M2_YAW_MINUS = 128u,
    M2_PITCH_PLUS = 256u, M2_PITCH_MINUS = 512u,
    M2_ROLL_PLUS = 1024u, M2_ROLL_MINUS = 2048u,
    M2_CAMERA_RESET = 4096u
};
void m2_camera_reset(M2Camera *camera);
// 0 rejected, 1 unchanged, 2 changed. Rejected steps leave camera unchanged.
uint8_t m2_camera_command(M2Camera *camera, uint16_t pressed);
