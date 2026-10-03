static uint8_t validate_capsule(uint8_t initial)
{
    uint32_t crc = 0xfffffffful;

    for (uint8_t guard = 0u; guard < 2u; guard++)
    {
        uint32_t offset = guard ? R0FG1X_GUARD_BYTES + R0FG1X_CONTEXT_BYTES : 0u;

        if (!transfer(0u, offset, R0FG1X_GUARD_BYTES, 0u))
        {
            return 0u;
        }
        for (uint8_t index = 0u; index < R0FG1X_GUARD_BYTES; index++)
        {
            if (buffer[index] != R0FG1X_GUARD_VALUE)
            {
                return 0u;
            }
        }
    }
    for (uint16_t offset = 0u; offset < R0FG1X_CONTEXT_BYTES;)
    {
        uint16_t remaining = (uint16_t)(R0FG1X_CONTEXT_BYTES - offset);
        uint8_t bytes = remaining > sizeof(buffer) ? sizeof(buffer) : (uint8_t)remaining;

        if (!transfer(0u, R0FG1X_GUARD_BYTES + offset, bytes, 0u))
        {
            return 0u;
        }
        crc = r0fs_crc32_update(crc, buffer, bytes);
        offset = (uint16_t)(offset + bytes);
    }
    if (initial)
    {
        capsule_crc = ~crc;
    }
    return (uint8_t)(capsule_crc == ~crc);
}
uint8_t r0fg1_transport_prepare(uint32_t bytes, uint32_t expected_crc)
{
    uint32_t actual_crc = 0xfffffffful;
    if (cffault || cfresult[5] != 127u || cfreclaimed)
    {
        return 0u;
    }
    for (uint32_t offset = 0u; offset < bytes;)
    {
        uint32_t remaining = bytes - offset;
        uint8_t count = remaining > sizeof(buffer) ? sizeof(buffer) : (uint8_t)remaining;
        if (!transfer(1u, offset, count, 0u) || !r0fg1_export_append(&export, count))
        {
            return 0u;
        }
        actual_crc = r0fs_crc32_update(actual_crc, buffer, count);
        offset += count;
    }
    if (~actual_crc != expected_crc || !r0fg1_export_freeze(&export, ~actual_crc))
    {
        return 0u;
    }
    r0fg1_export_readiness readiness = {
        .acquisition_stopped = 1u,
        .dma_empty = 1u, // Inherited application DMA is synchronous; main has stopped.
        .display_stopped = (uint8_t)((CFREG(0xd011u) & 0x10u) == 0u),
        .audio_stopped = (uint8_t)(CFREG(0xd720u) == 0u && CFREG(0xd730u) == 0u
                                   && CFREG(0xd740u) == 0u && CFREG(0xd750u) == 0u),
        .irq_masked = (uint8_t)((r0fsi_irq_cpu_status() & 4u) != 0u),
        .rom_verified = (uint8_t)(!cfreclaimed && cfresult[6] == 0u),
        .capsule_verified = validate_capsule(0u),
        .nmi_seen = r0f_pf_nmi_seen,
    };
    uint8_t rejection = r0fg1_export_begin_diagnostic(&export, &readiness);
    if (rejection != 0u)
    {
        r0fg1_export_status = rejection;
        return 0u;
    }
    r0fg1_export_bytes = export.bytes;
    r0fg1_export_permit = 0xa5u;
    return 1u;
}
