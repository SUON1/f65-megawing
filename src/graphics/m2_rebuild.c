#include <limits.h>
#include <string.h>

#include "io.h"
#include "m2_fixture.h"
#include "m2_rebuild.h"
#include "m2_record_private.h"

static void increment(uint32_t *value)
{
    if (*value != UINT32_MAX)
    {
        ++*value;
    }
}

static void fail(M2RebuildRenderer *renderer, uint8_t fault)
{
    renderer->fault = fault;
    renderer->prepared.ready = 0u;
    renderer->phase = M2RB_FAILED;
}

void m2rb_renderer_init(M2RebuildRenderer *renderer)
{
    memset(renderer, 0, sizeof(*renderer));
}

// Compare the immutable capture, never merely a caller-supplied revision number.
static void begin(M2RebuildRenderer *renderer, M1Snapshots *pool,
                  const M2Camera *camera)
{
    if (!m2_camera_valid(camera) || renderer->generation == UINT32_MAX)
    {
        fail(renderer, 1u);
        return;
    }
    uint8_t slot = m1_acquire(pool);
    if (slot == M1_SNAPSHOT_SLOTS)
    {
        return;
    }
    // Only the copy outlives the held slot. No renderer yield holds a pool slot.
    renderer->snapshot = pool->slots[slot];
    m1_release(pool, slot);
    if (renderer->snapshot.fault != 0u)
    {
        fail(renderer, 2u);
        return;
    }
    ++renderer->generation;
    renderer->prepared.camera = *camera;
    renderer->prepared.ready = 0u;
    renderer->destination = (uint8_t)(renderer->front ^ 1u);
    renderer->segment = 0u;
    renderer->tile_index = 0u;
    renderer->tile_row = 0u;
    renderer->raster_active = 0u;
    renderer->preparing_horizon = 0u;
    renderer->geometry_active = 0u;
    m2c_prepare_begin(&renderer->geometry);
    renderer->rejected = pool->rejected;
    memset(renderer->visible, 0, sizeof(renderer->visible));
    renderer->phase = M2RB_PREPARE;
}

static void prepare(M2RebuildRenderer *renderer)
{
    int8_t result = renderer->preparing_horizon
        ? m2c_horizon_service(&renderer->horizon, &renderer->geometry, &renderer->prepared)
        : m2c_prepare_service(&renderer->geometry, &renderer->prepared);
    if (result < 0)
    {
        fail(renderer, 3u);
        return;
    }
    if (result == 0)
    {
        return;
    }
    if (!renderer->preparing_horizon)
    {
        m2c_horizon_begin(&renderer->horizon);
        renderer->preparing_horizon = 1u;
        return;
    }
    if (!m2_bundle_fields(renderer, 0u))
    {
        fail(renderer, 3u);
        return;
    }
    increment(&renderer->prepared_count);
    renderer->phase = M2RB_PROJECT;
}

static void project(M2RebuildRenderer *renderer)
{
    if (!renderer->geometry_active)
    {
        M2Point first;
        M2Point last;
        if (!m2_fixture_segment(M2_FIXTURE_REVISION,
                m2rb_segment_ids[renderer->segment], &first, &last)
            || !m2c_project_begin(&renderer->geometry, &first, &last))
        {
            fail(renderer, 3u);
            return;
        }
        renderer->geometry_active = 1u;
        return;
    }
    int8_t visible = m2c_project_service(&renderer->geometry, &renderer->prepared,
                                         &renderer->lines[renderer->segment]);
    if (visible < 0)
    {
        fail(renderer, 3u);
        return;
    }
    if (visible == 0)
    {
        return;
    }
    renderer->geometry_active = 0u;
    renderer->visible[renderer->segment] = (uint8_t)(visible == 1);
    increment(&renderer->projected_count);
    ++renderer->segment;
    if (renderer->segment == M2RB_SEGMENTS)
    {
        renderer->segment = 0u;
        renderer->phase = M2RB_BACKGROUND;
    }
}

static void background(M2RebuildRenderer *renderer)
{
    uint16_t x = (uint16_t)((renderer->tile_index % M2RB_COLUMNS) * 8u);
    uint16_t y = (uint16_t)((renderer->tile_index / M2RB_COLUMNS) * 8u
        + renderer->tile_row);
    // Exact cached scanline boundaries: no wide arithmetic in tile painting.
    for (uint8_t column = 0u; column < 8u; ++column)
    {
        uint8_t ground = renderer->horizon.positive
            ? x + column >= renderer->horizon.boundary[y]
            : x + column < renderer->horizon.boundary[y];
        renderer->tile[renderer->tile_row * 8u + column]
            = ground ? M2RB_GROUND : M2RB_SKY;
    }
    ++renderer->tile_row;
    if (renderer->tile_row == 8u)
    {
        renderer->tile_row = 0u;
        renderer->pending_offset = (uint16_t)(M2RB_TILE_OFFSET
            + renderer->tile_index * M2RB_TILE_BYTES);
        renderer->after_copy = M2RB_BACKGROUND;
        renderer->phase = M2RB_COPY;
    }
}

static void copy_tile(M2RebuildRenderer *renderer)
{
    if (!m2rb_io_write(renderer->destination, renderer->pending_offset,
                       renderer->tile, (uint8_t)M2RB_TILE_BYTES))
    {
        fail(renderer, 4u);
        return;
    }
    ++renderer->tile_index;
    renderer->phase = renderer->after_copy;
    if (renderer->tile_index == 640u)
    {
        renderer->phase = M2RB_LINE;
    }
    else if (renderer->tile_index == 960u)
    {
        renderer->phase = M2RB_COMMIT;
    }
}

static void line(M2RebuildRenderer *renderer)
{
    if (renderer->segment == M2RB_SEGMENTS)
    {
        renderer->phase = M2RB_TEXT;
        return;
    }
    if (!renderer->visible[renderer->segment])
    {
        ++renderer->segment;
        return;
    }
    if (!renderer->raster_active)
    {
        if (!m2_raster_begin(&renderer->lines[renderer->segment], &renderer->raster))
        {
            fail(renderer, 3u);
            return;
        }
        renderer->raster_active = 1u;
        return;
    }
    M2Pixel pixel;
    if (!m2_raster_next(&renderer->raster, &pixel))
    {
        renderer->raster_active = 0u;
        ++renderer->segment;
        return;
    }
    uint16_t tile = (uint16_t)((pixel.y / 8u) * M2RB_COLUMNS + pixel.x / 8u);
    uint16_t offset = (uint16_t)(M2RB_TILE_OFFSET + tile * M2RB_TILE_BYTES
        + (pixel.y % 8u) * 8u + pixel.x % 8u);
    const uint8_t white = M2RB_WHITE;
    if (!m2rb_io_write(renderer->destination, offset, &white, 1u))
    {
        fail(renderer, 4u);
    }
}

static void text(M2RebuildRenderer *renderer, uint32_t current_tick)
{
    uint16_t index = (uint16_t)(renderer->tile_index - 640u);
    uint8_t column = (uint8_t)(index % M2RB_COLUMNS);
    if (index == 0u)
    {
        // Freeze this candidate's source age at telemetry construction, not
        // the previous front's age or an unmeasured eventual display age.
        if (current_tick < renderer->snapshot.tick)
        {
            fail(renderer, 8u);
            return;
        }
        renderer->source_age_at_text = current_tick - renderer->snapshot.tick;
    }
    if (column == 0u)
    {
        m2rb_text_row(renderer, (uint8_t)(index / M2RB_COLUMNS));
    }
    m2rb_glyph(renderer->text[column], renderer->tile);
    renderer->pending_offset = (uint16_t)(M2RB_TILE_OFFSET
        + renderer->tile_index * M2RB_TILE_BYTES);
    renderer->after_copy = M2RB_TEXT;
    renderer->phase = M2RB_COPY;
}

static void commit(M2RebuildRenderer *renderer)
{
    if (!m2_bundle_fields(renderer, 1u))
    {
        fail(renderer, 5u);
        return;
    }
    int8_t result = m2rb_io_commit(renderer->destination);
    if (result < 0)
    {
        // Hardware selection is uncertain: never claim the old generation is live.
        fail(renderer, 6u);
    }
    else if (result == 1)
    {
        // No yielding between physical selection and the matching record latch.
        renderer->front = renderer->destination;
        renderer->shown = 1u;
        increment(&renderer->commits);
        renderer->phase = M2RB_BEGIN;
    }
}

uint8_t m2rb_dispatch(M2RebuildRenderer *renderer, M1Snapshots *pool,
                       const M2Camera *wanted, uint32_t admitted_budget,
                       uint32_t current_tick)
{
    if (admitted_budget == 0u || renderer->phase >= M2RB_FAILED)
    {
        return 0u;
    }
    if (renderer->phase != M2RB_BEGIN
        && !m2_camera_same(wanted, &renderer->prepared.camera))
    {
        renderer->prepared.ready = 0u;
        memset(renderer->visible, 0, sizeof(renderer->visible));
        renderer->phase = M2RB_BEGIN;
        increment(&renderer->cancellations);
        return 1u;
    }
    switch (renderer->phase)
    {
        case M2RB_BEGIN:
            begin(renderer, pool, wanted);
            break;
        case M2RB_PREPARE:
            prepare(renderer);
            break;
        case M2RB_PROJECT:
            project(renderer);
            break;
        case M2RB_BACKGROUND:
            background(renderer);
            break;
        case M2RB_COPY:
            copy_tile(renderer);
            break;
        case M2RB_LINE:
            line(renderer);
            break;
        case M2RB_TEXT:
            text(renderer, current_tick);
            break;
        case M2RB_COMMIT:
            commit(renderer);
            break;
        default:
            fail(renderer, 7u);
            break;
    }
    return 1u;
}
