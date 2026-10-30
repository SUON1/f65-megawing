// Exact public adapters and narrow validation/raster. Host batch adapters are
// dead-stripped from the target; the real renderer uses resumable services.
#include <string.h>

#include "m2_compact.h"
#include "m2_raster_private.h"

uint8_t m2_camera_valid(const M2Camera *camera)
{
    if (!(camera != 0 && camera->revision != 0u
        && camera->yaw >= 0 && camera->yaw < 360
        && camera->pitch >= -M2_TILT_LIMIT_DEG && camera->pitch <= M2_TILT_LIMIT_DEG
        && camera->roll >= -M2_TILT_LIMIT_DEG && camera->roll <= M2_TILT_LIMIT_DEG))
    {
        return 0u;
    }
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
    for (uint8_t axis = 0u; axis < 3u; ++axis)
    {
        if (camera->position.v[axis] < minimum[axis]
            || camera->position.v[axis] > maximum[axis])
        {
            return 0u;
        }
    }
    return 1u;
}

static int16_t raster_coordinate(int32_t value, int32_t extent)
{
    uint32_t sample = (uint32_t)(value + M2_SCREEN_SCALE / 2) >> 16u;
    return (int16_t)(sample >= (uint32_t)extent ? (uint32_t)(extent - 1) : sample);
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

uint8_t m2_prepare(struct M2Prepared *prepared, const M2Camera *camera)
{
    if (prepared == 0)
    {
        return 0u;
    }
    prepared->ready = 0u;
    if (!m2_camera_valid(camera))
    {
        return 0u;
    }
    prepared->camera = *camera;
    M2Compact work;
    m2c_prepare_begin(&work);
    for (uint16_t step = 0u; step < 128u; ++step)
    {
        int8_t result = m2c_prepare_service(&work, prepared);
        if (result != 0)
        {
            return (uint8_t)(result == 1);
        }
    }
    return 0u;
}

uint8_t m2_transform(const M2Camera *camera, M2Transform *transform)
{
    struct M2Prepared prepared;
    if (transform == 0 || !m2_prepare(&prepared, camera))
    {
        return 0u;
    }
    *transform = prepared.rotation;
    return 1u;
}

int8_t m2_project_prepared(const struct M2Prepared *prepared,
                          const M2Point *first, const M2Point *last, M2Line *line)
{
    M2Compact work;
    if (prepared == 0 || prepared->ready != 1u || line == 0
        || !m2c_project_begin(&work, first, last))
    {
        return -1;
    }
    // 18*7 transform, 6*(1+3*104) clipping, 4*104 projection <2500.
    for (uint16_t step = 0u; step < 2500u; ++step)
    {
        int8_t result = m2c_project_service(&work, prepared, line);
        if (result != 0)
        {
            return result == 2 ? 0 : result;
        }
    }
    return -1;
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

int8_t m2_ground_prepared(const struct M2Prepared *prepared, uint16_t x, uint16_t y)
{
    if (prepared == 0 || prepared->ready != 1u || x >= M2_WIDTH || y >= M2_HEIGHT)
    {
        return -1;
    }
    // Host/public batch compatibility only; not called by target composition.
    int64_t down = prepared->rotation.m[2] * 320L
        + prepared->rotation.m[5] * (2L * x - 319L)
        + prepared->rotation.m[8] * (2L * y - 127L);
    return (int8_t)(down > 0);
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

uint8_t m2_registration(const M2Camera *camera, uint32_t generation,
                         uint32_t tick, uint8_t store, M2Registration *record)
{
    struct M2Prepared prepared;
    if (!m2_prepare(&prepared, camera))
    {
        return 0u;
    }
    return m2_registration_prepared(&prepared, generation, tick, store, record);
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
