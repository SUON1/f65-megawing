// Compile-only empty case block. No injected observation or acceptance claim.
#include <stdint.h>
#include "group1_transport.h"
#include "successor_lifecycle.h"
#include "r0f_group2_capture.h"

static uint8_t case_byte(uint16_t index)
{
    return index < sizeof(r0fg2_case_header)
        ? r0fg2_case_header[index] : R0FG2_UNUSED;
}

// Runs after acquisition region comparisons, with the existing record workspace.
// Every chunk is independently read back before entering the outer CRC.
uint8_t r0fg2_capture_empty(uint32_t *offset, uint32_t *outer_crc, uint8_t *record)
{
    uint32_t crc = 0xfffffffful;
    uint16_t at = 0u;
    while (at < R0FG2_BLOCK_BYTES)
    {
        uint8_t bytes = R0FG2_BLOCK_BYTES - at > R0FG2_WORK_BYTES
            ? R0FG2_WORK_BYTES : (uint8_t)(R0FG2_BLOCK_BYTES - at);
        for (uint8_t index = 0u; index < bytes; index++)
        {
            uint16_t position = at + index;
            if (position < R0FG2_CRC_OFFSET)
            {
                record[index] = case_byte(position);
                crc = r0fs_crc32_update(crc, record + index, 1u);
            }
            else
            {
                record[index] = (uint8_t)(~crc >> ((position - R0FG2_CRC_OFFSET) * 8u));
            }
        }
        uint32_t expected = r0fs_crc32(record, bytes);
        if (!r0fg1_trace_write(*offset, record, bytes)
            || !r0fg1_trace_read(*offset, record, bytes)
            || r0fs_crc32(record, bytes) != expected)
        {
            return 0u;
        }
        *outer_crc = r0fs_crc32_update(*outer_crc, record, bytes);
        *offset += bytes;
        at += bytes;
    }
    return 1u;
}
