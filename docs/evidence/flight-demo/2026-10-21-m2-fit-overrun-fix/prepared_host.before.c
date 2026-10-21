// Prepared-owner lifetime tests. Independent numeric expectations remain in
// the unchanged Decimal oracle, exercised through the legacy wrappers.
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "m2_prepared_private.h"
#include "m2_fixture.h"

int main(void)
{
    M2Camera camera = {{{-4500L * M2_POSITION_SCALE, 0,
                          -300L * M2_POSITION_SCALE}}, 0, -5, 0, 1u};
    struct M2Prepared prepared = {0};
    M2Point first;
    M2Point last;
    M2Line line;
    M2Line legacy;
    M2Registration record;
    M2Registration expected;
    assert(m2_fixture_segment(1u, 0u, &first, &last));
    memset(&line, 0x55, sizeof(line));
    legacy = line;
    assert(m2_project_prepared(&prepared, &first, &last, &line) == -1);
    assert(memcmp(&line, &legacy, sizeof(line)) == 0);
    assert(m2_ground_prepared(&prepared, 0u, 0u) == -1);
    assert(!m2_registration_prepared(&prepared, 1u, 1u, 0u, &record));
    unsigned cases = 0u;
    for (int16_t yaw = 0; yaw < 360; yaw = (int16_t)(yaw + 15))
    {
        for (int16_t pitch = -60; pitch <= 60; pitch = (int16_t)(pitch + 60))
        {
            for (int16_t roll = -60; roll <= 60; roll = (int16_t)(roll + 60))
            {
                camera.yaw = yaw;
                camera.pitch = pitch;
                camera.roll = roll;
                assert(m2_prepare(&prepared, &camera));
                M2Camera captured = camera;
                ++camera.revision;
                assert(prepared.camera.revision == captured.revision);
                for (uint8_t segment = 0u; segment < M2_SEGMENT_COUNT; ++segment)
                {
                    assert(m2_fixture_segment(1u, segment, &first, &last));
                    int8_t a = m2_project_prepared(&prepared, &first, &last, &line);
                    int8_t b = m2_project_segment(&captured, &first, &last, &legacy);
                    assert(a == b && a >= 0);
                    if (a == 1) assert(memcmp(&line, &legacy, sizeof(line)) == 0);
                    ++cases;
                }
                for (uint16_t y = 0u; y < 128u; y = (uint16_t)(y + 63u))
                {
                    for (uint16_t x = 0u; x < 320u; x = (uint16_t)(x + 159u))
                    {
                        assert(m2_ground_prepared(&prepared, x, y)
                               == m2_ground_sample(&captured, x, y));
                    }
                }
                assert(m2_registration_prepared(&prepared, 9u, 600u, 1u, &record));
                assert(m2_registration(&captured, 9u, 600u, 1u, &expected));
                assert(m2_pair_eligible(&record, &expected, captured.revision, 1u));
                assert(!m2_pair_eligible(&record, &expected, camera.revision, 1u));
            }
        }
    }
    assert(m2_ground_prepared(&prepared, M2_WIDTH, 0u) == -1);
    assert(m2_ground_prepared(&prepared, 0u, M2_HEIGHT) == -1);
    M2Registration saved = record;
    assert(!m2_registration_prepared(&prepared, 0u, 0u, 0u, &record));
    assert(memcmp(&saved, &record, sizeof(record)) == 0);
    camera.revision = 0u;
    assert(!m2_prepare(&prepared, &camera));
    assert(prepared.ready == 0u);
    assert(m2_project_prepared(&prepared, &first, &last, &line) == -1);
    assert(!m2_prepare(0, &camera));
    assert(!m2_prepare(&prepared, 0));
    puts("PASS prepared-context reuse/capture/invalidation, horizon, registration and output preservation");
    printf("Prepared segment comparisons: %u\n", cases);
    return 0;
}
