#include <limits.h>

#include "camera.h"
#include "m2_record_private.h"

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
    return m2_camera_same(first, last);
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
        static const int32_t minimum[3] = {
            -M2_NORTH_LIMIT_FT * M2_POSITION_SCALE,
            -M2_EAST_LIMIT_FT * M2_POSITION_SCALE,
            -M2_HEIGHT_MAX_FT * M2_POSITION_SCALE
        };
        static const int32_t maximum[3] = {
            M2_NORTH_LIMIT_FT * M2_POSITION_SCALE,
            M2_EAST_LIMIT_FT * M2_POSITION_SCALE,
            -M2_HEIGHT_MIN_FT * M2_POSITION_SCALE
        };
        uint16_t pairs = edges;
        for (uint8_t axis = 0u; axis < 3u; ++axis)
        {
            int8_t direction = (int8_t)(((pairs & 1u) != 0u) - ((pairs & 2u) != 0u));
            if (axis == 2u)
            {
                direction = (int8_t)-direction;
            }
            int32_t step = (axis == 2u ? 10L : 25L) * M2_POSITION_SCALE;
            int32_t value = next.position.v[axis];
            if (direction > 0)
            {
                value += step;
            }
            else if (direction < 0)
            {
                value -= step;
            }
            next.position.v[axis] = clamp(value, minimum[axis], maximum[axis]);
            pairs >>= 2u;
        }
        int16_t angles[3] = {next.yaw, next.pitch, next.roll};
        for (uint8_t axis = 0u; axis < 3u; ++axis)
        {
            int16_t direction = (int16_t)(((pairs & 2u) != 0u) - ((pairs & 1u) != 0u));
            if (axis == 1u)
            {
                direction = (int16_t)-direction;
            }
            int16_t value = (int16_t)(angles[axis] + direction);
            if (axis == 0u)
            {
                if (value < 0)
                {
                    value += 360;
                }
                else if (value >= 360)
                {
                    value -= 360;
                }
            }
            else
            {
                if (value < -M2_TILT_LIMIT_DEG)
                {
                    value = -M2_TILT_LIMIT_DEG;
                }
                if (value > M2_TILT_LIMIT_DEG)
                {
                    value = M2_TILT_LIMIT_DEG;
                }
            }
            angles[axis] = value;
            pairs >>= 2u;
        }
        next.yaw = angles[0];
        next.pitch = angles[1];
        next.roll = angles[2];
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
