#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "r0f_group1_trace.h"
#include "group1_pool_owners.h"
#include "successor_lifecycle.h"

// Exact checkpoint/finalization functions, generated from the candidate C.
// Mock only the trace transport and terminal metrics. No target evidence.
uint8_t cffault;
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
static uint8_t corrupt_pool, prepared;

static void r0fg1_display_metrics(void) {}
static void r0fc_stack_measure(void) {}
static uint32_t r0fg1_workload_hash(void) { return 0u; }
static uint16_t r0fg1_causality_errors(void) { return 0u; }
static uint16_t r0fg1_ai_runs(uint8_t tier) { (void)tier; return 0u; }

static uint8_t r0fg1_trace_write(uint32_t offset, const uint8_t *bytes, uint8_t length)
{
    assert(offset + length <= sizeof(trace));
    memcpy(trace + offset, bytes, length);
    return 1u;
}

static uint8_t r0fg1_trace_read(uint32_t offset, uint8_t *bytes, uint8_t length)
{
    assert(offset + length <= sizeof(trace));
    memcpy(bytes, trace + offset, length);
    if (corrupt_pool && offset == R0FG1_POOL_OFFSET)
    {
        bytes[0] ^= 1u;
    }
    return 1u;
}

static uint8_t r0fg1_transport_prepare(uint32_t length, uint32_t residue)
{
    assert(length == R0FG1_WORLD_OFFSET + R0FG1_WORLD_EVENT_BYTES + 4u);
    uint32_t crc = 0xffffffffu;
    for (uint32_t at = 0u; at < length; at++)
    {
        crc = r0fs_crc32_update(crc, trace + at, 1u);
    }
    assert(~crc == residue);
    prepared = 1u;
    return 1u;
}

#include "capture_owner_under_test.inc"

int main(void)
{
    assert(r0fg1_owners_begin());
    for (uint16_t tick = 0u; tick < records; tick++)
    {
        records_crc = r0fs_crc32_update(records_crc, record, sizeof(record));
    }
    worlds_crc = r0fs_crc32_update(worlds_crc, trace + R0FG1_WORLD_OFFSET,
                                    R0FG1_WORLD_EVENT_BYTES);
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
    assert(r0fg1_capture_finish() && prepared);
    prepared = 0u;
    corrupt_pool = 1u;
    assert(!r0fg1_capture_finish() && !prepared);
    puts("actual capture functions: two immutable checkpoints, boundaries, whole-stream CRC and pool readback corruption reject PASS");
    return 0;
}
