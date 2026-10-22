#include "camera.h"
#include "m2_geometry.h"

void m2_camera_reset(M2Camera *camera)
{
    M2Camera reset = {{{-4500L * M2_POSITION_SCALE, 0,
                        -300L * M2_POSITION_SCALE}}, 0, -5, 0, 1u};
    *camera = reset;
}

static int16_t direction(uint16_t pressed, uint8_t shift)
{
    return (int16_t)((int16_t)((pressed >> shift) & 1u)
                     - (int16_t)((pressed >> (shift + 1u)) & 1u));
}

uint8_t m2_camera_command(M2Camera *camera, uint16_t pressed)
{
    if (!m2_camera_valid(camera) || (pressed & 0xe000u) != 0u)
    {
        return 0u;
    }
    M2Camera next = *camera;
    if ((pressed & M2_CAMERA_RESET) != 0u)
    {
        m2_camera_reset(&next);
    }
    else
    {
        next.position.v[0] += direction(pressed, 0u) * (25L * M2_POSITION_SCALE);
        next.position.v[1] += direction(pressed, 2u) * (25L * M2_POSITION_SCALE);
        next.position.v[2] -= direction(pressed, 4u) * (10L * M2_POSITION_SCALE);
        next.yaw = (int16_t)((next.yaw + direction(pressed, 6u) + 360) % 360);
        next.pitch = (int16_t)(next.pitch + direction(pressed, 8u));
        next.roll = (int16_t)(next.roll + direction(pressed, 10u));
    }
    if (next.position.v[0] == camera->position.v[0]
        && next.position.v[1] == camera->position.v[1]
        && next.position.v[2] == camera->position.v[2]
        && next.yaw == camera->yaw && next.pitch == camera->pitch
        && next.roll == camera->roll)
    {
        return 1u;
    }
    if (camera->revision == UINT32_MAX || !m2_camera_valid(&next))
    {
        return 0u;
    }
    next.revision = camera->revision + 1u;
    *camera = next;
    return 2u;
}
