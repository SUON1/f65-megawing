uint8_t m2_transform(const M2Camera *camera, M2Transform *transform)
{
    if (!m2_camera_valid(camera) || transform == 0)
    {
        return 0u;
    }
    int64_t sy = sine(camera->yaw);
    int64_t cy = sine((int16_t)(camera->yaw + 90));
    int64_t sp = sine(camera->pitch);
    int64_t cp = sine((int16_t)(camera->pitch + 90));
    int64_t sr = sine(camera->roll);
    int64_t cr = sine((int16_t)(camera->roll + 90));
    int64_t sr_sp = multiply_rotation(sr, sp);
    int64_t cr_sp = multiply_rotation(cr, sp);
    // Transpose of Rz(yaw) Ry(pitch) Rx(roll): NED to camera.
    M2Transform result = {{
        multiply_rotation(cp, cy), multiply_rotation(cp, sy), -sp,
        multiply_rotation(sr_sp, cy) - multiply_rotation(cr, sy),
        multiply_rotation(sr_sp, sy) + multiply_rotation(cr, cy),
        multiply_rotation(sr, cp),
        multiply_rotation(cr_sp, cy) + multiply_rotation(sr, sy),
        multiply_rotation(cr_sp, sy) - multiply_rotation(sr, cy),
        multiply_rotation(cr, cp)
    }};
    *transform = result;
    return 1u;
}

