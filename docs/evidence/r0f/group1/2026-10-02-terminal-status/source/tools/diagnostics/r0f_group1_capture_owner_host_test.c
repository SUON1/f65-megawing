#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "r0f_group1_trace.h"
#include "group1_pool_owners.h"
#include "group1_transport.h"
#include "successor_lifecycle.h"

// Exact checkpoint/finalization functions, generated from the candidate C.
// Mock only the trace transport and terminal metrics. No target evidence.
uint8_t cffault;
volatile uint8_t r0fg1_export_status;
static uint8_t record[R0FG1_RECORD_BYTES], header[R0FG1_HEADER_BYTES];
static uint8_t phase, epoch, r0fg1_irq_epoch, r0fg1_irq_error;
static uint8_t r0fg1_irq_summary[R0FG1_EPOCHS * R0FG1_IRQ_SUMMARY_BYTES];
static uint8_t r0fc_hardware_low = 200u;
static uint16_t r0fc_software_low = 0xcff0u;
static uint8_t cfresult[R0FG1_RESULT_BYTES], trace[R0FG1_TRACE_BYTES];
static uint16_t records = R0FG1_RECORDS, world_generation = 1u;
static uint32_t capture_max, previous_capture;
static uint32_t records_crc = 0xffffffffu, worlds_crc = 0xffffffffu;
static uint32_t pools_crc = 0xffffffffu;
static uint8_t prepared;
static uint32_t corrupt_at = UINT32_MAX, fail_read_at = UINT32_MAX;
static uint32_t corrupt_write_at = UINT32_MAX, fail_write_at = UINT32_MAX;

static void r0fg1_display_metrics(void) {}
static void r0fc_stack_measure(void) {}
static uint32_t r0fg1_workload_hash(void) { return 0u; }
static uint16_t r0fg1_causality_errors(void) { return 0u; }
static uint16_t r0fg1_ai_runs(uint8_t tier) { (void)tier; return 0u; }

uint8_t r0fg1_trace_write(uint32_t offset, const uint8_t *bytes, uint8_t length)
{
    assert(offset + length <= sizeof(trace));
    if (offset <= fail_write_at && fail_write_at < offset + length)
    {
        return 0u;
    }
    memcpy(trace + offset, bytes, length);
    if (offset <= corrupt_write_at && corrupt_write_at < offset + length)
    {
        trace[corrupt_write_at] ^= 1u;
    }
    return 1u;
}

uint8_t r0fg1_trace_read(uint32_t offset, uint8_t *bytes, uint8_t length)
{
    assert(offset + length <= sizeof(trace));
    if (offset <= fail_read_at && fail_read_at < offset + length)
    {
        return 0u;
    }
    memcpy(bytes, trace + offset, length);
    if (offset <= corrupt_at && corrupt_at < offset + length)
    {
        bytes[corrupt_at - offset] ^= 1u;
    }
    return 1u;
}

uint8_t r0fg1_transport_prepare(uint32_t length, uint32_t residue)
{
    assert(r0fg1_export_status == 0x6du);
    r0fg1_export_status++;
    assert(length == R0FG1_TRACE_BYTES);
    uint32_t crc = 0xffffffffu;
    for (uint32_t at = 0u; at < length; at++)
    {
        crc = r0fs_crc32_update(crc, trace + at, 1u);
    }
    if (~crc != residue)
    {
        return 0u;
    }
    prepared = 1u;
    return 1u;
}

#include "capture_owner_under_test.inc"

static uint8_t finish_capture(void)
{
    // Each injection models a fresh one-shot terminal attempt.
    r0fg1_export_status = 0x6bu;
    return r0fg1_capture_finish();
}

static void check_capture(uint16_t worlds)
{
    world_generation = worlds;
    memset(record, 0, sizeof(record));
    memset(trace, 0, sizeof(trace));
    phase = epoch = cffault = prepared = 0u;
    records_crc = worlds_crc = pools_crc = 0xffffffffu;
    corrupt_at = fail_read_at = corrupt_write_at = fail_write_at = UINT32_MAX;
    assert(r0fg1_owners_begin());
    for (uint16_t tick = 0u; tick < records; tick++)
    {
        records_crc = r0fs_crc32_update(records_crc, record, sizeof(record));
    }
    worlds_crc = r0fs_crc32_update(worlds_crc, trace + R0FG1_WORLD_OFFSET,
        (uint16_t)(world_generation * R0FG1_WORLD_EVENT_BYTES));
    r0fg1_phase_end();
    assert(trace[R0FG1_POOL_OFFSET] == 0u);
    phase = R0FG1_PHASES - 1u;
    r0fg1_phase_end();
    uint8_t pre[R0FG1_POOL_EPOCH_BYTES];
    memcpy(pre, trace + R0FG1_POOL_OFFSET, sizeof(pre));
    assert(pre[0] == R0FG1_POOL_FACES_CAPACITY);
    for (uint8_t owner = 0u; owner < R0FG1_POOL_COUNT; owner++)
    {
        r0fg1_owner_sample(owner, 1u);
    }
    epoch = 1u;
    r0fg1_phase_end();
    assert(!cffault && !r0fg1_irq_epoch);
    assert(memcmp(pre, trace + R0FG1_POOL_OFFSET, sizeof(pre)) == 0);
    assert(finish_capture() && prepared);
    uint32_t tail = R0FG1_WORLD_OFFSET + (uint32_t)worlds * R0FG1_WORLD_EVENT_BYTES;
    for (uint32_t at = tail; at < R0FG1_TRACE_BYTES - 4u; at++)
    {
        assert(trace[at] == (uint8_t)((at & 255u) ^ R0FG1_CAPACITY_PATTERN_XOR));
    }
    static const uint32_t regions[] = {
        0u, R0FG1_HEADER_BYTES,
        R0FG1_HEADER_BYTES + (uint32_t)R0FG1_RECORDS * R0FG1_RECORD_BYTES,
        R0FG1_POOL_OFFSET, R0FG1_WORLD_OFFSET,
    };
    for (unsigned region = 0u; region < (worlds ? 5u : 4u); region++)
    {
        prepared = 0u;
        corrupt_at = regions[region];
        assert(!finish_capture() && !prepared);
        corrupt_at = UINT32_MAX;
        fail_read_at = regions[region];
        assert(!finish_capture() && !prepared);
        fail_read_at = UINT32_MAX;
    }
    const uint32_t tail_boundaries[] = {
        tail, (tail + 255u) & ~255ul, R0FG1_TRACE_BYTES - 5u,
    };
    for (unsigned index = 0u; index < sizeof(tail_boundaries) / sizeof(tail_boundaries[0]); index++)
    {
        uint32_t at = tail_boundaries[index];
        prepared = 0u;
        corrupt_at = at;
        assert(!finish_capture() && !prepared);
        corrupt_at = UINT32_MAX;
        fail_read_at = at;
        assert(!finish_capture() && !prepared);
        fail_read_at = UINT32_MAX;
        corrupt_write_at = at;
        assert(!finish_capture() && !prepared);
        corrupt_write_at = UINT32_MAX;
        fail_write_at = at;
        assert(!finish_capture() && !prepared);
        fail_write_at = UINT32_MAX;
    }
    const uint32_t writes[] = {0u, 255u, R0FG1_POOL_OFFSET - R0FG1_RESULT_BYTES,
                              R0FG1_TRACE_BYTES - 4u};
    for (unsigned index = 0u; index < sizeof(writes) / sizeof(writes[0]); index++)
    {
        prepared = 0u;
        fail_write_at = writes[index];
        assert(!finish_capture() && !prepared);
        fail_write_at = UINT32_MAX;
    }
    assert(finish_capture() && prepared);
}

int main(void)
{
    static const uint16_t worlds[] = {0u, 1u, 5u, 6u, 100u, R0FG1_MAX_WORLD_EVENTS};
    for (unsigned index = 0u; index < sizeof(worlds) / sizeof(worlds[0]); index++)
    {
        check_capture(worlds[index]);
    }
    puts("actual capture functions: zero/partial/full real world capacity; full allocation tail pattern; five region CRC/read failures; tail first/page/last corrupt writes/reads and copy failures; header/result/final CRC write failures; immutable checkpoints and repeated finalization PASS");
    return 0;
}
