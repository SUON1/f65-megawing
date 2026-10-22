// Pure tile construction. Physical transfer and activation belong to Platform.
// One exclusive owner; only a complete hidden store may be published.
#include <string.h>

#include "m2_fixture.h"
#include "m2_renderer.h"

#define TILE_COLUMNS 40u
#define WORLD_TILES 640u
#define NO_LABEL 255u
#define COLOR_SKY 6u
#define COLOR_GROUND 5u
#define COLOR_INK 1u
#define COLOR_ANCHOR 7u

static void fail(M2Renderer *renderer)
{
    if (renderer->faults != UINT32_MAX)
    {
        ++renderer->faults;
    }
    renderer->cache_generation = 0u;
    renderer->cache_revision = 0u;
    renderer->prepared.ready = 0u;
    renderer->phase = M2_RENDER_FATAL;
}

void m2_renderer_init(M2Renderer *renderer)
{
    memset(renderer, 0, sizeof(*renderer));
}

void m2_label_offer(M2Bundle *bundle, uint8_t corner)
{
    if (corner >= M2_FULL_ANCHOR_COUNT || !bundle->anchors[corner].visible
        || bundle->labels[0] == corner || bundle->labels[1] == corner)
    {
        return;
    }
    if (corner < bundle->labels[0])
    {
        bundle->labels[1] = bundle->labels[0];
        bundle->labels[0] = corner;
    }
    else if (corner < bundle->labels[1])
    {
        bundle->labels[1] = corner;
    }
}

static void put_text(char *text, uint16_t offset, const char *value)
{
    while (*value != '\0' && offset < 320u)
    {
        text[offset++] = *value++;
    }
}

static void hex(char *text, uint16_t offset, uint32_t value)
{
    static const char digits[] = "0123456789ABCDEF";
    for (uint8_t i = 0u; i < 8u; ++i)
    {
        text[offset + 7u - i] = digits[value & 15u];
        value >>= 4u;
    }
}

static void telemetry(M2Renderer *renderer, uint32_t tick)
{
    char *text = renderer->workspace.text;
    memset(text, ' ', sizeof(renderer->workspace.text));
    put_text(text, 0u, "NON-FLIGHT  COUNTERS HEX");
    put_text(text, 40u, "TICK");
    hex(text, 45u, renderer->source.tick);
    put_text(text, 60u, "SUM");
    hex(text, 64u, renderer->source.checksum);
    put_text(text, 80u, "GEN");
    hex(text, 84u, renderer->generation);
    put_text(text, 100u, "CAM");
    hex(text, 104u, renderer->prepared.camera.revision);
    put_text(text, 120u, "AGE AT START");
    hex(text, 133u, tick - renderer->source.tick);
    put_text(text, 144u, "H FT DATUM HEX");
    hex(text, 160u, (uint32_t)(-renderer->prepared.camera.position.v[2]
                              / M2_POSITION_SCALE));
    put_text(text, 171u, "CANCEL");
    hex(text, 178u, renderer->cancellations);
    put_text(text, 187u, "FAULT");
    hex(text, 193u, renderer->faults);
    put_text(text, 201u, "ALTITUDE");
    put_text(text, 221u, "AIRSPEED");
    put_text(text, 241u, "NOT IMPLEMENTED");
    put_text(text, 261u, "NOT IMPLEMENTED");
    put_text(text, 281u, "NO FLIGHT STATE OR VALID FLIGHT UNITS");
}

uint8_t m2_renderer_begin(M2Renderer *renderer, const M2Camera *camera,
                          const M1Snapshot *snapshot, uint32_t tick)
{
    if (renderer == 0 || snapshot == 0 || renderer->phase != M2_RENDER_IDLE
        || snapshot->fault != 0u || snapshot->tick > tick || !m2_camera_valid(camera))
    {
        return 0u;
    }
    if (renderer->generation == UINT32_MAX)
    {
        fail(renderer);
        return 0u;
    }
    renderer->prepared.camera = *camera;
    renderer->prepared.ready = 0u;
    renderer->source = *snapshot;
    renderer->sampled_tick = tick;
    ++renderer->generation;
    renderer->pending = (uint8_t)(renderer->displayed ^ 1u);
    renderer->cache_generation = 0u;
    renderer->cache_revision = 0u;
    renderer->phase = M2_RENDER_PREPARE;
    return 1u;
}

static void registration(M2Renderer *renderer)
{
    M2Bundle *bundle = &renderer->bundles[renderer->pending];
    memset(bundle, 0, sizeof(*bundle));
    bundle->composition_revision = M2_FULL_COMPOSITION_REVISION;
    bundle->labels[0] = NO_LABEL;
    bundle->labels[1] = NO_LABEL;
    if (!m2_registration_prepared(&renderer->prepared, renderer->generation,
                                  renderer->source.tick, renderer->pending,
                                  &bundle->registration))
    {
        fail(renderer);
        return;
    }
    renderer->segment = 0u;
    renderer->phase = M2_RENDER_ANCHOR;
}

static void anchor(M2Renderer *renderer)
{
    uint8_t i = renderer->segment;
    M2Point corner;
    M2Point next;
    M2Pixel pixel;
    M2Bundle *bundle = &renderer->bundles[renderer->pending];
    if (!m2_fixture_segment(M2_FIXTURE_REVISION, i, &corner, &next))
    {
        fail(renderer);
        return;
    }
    int8_t visible = m2_project_prepared(&renderer->prepared, &corner, &corner,
                                         &renderer->line);
    if (visible < 0)
    {
        fail(renderer);
        return;
    }
    if (visible == 1)
    {
        if (!m2_raster_begin(&renderer->line, &renderer->cursor)
            || !m2_raster_next(&renderer->cursor, &pixel))
        {
            fail(renderer);
            return;
        }
        bundle->anchors[i].pixel = pixel;
        bundle->anchors[i].visible = 1u;
        m2_label_offer(bundle, i);
    }
    if (++renderer->segment == M2_FULL_ANCHOR_COUNT)
    {
        renderer->phase = M2_RENDER_TELEMETRY;
    }
}

static void cache_segment(M2Renderer *renderer)
{
    uint8_t i = renderer->segment;
    M2Point first;
    M2Point last;
    if (!m2_fixture_segment(M2_FIXTURE_REVISION, i, &first, &last))
    {
        fail(renderer);
        return;
    }
    int8_t visible = m2_project_prepared(&renderer->prepared, &first, &last,
                                         &renderer->workspace.cache.lines[i]);
    if (visible < 0)
    {
        fail(renderer);
        return;
    }
    renderer->workspace.cache.visible[i] = (uint8_t)visible;
    if (++renderer->segment == M2_SEGMENT_COUNT)
    {
        // Publish cache identity only after every entry has been assigned.
        renderer->cache_generation = renderer->generation;
        renderer->cache_revision = renderer->prepared.camera.revision;
        renderer->tile_index = 0u;
        renderer->sample = 0u;
        renderer->phase = M2_RENDER_BACKGROUND;
    }
}

void m2_renderer_cancel(M2Renderer *renderer)
{
    if (renderer->phase != M2_RENDER_IDLE && renderer->phase != M2_RENDER_FATAL)
    {
        if (renderer->cancellations == UINT32_MAX)
        {
            fail(renderer);
            return;
        }
        ++renderer->cancellations;
        renderer->cache_generation = 0u;
        renderer->cache_revision = 0u;
        renderer->prepared.ready = 0u;
        renderer->phase = M2_RENDER_IDLE;
    }
}

static void paint(M2Renderer *renderer, uint16_t x, uint16_t y, uint8_t color)
{
    if (x < M2_WIDTH && y < M2_HEIGHT
        && x / 8u + (y / 8u) * TILE_COLUMNS == renderer->tile_index)
    {
        renderer->tile[(y % 8u) * 8u + x % 8u] = color;
    }
}

static void background(M2Renderer *renderer)
{
    uint16_t index = renderer->tile_index;
    for (uint8_t n = 0u; n < M2_FULL_SAMPLE_QUANTUM; ++n)
    {
        uint8_t sample = renderer->sample++;
        uint16_t x = (uint16_t)((index % TILE_COLUMNS) * 8u + sample % 8u);
        uint16_t y = (uint16_t)((index / TILE_COLUMNS) * 8u + sample / 8u);
        uint8_t color = 0u;
        if (index < WORLD_TILES)
        {
            int8_t ground = m2_ground_prepared(&renderer->prepared, x, y);
            if (ground < 0)
            {
                fail(renderer);
                return;
            }
            color = ground ? COLOR_GROUND : COLOR_SKY;
        }
        else if (index < M2_FULL_TILES)
        {
            char character = renderer->workspace.text[index - WORLD_TILES];
            color = (m2_font_row(character, (uint8_t)(sample / 8u))
                     & (128u >> (sample % 8u))) != 0u ? COLOR_INK : 0u;
        }
        renderer->tile[sample] = color;
    }
    if (renderer->sample == M2_FULL_TILE_BYTES)
    {
        renderer->segment = 0u;
        renderer->phase = index < WORLD_TILES ? M2_RENDER_SEGMENT : M2_RENDER_TRANSFER;
    }
}

static void segment(M2Renderer *renderer)
{
    if (renderer->segment == M2_SEGMENT_COUNT)
    {
        renderer->sample = 0u;
        renderer->phase = M2_RENDER_OVERLAY;
        return;
    }
    uint8_t i = renderer->segment++;
    if (renderer->cache_generation != renderer->generation
        || renderer->cache_revision != renderer->prepared.camera.revision)
    {
        fail(renderer);
        return;
    }
    if (renderer->workspace.cache.visible[i] != 0u)
    {
        if (!m2_raster_begin(&renderer->workspace.cache.lines[i], &renderer->cursor))
        {
            fail(renderer);
            return;
        }
        renderer->phase = M2_RENDER_RASTER;
    }
}

static void overlay(M2Renderer *renderer)
{
    const M2Bundle *bundle = &renderer->bundles[renderer->pending];
    uint16_t index = renderer->tile_index;
    for (uint8_t n = 0u; n < M2_FULL_SAMPLE_QUANTUM; ++n)
    {
        uint8_t sample = renderer->sample++;
        uint16_t x = (uint16_t)((index % TILE_COLUMNS) * 8u + sample % 8u);
        uint16_t y = (uint16_t)((index / TILE_COLUMNS) * 8u + sample / 8u);
        for (uint8_t i = 0u; i < M2_FULL_OPTIONAL_LABELS; ++i)
        {
            uint8_t id = bundle->labels[i];
            if (id != NO_LABEL)
            {
                uint16_t left = (uint16_t)(bundle->anchors[id].pixel.x + 4u);
                uint16_t top = bundle->anchors[id].pixel.y;
                if (x >= left && x < left + 8u && y >= top && y < top + 8u
                    && (m2_font_row((char)('0' + id), (uint8_t)(y - top))
                        & (128u >> (x - left))) != 0u)
                {
                    renderer->tile[sample] = COLOR_INK;
                }
            }
        }
        // Protected anchors are painted last, so labels cannot evict them.
        for (uint8_t i = 0u; i < M2_FULL_ANCHOR_COUNT; ++i)
        {
            const M2Anchor *anchor = &bundle->anchors[i];
            int16_t dx = (int16_t)((int16_t)x - (int16_t)anchor->pixel.x);
            int16_t dy = (int16_t)((int16_t)y - (int16_t)anchor->pixel.y);
            if (anchor->visible && ((dx == 0 && dy >= -2 && dy <= 2)
                || (dy == 0 && dx >= -2 && dx <= 2)))
            {
                renderer->tile[sample] = COLOR_ANCHOR;
            }
        }
    }
    if (renderer->sample == M2_FULL_TILE_BYTES)
    {
        renderer->phase = M2_RENDER_TRANSFER;
    }
}

void m2_renderer_service(M2Renderer *renderer, uint32_t wanted_revision)
{
    if (renderer == 0 || renderer->phase == M2_RENDER_IDLE
        || renderer->phase == M2_RENDER_FATAL)
    {
        return;
    }
    if (renderer->prepared.camera.revision != wanted_revision)
    {
        m2_renderer_cancel(renderer);
        return;
    }
    switch (renderer->phase)
    {
        case M2_RENDER_PREPARE:
            if (!m2_prepare(&renderer->prepared, &renderer->prepared.camera))
            {
                fail(renderer);
                break;
            }
            renderer->phase = M2_RENDER_REGISTER;
            break;
        case M2_RENDER_REGISTER:
            registration(renderer);
            break;
        case M2_RENDER_ANCHOR:
            anchor(renderer);
            break;
        case M2_RENDER_TELEMETRY:
            telemetry(renderer, renderer->sampled_tick);
            // Text lives only through the telemetry/footer transfer phase.
            renderer->tile_index = WORLD_TILES;
            renderer->sample = 0u;
            renderer->phase = M2_RENDER_BACKGROUND;
            break;
        case M2_RENDER_CACHE:
            cache_segment(renderer);
            break;
        case M2_RENDER_BACKGROUND:
            background(renderer);
            break;
        case M2_RENDER_SEGMENT:
            segment(renderer);
            break;
        case M2_RENDER_RASTER:
            for (uint8_t n = 0u; n < M2_FULL_SAMPLE_QUANTUM; ++n)
            {
                M2Pixel pixel;
                if (!m2_raster_next(&renderer->cursor, &pixel))
                {
                    renderer->phase = M2_RENDER_SEGMENT;
                    break;
                }
                paint(renderer, pixel.x, pixel.y, COLOR_INK);
            }
            break;
        case M2_RENDER_OVERLAY:
            overlay(renderer);
            break;
        case M2_RENDER_TRANSFER:
            if (!m2_backend_tile(renderer->pending, renderer->tile_index, renderer->tile))
            {
                fail(renderer);
                break;
            }
            ++renderer->tile_index;
            if (renderer->tile_index > M2_FULL_TILES)
            {
                // All 320 text cells and the blank tile are copied; no backend
                // retains a borrowed pointer. The union can now become a cache.
                renderer->segment = 0u;
                renderer->phase = M2_RENDER_CACHE;
            }
            else if (renderer->tile_index == WORLD_TILES)
            {
                renderer->phase = M2_RENDER_READY;
            }
            else
            {
                renderer->sample = 0u;
                renderer->phase = M2_RENDER_BACKGROUND;
            }
            break;
        default:
            break;
    }
}

uint8_t m2_renderer_commit(M2Renderer *renderer, uint32_t wanted_revision)
{
    if (renderer == 0 || renderer->phase != M2_RENDER_READY)
    {
        return 0u;
    }
    M2Bundle *bundle = &renderer->bundles[renderer->pending];
    if (renderer->prepared.camera.revision != wanted_revision)
    {
        m2_renderer_cancel(renderer);
        return 0u;
    }
    if (bundle->composition_revision != M2_FULL_COMPOSITION_REVISION
        || bundle->registration.generation != renderer->generation
        || bundle->registration.source_tick != renderer->source.tick
        || bundle->registration.store != renderer->pending
        || renderer->pending == renderer->displayed
        || renderer->cache_generation != renderer->generation
        || renderer->cache_revision != wanted_revision
        || !m2_registration_matches_prepared(&renderer->prepared, &bundle->registration,
             renderer->generation, renderer->source.tick, renderer->pending))
    {
        fail(renderer);
        return 0u;
    }
    if (!m2_backend_activate(renderer->pending))
    {
        fail(renderer);
        return 0u;
    }
    renderer->displayed = renderer->pending;
    renderer->has_display = 1u;
    renderer->cache_generation = 0u;
    renderer->cache_revision = 0u;
    renderer->phase = M2_RENDER_IDLE;
    return 1u;
}
