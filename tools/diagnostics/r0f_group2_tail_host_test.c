// Actual terminal tail statements; independent bytes/CRC and failing transport.
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "r0f_group1_trace.h"
#include "r0f_group2_capture.h"
#include "successor_lifecycle.h"

static uint8_t record[R0FG1_RECORD_BYTES];
static uint8_t trace[R0FG1_TRACE_BYTES];
static uint32_t host_outer_crc;
static unsigned copies, failure_at, corrupt_at, corrupt_byte;

static uint8_t r0fg1_trace_write(uint32_t offset, const uint8_t *data, uint8_t bytes)
{
    assert(bytes && bytes <= sizeof(record));
    assert(offset <= sizeof(trace) && bytes <= sizeof(trace) - offset);
    if (++copies == failure_at)
    {
        return 0u;
    }
    memcpy(trace + offset, data, bytes);
    return 1u;
}

static uint8_t r0fg1_trace_read(uint32_t offset, uint8_t *data, uint8_t bytes)
{
    assert(bytes && bytes <= sizeof(record));
    assert(offset <= sizeof(trace) && bytes <= sizeof(trace) - offset);
    if (++copies == failure_at)
    {
        return 0u;
    }
    memcpy(data, trace + offset, bytes);
    if (copies == corrupt_at)
    {
        assert(corrupt_byte < bytes);
        data[corrupt_byte] ^= 1u;
    }
    return 1u;
}

#include "tail_under_test.h"

static uint32_t independent_crc(const uint8_t *data, uint32_t bytes)
{
    uint32_t crc = UINT32_MAX;
    while (bytes--)
    {
        crc ^= *data++;
        for (unsigned bit = 0; bit < 8; bit++)
        {
            crc = crc & 1 ? (crc >> 1) ^ 0xedb88320u : crc >> 1;
        }
    }
    return ~crc;
}

static void reset(void)
{
    memset(trace, 0x73, sizeof(trace));
    copies = failure_at = corrupt_at = corrupt_byte = 0;
    host_outer_crc = 0;
}

int main(void)
{
    const uint32_t prefix = R0FG1_HEADER_BYTES + R0FG1_RECORDS * R0FG1_RECORD_BYTES
        + R0FG1_RESULT_BYTES + R0FG1_EPOCHS * R0FG1_POOL_EPOCH_BYTES;
    const unsigned worlds[] = {0, 1, 955, 1999, 2000};
    unsigned tested = 0;
    for (unsigned fixture = 0; fixture < sizeof(worlds) / sizeof(worlds[0]); fixture++)
    {
        uint32_t start = prefix + worlds[fixture] * R0FG1_WORLD_EVENT_BYTES;
        reset();
        assert(encode_tail(start));
        unsigned calls = copies;
        assert(memcmp(trace + start, r0fg2_empty_identity, R0FG2_HEADER_BYTES) == 0);
        for (uint32_t at = R0FG2_HEADER_BYTES; at < R0FG2_CRC_AT; at++)
        {
            assert(trace[start + at] == R0FG2_UNUSED);
        }
        uint32_t block_crc = independent_crc(trace + start, R0FG2_CRC_AT);
        for (unsigned i = 0; i < 4; i++)
        {
            assert(trace[start + R0FG2_CRC_AT + i] == (uint8_t)(block_crc >> (i * 8)));
        }
        for (uint32_t at = start + R0FG2_BLOCK_BYTES; at < sizeof(trace) - 4; at++)
        {
            assert(trace[at] == (uint8_t)((at & 255u) ^ R0FG1_CAPACITY_PATTERN_XOR));
        }
        for (uint32_t at = 0; at < start; at++)
        {
            assert(trace[at] == 0x73);
        }
        for (uint32_t at = sizeof(trace) - 4; at < sizeof(trace); at++)
        {
            assert(trace[at] == 0x73);
        }
        assert(host_outer_crc == independent_crc(trace + start, sizeof(trace) - 4 - start));
        const unsigned failures[] = {1, 2, 3, 4, calls - 1, calls};
        for (unsigned i = 0; i < sizeof(failures) / sizeof(failures[0]); i++)
        {
            reset();
            failure_at = failures[i];
            assert(!encode_tail(start) && copies == failure_at);
            tested++;
        }
        tested++;
    }
    // Every byte in the first four chunks includes all header/slots/CRC edges.
    const uint32_t start = prefix + R0FG1_MAX_WORLD_EVENTS * R0FG1_WORLD_EVENT_BYTES;
    for (unsigned chunk = 0; chunk < 4; chunk++)
    {
        for (unsigned byte = 0; byte < R0FG1_RECORD_BYTES; byte++)
        {
            reset();
            corrupt_at = 2 * (chunk + 1);
            corrupt_byte = byte;
            assert(!encode_tail(start) && copies == corrupt_at);
            tested++;
        }
    }
    printf("PASS: %u tail boundary/failure/corruption cases; 2000-event capacity retained\n", tested);
    return 0;
}
