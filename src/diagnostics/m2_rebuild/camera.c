#include <limits.h>

#include "camera.h"

void m2rb_camera_init(M2Camera *camera)
{
    camera->position.v[0] = -4500L * M2_POSITION_SCALE;
    camera->position.v[1] = 0;
    camera->position.v[2] = -300L * M2_POSITION_SCALE;
    camera->yaw = 0;
    camera->pitch = -5;
    camera->roll = 0;
    camera->revision = 1u;
}

uint8_t m2rb_camera_equal(const M2Camera *first, const M2Camera *last)
{
    if (first->revision != last->revision || first->yaw != last->yaw
        || first->pitch != last->pitch || first->roll != last->roll)
    {
        return 0u;
    }
    for (uint8_t axis = 0u; axis < 3u; ++axis)
    {
        if (first->position.v[axis] != last->position.v[axis])
        {
            return 0u;
        }
    }
    return 1u;
}

static int8_t direction(uint16_t edges, uint16_t plus, uint16_t minus)
{
    return (int8_t)(((edges & plus) != 0u) - ((edges & minus) != 0u));
}

static int32_t clamp(int32_t value, int32_t minimum, int32_t maximum)
{
    if (value < minimum)
    {
        return minimum;
    }
    return value > maximum ? maximum : value;
}

int8_t m2rb_camera_edges(M2Camera *camera, uint16_t edges)
{
    if (!m2_camera_valid(camera))
    {
        return -1;
    }
    M2Camera next = *camera;
    if ((edges & M2RB_RESET) != 0u)
    {
        m2rb_camera_init(&next);
    }
    else
    {
        next.position.v[0] = clamp(next.position.v[0]
            + (int32_t)direction(edges, M2RB_NORTH, M2RB_SOUTH)
                * 25L * M2_POSITION_SCALE,
            -M2_NORTH_LIMIT_FT * M2_POSITION_SCALE,
            M2_NORTH_LIMIT_FT * M2_POSITION_SCALE);
        next.position.v[1] = clamp(next.position.v[1]
            + (int32_t)direction(edges, M2RB_EAST, M2RB_WEST)
                * 25L * M2_POSITION_SCALE,
            -M2_EAST_LIMIT_FT * M2_POSITION_SCALE,
            M2_EAST_LIMIT_FT * M2_POSITION_SCALE);
        next.position.v[2] = clamp(next.position.v[2]
            + (int32_t)direction(edges, M2RB_DOWN, M2RB_UP)
                * 10L * M2_POSITION_SCALE,
            -M2_HEIGHT_MAX_FT * M2_POSITION_SCALE,
            -M2_HEIGHT_MIN_FT * M2_POSITION_SCALE);
        next.yaw = (int16_t)((next.yaw
            + direction(edges, M2RB_YAW_RIGHT, M2RB_YAW_LEFT) + 360) % 360);
        next.pitch = (int16_t)clamp(next.pitch
            + direction(edges, M2RB_PITCH_UP, M2RB_PITCH_DOWN),
            -M2_TILT_LIMIT_DEG, M2_TILT_LIMIT_DEG);
        next.roll = (int16_t)clamp(next.roll
            + direction(edges, M2RB_ROLL_RIGHT, M2RB_ROLL_LEFT),
            -M2_TILT_LIMIT_DEG, M2_TILT_LIMIT_DEG);
    }
    next.revision = camera->revision;
    if (m2rb_camera_equal(camera, &next))
    {
        return 0;
    }
    if (camera->revision == UINT32_MAX)
    {
        return -1;
    }
    next.revision++;
    *camera = next;
    return 1;
}
