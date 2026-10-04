static uint8_t case_tail_byte(uint16_t position, uint8_t absolute)
{
    if (position < R0FG2_HEADER_BYTES)
    {
        return r0fg2_empty_identity[position];
    }
    if (position < R0FG2_CRC_AT)
    {
        return R0FG2_UNUSED;
    }
    if (position < R0FG2_BLOCK_BYTES)
    {
        return r0fg2_empty_identity[R0FG2_HEADER_BYTES + position - R0FG2_CRC_AT];
    }
    return absolute ^ R0FG1_CAPACITY_PATTERN_XOR;
}
static uint8_t encode_tail(uint32_t offset)
{
    uint32_t crc = 0xfffffffful;
    uint16_t case_at = 0u;
    uint16_t tail_left = (uint16_t)(R0FG1_TRACE_BYTES - 4u - offset);
    while (tail_left)
    {
        uint8_t bytes = tail_left > sizeof(record) ? sizeof(record) : (uint8_t)tail_left;
        uint8_t value = (uint8_t)offset;
        for (uint8_t index = 0u; index < bytes; index++)
        {
            record[index] = case_tail_byte((uint16_t)(case_at + index), value++);
        }
        if (!r0fg1_trace_write(offset, record, bytes)
            || !r0fg1_trace_read(offset, record, bytes))
        {
            return 0u;
        }
        value = (uint8_t)offset;
        for (uint8_t index = 0u; index < bytes; index++)
        {
            if (record[index] != case_tail_byte((uint16_t)(case_at + index), value++))
            {
                return 0u;
            }
        }
        crc = r0fs_crc32_update(crc, record, bytes);
        offset += bytes;
        case_at = (uint16_t)(case_at + bytes);
        tail_left = (uint16_t)(tail_left - bytes);
    }
    host_outer_crc = ~crc;
    return 1u;
}
