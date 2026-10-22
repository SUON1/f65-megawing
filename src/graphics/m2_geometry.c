#include <limits.h>

#include "m2_fixture.h"
#include "m2_geometry.h"
#include "m2_raster_private.h"
#include "m2_prepared_private.h"
#include "m2_q46_private.h"

// All callers bound magnitudes below INT64_MAX, including the rounding bias.
static int32_t rounded_ratio(int64_t value, int64_t divisor)
{
    return (int32_t)(value >= 0 ? (value + divisor / 2) / divisor
                               : -((-value + divisor / 2) / divisor));
}

// Compute round(delta * numerator / denominator) without forming the product.
// Used for Q24 interpolation and Q46 rotation. Fractions are in [0,1];
// 3*denominator is below 2^48. No intermediate product is formed.
// Each of 64 fixed iterations has at most two subtractions; no data-dependent
// loop or wide multiplication. Quotient magnitude never exceeds abs(delta).
static int64_t interpolate_delta(int64_t delta, int64_t numerator,
                                  int64_t denominator)
{
    uint64_t magnitude = (uint64_t)(delta < 0 ? -delta : delta);
    uint64_t divisor = (uint64_t)denominator;
    uint64_t fraction = (uint64_t)numerator;
    uint64_t quotient = 0u;
    uint64_t remainder = 0u;
    for (uint8_t bit = 64u; bit != 0u; --bit)
    {
        quotient *= 2u;
        remainder *= 2u;
        if (((magnitude >> (bit - 1u)) & 1u) != 0u)
        {
            remainder += fraction;
        }
        for (uint8_t subtraction = 0u; subtraction < 2u; ++subtraction)
        {
            if (remainder >= divisor)
            {
                remainder -= divisor;
                ++quotient;
            }
        }
    }
    if (remainder >= (divisor + 1u) / 2u)
    {
        ++quotient;
    }
    return delta < 0 ? -(int64_t)quotient : (int64_t)quotient;
}

static int64_t multiply_rotation(int64_t value, int64_t coefficient)
{
    return m2_multiply_q46(value, coefficient);
}

static int64_t sine(int16_t angle)
{
    int16_t wrapped = (int16_t)(angle % 360);
    if (wrapped < 0)
    {
        wrapped += 360;
    }
    uint8_t negative = (uint8_t)(wrapped > 180);
    if (negative)
    {
        wrapped = (int16_t)(wrapped - 180);
    }
    if (wrapped > 90)
    {
        wrapped = (int16_t)(180 - wrapped);
    }
    int64_t value = m2_sine_q46[(uint16_t)wrapped];
    return negative ? -value : value;
}

uint8_t m2_camera_valid(const M2Camera *camera)
{
    return (uint8_t)(camera != 0 && camera->revision != 0u
        && camera->yaw >= 0 && camera->yaw < 360
        && camera->pitch >= -M2_TILT_LIMIT_DEG && camera->pitch <= M2_TILT_LIMIT_DEG
        && camera->roll >= -M2_TILT_LIMIT_DEG && camera->roll <= M2_TILT_LIMIT_DEG
        && camera->position.v[0] >= -M2_NORTH_LIMIT_FT * M2_POSITION_SCALE
        && camera->position.v[0] <= M2_NORTH_LIMIT_FT * M2_POSITION_SCALE
        && camera->position.v[1] >= -M2_EAST_LIMIT_FT * M2_POSITION_SCALE
        && camera->position.v[1] <= M2_EAST_LIMIT_FT * M2_POSITION_SCALE
        && camera->position.v[2] >= -M2_HEIGHT_MAX_FT * M2_POSITION_SCALE
        && camera->position.v[2] <= -M2_HEIGHT_MIN_FT * M2_POSITION_SCALE);
}

uint8_t m2_transform(const M2Camera *camera, M2Transform *transform)
{
    if (!m2_camera_valid(camera) || transform == 0)
    {
        return 0u;
    }
    enum
    {
        YAW_SIN, YAW_COS, PITCH_SIN, PITCH_COS, ROLL_SIN, ROLL_COS,
        ROLL_SIN_PITCH_SIN, ROLL_COS_PITCH_SIN
    };
    enum { SAVE_OPERAND, SET_COEFFICIENT, ADD_COEFFICIENT, SUB_COEFFICIENT };
    // Fixed evaluation of transpose(Rz(yaw) Ry(pitch) Rx(roll)).
    // Keep both rounded pitch/roll intermediates and all fourteen products.
    static const struct
    {
        uint8_t first;
        uint8_t second;
        uint8_t destination;
        uint8_t operation;
    } products[] = {
        {ROLL_SIN, PITCH_SIN, ROLL_SIN_PITCH_SIN, SAVE_OPERAND},
        {ROLL_COS, PITCH_SIN, ROLL_COS_PITCH_SIN, SAVE_OPERAND},
        {PITCH_COS, YAW_COS, 0u, SET_COEFFICIENT},
        {PITCH_COS, YAW_SIN, 1u, SET_COEFFICIENT},
        {ROLL_SIN_PITCH_SIN, YAW_COS, 3u, SET_COEFFICIENT},
        {ROLL_COS, YAW_SIN, 3u, SUB_COEFFICIENT},
        {ROLL_SIN_PITCH_SIN, YAW_SIN, 4u, SET_COEFFICIENT},
        {ROLL_COS, YAW_COS, 4u, ADD_COEFFICIENT},
        {ROLL_SIN, PITCH_COS, 5u, SET_COEFFICIENT},
        {ROLL_COS_PITCH_SIN, YAW_COS, 6u, SET_COEFFICIENT},
        {ROLL_SIN, YAW_SIN, 6u, ADD_COEFFICIENT},
        {ROLL_COS_PITCH_SIN, YAW_SIN, 7u, SET_COEFFICIENT},
        {ROLL_SIN, YAW_COS, 7u, SUB_COEFFICIENT},
        {ROLL_COS, PITCH_COS, 8u, SET_COEFFICIENT}
    };
    const int16_t angles[3] = {camera->yaw, camera->pitch, camera->roll};
    int64_t operands[8];
    for (uint8_t i = 0u; i < 6u; ++i)
    {
        int16_t angle = (int16_t)(angles[i / 2u] + (i % 2u != 0u ? 90 : 0));
        operands[i] = sine(angle);
    }
    M2Transform result;
    result.m[2] = -operands[PITCH_SIN];
    for (uint8_t i = 0u; i < sizeof(products) / sizeof(products[0]); ++i)
    {
        int64_t product = multiply_rotation(operands[products[i].first],
                                             operands[products[i].second]);
        uint8_t destination = products[i].destination;
        switch (products[i].operation)
        {
            case SAVE_OPERAND:
                operands[destination] = product;
                break;
            case SET_COEFFICIENT:
                result.m[destination] = product;
                break;
            case ADD_COEFFICIENT:
                result.m[destination] += product;
                break;
            case SUB_COEFFICIENT:
                result.m[destination] -= product;
                break;
        }
    }
    *transform = result;
    return 1u;
}

// Private precision survives transformation and all clip planes. Public
// fixture/camera position units remain unchanged; the generated rotation
// record is versioned Q46 to retain angular precision at the far plane.
typedef struct
{
    int64_t v[3];
} ClipPoint;

static ClipPoint to_camera(const M2Camera *camera, const M2Transform *rotation,
                          const M2Point *point)
{
    ClipPoint result;
    for (uint8_t row = 0u; row < 3u; ++row)
    {
        int64_t sum = 0;
        for (uint8_t axis = 0u; axis < 3u; ++axis)
        {
            int32_t delta = point->v[axis] - camera->position.v[axis];
            int64_t precise_delta = (int64_t)delta
                * (M2_CLIP_SCALE / M2_POSITION_SCALE);
            sum += multiply_rotation(precise_delta, rotation->m[row * 3u + axis]);
        }
        result.v[row] = sum;
    }
    return result;
}

// Six homogeneous halfspaces, positive on the visible side. Multipliers
// encode the admitted square-sample projection: vertical half-angle = 64/160.
static int64_t plane_distance(const ClipPoint *p, uint8_t plane)
{
    switch (plane)
    {
        case 0: return (int64_t)p->v[0] - (int64_t)M2_NEAR_FT * M2_CLIP_SCALE;
        case 1: return (int64_t)M2_FAR_FT * M2_CLIP_SCALE - (int64_t)p->v[0];
        case 2: return (int64_t)p->v[0] + p->v[1];
        case 3: return (int64_t)p->v[0] - p->v[1];
        case 4: return (int64_t)M2_VERTICAL_NUM * p->v[0] + (int64_t)M2_VERTICAL_DEN * p->v[2];
        default: return (int64_t)M2_VERTICAL_NUM * p->v[0] - (int64_t)M2_VERTICAL_DEN * p->v[2];
    }
}

static int32_t project_axis(int64_t component, int64_t forward, int32_t extent)
{
    int32_t projected = (extent - 1) * (M2_SCREEN_SCALE / 2)
        + rounded_ratio((int64_t)component * M2_FOCAL * M2_SCREEN_SCALE, forward);
    int32_t minimum = -M2_SCREEN_SCALE / 2;
    int32_t maximum = extent * M2_SCREEN_SCALE - M2_SCREEN_SCALE / 2;
    // Clip interpolation rounds to Q24; clamp only the resulting subpixel edge.
    if (projected < minimum)
    {
        return minimum;
    }
    return projected > maximum ? maximum : projected;
}

uint8_t m2_prepare(struct M2Prepared *prepared, const M2Camera *camera)
{
    if (prepared == 0)
    {
        return 0u;
    }
    prepared->ready = 0u;
    if (!m2_transform(camera, &prepared->rotation))
    {
        return 0u;
    }
    prepared->camera = *camera;
    prepared->ready = 1u;
    return 1u;
}

int8_t m2_project_segment(const M2Camera *camera, const M2Point *first,
                          const M2Point *last, M2Line *line)
{
    struct M2Prepared prepared;
    if (!m2_prepare(&prepared, camera))
    {
        return -1;
    }
    return m2_project_prepared(&prepared, first, last, line);
}

int8_t m2_project_prepared(const struct M2Prepared *prepared,
                          const M2Point *first, const M2Point *last, M2Line *line)
{
    if (prepared == 0 || prepared->ready != 1u || line == 0
        || !m2_point_valid(first) || !m2_point_valid(last))
    {
        return -1;
    }
    ClipPoint a = to_camera(&prepared->camera, &prepared->rotation, first);
    ClipPoint b = to_camera(&prepared->camera, &prepared->rotation, last);
    for (uint8_t plane = 0u; plane < M2_CLIP_PLANES; ++plane)
    {
        int64_t da = plane_distance(&a, plane);
        int64_t db = plane_distance(&b, plane);
        if (da < 0 && db < 0)
        {
            return 0;
        }
        if ((da < 0) != (db < 0))
        {
            // Interpolate from the inside endpoint; ratio is in [0,1].
            ClipPoint inside = da >= 0 ? a : b;
            ClipPoint outside = da < 0 ? a : b;
            int64_t numerator = da >= 0 ? da : db;
            int64_t denominator = da >= 0 ? da - db : db - da;
            for (uint8_t axis = 0u; axis < 3u; ++axis)
            {
                int64_t delta = (int64_t)outside.v[axis] - inside.v[axis];
                outside.v[axis] = inside.v[axis]
                    + interpolate_delta(delta, numerator, denominator);
            }
            if (da < 0)
            {
                a = outside;
            }
            else
            {
                b = outside;
            }
        }
    }
    if (a.v[0] <= 0 || b.v[0] <= 0)
    {
        return -1;
    }
    M2Line result;
    result.x[0] = project_axis(a.v[1], a.v[0], M2_WIDTH);
    result.y[0] = project_axis(a.v[2], a.v[0], M2_HEIGHT);
    result.x[1] = project_axis(b.v[1], b.v[0], M2_WIDTH);
    result.y[1] = project_axis(b.v[2], b.v[0], M2_HEIGHT);
    *line = result;
    return 1;
}

static int16_t raster_coordinate(int32_t value, int32_t extent)
{
    int32_t sample = (value + M2_SCREEN_SCALE / 2) / M2_SCREEN_SCALE;
    return (int16_t)(sample >= extent ? extent - 1 : sample);
}

uint8_t m2_raster_begin(const M2Line *line, struct M2RasterCursor *cursor)
{
    if (line == 0 || cursor == 0)
    {
        return 0u;
    }
    for (uint8_t end = 0u; end < 2u; ++end)
    {
        if (line->x[end] < -M2_SCREEN_SCALE / 2
            || line->x[end] > (M2_WIDTH * M2_SCREEN_SCALE - M2_SCREEN_SCALE / 2)
            || line->y[end] < -M2_SCREEN_SCALE / 2
            || line->y[end] > (M2_HEIGHT * M2_SCREEN_SCALE - M2_SCREEN_SCALE / 2))
        {
            return 0u;
        }
    }
    struct M2RasterCursor result;
    result.x = raster_coordinate(line->x[0], M2_WIDTH);
    result.y = raster_coordinate(line->y[0], M2_HEIGHT);
    int16_t end_x = raster_coordinate(line->x[1], M2_WIDTH);
    int16_t end_y = raster_coordinate(line->y[1], M2_HEIGHT);
    result.dx = (int16_t)(end_x > result.x ? end_x - result.x : result.x - end_x);
    result.dy = (int16_t)(end_y > result.y ? end_y - result.y : result.y - end_y);
    result.remaining = (uint16_t)((result.dx > result.dy ? result.dx : result.dy) + 1);
    if (result.remaining > M2_RASTER_POINTS)
    {
        return 0u;
    }
    result.step_x = end_x > result.x ? 1 : -1;
    result.step_y = end_y > result.y ? 1 : -1;
    result.error = (int16_t)(result.dx - result.dy);
    *cursor = result;
    return 1u;
}

uint8_t m2_raster_next(struct M2RasterCursor *cursor, M2Pixel *pixel)
{
    if (cursor == 0 || pixel == 0 || cursor->remaining == 0u)
    {
        return 0u;
    }
    pixel->x = (uint16_t)cursor->x;
    pixel->y = (uint16_t)cursor->y;
    --cursor->remaining;
    if (cursor->remaining != 0u)
    {
        int16_t twice = (int16_t)(2 * cursor->error);
        if (twice > -cursor->dy)
        {
            cursor->error = (int16_t)(cursor->error - cursor->dy);
            cursor->x = (int16_t)(cursor->x + cursor->step_x);
        }
        if (twice < cursor->dx)
        {
            cursor->error = (int16_t)(cursor->error + cursor->dx);
            cursor->y = (int16_t)(cursor->y + cursor->step_y);
        }
    }
    return 1u;
}

uint8_t m2_raster_line(const M2Line *line, M2Pixel *pixels,
                        uint16_t capacity, uint16_t *count)
{
    struct M2RasterCursor cursor;
    if (pixels == 0 || count == 0 || !m2_raster_begin(line, &cursor)
        || capacity < cursor.remaining)
    {
        return 0u;
    }
    uint16_t needed = cursor.remaining;
    for (uint16_t i = 0u; i < needed; ++i)
    {
        (void)m2_raster_next(&cursor, &pixels[i]);
    }
    *count = needed;
    return 1u;
}

int8_t m2_ground_sample(const M2Camera *camera, uint16_t x, uint16_t y)
{
    struct M2Prepared prepared;
    if (!m2_prepare(&prepared, camera))
    {
        return -1;
    }
    return m2_ground_prepared(&prepared, x, y);
}

int8_t m2_ground_prepared(const struct M2Prepared *prepared, uint16_t x, uint16_t y)
{
    if (prepared == 0 || prepared->ready != 1u || x >= M2_WIDTH || y >= M2_HEIGHT)
    {
        return -1;
    }
    const M2Transform *rotation = &prepared->rotation;
    int64_t down = rotation->m[2] * (2L * M2_FOCAL)
        + rotation->m[5] * (2L * x - (M2_WIDTH - 1))
        + rotation->m[8] * (2L * y - (M2_HEIGHT - 1));
    return (int8_t)(down > 0);
}

uint8_t m2_registration(const M2Camera *camera, uint32_t generation,
                         uint32_t source_tick, uint8_t store,
                         M2Registration *record)
{
    struct M2Prepared prepared;
    if (!m2_prepare(&prepared, camera))
    {
        return 0u;
    }
    return m2_registration_prepared(&prepared, generation, source_tick, store, record);
}

uint8_t m2_registration_prepared(const struct M2Prepared *prepared,
                                 uint32_t generation, uint32_t tick, uint8_t store,
                                 M2Registration *record)
{
    if (prepared == 0 || prepared->ready != 1u || record == 0
        || generation == 0u || store > 1u)
    {
        return 0u;
    }
    // All validation precedes output writes. Every generated field is assigned;
    // avoid a second full registration record and the final structure copy.
    record->camera = prepared->camera;
    record->transform = prepared->rotation;
    record->generation = generation;
    record->source_tick = tick;
    record->fixture_revision = M2_FIXTURE_REVISION;
    record->projection_revision = M2_PROJECTION_REVISION;
    record->composition_revision = M2_COMPOSITION_REVISION;
    record->view_id = 0u;
    record->tier_id = 0u;
    record->store = store;
    return 1u;
}

static uint8_t record_valid(const M2Registration *record)
{
    M2Transform rotation;
    if (record == 0 || record->generation == 0u || record->store > 1u
        || record->fixture_revision != M2_FIXTURE_REVISION
        || record->projection_revision != M2_PROJECTION_REVISION
        || record->composition_revision != M2_COMPOSITION_REVISION
        || record->view_id != 0u || record->tier_id != 0u
        || !m2_transform(&record->camera, &rotation))
    {
        return 0u;
    }
    for (uint8_t i = 0u; i < 9u; ++i)
    {
        if (rotation.m[i] != record->transform.m[i])
        {
            return 0u;
        }
    }
    return 1u;
}

uint8_t m2_pair_eligible(const M2Registration *world,
                          const M2Registration *record,
                          uint32_t wanted_camera_revision, uint8_t complete)
{
    if (complete != 1u || !record_valid(world) || !record_valid(record)
        || world->camera.revision != wanted_camera_revision
        || world->camera.revision != record->camera.revision
        || world->generation != record->generation
        || world->source_tick != record->source_tick || world->store != record->store
        || world->camera.yaw != record->camera.yaw
        || world->camera.pitch != record->camera.pitch
        || world->camera.roll != record->camera.roll)
    {
        return 0u;
    }
    for (uint8_t i = 0u; i < 3u; ++i)
    {
        if (world->camera.position.v[i] != record->camera.position.v[i])
        {
            return 0u;
        }
    }
    return 1u;
}
