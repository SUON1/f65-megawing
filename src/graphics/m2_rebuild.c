#include <limits.h>
#include <string.h>

#include "io.h"
#include "m2_fixture.h"
#include "m2_rebuild.h"

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
static uint8_t same_camera(const M2Camera *first, const M2Camera *last)
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
    renderer->rejected = pool->rejected;
    memset(renderer->visible, 0, sizeof(renderer->visible));
    renderer->phase = M2RB_PREPARE;
}

static void prepare(M2RebuildRenderer *renderer)
{
    if (!m2_prepare(&renderer->prepared, &renderer->prepared.camera))
    {
        fail(renderer, 3u);
        return;
    }
    M2RebuildBundle *bundle = &renderer->bundles[renderer->destination];
    if (!m2_registration_prepared(&renderer->prepared, renderer->generation,
            renderer->snapshot.tick, renderer->destination, &bundle->registration))
    {
        fail(renderer, 3u);
        return;
    }
    bundle->composition_revision = M2RB_COMPOSITION_REVISION;
    bundle->checksum = renderer->snapshot.checksum;
    // The original predicate is affine in x/y. Preserve the full Q46 integer
    // result; bounded additions replace repeated full-width multiplication.
    const M2Transform *rotation = &renderer->prepared.rotation;
    renderer->horizon_band = rotation->m[2] * (2L * M2_FOCAL)
        - rotation->m[5] * (M2_WIDTH - 1L)
        - rotation->m[8] * (M2_HEIGHT - 1L);
    renderer->horizon_tile = renderer->horizon_band;
    renderer->horizon_row = renderer->horizon_band;
    increment(&renderer->prepared_count);
    renderer->phase = M2RB_PROJECT;
}

static void project(M2RebuildRenderer *renderer)
{
    M2Point first;
    M2Point last;
    if (!m2_fixture_segment(M2_FIXTURE_REVISION,
            m2rb_segment_ids[renderer->segment], &first, &last))
    {
        fail(renderer, 3u);
        return;
    }
    int8_t visible = m2_project_prepared(&renderer->prepared, &first, &last,
                                         &renderer->lines[renderer->segment]);
    if (visible < 0)
    {
        fail(renderer, 3u);
        return;
    }
    renderer->visible[renderer->segment] = (uint8_t)visible;
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
    const M2Transform *rotation = &renderer->prepared.rotation;
    int64_t down = renderer->horizon_row;
    for (uint8_t column = 0u; column < 8u; ++column)
    {
        renderer->tile[renderer->tile_row * 8u + column]
            = down > 0 ? M2RB_GROUND : M2RB_SKY;
        down += rotation->m[5] * 2;
    }
    renderer->horizon_row += rotation->m[8] * 2;
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
    if (renderer->after_copy == M2RB_BACKGROUND && renderer->tile_index < 640u)
    {
        const M2Transform *rotation = &renderer->prepared.rotation;
        if (renderer->tile_index % M2RB_COLUMNS == 0u)
        {
            renderer->horizon_band += rotation->m[8] * 16;
            renderer->horizon_tile = renderer->horizon_band;
        }
        else
        {
            renderer->horizon_tile += rotation->m[5] * 16;
        }
        renderer->horizon_row = renderer->horizon_tile;
    }
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

static uint8_t bundle_valid(const M2RebuildRenderer *renderer)
{
    const M2RebuildBundle *bundle = &renderer->bundles[renderer->destination];
    const M2Registration *record = &bundle->registration;
    if (renderer->prepared.ready != 1u || renderer->tile_index != 960u
        || bundle->composition_revision != M2RB_COMPOSITION_REVISION
        || bundle->checksum != renderer->snapshot.checksum
        || record->composition_revision != M2_COMPOSITION_REVISION
        || record->fixture_revision != M2_FIXTURE_REVISION
        || record->projection_revision != M2_PROJECTION_REVISION
        || record->generation != renderer->generation
        || record->source_tick != renderer->snapshot.tick
        || record->store != renderer->destination
        || record->view_id != 0u || record->tier_id != 0u
        || !same_camera(&record->camera, &renderer->prepared.camera))
    {
        return 0u;
    }
    for (uint8_t i = 0u; i < 9u; ++i)
    {
        if (record->transform.m[i] != renderer->prepared.rotation.m[i])
        {
            return 0u;
        }
    }
    return 1u;
}

static void commit(M2RebuildRenderer *renderer)
{
    if (!bundle_valid(renderer))
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
        && !same_camera(wanted, &renderer->prepared.camera))
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
