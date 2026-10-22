// Frozen analytic/text/transaction requirements plus legacy geometry regression.
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "camera.h"
#include "dispatch.h"
#include "m1_input.h"
#include "m1_snapshot.h"
#include "m2_camera_input.h"
#include "m2_fixture.h"
#include "m2_renderer.h"

static uint8_t stores[2][M2_FULL_TILES + 1u][M2_FULL_TILE_BYTES];
static uint8_t active;
static uint8_t copy_fail;
static uint8_t activate_fail;
static uint32_t copies;
static uint32_t cache_projections;
static uint32_t hud_copies;
static M2Renderer renderer;

uint8_t m2_backend_tile(uint8_t store, uint16_t index, const uint8_t *bytes)
{
    assert(store < 2u && store != active && index <= M2_FULL_TILES);
    if (copy_fail)
    {
        return 0u;
    }
    if (index >= 640u)
    {
        ++hud_copies;
    }
    memcpy(stores[store][index], bytes, M2_FULL_TILE_BYTES);
    ++copies;
    return 1u;
}

uint8_t m2_backend_activate(uint8_t store)
{
    assert(store != active && store < 2u);
    if (activate_fail)
    {
        return 0u;
    }
    active = store;
    return 1u;
}

static void reset(void)
{
    m2_renderer_init(&renderer);
    memset(stores, 0xa5, sizeof(stores));
    active = 0u;
    copies = 0u;
    cache_projections = 0u;
    hud_copies = 0u;
    copy_fail = 0u;
    activate_fail = 0u;
}

static uint8_t pixel(uint16_t x, uint16_t y)
{
    uint16_t tile = y >= 192u ? M2_FULL_TILES : (uint16_t)((y / 8u) * 40u + x / 8u);
    return stores[active][tile][(y % 8u) * 8u + x % 8u];
}

static void finish(uint32_t revision)
{
    unsigned steps = 0u;
    while (renderer.phase != M2_RENDER_READY)
    {
        uint32_t before = copies;
        uint8_t phase = renderer.phase;
        uint8_t sample = renderer.sample;
        if (phase == M2_RENDER_CACHE)
        {
            assert(hud_copies == 321u);
            assert(renderer.cache_generation == 0u);
            ++cache_projections;
        }
        m2_renderer_service(&renderer, revision);
        assert(renderer.phase != M2_RENDER_FATAL);
        assert(copies - before <= 1u);
        if (phase == M2_RENDER_BACKGROUND || phase == M2_RENDER_OVERLAY)
        {
            assert(renderer.sample - sample == M2_FULL_SAMPLE_QUANTUM);
        }
        assert(++steps < 2000000u);
    }
}

static void image(const char *directory, unsigned pose)
{
    char path[1024];
    assert(snprintf(path, sizeof(path), "%s/pose-%u.ppm", directory, pose) > 0);
    FILE *file = fopen(path, "wb");
    assert(file != 0);
    fputs("P6\n320 200\n255\n", file);
    static const uint8_t palette[8][3] =
    {
        {0,0,0}, {255,255,255}, {255,0,0}, {0,255,255},
        {255,0,255}, {0,128,0}, {0,80,220}, {255,255,0}
    };
    for (uint16_t y = 0u; y < 200u; ++y)
    {
        for (uint16_t x = 0u; x < 320u; ++x)
        {
            uint8_t color = pixel(x, y);
            assert(color < 8u);
            assert(fwrite(palette[color], 1u, 3u, file) == 3u);
        }
    }
    assert(fclose(file) == 0);
}

static void poses(const char *directory)
{
    const int16_t yaw[] = {0, 0, 0, 0, 180};
    const int16_t pitch[] = {-5, 60, -60, 0, -5};
    const int16_t roll[] = {0, 0, 0, 60, 0};
    M1Snapshot snapshot = {600u, 24u, 0xDE675132ul, 0u};
    for (unsigned pose = 0u; pose < 5u; ++pose)
    {
        reset();
        M2Camera camera;
        m2_camera_reset(&camera);
        camera.yaw = yaw[pose];
        camera.pitch = pitch[pose];
        camera.roll = roll[pose];
        assert(m2_renderer_begin(&renderer, &camera, &snapshot, 620u));
        finish(camera.revision);
        assert(copies == M2_FULL_TILES + 1u);
        assert(cache_projections == 17u);
        assert(renderer.cache_generation == renderer.generation);
        assert(renderer.cache_revision == camera.revision);
        for (uint8_t segment = 0u; segment < M2_SEGMENT_COUNT; ++segment)
        {
            M2Point first;
            M2Point last;
            M2Line expected;
            assert(m2_fixture_segment(M2_FIXTURE_REVISION, segment, &first, &last));
            int8_t visible = m2_project_segment(&camera, &first, &last, &expected);
            assert(visible >= 0);
            assert(renderer.workspace.cache.visible[segment] == (uint8_t)visible);
            if (visible == 1)
            {
                assert(memcmp(&expected, &renderer.workspace.cache.lines[segment], sizeof(expected)) == 0);
            }
        }
        // Every hidden tile was replaced; displayed storage remained untouched.
        for (unsigned tile = 0u; tile <= M2_FULL_TILES; ++tile)
        {
            for (unsigned sample = 0u; sample < 64u; ++sample)
            {
                assert(stores[0][tile][sample] == 0xa5u);
                assert(stores[1][tile][sample] < 8u);
            }
        }
        assert(m2_renderer_commit(&renderer, camera.revision));
        assert(renderer.has_display && active == renderer.displayed);
        for (uint16_t y = 0u; y < 128u; ++y)
        {
            for (uint16_t x = 0u; x < 320u; ++x)
            {
                if (pose == 1u)
                {
                    assert(pixel(x, y) == 6u);
                }
                if (pose == 2u)
                {
                    assert(pixel(x, y) == 5u || pixel(x, y) == 1u || pixel(x, y) == 7u);
                }
            }
        }
        for (uint16_t y = 192u; y < 200u; ++y)
        {
            for (uint16_t x = 0u; x < 320u; ++x)
            {
                assert(pixel(x, y) == 0u);
            }
        }
        // Text no longer lives in the union: check the completed HUD tiles.
        const char *labels[] = {"ALTITUDE", "AIRSPEED", "NOT IMPLEMENTED", "NOT IMPLEMENTED"};
        const uint16_t offsets[] = {201u, 221u, 241u, 261u};
        for (unsigned label = 0u; label < 4u; ++label)
        {
            for (unsigned c = 0u; labels[label][c] != '\0'; ++c)
            {
                uint16_t cell = (uint16_t)(offsets[label] + c);
                for (uint8_t row = 0u; row < 8u; ++row)
                {
                    for (uint8_t bit = 0u; bit < 8u; ++bit)
                    {
                        uint8_t ink = (m2_font_row(labels[label][c], row) & (128u >> bit)) != 0u;
                        assert(pixel((uint16_t)((cell % 40u) * 8u + bit),
                                     (uint16_t)(128u + (cell / 40u) * 8u + row)) == ink);
                    }
                }
            }
        }
        image(directory, pose);
    }
}

static void transactions(void)
{
    M2Camera camera;
    m2_camera_reset(&camera);
    M1Snapshot snapshot = {1u, 0u, 0u, 0u};
    for (uint8_t phase = M2_RENDER_PREPARE; phase <= M2_RENDER_READY; ++phase)
    {
        reset();
        assert(m2_renderer_begin(&renderer, &camera, &snapshot, 1u));
        unsigned steps = 0u;
        while (renderer.phase != phase)
        {
            m2_renderer_service(&renderer, 1u);
            assert(++steps < 2000000u);
        }
        m2_renderer_service(&renderer, 2u);
        assert(renderer.phase == M2_RENDER_IDLE && renderer.cancellations == 1u);
        assert(renderer.cache_generation == 0u && renderer.cache_revision == 0u);
        assert(m2_renderer_begin(&renderer, &camera, &snapshot, 1u));
        assert(renderer.phase == M2_RENDER_PREPARE && renderer.cache_generation == 0u);
        m2_renderer_cancel(&renderer);
        assert(active == 0u && !m2_renderer_commit(&renderer, 1u));
    }
    reset();
    assert(m2_renderer_begin(&renderer, &camera, &snapshot, 1u));
    copy_fail = 1u;
    while (renderer.phase != M2_RENDER_FATAL)
    {
        m2_renderer_service(&renderer, 1u);
    }
    assert(active == 0u && renderer.faults == 1u);
    assert(renderer.cache_generation == 0u && renderer.cache_revision == 0u);
    reset();
    assert(m2_renderer_begin(&renderer, &camera, &snapshot, 1u));
    finish(1u);
    activate_fail = 1u;
    assert(!m2_renderer_commit(&renderer, 1u));
    assert(renderer.phase == M2_RENDER_FATAL && !renderer.has_display);
    assert(renderer.cache_generation == 0u && renderer.cache_revision == 0u);
    reset();
    assert(m2_renderer_begin(&renderer, &camera, &snapshot, 1u));
    finish(1u);
    ++renderer.bundles[renderer.pending].registration.transform.m[0];
    assert(!m2_renderer_commit(&renderer, 1u));
    assert(renderer.phase == M2_RENDER_FATAL && renderer.cache_generation == 0u);
    reset();
    assert(m2_renderer_begin(&renderer, &camera, &snapshot, 1u));
    finish(1u);
    renderer.cache_revision = 2u;
    assert(!m2_renderer_commit(&renderer, 1u));
    assert(renderer.phase == M2_RENDER_FATAL && renderer.cache_generation == 0u);
    reset();
    renderer.generation = UINT32_MAX;
    assert(!m2_renderer_begin(&renderer, &camera, &snapshot, 1u));
    assert(renderer.phase == M2_RENDER_FATAL);
    reset();
    assert(!m2_renderer_begin(&renderer, &camera, 0, 1u));
    snapshot.fault = 1u;
    assert(!m2_renderer_begin(&renderer, &camera, &snapshot, 1u));
    snapshot.fault = 0u;
    assert(m2_renderer_begin(&renderer, &camera, &snapshot, 1u));
    finish(1u);
    renderer.bundles[renderer.pending].composition_revision = 1u;
    assert(!m2_renderer_commit(&renderer, 1u));
    assert(renderer.phase == M2_RENDER_FATAL);
}

static void camera_and_labels(void)
{
    M2Camera camera;
    m2_camera_reset(&camera);
    uint16_t previous = 0u;
    assert(m2_camera_command(&camera, m2_camera_pressed(&previous, M2_NORTH_PLUS)) == 2u);
    assert(camera.position.v[0] == -4475L * M2_POSITION_SCALE);
    assert(m2_camera_command(&camera, m2_camera_pressed(&previous, M2_NORTH_PLUS)) == 1u);
    assert(m2_camera_command(&camera, M2_NORTH_PLUS | M2_NORTH_MINUS) == 1u);
    assert(m2_camera_command(&camera, M2_CAMERA_RESET | M2_NORTH_PLUS) == 2u);
    camera.revision = UINT32_MAX;
    M2Camera saved = camera;
    assert(!m2_camera_command(&camera, M2_YAW_PLUS));
    assert(memcmp(&camera, &saved, sizeof(camera)) == 0);
    camera.revision = 1u;
    camera.pitch = 60;
    assert(!m2_camera_command(&camera, M2_PITCH_PLUS));
    for (uint8_t a = 0u; a < 4u; ++a)
    {
        for (uint8_t b = 0u; b < 4u; ++b)
        {
            for (uint8_t c = 0u; c < 4u; ++c)
            {
                if (a == b || a == c || b == c)
                {
                    continue;
                }
                uint8_t d = (uint8_t)(6u - a - b - c);
                M2Bundle bundle = {0};
                for (uint8_t i = 0u; i < 4u; ++i)
                {
                    bundle.anchors[i].visible = 1u;
                }
                bundle.labels[0] = 255u;
                bundle.labels[1] = 255u;
                m2_label_offer(&bundle, a);
                m2_label_offer(&bundle, b);
                m2_label_offer(&bundle, c);
                m2_label_offer(&bundle, d);
                assert(bundle.labels[0] == 0u && bundle.labels[1] == 1u);
                for (uint8_t i = 0u; i < 4u; ++i)
                {
                    assert(bundle.anchors[i].visible == 1u);
                }
            }
        }
    }
}

static void replay(void)
{
    M1Core core[3];
    M1Snapshots pools[3] = {0};
    M1Input input[3] = {0};
    M2Renderer renderers[2];
    M2Camera camera;
    m2_camera_reset(&camera);
    uint8_t stages[M1_STAGES];
    for (uint8_t mode = 0u; mode < 3u; ++mode)
    {
        m1_core_init(&core[mode]);
        if (mode != 0u)
        {
            m2_renderer_init(&renderers[mode - 1u]);
        }
    }
    for (uint32_t tick = 0u; tick < 600u; ++tick)
    {
        for (uint8_t mode = 0u; mode < 3u; ++mode)
        {
            assert(m1_input_sample(&input[mode], &core[mode], (uint8_t)((tick / 25u) & 1u)));
            m1_tick(&core[mode], &pools[mode], stages);
            if (mode != 0u)
            {
                M2Renderer *r = &renderers[mode - 1u];
                uint8_t slot = m1_acquire(&pools[mode]);
                if (slot < M1_SNAPSHOT_SLOTS)
                {
                    M1Snapshot source = pools[mode].slots[slot];
                    m1_release(&pools[mode], slot);
                    if (r->phase == M2_RENDER_IDLE)
                    {
                        assert(m2_renderer_begin(r, &camera, &source, core[mode].tick));
                    }
                }
                // Both modes cancel before any transfer; this checks Core isolation.
                m2_renderer_service(r, camera.revision);
                if (mode == 1u || tick % 17u == 0u)
                {
                    m2_renderer_cancel(r);
                }
            }
        }
        assert(core[0].checksum == core[1].checksum && core[0].checksum == core[2].checksum);
    }
    assert(core[0].checksum == 0xDE675132ul);
    // Full and held pool semantics retain payloads across attempted publication.
    M1Snapshots pool = {0};
    M1Snapshot source = {1u, 0u, 123u, 0u};
    assert(m1_publish(&pool, &source));
    uint8_t held = m1_acquire(&pool);
    assert(held < M1_SNAPSHOT_SLOTS);
    for (uint8_t i = 1u; i < M1_SNAPSHOT_SLOTS; ++i)
    {
        assert(m1_publish(&pool, &source));
    }
    assert(!m1_publish(&pool, &source));
    assert(pool.slots[held].checksum == 123u);
    m1_release(&pool, held);
    assert(m1_publish(&pool, &source));
}

int main(int argc, char **argv)
{
    assert(argc == 2);
    poses(argv[1]);
    transactions();
    camera_and_labels();
    replay();
    assert(m2_dispatch_allows(100u, 120u, 15u, 5u));
    assert(!m2_dispatch_allows(101u, 120u, 15u, 5u));
    assert(!m2_dispatch_allows(100u, 120u, 0u, 5u));
    assert(!m2_dispatch_allows(100u, 120u, 5u, 0u));
    assert(!m2_dispatch_allows(120u, 120u, 1u, 1u));
    assert(!m2_dispatch_allows(121u, 120u, 1u, 1u));
    assert(!m2_dispatch_allows(0u, 10u, UINT32_MAX, 1u));
    assert(m2_dispatch_allows(UINT32_MAX - 4u, 10u, 10u, 5u));
    M2Dispatch dispatch = {UINT32_MAX - 4u, 0u};
    for (unsigned i = 0u; i < 4u; ++i)
    {
        m2_dispatch_next(&dispatch, (10ul << 16u) + 32768u);
    }
    assert(dispatch.release == 37u && dispatch.fraction == 0u);
    puts("PASS generation-cache/workspace/dispatch; five host images, bounds/hidden writes, analytic sky/ground, footer/text, cancellation/faults, label permutations, camera edges and 600-tick replay");
    return 0;
}
