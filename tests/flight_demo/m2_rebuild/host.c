// Synthetic host timing/copies establish behavior only; no target qualification.
#include <assert.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "camera.h"
#include "guard.h"
#include "io.h"
#include "m1_input.h"
#include "m2_fixture.h"
#include "m2_rebuild.h"

static uint8_t stores[2][M2RB_STORE_BYTES];
static uint8_t selected;
static uint8_t selected_valid;
static uint32_t copies;
static uint32_t fail_at;
static int8_t commit_result;
static uint32_t commit_calls;

// Explicit synthetic tick input; never target execution/timing evidence.
static uint32_t current_tick = 1000u;

static uint8_t dispatch(M2RebuildRenderer *renderer, M1Snapshots *pool,
                         const M2Camera *camera, uint32_t budget)
{
    return m2rb_dispatch(renderer, pool, camera, budget, current_tick);
}

uint8_t m2rb_io_write(uint8_t store, uint16_t offset,
                       const uint8_t *bytes, uint8_t count)
{
    assert(store < 2u && count != 0u && count <= 64u);
    assert(offset >= M2RB_TILE_OFFSET);
    assert((uint32_t)offset + count <= M2RB_BLANK_OFFSET);
    assert(!selected_valid || store != selected);
    ++copies;
    if (fail_at != 0u && copies == fail_at)
    {
        return 0u;
    }
    memcpy(&stores[store][offset], bytes, count);
    return 1u;
}

int8_t m2rb_io_commit(uint8_t store)
{
    ++commit_calls;
    if (commit_result == 1)
    {
        selected = store;
        selected_valid = 1u;
    }
    return commit_result;
}

static void reset_backend(void)
{
    memset(stores, M2RB_BLACK, sizeof(stores));
    selected = 0u;
    selected_valid = 0u;
    copies = 0u;
    fail_at = 0u;
    commit_calls = 0u;
    commit_result = 1;
    current_tick = 1000u;
}

static void publish(M1Snapshots *pool, uint32_t tick)
{
    M1Snapshot sample = {tick, 17u, 0x12345678u, 0u};
    assert(m1_publish(pool, &sample));
}

static void until(M2RebuildRenderer *renderer, M1Snapshots *pool,
                  const M2Camera *camera, uint8_t phase)
{
    // Nine <=2500-step projections + horizon/paint/copy/raster/text <32768.
    for (uint32_t work = 0u; work < 32768u; ++work)
    {
        if (renderer->phase == phase)
        {
            return;
        }
        assert(renderer->fault == 0u);
        assert(dispatch(renderer, pool, camera, 1u));
    }
    assert(0 && "finite renderer operation cap exhausted");
}

static uint8_t pixel(uint8_t store, uint16_t x, uint16_t y)
{
    uint16_t tile = (uint16_t)((y / 8u) * 40u + x / 8u);
    return stores[store][M2RB_TILE_OFFSET + tile * 64u + (y % 8u) * 8u + x % 8u];
}

// A separate frame assembly uses the public batch geometry path and draws all
// world pixels directly. The Decimal geometry oracle is run separately.
static void compare_world(const M2Camera *camera, uint8_t store)
{
    static uint8_t expected[128][320];
    struct M2Prepared prepared;
    assert(m2_prepare(&prepared, camera));
    for (uint16_t y = 0u; y < 128u; ++y)
    {
        for (uint16_t x = 0u; x < 320u; ++x)
        {
            int64_t down = prepared.rotation.m[2] * 320L
                + prepared.rotation.m[5] * (2L * x - 319L)
                + prepared.rotation.m[8] * (2L * y - 127L);
            expected[y][x] = down > 0 ? M2RB_GROUND : M2RB_SKY;
        }
    }
    for (uint8_t i = 0u; i < 9u; ++i)
    {
        M2Point first;
        M2Point last;
        M2Line line;
        assert(m2_fixture_segment(1u, m2rb_segment_ids[i], &first, &last));
        int8_t visible = m2_project_segment(camera, &first, &last, &line);
        assert(visible >= 0);
        if (visible)
        {
            M2Pixel pixels[320];
            uint16_t count;
            assert(m2_raster_line(&line, pixels, 320u, &count));
            for (uint16_t j = 0u; j < count; ++j)
            {
                expected[pixels[j].y][pixels[j].x] = M2RB_WHITE;
            }
        }
    }
    uint32_t counts[5] = {0};
    for (uint16_t y = 0u; y < 128u; ++y)
    {
        for (uint16_t x = 0u; x < 320u; ++x)
        {
            assert(pixel(store, x, y) == expected[y][x]);
            ++counts[expected[y][x]];
        }
    }
    if (camera->yaw == 0 && camera->pitch == -5 && camera->roll == 0)
    {
        assert(counts[M2RB_SKY] > 1000u && counts[M2RB_GROUND] > 1000u);
        assert(counts[M2RB_WHITE] > 0u);
        printf("default world exact comparison: sky %u ground %u runway %u pixels\n",
               counts[M2RB_SKY], counts[M2RB_GROUND], counts[M2RB_WHITE]);
    }
}

static void camera_tests(void)
{
    M2Camera camera;
    M2RebuildInput input = {0};
    m2rb_camera_init(&camera);
    assert(m2rb_camera_edges(&camera, m2rb_input_edges(&input, M2RB_NORTH)) == 1);
    assert(camera.position.v[0] == -4475L * M2_POSITION_SCALE);
    assert(m2rb_camera_edges(&camera, m2rb_input_edges(&input, M2RB_NORTH)) == 0);
    (void)m2rb_input_edges(&input, 0u);
    assert(m2rb_camera_edges(&camera, M2RB_NORTH | M2RB_SOUTH) == 0);
    assert(m2rb_camera_edges(&camera, M2RB_RESET | M2RB_NORTH) == 1);
    assert(camera.position.v[0] == -4500L * M2_POSITION_SCALE);
    assert(m2rb_camera_edges(&camera, M2RB_YAW_LEFT) == 1 && camera.yaw == 359);
    assert(m2rb_camera_edges(&camera, M2RB_YAW_RIGHT) == 1 && camera.yaw == 0);
    camera.position.v[0] = M2_NORTH_LIMIT_FT * M2_POSITION_SCALE;
    camera.position.v[1] = -M2_EAST_LIMIT_FT * M2_POSITION_SCALE;
    camera.position.v[2] = -M2_HEIGHT_MAX_FT * M2_POSITION_SCALE;
    camera.pitch = M2_TILT_LIMIT_DEG;
    camera.roll = -M2_TILT_LIMIT_DEG;
    M2Camera saved = camera;
    assert(m2rb_camera_edges(&camera,
        M2RB_NORTH | M2RB_WEST | M2RB_UP | M2RB_PITCH_UP | M2RB_ROLL_LEFT) == 0);
    assert(m2rb_camera_equal(&camera, &saved));
    camera.revision = UINT32_MAX;
    saved = camera;
    assert(m2rb_camera_edges(&camera, M2RB_SOUTH) == -1);
    assert(m2rb_camera_equal(&camera, &saved));
    camera.pitch = 61;
    assert(m2rb_camera_edges(&camera, M2RB_RESET) == -1);
}

static void guard_tests(void)
{
    assert(!m2rb_guard(100u, 1000u, 0u, 1u));
    assert(!m2rb_guard(100u, 1000u, 1u, 0u));
    assert(!m2rb_guard(100u, 1000u, UINT32_MAX, 1u));
    assert(!m2rb_guard(100u, 100u, 1u, 1u));
    assert(!m2rb_guard(101u, 100u, 1u, 1u));
    assert(!m2rb_guard(100u, 1000u, 899u, 1u));
    assert(m2rb_guard(100u, 1000u, 898u, 1u));
    assert(m2rb_guard(UINT32_MAX - 9u, 20u, 20u, 9u));
    assert(!m2rb_guard(0u, 0x80000000u, 1u, 1u));
}

static void complete_frame(const char *output)
{
    M2RebuildRenderer renderer;
    M1Snapshots pool = {0};
    M2Camera camera;
    m2rb_camera_init(&camera);
    m2rb_renderer_init(&renderer);
    reset_backend();
    publish(&pool, 42u);
    M2RebuildRenderer unchanged = renderer;
    assert(!dispatch(&renderer, &pool, &camera, 0u));
    assert(memcmp(&unchanged, &renderer, sizeof(renderer)) == 0);
    until(&renderer, &pool, &camera, M2RB_COMMIT);
    assert(renderer.prepared_count == 1u && renderer.projected_count == 9u);
    assert(renderer.commits == 0u && !renderer.shown && !selected_valid);
    for (uint8_t i = 0u; i < 3u; ++i)
    {
        assert(pool.state[i] == 0u);
    }
    compare_world(&camera, renderer.destination);
    m2rb_text_row(&renderer, 0u);
    assert(memcmp(renderer.text, "NON-FLIGHT DIAGNOSTIC", 21u) == 0);
    m2rb_text_row(&renderer, 1u);
    assert(memcmp(renderer.text, "TICK 0000002A CMD 00000011", 26u) == 0);
    m2rb_text_row(&renderer, 6u);
    assert(memcmp(renderer.text, "ALTITUDE: NOT IMPLEMENTED", 25u) == 0);
    m2rb_text_row(&renderer, 7u);
    assert(memcmp(renderer.text + 15u, "AIRSPEED: NOT IMPLEMENTED", 25u) == 0);
    commit_result = 0;
    assert(dispatch(&renderer, &pool, &camera, 1u));
    assert(!renderer.shown && renderer.phase == M2RB_COMMIT);
    commit_result = 1;
    assert(dispatch(&renderer, &pool, &camera, 1u));
    assert(renderer.commits == 1u && renderer.shown && renderer.front == selected);
    assert(renderer.bundles[selected].registration.source_tick == 42u);
    assert(renderer.bundles[selected].composition_revision == 3u);
    assert(renderer.bundles[selected].registration.composition_revision == M2_COMPOSITION_REVISION);
    FILE *file = fopen(output, "wb");
    assert(file != NULL);
    for (uint16_t y = 0u; y < 200u; ++y)
    {
        for (uint16_t x = 0u; x < 320u; ++x)
        {
            uint8_t value = y < 192u ? pixel(selected, x, y) : M2RB_BLACK;
            assert(fwrite(&value, 1u, 1u, file) == 1u);
        }
    }
    assert(fclose(file) == 0);
    uint8_t previous_store = selected;
    static uint8_t front_copy[M2RB_STORE_BYTES];
    memcpy(front_copy, stores[selected], sizeof(front_copy));
    publish(&pool, 43u);
    fail_at = copies + 1u;
    until(&renderer, &pool, &camera, M2RB_COPY);
    assert(dispatch(&renderer, &pool, &camera, 1u));
    assert(renderer.fault == 4u && renderer.phase == M2RB_FAILED);
    assert(renderer.front == previous_store && selected == previous_store);
    assert(memcmp(front_copy, stores[selected], sizeof(front_copy)) == 0);
}

static void source_age_generations(void)
{
    M2RebuildRenderer renderer;
    M1Snapshots pool = {0};
    M2Camera camera;
    m2rb_camera_init(&camera);
    m2rb_renderer_init(&renderer);
    reset_backend();
    publish(&pool, 42u);
    until(&renderer, &pool, &camera, M2RB_TEXT);
    current_tick = 50u;
    assert(dispatch(&renderer, &pool, &camera, 1u));
    assert(renderer.source_age_at_text == 8u);
    until(&renderer, &pool, &camera, M2RB_COMMIT);
    // Time may advance before publication. The label explicitly names the
    // telemetry construction point; it must not claim a current display age.
    current_tick = 90u;
    commit_result = 0;
    assert(dispatch(&renderer, &pool, &camera, 1u));
    assert(renderer.source_age_at_text == 8u);
    commit_result = 1;
    assert(dispatch(&renderer, &pool, &camera, 1u));
    assert(renderer.bundles[renderer.front].registration.source_tick == 42u);
    m2rb_text_row(&renderer, 3u);
    assert(memcmp(renderer.text, "AGE AT TEXT 00000008", 20u) == 0);
    publish(&pool, 100u);
    until(&renderer, &pool, &camera, M2RB_TEXT);
    current_tick = 105u;
    assert(dispatch(&renderer, &pool, &camera, 1u));
    // The previous displayed source is 42; the new source is 100, so age is
    // five, not 63. Both successful generations carry their own source age.
    assert(renderer.source_age_at_text == 5u);
    until(&renderer, &pool, &camera, M2RB_COMMIT);
    assert(dispatch(&renderer, &pool, &camera, 1u));
    assert(renderer.commits == 2u);
    assert(renderer.bundles[renderer.front].registration.source_tick == 100u);
    m2rb_text_row(&renderer, 3u);
    assert(memcmp(renderer.text, "AGE AT TEXT 00000005", 20u) == 0);
    uint8_t old_front = renderer.front;
    publish(&pool, 200u);
    until(&renderer, &pool, &camera, M2RB_TEXT);
    current_tick = 199u;
    assert(dispatch(&renderer, &pool, &camera, 1u));
    assert(renderer.fault == 8u && renderer.phase == M2RB_FAILED);
    assert(renderer.front == old_front && renderer.commits == 2u);
}

static void cancellation_and_faults(void)
{
    const uint8_t phases[] = {M2RB_PREPARE, M2RB_PROJECT, M2RB_BACKGROUND,
                              M2RB_COPY, M2RB_LINE, M2RB_TEXT, M2RB_COMMIT};
    for (uint8_t i = 0u; i < sizeof(phases); ++i)
    {
        M2RebuildRenderer renderer;
        M1Snapshots pool = {0};
        M2Camera camera;
        m2rb_camera_init(&camera);
        m2rb_renderer_init(&renderer);
        reset_backend();
        publish(&pool, 1u);
        until(&renderer, &pool, &camera, phases[i]);
        assert(m2rb_camera_edges(&camera, M2RB_YAW_RIGHT) == 1);
        uint32_t before = copies;
        assert(dispatch(&renderer, &pool, &camera, 1u));
        assert(renderer.phase == M2RB_BEGIN && renderer.cancellations == 1u);
        assert(!renderer.prepared.ready && copies == before && !selected_valid);
        for (uint8_t line = 0u; line < 9u; ++line)
        {
            assert(renderer.visible[line] == 0u);
        }
        publish(&pool, 2u);
        until(&renderer, &pool, &camera, M2RB_COMMIT);
        compare_world(&camera, renderer.destination);
        assert(dispatch(&renderer, &pool, &camera, 1u));
        assert(renderer.bundles[renderer.front].registration.camera.revision == camera.revision);
    }
    // A changed pose cannot borrow an existing revision to publish stale geometry.
    M2RebuildRenderer renderer;
    M1Snapshots pool = {0};
    M2Camera camera;
    m2rb_camera_init(&camera);
    m2rb_renderer_init(&renderer);
    reset_backend();
    publish(&pool, 3u);
    until(&renderer, &pool, &camera, M2RB_COMMIT);
    renderer.bundles[renderer.destination].registration.transform.m[0]++;
    assert(dispatch(&renderer, &pool, &camera, 1u));
    assert(renderer.fault == 5u && !selected_valid && commit_calls == 0u);
    m2rb_renderer_init(&renderer);
    publish(&pool, 4u);
    until(&renderer, &pool, &camera, M2RB_COMMIT);
    commit_result = -1;
    assert(dispatch(&renderer, &pool, &camera, 1u));
    assert(renderer.fault == 6u && !renderer.shown);
    assert(!dispatch(&renderer, &pool, &camera, 1u));
    m2rb_renderer_init(&renderer);
    renderer.generation = UINT32_MAX;
    publish(&pool, 5u);
    assert(dispatch(&renderer, &pool, &camera, 1u));
    assert(renderer.fault == 1u);
    m2rb_renderer_init(&renderer);
    uint8_t slot = m1_acquire(&pool);
    m1_release(&pool, slot);
    M1Snapshot bad = {6u, 0u, 0u, 1u};
    assert(m1_publish(&pool, &bad));
    assert(dispatch(&renderer, &pool, &camera, 1u));
    assert(renderer.fault == 2u && renderer.phase == M2RB_FAILED);
}

static void held_and_replay(void)
{
    M1Core core[3];
    M1Snapshots pools[3] = {0};
    M1Input inputs[3] = {0};
    M2RebuildRenderer renderer[2];
    M2Camera camera[2];
    uint8_t stages[M1_STAGES];
    reset_backend();
    // Replay rendering uses the same hidden destination; don't publish in this test.
    commit_result = 0;
    for (uint8_t mode = 0u; mode < 3u; ++mode)
    {
        m1_core_init(&core[mode]);
        if (mode < 2u)
        {
            m2rb_renderer_init(&renderer[mode]);
            m2rb_camera_init(&camera[mode]);
        }
    }
    publish(&pools[2], 0u);
    uint8_t held = m1_acquire(&pools[2]);
    M1Snapshot saved = pools[2].slots[held];
    for (uint32_t tick = 0u; tick < 600u; ++tick)
    {
        for (uint8_t mode = 0u; mode < 3u; ++mode)
        {
            (void)m1_input_sample(&inputs[mode], &core[mode], (uint8_t)((tick / 25u) & 1u));
            m1_tick(&core[mode], &pools[mode], stages);
            for (uint8_t stage = 0u; stage < M1_STAGES; ++stage)
            {
                assert(stages[stage] == stage + 1u);
            }
            if (mode < 2u)
            {
                if (mode == 1u && tick % 17u == 0u)
                {
                    assert(m2rb_camera_edges(&camera[mode], M2RB_YAW_RIGHT) == 1);
                }
                uint8_t quanta = mode == 0u ? 40u : 1u;
                for (uint8_t work = 0u; work < quanta; ++work)
                {
                    assert(dispatch(&renderer[mode], &pools[mode], &camera[mode], 1u));
                }
            }
        }
        assert(core[0].tick == tick + 1u && core[0].checksum == core[1].checksum);
        assert(core[0].checksum == core[2].checksum);
        assert(memcmp(&saved, &pools[2].slots[held], sizeof(saved)) == 0);
    }
    assert(pools[2].state[held] == 2u && pools[2].rejected > 0u);
    assert(core[0].checksum == 0xDE675132u);
    m1_release(&pools[2], held);
}

static void exact_horizon_spans(void)
{
    static const int16_t tilts[] = {-60,-59,-45,-1,0,1,45,59,60};
    uint32_t comparisons = 0u;
    uint16_t maximum_work = 0u;
    for (uint8_t pitch = 0u; pitch < sizeof(tilts) / sizeof(tilts[0]); ++pitch)
    {
        for (uint8_t roll = 0u; roll < sizeof(tilts) / sizeof(tilts[0]); ++roll)
        {
            for (uint16_t yaw = 0u; yaw < 360u; yaw += 89u)
            {
                M2Camera camera;
                m2rb_camera_init(&camera);
                camera.pitch = tilts[pitch];
                camera.roll = tilts[roll];
                camera.yaw = (int16_t)yaw;
                struct M2Prepared prepared;
                assert(m2_prepare(&prepared, &camera));
                M2Compact work;
                M2Horizon horizon;
                m2c_horizon_begin(&horizon);
                uint16_t count = 0u;
                int8_t result;
                do
                {
                    result = m2c_horizon_service(&horizon, &work, &prepared);
                    assert(++count <= 469u && result >= 0);
                } while (result == 0);
                if (count > maximum_work)
                {
                    maximum_work = count;
                }
                for (uint16_t y = 0u; y < 128u; ++y)
                {
                    for (uint16_t x = 0u; x < 320u; ++x)
                    {
                        int64_t down = prepared.rotation.m[2] * 320L
                            + prepared.rotation.m[5] * (2L * x - 319L)
                            + prepared.rotation.m[8] * (2L * y - 127L);
                        uint8_t ground = horizon.positive ? x >= horizon.boundary[y]
                                                         : x < horizon.boundary[y];
                        assert(ground == (down > 0));
                        ++comparisons;
                    }
                }
            }
        }
    }
    printf("HORIZON PASS: %u exact pixels, max %u preparation services (not cycles)\n",
           comparisons, maximum_work);
}

static void cancel_every_numeric_boundary(void)
{
    M2RebuildRenderer renderer;
    M1Snapshots pool = {0};
    M2Camera camera;
    m2rb_camera_init(&camera);
    m2rb_renderer_init(&renderer);
    reset_backend();
    publish(&pool, 42u);
    uint32_t cutpoints = 0u;
    for (uint32_t steps = 0u; steps < 23000u; ++steps)
    {
        if (renderer.phase == M2RB_BACKGROUND)
        {
            printf("CANCELLATION PASS: %u numeric continuation cutpoints\n", cutpoints);
            return;
        }
        if (renderer.phase == M2RB_PREPARE || renderer.phase == M2RB_PROJECT)
        {
            M2RebuildRenderer cancelled = renderer;
            M1Snapshots cancelled_pool = pool;
            M2Camera changed = camera;
            assert(m2rb_camera_edges(&changed, M2RB_YAW_RIGHT) == 1);
            assert(dispatch(&cancelled, &cancelled_pool, &changed, 1u));
            assert(cancelled.phase == M2RB_BEGIN && !cancelled.prepared.ready);
            assert(cancelled.cancellations == 1u && copies == 0u);
            // The captured snapshot was already released. A fresh generation
            // waits for a new publication; the cloned test must not consume
            // the original renderer's pool.
            publish(&cancelled_pool, 43u);
            assert(dispatch(&cancelled, &cancelled_pool, &changed, 1u));
            assert(cancelled.phase == M2RB_PREPARE && cancelled.geometry.job.phase == 0u);
            assert(cancelled.prepared.camera.revision == changed.revision);
            ++cutpoints;
        }
        assert(dispatch(&renderer, &pool, &camera, 1u) && !renderer.fault);
    }
    assert(0 && "numeric preparation must exhaust its proved cardinality");
}

int main(int argc, char **argv)
{
    assert(argc == 2);
    camera_tests();
    guard_tests();
    complete_frame(argv[1]);
    source_age_generations();
    cancellation_and_faults();
    held_and_replay();
    exact_horizon_spans();
    cancel_every_numeric_boundary();
    puts("HOST PASS: frame/cache/camera/horizon/cancellation/held/fault/exhaustion/guard/replay DE675132");
    printf("host workspace %zu bytes; NOT target ABI/stack/timing evidence\n", sizeof(M2RebuildRenderer));
    return 0;
}
