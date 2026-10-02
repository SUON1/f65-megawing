#include <assert.h>
#include <stdint.h>
#include <stdio.h>

#include "combined_model.h"
#include "group1_capture.h"
#include "group1_workload.h"
#include "successor_lifecycle.h"

static uint8_t expected_stage = 1u;
static uint16_t latched;

void r0fg1_stage_begin(uint8_t stage)
{
    assert(stage == expected_stage);
}

void r0fg1_stage_end(uint8_t stage)
{
    assert(stage == expected_stage);
    expected_stage++;
}

void cfinput_tick(uint8_t input)
{
    assert(expected_stage == 2u && input == 0u);
    latched++;
}

static uint32_t independent_crc(const uint8_t *data, uint16_t bytes)
{
    uint32_t value = 0xffffffffu;
    for (uint16_t index = 0u; index < bytes; index++)
    {
        value ^= data[index];
        for (uint8_t bit = 0u; bit < 8u; bit++)
        {
            uint32_t mask = 0u - (value & 1u);
            value = (value >> 1u) ^ (mask & 0xedb88320u);
        }
    }
    return ~value;
}

int main(void)
{
    r0fc_model model;
    uint8_t data[1024];
    r0fc_reset(&model);
    for (uint16_t tick = 1u; tick <= R0FG1_RECORDS; tick++)
    {
        expected_stage = 1u;
        r0fc_tick(&model);
        assert(expected_stage == 21u);
        r0fg1_stage_begin(21u);
        r0fg1_stage_end(21u);
        assert(expected_stage == 22u && latched == tick && model.tick == tick);
        assert(r0fg1_causality_errors() == 0u);
        if (tick == R0FG1_RECORDS / 2u || tick == R0FG1_RECORDS)
        {
            printf("lineage %u %08X\n", tick, (unsigned int)model.checksum);
        }
    }
    printf("sidecar %08X %u %u %u\n", (unsigned int)r0fg1_workload_hash(),
           r0fg1_ai_runs(0u), r0fg1_ai_runs(1u), r0fg1_ai_runs(2u));
    for (uint16_t index = 0u; index < sizeof(data); index++)
    {
        data[index] = (uint8_t)(index ^ (index >> 3u) ^ 0xa7u);
    }
    for (uint16_t length = 0u; length <= sizeof(data); length++)
    {
        uint16_t split = (uint16_t)(length / 3u);
        uint32_t streamed = r0fs_crc32_update(0xffffffffu, data, split);
        streamed = r0fs_crc32_update(streamed, data + split, (uint16_t)(length - split));
        assert(~streamed == independent_crc(data, length));
        assert(r0fs_crc32(data, length) == independent_crc(data, length));
    }
    puts("Stage/input/AI causality and 1025 streaming CRC lengths PASS");
    return 0;
}
