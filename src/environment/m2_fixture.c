#include "m2_fixture.h"

uint8_t m2_point_valid(const M2Point *point)
{
    if (point == 0)
    {
        return 0u;
    }
    for (uint8_t axis = 0u; axis < 3u; ++axis)
    {
        if (point->v[axis] < -M2_WORLD_LIMIT_FT * M2_POSITION_SCALE
            || point->v[axis] > M2_WORLD_LIMIT_FT * M2_POSITION_SCALE)
        {
            return 0u;
        }
    }
    return 1u;
}

uint8_t m2_fixture_segment(uint32_t revision, uint8_t index,
                           M2Point *first, M2Point *last)
{
    if (revision != M2_FIXTURE_REVISION || index >= M2_SEGMENT_COUNT
        || first == 0 || last == 0 || first == last)
    {
        return 0u;
    }
    M2Point a = {{0, 0, 0}};
    M2Point b = a;
    if (index < 4u)
    {
        // Four ordered corners; all dimensions come from the fixture contract.
        uint8_t next = (uint8_t)((index + 1u) % 4u);
        a.v[0] = index < 2u ? -M2_RUNWAY_HALF_LENGTH_FT : M2_RUNWAY_HALF_LENGTH_FT;
        a.v[1] = index == 0u || index == 3u
                 ? -M2_RUNWAY_HALF_WIDTH_FT : M2_RUNWAY_HALF_WIDTH_FT;
        b.v[0] = next < 2u ? -M2_RUNWAY_HALF_LENGTH_FT : M2_RUNWAY_HALF_LENGTH_FT;
        b.v[1] = next == 0u || next == 3u
                 ? -M2_RUNWAY_HALF_WIDTH_FT : M2_RUNWAY_HALF_WIDTH_FT;
    }
    else if (index < 6u)
    {
        a.v[0] = index == 4u ? -M2_THRESHOLD_NORTH_FT : M2_THRESHOLD_NORTH_FT;
        b.v[0] = a.v[0];
        a.v[1] = -M2_RUNWAY_HALF_WIDTH_FT;
        b.v[1] = M2_RUNWAY_HALF_WIDTH_FT;
    }
    else
    {
        int32_t center = M2_MARK_FIRST_FT + (index - 6L) * M2_MARK_STEP_FT;
        a.v[0] = center - M2_MARK_HALF_LENGTH_FT;
        b.v[0] = center + M2_MARK_HALF_LENGTH_FT;
    }
    for (uint8_t axis = 0u; axis < 3u; ++axis)
    {
        a.v[axis] *= M2_POSITION_SCALE;
        b.v[axis] *= M2_POSITION_SCALE;
    }
    *first = a;
    *last = b;
    return 1u;
}

uint8_t m2_surface_query(uint32_t revision, const M2Point *point,
                         M2Surface *surface)
{
    if (revision != M2_FIXTURE_REVISION || !m2_point_valid(point) || surface == 0)
    {
        return 0u;
    }
    M2Surface result = {M2_FIXTURE_REVISION, 0, 0u};
    result.inside = (uint8_t)(point->v[0] >= -M2_RUNWAY_HALF_LENGTH_FT * M2_POSITION_SCALE
        && point->v[0] <= M2_RUNWAY_HALF_LENGTH_FT * M2_POSITION_SCALE
        && point->v[1] >= -M2_RUNWAY_HALF_WIDTH_FT * M2_POSITION_SCALE
        && point->v[1] <= M2_RUNWAY_HALF_WIDTH_FT * M2_POSITION_SCALE);
    *surface = result;
    return 1u;
}
