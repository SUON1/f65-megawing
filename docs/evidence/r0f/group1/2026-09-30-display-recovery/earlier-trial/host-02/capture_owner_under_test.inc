static void put16(uint8_t *out, uint16_t value)
{
    out[0] = (uint8_t)value;
    out[1] = (uint8_t)(value >> 8u);
}

static void put32(uint8_t *out, uint32_t value)
{
    for (uint8_t index = 0u; index < 4u; index++)
    {
        out[index] = (uint8_t)value;
        value >>= 8u;
    }
}

void r0fg1_phase_end(void)
{
    r0fg1_irq_epoch = 0u;
    if (phase == R0FG1_PHASES - 1u)
    {
        r0fg1_owners_encode(record);
        pools_crc = r0fs_crc32_update(pools_crc, record, R0FG1_POOL_EPOCH_BYTES);
        if (!r0fg1_trace_write(R0FG1_POOL_OFFSET
                + (uint32_t)epoch * R0FG1_POOL_EPOCH_BYTES,
                record, R0FG1_POOL_EPOCH_BYTES))
        {
            cffault = 110u;
        }
    }
}

uint8_t r0fg1_capture_finish(void)
{
    if (records != R0FG1_RECORDS || cffault || r0fg1_irq_error)
    {
        return 0u;
    }
    // Caller has stopped IRQs. Metrics are immutable and need no seqlock.
    for (uint8_t index = 0u; index < sizeof(r0fg1_irq_summary); index++)
    {
        header[R0FG1_H_IRQ_SUMMARIES + index] = r0fg1_irq_summary[index];
    }
    header[R0FG1_H_IRQ_ERROR] = r0fg1_irq_error;
    r0fg1_display_metrics();
    r0fc_stack_measure();
    put16(header + R0FG1_H_HARDWARE_STACK, (uint16_t)(256u - r0fc_hardware_low));
    put16(header + R0FG1_H_SOFTWARE_STACK, (uint16_t)(0xd000u - r0fc_software_low));
    put32(header + R0FG1_H_CAPTURE_MAX, capture_max);
    put32(header + R0FG1_H_FINAL_CAPTURE, previous_capture);
    put32(header + R0FG1_H_RECORDS, records);
    uint32_t trace_bytes = R0FG1_WORLD_OFFSET
        + (uint32_t)world_generation * R0FG1_WORLD_EVENT_BYTES + 4u;
    put32(header + R0FG1_H_TRACE_BYTES, trace_bytes);
    put32(header + R0FG1_H_WORLD_EVENTS, world_generation);
    put32(header + R0FG1_H_SIDECAR_HASH, r0fg1_workload_hash());
    put16(header + R0FG1_H_AI_CAUSALITY_ERRORS, r0fg1_causality_errors());
    header[R0FG1_H_TRACK_HIGH] = (uint8_t)r0fg1_owner_peak(R0FG1_POOL_MEGA_TRACKS);
    header[R0FG1_H_TRACK_HIGH + 1u] = (uint8_t)r0fg1_owner_peak(R0FG1_POOL_RED_TRACKS);
    header[R0FG1_H_LIVE_SIX_DOF] = R0FG1_SIX_DOF;
    header[R0FG1_H_LIVE_KINEMATIC] = R0FG1_KINEMATIC;
    for (uint8_t tier = 0u; tier < 3u; tier++)
    {
        put16(header + R0FG1_H_AI_RUNS + tier * 2u, r0fg1_ai_runs(tier));
    }
    if (!r0fg1_trace_write(0u, header, 255u) || !r0fg1_trace_write(255u, header + 255u, 1u))
    {
        return 0u;
    }
    uint32_t result_offset = R0FG1_HEADER_BYTES + (uint32_t)records * sizeof(record);
    for (uint16_t offset = 0u; offset < R0FG1_RESULT_BYTES;)
    {
        uint8_t bytes = R0FG1_RESULT_BYTES - offset > sizeof(record) ? sizeof(record) : (uint8_t)(R0FG1_RESULT_BYTES - offset);
        for (uint8_t index = 0u; index < bytes; index++)
        {
            record[index] = cfresult[offset + index];
        }
        if (!r0fg1_trace_write(result_offset + offset, record, bytes))
        {
            return 0u;
        }
        offset = (uint16_t)(offset + bytes);
    }
    // Traverse declared regions in wire order. One reusable region CRC keeps
    // all three acquisition/readback comparisons without per-chunk 32-bit
    // range classification or three simultaneously live CRC accumulators.
    // The record region counts whole records; all other regions count bytes.
    // This keeps remaining work in 16 bits without narrowing a trace address.
    _Static_assert(R0FG1_MAX_WORLD_EVENTS * (uint32_t)R0FG1_WORLD_EVENT_BYTES
        <= UINT16_MAX, "world region must fit the bounded byte counter");
    static const uint16_t fixed_units[] = {
        R0FG1_HEADER_BYTES, R0FG1_RECORDS,
        R0FG1_RESULT_BYTES, R0FG1_EPOCHS * R0FG1_POOL_EPOCH_BYTES,
    };
    uint32_t crc = 0xfffffffful;
    uint32_t offset = 0u;
    for (uint8_t region = 0u; region < 5u; region++)
    {
        uint16_t remaining = region < 4u ? fixed_units[region]
            : (uint16_t)(world_generation * R0FG1_WORLD_EVENT_BYTES);
        uint32_t region_crc = 0xfffffffful;
        while (remaining)
        {
            uint8_t bytes;
            if (region == 1u)
            {
                bytes = sizeof(record);
                remaining--;
            }
            else
            {
                bytes = remaining > sizeof(record) ? sizeof(record) : (uint8_t)remaining;
                remaining = (uint16_t)(remaining - bytes);
            }
            if (!r0fg1_trace_read(offset, record, bytes))
            {
                return 0u;
            }
            crc = r0fs_crc32_update(crc, record, bytes);
            region_crc = r0fs_crc32_update(region_crc, record, bytes);
            offset += bytes;
        }
        if ((region == 1u && region_crc != records_crc)
            || (region == 3u && region_crc != pools_crc)
            || (region == 4u && region_crc != worlds_crc))
        {
            return 0u;
        }
    }
    put32(record, ~crc);
    if (!r0fg1_trace_write(trace_bytes - 4u, record, 4u))
    {
        return 0u;
    }
    // CRC32 of any valid CRC32-appended stream has this fixed residue.
    return r0fg1_transport_prepare(trace_bytes, 0x2144df1cul);
}
