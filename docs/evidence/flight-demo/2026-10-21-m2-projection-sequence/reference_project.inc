int8_t m2_project_prepared(const struct M2Prepared *prepared,
                          const M2Point *first, const M2Point *last, M2Line *line)
{
    if (prepared == 0 || prepared->ready != 1u || line == 0
        || !m2_point_valid(first) || !m2_point_valid(last))
    {
        return -1;
    }
    ClipPoint a = to_camera(&prepared->camera, &prepared->rotation, first);
    ClipPoint b = to_camera(&prepared->camera, &prepared->rotation, last);
    for (uint8_t plane = 0u; plane < M2_CLIP_PLANES; ++plane)
    {
        int64_t da = plane_distance(&a, plane);
        int64_t db = plane_distance(&b, plane);
        if (da < 0 && db < 0)
        {
            return 0;
        }
        if ((da < 0) != (db < 0))
        {
            // Interpolate from the inside endpoint; ratio is in [0,1].
            ClipPoint inside = da >= 0 ? a : b;
            ClipPoint outside = da < 0 ? a : b;
            int64_t numerator = da >= 0 ? da : db;
            int64_t denominator = da >= 0 ? da - db : db - da;
            for (uint8_t axis = 0u; axis < 3u; ++axis)
            {
                int64_t delta = (int64_t)outside.v[axis] - inside.v[axis];
                outside.v[axis] = inside.v[axis]
                    + interpolate_delta(delta, numerator, denominator);
            }
            if (da < 0)
            {
                a = outside;
            }
            else
            {
                b = outside;
            }
        }
    }
    if (a.v[0] <= 0 || b.v[0] <= 0)
    {
        return -1;
    }
    M2Line result;
    result.x[0] = project_axis(a.v[1], a.v[0], M2_WIDTH);
    result.y[0] = project_axis(a.v[2], a.v[0], M2_HEIGHT);
    result.x[1] = project_axis(b.v[1], b.v[0], M2_WIDTH);
    result.y[1] = project_axis(b.v[2], b.v[0], M2_HEIGHT);
    *line = result;
    return 1;
}
