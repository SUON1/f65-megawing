#include <assert.h>
#include <stdio.h>
#include <string.h>

#include "m1_input.h"
#include "m1_snapshot.h"
#include "m2_fixture.h"
#include "m2_geometry.h"

static M2Pixel pixels[M2_RASTER_POINTS];

static void negative_and_identity(void)
{
    M2Camera camera = {{{-4500L * M2_POSITION_SCALE, 0, -300L * M2_POSITION_SCALE}},
                        0, -5, 0, 1u};
    M2Registration record;
    assert(m2_registration(&camera, 1u, 600u, 0u, &record));
    M2Registration other = record;
    assert(m2_pair_eligible(&record, &other, 1u, 1u));
    assert(!m2_pair_eligible(&record, &other, 1u, 0u));
    assert(!m2_pair_eligible(&record, &other, 2u, 1u));
    other.source_tick++;
    assert(!m2_pair_eligible(&record, &other, 1u, 1u));
    other = record;
    other.camera.position.v[0]++;
    assert(!m2_pair_eligible(&record, &other, 1u, 1u));
    other = record;
    other.transform.m[0]++;
    assert(!m2_pair_eligible(&record, &other, 1u, 1u));
    other = record;
    other.fixture_revision++;
    assert(!m2_pair_eligible(&record, &other, 1u, 1u));
    other = record;
    other.projection_revision++;
    assert(!m2_pair_eligible(&record, &other, 1u, 1u));
    other = record;
    other.composition_revision++;
    assert(!m2_pair_eligible(&record, &other, 1u, 1u));
    other = record;
    other.generation++;
    assert(!m2_pair_eligible(&record, &other, 1u, 1u));
    other = record;
    other.store = 1u;
    assert(!m2_pair_eligible(&record, &other, 1u, 1u));
    other = record;
    other.view_id = 1u;
    assert(!m2_pair_eligible(&record, &other, 1u, 1u));
    other = record;
    other.tier_id = 1u;
    assert(!m2_pair_eligible(&record, &other, 1u, 1u));
    camera.revision = 0u;
    other = record;
    assert(!m2_registration(&camera, 2u, 600u, 0u, &other));
    assert(memcmp(&record, &other, sizeof(record)) == 0);
    camera.revision = 1u;
    camera.pitch = 61;
    M2Transform rotation;
    assert(!m2_transform(&camera, &rotation));
    camera.pitch = -5;
    M2Point a;
    M2Point b;
    assert(m2_fixture_segment(1u, 0u, &a, &b));
    M2Point original = a;
    assert(!m2_fixture_segment(2u, 0u, &a, &b));
    assert(memcmp(&a, &original, sizeof(a)) == 0);
    assert(!m2_fixture_segment(1u, M2_SEGMENT_COUNT, &a, &b));
    M2Surface surface;
    M2Point center = {{0, 0, 0}};
    assert(m2_surface_query(1u, &center, &surface) && surface.inside);
    center.v[1] = (M2_RUNWAY_HALF_WIDTH_FT + 1) * M2_POSITION_SCALE;
    assert(m2_surface_query(1u, &center, &surface) && !surface.inside);
    M2Line line;
    assert(m2_project_segment(&camera, &a, &b, &line) == 1);
    memset(pixels, 0x55, sizeof(pixels));
    uint16_t count = 123u;
    assert(!m2_raster_line(&line, pixels, 0u, &count));
    assert(count == 123u && pixels[0].x == 0x5555u);
    a.v[0] = INT32_MAX;
    assert(m2_project_segment(&camera, &a, &b, &line) == -1);
    assert(m2_ground_sample(&camera, M2_WIDTH, 0u) == -1);
}

static void replay(void)
{
    M1Core core[3];
    M1Snapshots snapshots[3] = {0};
    M1Input input[3] = {0};
    uint8_t stages[M1_STAGES];
    for (uint8_t mode = 0u; mode < 3u; ++mode)
    {
        m1_core_init(&core[mode]);
    }
    for (uint32_t tick = 0u; tick < 600u; ++tick)
    {
        for (uint8_t mode = 0u; mode < 3u; ++mode)
        {
            (void)m1_input_sample(&input[mode], &core[mode], (uint8_t)((tick / 25u) & 1u));
            m1_tick(&core[mode], &snapshots[mode], stages);
            if (mode != 0u && (mode == 1u || tick % 17u == 0u))
            {
                M2Camera camera = {{{-4500L * M2_POSITION_SCALE, 0,
                                     -300L * M2_POSITION_SCALE}},
                                     (int16_t)(tick % 360u), -5, 0, tick + 1u};
                M2Registration record;
                assert(m2_registration(&camera, tick + 1u, tick, 0u, &record));
                assert(!m2_pair_eligible(&record, &record, tick + 2u, 1u));
                for (uint8_t i = 0u; i < M2_SEGMENT_COUNT; ++i)
                {
                    M2Point a;
                    M2Point b;
                    M2Line line;
                    assert(m2_fixture_segment(1u, i, &a, &b));
                    int8_t result = m2_project_segment(&camera, &a, &b, &line);
                    assert(result >= 0);
                    if (result == 1)
                    {
                        uint16_t count;
                        assert(m2_raster_line(&line, pixels, M2_RASTER_POINTS, &count));
                    }
                }
            }
        }
        assert(core[0].checksum == core[1].checksum);
        assert(core[0].checksum == core[2].checksum);
    }
    assert(core[0].checksum == 0xDE675132ul);
}

int main(void)
{
    negative_and_identity();
    replay();
    puts("M2 HOST PASS: negative/identity/capacity checks; 600 per-tick replay comparisons DE675132");
    return 0;
}
