// Exact private presentation arithmetic; no native64 expressions or hardware.
#include <string.h>

#include "m2_compact.h"
#include "m2_fixture.h"

enum
{
    SINE, TRANSFORM_START, TRANSFORM_WAIT,
    CAMERA_START, CAMERA_WAIT, CLIP, INTERPOLATE_START, INTERPOLATE_WAIT,
    INTERPOLATE_DIVIDE, PROJECT_START, PROJECT_WAIT, PROJECT_DIVIDE, DONE
};

static void sine(M2Wide out, int16_t angle)
{
    int16_t wrapped = (int16_t)(angle % 360);
    if (wrapped < 0)
    {
        wrapped += 360;
    }
    uint8_t negative = (uint8_t)(wrapped > 180);
    if (negative)
    {
        wrapped -= 180;
    }
    if (wrapped > 90)
    {
        wrapped = (int16_t)(180 - wrapped);
    }
    memcpy(out, &m2_sine_q46[(uint16_t)wrapped], 8u);
    if (negative)
    {
        m2w_negate(out, 8u);
    }
}

void m2c_prepare_begin(M2Compact *work)
{
    work->state = SINE;
    work->index = 0u;
    work->job.phase = 0u;
}

int8_t m2c_prepare_service(M2Compact *work, struct M2Prepared *prepared)
{
    // Identical fourteen products and intermediate rounding to the native
    // reference. Table operands 6/7 hold rounded pitch/roll intermediates.
    static const uint8_t products[14][4] = {
        {4,2,6,0}, {5,2,7,0}, {3,1,0,1}, {3,0,1,1},
        {6,1,3,1}, {5,0,3,3}, {6,0,4,1}, {5,1,4,2},
        {4,3,5,1}, {7,1,6,1}, {4,0,6,2},
        {7,0,7,1}, {4,1,7,3}, {5,3,8,1}
    };
    if (work->state == SINE)
    {
        int16_t angle;
        uint8_t axis = (uint8_t)(work->index / 2u);
        if (axis == 0u)
        {
            angle = prepared->camera.yaw;
        }
        else
        {
            angle = axis == 1u ? prepared->camera.pitch : prepared->camera.roll;
        }
        sine(work->registers[work->index],
              (int16_t)(angle + (work->index % 2u ? 90 : 0)));
        if (++work->index == 6u)
        {
            memcpy(work->temporary, work->registers[2], 8u);
            m2w_negate(work->temporary, 8u);
            memcpy(&prepared->rotation.m[2], work->temporary, 8u);
            work->index = 0u;
            work->state = TRANSFORM_START;
        }
        return 0;
    }
    if (work->state == TRANSFORM_START)
    {
        const uint8_t *product = products[work->index];
        if (!m2l_multiply(&work->job, work->registers[product[0]],
                          work->registers[product[1]], 46u))
        {
            return -1;
        }
        work->state = TRANSFORM_WAIT;
        return 0;
    }
    if (work->state != TRANSFORM_WAIT)
    {
        return -1;
    }
    int8_t result = m2l_service(&work->job);
    if (result <= 0)
    {
        return result;
    }
    const uint8_t *product = products[work->index];
    uint8_t *destination = product[3] == 0u ? work->registers[product[2]]
        : (uint8_t *)&prepared->rotation.m[product[2]];
    if (product[3] < 2u)
    {
        memcpy(destination, work->job.value, 8u);
    }
    else
    {
        m2w_add(destination, destination, work->job.value,
                  (uint8_t)(product[3] == 3u));
    }
    if (++work->index == 14u)
    {
        prepared->ready = 1u;
        work->state = DONE;
        return 1;
    }
    work->state = TRANSFORM_START;
    return 0;
}

uint8_t m2c_project_begin(M2Compact *work, const M2Point *first, const M2Point *last)
{
    if (!m2_point_valid(first) || !m2_point_valid(last))
    {
        return 0u;
    }
    work->endpoints[0] = *first;
    work->endpoints[1] = *last;
    work->endpoint = 0u;
    work->row = 0u;
    work->axis = 0u;
    work->state = CAMERA_START;
    work->job.phase = 0u;
    return 1u;
}

static void distance(M2Wide out, const M2Wide *point, uint8_t plane)
{
    M2Wide temporary;
    if (plane < 2u)
    {
        // FAR*Q24 exceeds32bits: assemble this integer exactly in bytes.
        m2w_i32(temporary, (int32_t)(plane ? M2_FAR_FT : M2_NEAR_FT));
        for (uint8_t i = 8u; i != 0u; --i)
        {
            temporary[i - 1u] = i > 3u ? temporary[i - 4u] : 0u;
        }
        m2w_add(out, plane ? temporary : point[0], plane ? point[0] : temporary, 1u);
    }
    else if (plane < 4u)
    {
        m2w_add(out, point[0], point[1], (uint8_t)(plane == 3u));
    }
    else
    {
        memcpy(temporary, point[2], 8u);
        m2w_double(temporary);
        m2w_double(temporary);
        m2w_add(temporary, temporary, point[2], 0u);
        memcpy(out, point[0], 8u);
        m2w_double(out);
        m2w_add(out, out, temporary, (uint8_t)(plane == 5u));
    }
}

int8_t m2c_project_service(M2Compact *work, const struct M2Prepared *prepared,
                            M2Line *line)
{
    if (prepared->ready != 1u || line == 0)
    {
        return -1;
    }
    uint8_t point = (uint8_t)(work->endpoint * 3u);
    if (work->state == CAMERA_START)
    {
        if (work->axis == 0u)
        {
            memset(work->sum, 0, 8u);
        }
        int32_t delta = work->endpoints[work->endpoint].v[work->axis]
            - prepared->camera.position.v[work->axis];
        m2w_i32(work->temporary, delta);
        for (uint8_t bit = 0u; bit < 12u; ++bit)
        {
            m2w_double(work->temporary);
        }
        if (!m2l_multiply(&work->job, work->temporary,
              (const uint8_t *)&prepared->rotation.m[work->row * 3u + work->axis], 46u))
        {
            return -1;
        }
        work->state = CAMERA_WAIT;
        return 0;
    }
    if (work->state == CAMERA_WAIT)
    {
        int8_t result = m2l_service(&work->job);
        if (result <= 0)
        {
            return result;
        }
        m2w_add(work->sum, work->sum, work->job.value, 0u);
        if (++work->axis == 3u)
        {
            memcpy(work->registers[point + work->row], work->sum, 8u);
            work->axis = 0u;
            if (++work->row == 3u)
            {
                work->row = 0u;
                if (++work->endpoint == 2u)
                {
                    work->plane = 0u;
                    work->state = CLIP;
                    return 0;
                }
            }
        }
        work->state = CAMERA_START;
        return 0;
    }
    if (work->state == CLIP)
    {
        if (work->plane == 6u)
        {
            work->endpoint = 0u;
            work->axis = 0u;
            work->state = PROJECT_START;
            return 0;
        }
        distance(work->registers[6], &work->registers[0], work->plane);
        distance(work->registers[7], &work->registers[3], work->plane);
        uint8_t first = (uint8_t)(work->registers[6][7] >> 7u);
        uint8_t last = (uint8_t)(work->registers[7][7] >> 7u);
        if (first && last)
        {
            return 2;
        }
        if (first != last)
        {
            work->outside = first ? 0u : 3u;
            work->inside = first ? 3u : 0u;
            memcpy(work->registers[8], work->registers[first ? 7u : 6u], 8u);
            m2w_add(work->registers[9], work->registers[8],
                      work->registers[first ? 6u : 7u], 1u);
            work->axis = 0u;
            work->state = INTERPOLATE_START;
        }
        else
        {
            ++work->plane;
        }
        return 0;
    }
    if (work->state == INTERPOLATE_START)
    {
        m2w_add(work->temporary, work->registers[work->outside + work->axis],
                  work->registers[work->inside + work->axis], 1u);
        if (!m2l_multiply(&work->job, work->temporary, work->registers[8], 255u))
        {
            return -1;
        }
        work->state = INTERPOLATE_WAIT;
        return 0;
    }
    if (work->state == INTERPOLATE_WAIT || work->state == PROJECT_WAIT)
    {
        int8_t result = m2l_service(&work->job);
        if (result <= 0)
        {
            return result;
        }
        uint8_t interpolation = (uint8_t)(work->state == INTERPOLATE_WAIT);
        if (!m2l_divide(&work->job,
              work->registers[interpolation ? 9u : point]))
        {
            return -1;
        }
        work->state = interpolation ? INTERPOLATE_DIVIDE : PROJECT_DIVIDE;
        return 0;
    }
    if (work->state == INTERPOLATE_DIVIDE)
    {
        int8_t result = m2l_service(&work->job);
        if (result <= 0)
        {
            return result;
        }
        m2w_add(work->registers[work->outside + work->axis],
                  work->registers[work->inside + work->axis], work->job.value, 0u);
        if (++work->axis == 3u)
        {
            ++work->plane;
            work->state = CLIP;
        }
        else
        {
            work->state = INTERPOLATE_START;
        }
        return 0;
    }
    if (work->state == PROJECT_START)
    {
        if (!m2w_positive(work->registers[point]))
        {
            return -1;
        }
        m2w_i32(work->temporary, (int32_t)(M2_FOCAL * M2_SCREEN_SCALE));
        if (!m2l_multiply(&work->job, work->registers[point + work->axis + 1u],
                           work->temporary, 255u))
        {
            return -1;
        }
        work->state = PROJECT_WAIT;
        return 0;
    }
    if (work->state == PROJECT_DIVIDE)
    {
        int8_t result = m2l_service(&work->job);
        if (result <= 0)
        {
            return result;
        }
        int32_t value;
        if (!m2w_narrow(work->job.value, &value))
        {
            return -1;
        }
        int32_t extent = work->axis == 0u ? M2_WIDTH : M2_HEIGHT;
        value += (extent - 1) * (M2_SCREEN_SCALE / 2);
        int32_t maximum = extent * M2_SCREEN_SCALE - M2_SCREEN_SCALE / 2;
        if (value < -M2_SCREEN_SCALE / 2)
        {
            value = -M2_SCREEN_SCALE / 2;
        }
        if (value > maximum)
        {
            value = maximum;
        }
        if (work->axis == 0u)
        {
            work->line.x[work->endpoint] = value;
        }
        else
        {
            work->line.y[work->endpoint] = value;
        }
        if (++work->axis == 2u)
        {
            work->axis = 0u;
            if (++work->endpoint == 2u)
            {
                *line = work->line;
                work->state = DONE;
                return 1;
            }
        }
        work->state = PROJECT_START;
        return 0;
    }
    return -1;
}

void m2c_horizon_begin(M2Horizon *horizon)
{
    horizon->state = 0u;
}

int8_t m2c_horizon_service(M2Horizon *horizon, M2Compact *work,
                            const struct M2Prepared *prepared)
{
    if (horizon->state < 6u)
    {
        uint8_t index = (uint8_t)(horizon->state / 2u);
        if (horizon->state % 2u == 0u)
        {
            const uint8_t *coefficient = (const uint8_t *)&prepared->rotation.m[index * 3u + 2u];
            if (index == 0u)
            {
                horizon->positive = (uint8_t)
                    ((((const uint8_t *)&prepared->rotation.m[5])[7] & 128u) == 0u);
                memcpy(horizon->dx, &prepared->rotation.m[5], 8u);
                m2w_double(horizon->dx);
                memcpy(horizon->dy, &prepared->rotation.m[8], 8u);
                m2w_double(horizon->dy);
                // The legal +/-60-degree camera has cos(pitch)*cos(roll)>0.
                if (!m2w_positive(horizon->dy))
                {
                    return -1;
                }
                memset(horizon->edge, 0, 8u);
            }
            int32_t factor = index == 0u ? 320
                : (index == 1u ? (horizon->positive ? 319 : -319) : -127);
            m2w_i32(work->temporary, factor);
            if (!m2l_multiply(&work->job, coefficient, work->temporary, 0u))
            {
                return -1;
            }
            ++horizon->state;
            return 0;
        }
        int8_t result = m2l_service(&work->job);
        if (result <= 0)
        {
            return result;
        }
        m2w_add(horizon->edge, horizon->edge, work->job.value, 0u);
        if (++horizon->state == 6u)
        {
            horizon->cursor = horizon->positive ? 320u : 0u;
            horizon->row = 0u;
        }
        return 0;
    }
    if (horizon->state != 6u)
    {
        return -1;
    }
    uint8_t can_advance = horizon->positive ? horizon->cursor != 0u
                                          : horizon->cursor != 320u;
    if (can_advance && m2w_positive(horizon->edge))
    {
        if (horizon->positive)
        {
            --horizon->cursor;
        }
        else
        {
            ++horizon->cursor;
        }
        m2w_add(horizon->edge, horizon->edge, horizon->dx, horizon->positive);
        return 0;
    }
    horizon->boundary[horizon->row] = horizon->cursor;
    if (++horizon->row == 128u)
    {
        horizon->state = 7u;
        return 1;
    }
    m2w_add(horizon->edge, horizon->edge, horizon->dy, 0u);
    return 0;
}
