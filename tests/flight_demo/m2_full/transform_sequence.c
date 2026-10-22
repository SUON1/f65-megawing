// Host-only comparison of the candidate sequence with archived expressions.
#include <assert.h>
#include <limits.h>
#include <stdio.h>
#include <string.h>

#include "m2_geometry.c"

// Only the transform function is renamed. Its frozen arithmetic, sine table
// and validation dependencies are unchanged and separately oracle-checked.
#define m2_transform m2_reference_transform
#include M2_TRANSFORM_REFERENCE
#undef m2_transform

uint8_t m2_test_transform(int16_t yaw, int16_t pitch, int16_t roll,
                           int64_t coefficients[9])
{
    M2Camera camera = {{{-4500L * M2_POSITION_SCALE, 0,
                         -300L * M2_POSITION_SCALE}}, yaw, pitch, roll, 1u};
    M2Transform result;
    if (!m2_transform(&camera, &result))
    {
        return 0u;
    }
    memcpy(coefficients, result.m, sizeof(result.m));
    return 1u;
}

#ifdef M2_TRANSFORM_EQUIVALENCE_MAIN
static uint32_t boundary_cases;

static void same_camera(const M2Camera *first, const M2Camera *second)
{
    assert(first->yaw == second->yaw && first->pitch == second->pitch
           && first->roll == second->roll && first->revision == second->revision);
    for (uint8_t axis = 0u; axis < 3u; ++axis)
    {
        assert(first->position.v[axis] == second->position.v[axis]);
    }
}

static void compare_boundary(const M2Camera *camera, uint8_t valid)
{
    M2Transform actual;
    M2Transform expected;
    memset(&actual, 0xA5, sizeof(actual));
    expected = actual;
    assert(m2_transform(camera, &actual) == valid);
    assert(m2_reference_transform(camera, &expected) == valid);
    assert(memcmp(&actual, &expected, sizeof(actual)) == 0);
    ++boundary_cases;
}

static void boundaries(void)
{
    M2Camera camera = {{{0, 0, -M2_HEIGHT_MIN_FT * M2_POSITION_SCALE}},
                        0, 0, 0, 1u};
    compare_boundary(0, 0u);
    assert(!m2_transform(&camera, 0));
    assert(!m2_reference_transform(&camera, 0));
    assert(!m2_transform(0, 0));
    assert(!m2_reference_transform(0, 0));
    camera.revision = 0u;
    compare_boundary(&camera, 0u);
    camera.revision = UINT32_MAX;
    compare_boundary(&camera, 1u);
    camera.revision = 1u;
    const int16_t bad_yaw[] = {INT16_MIN, -1, 360, INT16_MAX};
    const int16_t bad_tilt[] = {INT16_MIN, -61, 61, INT16_MAX};
    for (uint8_t i = 0u; i < 4u; ++i)
    {
        camera.yaw = bad_yaw[i];
        compare_boundary(&camera, 0u);
        camera.yaw = 0;
        camera.pitch = bad_tilt[i];
        compare_boundary(&camera, 0u);
        camera.pitch = 0;
        camera.roll = bad_tilt[i];
        compare_boundary(&camera, 0u);
        camera.roll = 0;
    }
    const int32_t low[3] = {-M2_NORTH_LIMIT_FT * M2_POSITION_SCALE,
        -M2_EAST_LIMIT_FT * M2_POSITION_SCALE,
        -M2_HEIGHT_MAX_FT * M2_POSITION_SCALE};
    const int32_t high[3] = {M2_NORTH_LIMIT_FT * M2_POSITION_SCALE,
        M2_EAST_LIMIT_FT * M2_POSITION_SCALE,
        -M2_HEIGHT_MIN_FT * M2_POSITION_SCALE};
    for (uint8_t axis = 0u; axis < 3u; ++axis)
    {
        int32_t original = camera.position.v[axis];
        const int32_t positions[] = {low[axis] - 1, low[axis], high[axis],
                                     high[axis] + 1, INT32_MIN, INT32_MAX};
        for (uint8_t i = 0u; i < 6u; ++i)
        {
            camera.position.v[axis] = positions[i];
            compare_boundary(&camera, (uint8_t)(i == 1u || i == 2u));
        }
        camera.position.v[axis] = original;
    }
    M2Transform expected;
    assert(m2_reference_transform(&camera, &expected));
    struct M2Prepared prepared;
    memset(&prepared, 0xA5, sizeof(prepared));
    prepared.camera = camera;
    assert(m2_prepare(&prepared, &prepared.camera));
    assert(memcmp(&prepared.rotation, &expected, sizeof(expected)) == 0);
    same_camera(&prepared.camera, &camera);
    M2Registration record;
    memset(&record, 0xA5, sizeof(record));
    record.camera = camera;
    assert(m2_registration(&record.camera, 1u, 2u, 0u, &record));
    assert(memcmp(&record.transform, &expected, sizeof(expected)) == 0);
    same_camera(&record.camera, &camera);
}

int main(void)
{
    boundaries();
    M2Camera camera = {{{0, 0, -M2_HEIGHT_MIN_FT * M2_POSITION_SCALE}},
                        0, 0, 0, 1u};
    uint32_t cases = 0u;
    for (int16_t yaw = 0; yaw < 360; ++yaw)
    {
        camera.yaw = yaw;
        for (int16_t pitch = -M2_TILT_LIMIT_DEG;
             pitch <= M2_TILT_LIMIT_DEG; ++pitch)
        {
            camera.pitch = pitch;
            for (int16_t roll = -M2_TILT_LIMIT_DEG;
                 roll <= M2_TILT_LIMIT_DEG; ++roll)
            {
                camera.roll = roll;
                M2Transform actual;
                M2Transform expected;
                assert(m2_transform(&camera, &actual));
                assert(m2_reference_transform(&camera, &expected));
                assert(memcmp(&actual, &expected, sizeof(actual)) == 0);
                for (uint8_t i = 0u; i < 9u; ++i)
                {
                    assert(actual.m[i] >= -M2_ROTATION_SCALE);
                    assert(actual.m[i] <= M2_ROTATION_SCALE);
                }
                ++cases;
            }
        }
    }
    assert(cases == 5270760u);
    printf("PASS exact transform equivalence: %lu angle triples; %lu boundary cases; "
           "same-object prepare/registration aliases\n",
           (unsigned long)cases, (unsigned long)boundary_cases);
    return 0;
}
#endif
