// Exact old/new projection comparison; frozen helpers are shared here only.
// The existing Decimal oracle supplies independent numerical coverage.
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "m2_geometry.c"

#define m2_project_prepared m2_reference_project_prepared
#include "reference_project.inc"
#undef m2_project_prepared

static const M2Line sentinel = {{1234567, -2345678}, {3456789, -4567890}};
static unsigned long contract_count;

static int same_line(const M2Line *a, const M2Line *b)
{
    return a->x[0] == b->x[0] && a->x[1] == b->x[1]
        && a->y[0] == b->y[0] && a->y[1] == b->y[1];
}

static int8_t compare(const struct M2Prepared *prepared,
                      const M2Point *a, const M2Point *b)
{
    M2Line expected = sentinel;
    M2Line actual = sentinel;
    int8_t old = m2_reference_project_prepared(prepared, a, b, &expected);
    int8_t candidate = m2_project_prepared(prepared, a, b, &actual);
    assert(old == candidate && same_line(&expected, &actual));
    if (old != 1)
    {
        assert(same_line(&actual, &sentinel));
    }
    return old;
}

static void contracts(void)
{
    M2Camera camera = {{{0, 0, -10L * M2_POSITION_SCALE}}, 0, 0, 0, 1u};
    struct M2Prepared prepared;
    assert(m2_prepare(&prepared, &camera));
    M2Point a = {{100L * M2_POSITION_SCALE, 0, camera.position.v[2]}};
    M2Point b = {{110L * M2_POSITION_SCALE, 0, camera.position.v[2]}};
    assert(compare(0, &a, &b) == -1);
    assert(compare(&prepared, 0, &b) == -1);
    assert(compare(&prepared, &a, 0) == -1);
    assert(m2_project_prepared(&prepared, &a, &b, 0) == -1);
    assert(m2_reference_project_prepared(&prepared, &a, &b, 0) == -1);
    contract_count += 4u;
    for (uint8_t ready = 0u; ready < 3u; ++ready)
    {
        prepared.ready = ready;
        assert(compare(&prepared, &a, &b) == (ready == 1u ? 1 : -1));
        ++contract_count;
    }
    prepared.ready = 1u;
    for (uint8_t axis = 0u; axis < 3u; ++axis)
    {
        for (int32_t sign = -1; sign <= 1; sign += 2)
        {
            for (int32_t offset = 0; offset <= 1; ++offset)
            {
                M2Point bound = a;
                bound.v[axis] = sign * (M2_WORLD_LIMIT_FT * M2_POSITION_SCALE + offset);
                int8_t status = compare(&prepared, &bound, &b);
                assert(offset == 0 || status == -1);
                status = compare(&prepared, &a, &bound);
                assert(offset == 0 || status == -1);
                contract_count += 2u;
            }
        }
    }
    // Legal overlap: union storage is activated by the final struct assignment.
    // All endpoint/prepared reads must precede the successful output write.
    for (uint8_t overlap = 0u; overlap < 3u; ++overlap)
    {
        union { M2Point point; M2Line line; struct M2Prepared prepared; } old, now;
        old.prepared = prepared;
        now.prepared = prepared;
        if (overlap < 2u)
        {
            old.point = overlap == 0u ? a : b;
            now.point = old.point;
        }
        const struct M2Prepared *op = overlap == 2u ? &old.prepared : &prepared;
        const struct M2Prepared *np = overlap == 2u ? &now.prepared : &prepared;
        int8_t before = m2_reference_project_prepared(op,
            overlap == 0u ? &old.point : &a, overlap == 1u ? &old.point : &b, &old.line);
        int8_t after = m2_project_prepared(np,
            overlap == 0u ? &now.point : &a, overlap == 1u ? &now.point : &b, &now.line);
        assert(before == 1 && after == before && same_line(&old.line, &now.line));
        ++contract_count;
    }
}

static uint32_t read_u32(const unsigned char *bytes)
{
    return (uint32_t)bytes[0] | ((uint32_t)bytes[1] << 8u)
        | ((uint32_t)bytes[2] << 16u) | ((uint32_t)bytes[3] << 24u);
}

static int32_t read_i32(const unsigned char *bytes)
{
    uint32_t value = read_u32(bytes);
    return value <= INT32_MAX ? (int32_t)value
        : (int32_t)((int64_t)value - 4294967296LL);
}

int main(int argc, char **argv)
{
    assert(argc == 2);
    FILE *stream = fopen(argv[1], "rb");
    assert(stream != 0);
    unsigned char record[56];
    unsigned long count = 0u;
    unsigned long visible = 0u;
    unsigned long clipped = 0u;
    unsigned long degenerate = 0u;
    M2Camera prior = {0};
    struct M2Prepared prepared;
    size_t bytes;
    while ((bytes = fread(record, 1u, sizeof(record), stream)) != 0u)
    {
        assert(bytes == sizeof(record));
        M2Camera camera;
        M2Point a;
        M2Point b;
        for (uint8_t axis = 0u; axis < 3u; ++axis)
        {
            camera.position.v[axis] = read_i32(record + 4u * axis);
            a.v[axis] = read_i32(record + 28u + 4u * axis);
            b.v[axis] = read_i32(record + 40u + 4u * axis);
        }
        camera.yaw = (int16_t)read_i32(record + 12u);
        camera.pitch = (int16_t)read_i32(record + 16u);
        camera.roll = (int16_t)read_i32(record + 20u);
        camera.revision = read_u32(record + 24u);
        assert(m2_camera_valid(&camera) && m2_point_valid(&a) && m2_point_valid(&b));
        // Padding is not compared. Reusing a prepared context is valid only
        // when every defining camera field is unchanged.
        if (count == 0u || camera.revision != prior.revision
            || camera.yaw != prior.yaw || camera.pitch != prior.pitch || camera.roll != prior.roll
            || memcmp(camera.position.v, prior.position.v, sizeof(camera.position.v)) != 0)
        {
            assert(m2_prepare(&prepared, &camera));
            prior = camera;
        }
        if (count < 599760u)
        {
            M2Point first;
            M2Point last;
            assert(m2_fixture_segment(M2_FIXTURE_REVISION,
                (uint8_t)((count / 2u) % M2_SEGMENT_COUNT), &first, &last));
            const M2Point *expected_a = count % 2u == 0u ? &first : &last;
            const M2Point *expected_b = count % 2u == 0u ? &last : &first;
            assert(memcmp(&a, expected_a, sizeof(a)) == 0);
            assert(memcmp(&b, expected_b, sizeof(b)) == 0);
        }
        uint32_t same = read_u32(record + 52u);
        assert(same <= 1u);
        int8_t status = compare(&prepared, &a, same != 0u ? &a : &b);
        assert(status == 0 || status == 1);
        visible += status == 1;
        clipped += status == 0;
        degenerate += same;
        ++count;
    }
    assert(!ferror(stream) && fclose(stream) == 0);
    assert(count == 799886u && degenerate == 18u);
    contracts();
    printf("PASS %lu exact cases; visible %lu clipped %lu same-pointer %lu; %lu contract checks\n",
           count, visible, clipped, degenerate, contract_count);
    return EXIT_SUCCESS;
}
