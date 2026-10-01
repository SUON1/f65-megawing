#include <stdint.h>

#include "combined_platform.h"
#include "group1_capture.h"
#include "group1_timing.h"
#include "group1_transport.h"
#include "group1_workload.h"
#include "group1_pool_owners.h"
#include "successor_irq.h"
#include "successor_lifecycle.h"

// Owns measurement/encoding only. Service and workload owners invoke hooks.
// CIA coherent reads use the inherited bounded cfnow wrapper. B=2 is retained.
static uint8_t record[R0FG1_RECORD_BYTES], header[R0FG1_HEADER_BYTES];
static r0fg1_clock clock;
static uint32_t stage_start, previous_capture, capture_max;
static uint32_t records_crc = 0xfffffffful;
static uint32_t worlds_crc = 0xfffffffful;
static uint16_t records, world_generation, world_tick;
static uint16_t phase_edges[R0FG1_PHASE_BINS - 1u];
static uint8_t epoch, phase, active, next_stage;
extern void r0fc_stack_measure(void);
extern volatile uint8_t r0fc_hardware_low;
extern volatile uint8_t r0f_pf_stack_high;
extern volatile uint16_t r0fc_software_low;
extern volatile uint8_t r0fg1_irq_epoch, r0fg1_irq_error;
extern volatile uint8_t r0fg1_irq_summary[R0FG1_EPOCHS * R0FG1_IRQ_SUMMARY_BYTES];

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

static uint16_t get16(const uint8_t *in)
{
    return (uint16_t)(in[0] | (uint16_t)in[1] << 8u);
}

static void duration(uint8_t offset, uint32_t counts, uint8_t accumulate)
{
    if (accumulate)
    {
        counts += get16(record + offset);
    }
    if (counts > 65535ul)
    {
        cffault = 108u;
        return;
    }
    put16(record + offset, (uint16_t)counts);
}

uint8_t r0fg1_capture_init(void)
{
    return r0fg1_owners_begin() && r0fg1_transport_init();
}

void r0fg1_calibration(uint8_t after)
{
    uint8_t base = after ? R0FG1_H_POST_FRAME_SAMPLES : R0FG1_H_PRE_FRAME_SAMPLES;
    for (uint8_t index = 0u; index < 64u; index++)
    {
        header[base + index] = cfresult[(after ? 1536u : 176u) + index];
    }
    if (after)
    {
        put32(header + R0FG1_H_AUDIO_SERVICE_GAP, cfget32(R0FC_O_SERVICE_GAP));
        put32(header + R0FG1_H_POST_CIA_FRAME, cfget32(R0FC_O_AFTER_CIA_FRAME));
        return;
    }
    header[0] = 'G';
    header[1] = '1';
    header[2] = 'T';
    header[3] = '0' + R0FG1_VERSION;
    put16(header + R0FG1_H_VERSION, R0FG1_VERSION);
    put16(header + R0FG1_H_RECORD_BYTES, R0FG1_RECORD_BYTES);
    put32(header + R0FG1_H_PERIOD_Q16, cfperiod);
    put32(header + R0FG1_H_CIA_FRAME, cfcia_frame);
    put32(header + R0FG1_H_CYCLES_FRAME, cfcycles_frame);
    header[R0FG1_H_REFERENCE] = cfresult[R0FC_O_REFERENCE];
    header[R0FG1_H_VIDEO] = CFREG(0xd06fu);
    header[R0FG1_H_CPU_SPEED] = CFREG(0xd054u);
    header[R0FG1_H_BASE_PAGE] = 2u;
    uint32_t minimum = 0xfffffffful, maximum = 0u;
    for (uint8_t index = 0u; index < R0FG1_CALIBRATION_READS; index++)
    {
        uint32_t start = cfnow();
        uint32_t counts = cfnow() - start;
        if (counts < minimum)
        {
            minimum = counts;
        }
        if (counts > maximum)
        {
            maximum = counts;
        }
    }
    put32(header + R0FG1_H_READ_MIN, minimum);
    put32(header + R0FG1_H_READ_MAX, maximum);
}

void r0fg1_phase(uint8_t selected_epoch, uint8_t selected_phase, uint32_t release)
{
    epoch = selected_epoch;
    phase = selected_phase;
    if (!r0fg1_clock_init(&clock, release, cfperiod)
        || !r0fg1_phase_edges((uint16_t)(cfperiod >> 16u), phase_edges))
    {
        cffault = 108u;
    }
    r0fg1_irq_epoch = (uint8_t)(epoch + 1u);
}

void r0fg1_phase_end(void)
{
    r0fg1_irq_epoch = 0u;
    if (phase == R0FG1_PHASES - 1u)
    {
        r0fg1_owners_encode(record);
        if (!r0fg1_trace_write(R0FG1_POOL_OFFSET
                + (uint32_t)epoch * R0FG1_POOL_EPOCH_BYTES,
                record, R0FG1_POOL_EPOCH_BYTES))
        {
            cffault = 110u;
        }
    }
}

void r0fg1_tick_open(void)
{
    for (uint8_t index = 0u; index < sizeof(record); index++)
    {
        record[index] = 0u;
    }
    record[R0FG1_O_EPOCH] = epoch;
    record[R0FG1_O_PHASE] = phase;
    put32(record + R0FG1_O_RELEASE, clock.release_counts);
    put32(record + R0FG1_O_PREVIOUS_CAPTURE_COUNTS, previous_capture);
    uint16_t irq;
    if (!r0fsi_irq_snapshot(&irq))
    {
        cffault = 108u;
    }
    put16(record + R0FG1_O_IRQ_BEFORE, irq);
    next_stage = 1u;
    active = 1u;
}

void r0fg1_tick_start(void)
{
    put32(record + R0FG1_O_START, cfnow());
}

void r0fg1_stage_begin(uint8_t stage)
{
    if (stage != next_stage)
    {
        cffault = 109u;
    }
    stage_start = cfnow();
}

void r0fg1_stage_end(uint8_t stage)
{
    uint32_t now = cfnow();
    duration((uint8_t)(R0FG1_O_STAGE_COUNTS + (stage - 1u) * 2u), now - stage_start, 0u);
    next_stage++;
    if (stage == R0FG1_STAGES)
    {
        put32(record + R0FG1_O_PUBLICATION, now);
    }
}

void r0fg1_service(uint8_t service, uint32_t start)
{
    if (active && service < 3u)
    {
        uint8_t offset = (uint8_t)(R0FG1_H_SERVICE_PHASE_MASKS
            + (epoch * 3u + service) * 2u);
        uint16_t mask = get16(header + offset);
        if (mask != 0xffffu)
        {
            uint8_t bin = r0fg1_service_phase_bin(
                start, clock.release_counts,
                (uint16_t)(clock.period_q16 >> 16u), phase_edges);
            if (bin != R0FG1_NO_PHASE_BIN)
            {
                put16(header + offset, (uint16_t)(mask | (uint16_t)(1u << bin)));
            }
        }
        duration((uint8_t)(R0FG1_O_INPUT_COUNTS + service * 2u), cfnow() - start, 1u);
    }
}

void r0fg1_service_order(uint8_t order)
{
    if (active && order < 6u)
    {
        header[R0FG1_H_SERVICE_ORDER_MASKS + epoch] |= (uint8_t)(1u << order);
    }
}

void r0fg1_dma(uint32_t start)
{
    if (active)
    {
        uint32_t counts = cfnow() - start;
        put16(record + R0FG1_O_DMA_JOBS, (uint16_t)(get16(record + R0FG1_O_DMA_JOBS) + 1u));
        if (counts > get16(record + R0FG1_O_DMA_MAX))
        {
            duration(R0FG1_O_DMA_MAX, counts, 0u);
        }
    }
}

void r0fg1_world(uint16_t source_tick, uint16_t request_tick,
                 uint8_t key_flags, uint8_t anchor_mask,
                 uint32_t registration_crc)
{
    uint8_t event[R0FG1_WORLD_EVENT_BYTES];
    if (world_generation >= R0FG1_MAX_WORLD_EVENTS)
    {
        cffault = 112u;
        return;
    }
    world_tick = source_tick;
    event[R0FG1_W_EPOCH] = epoch;
    event[R0FG1_W_PHASE] = phase;
    put16(event + R0FG1_W_SOURCE_TICK, source_tick);
    put32(event + R0FG1_W_SWAP_TIME, cfnow());
    event[R0FG1_W_KEY_FLAGS] = key_flags;
    event[R0FG1_W_ANCHOR_MASK] = anchor_mask;
    put16(event + R0FG1_W_REQUEST_TICK, request_tick);
    put32(event + R0FG1_W_REGISTRATION_CRC, registration_crc);
    worlds_crc = r0fs_crc32_update(worlds_crc, event, sizeof(event));
    if (!r0fg1_trace_write(R0FG1_WORLD_OFFSET
                          + (uint32_t)world_generation * sizeof(event),
                          event, sizeof(event)))
    {
        cffault = 110u;
    }
    world_generation++;
}

void r0fg1_presentation_metrics(uint8_t anchor_high, uint8_t occlusion_high,
    uint16_t drops, uint16_t requests, uint16_t cancels,
    uint8_t views, uint8_t tiers)
{
    header[R0FG1_H_ANCHOR_HIGH] = anchor_high;
    header[R0FG1_H_OCCLUSION_HIGH] = occlusion_high;
    put16(header + R0FG1_H_ANCHOR_DROPS, drops);
    put16(header + R0FG1_H_VIEW_REQUESTS, requests);
    put16(header + R0FG1_H_VIEW_CANCELS, cancels);
    header[R0FG1_H_VIEW_MASK] = views;
    header[R0FG1_H_TIER_MASK] = tiers;
}

void r0fg1_tick_close(uint16_t tick, uint16_t published,
                      uint16_t reading_tick, uint8_t snapshot_high,
                      uint8_t queue_high, uint8_t display_valid)
{
    if (records >= R0FG1_RECORDS || next_stage != R0FG1_STAGES + 1u)
    {
        cffault = 109u;
        return;
    }
    uint16_t irq;
    if (!r0fsi_irq_snapshot(&irq))
    {
        cffault = 108u;
    }
    put16(record + R0FG1_O_TICK, tick);
    put16(record + R0FG1_O_IRQ_AFTER, irq);
    put16(record + R0FG1_O_PUBLISHED, published);
    put16(record + R0FG1_O_READING_TICK, reading_tick);
    put16(record + R0FG1_O_WORLD_GENERATION, world_generation);
    put16(record + R0FG1_O_WORLD_SOURCE_TICK, world_tick);
    record[R0FG1_O_SNAPSHOT_HIGH] = snapshot_high;
    record[R0FG1_O_QUEUE_HIGH] = queue_high;
    record[R0FG1_O_DISPLAY_VALID] = display_valid;
    record[R0FG1_O_ENTRY_STACK_POINTER] = r0f_pf_stack_high;
    uint32_t end = cfnow();
    put32(record + R0FG1_O_END, end);
    records_crc = r0fs_crc32_update(records_crc, record, sizeof(record));
    if (!r0fg1_trace_write(R0FG1_HEADER_BYTES + (uint32_t)records * sizeof(record), record, sizeof(record)))
    {
        cffault = 110u;
    }
    records++;
    previous_capture = cfnow() - end;
    if (previous_capture > capture_max)
    {
        capture_max = previous_capture;
    }
    active = 0u;
}

uint32_t r0fg1_next_tick(void)
{
    r0fg1_clock_advance(&clock);
    return clock.release_counts;
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
    uint32_t crc = 0xfffffffful, read_records_crc = 0xfffffffful;
    uint32_t read_worlds_crc = 0xfffffffful;
    for (uint32_t offset = 0u; offset < trace_bytes - 4u;)
    {
        // Bound each read at header/record/result boundaries for independent
        // verification against the CRC accumulated before acquisition writes.
        uint32_t boundary = offset < R0FG1_HEADER_BYTES ? R0FG1_HEADER_BYTES
            : offset < result_offset ? result_offset
            : offset < R0FG1_WORLD_OFFSET ? R0FG1_WORLD_OFFSET : trace_bytes - 4u;
        uint8_t bytes = boundary - offset > sizeof(record) ? sizeof(record) : (uint8_t)(boundary - offset);
        if (!r0fg1_trace_read(offset, record, bytes))
        {
            return 0u;
        }
        crc = r0fs_crc32_update(crc, record, bytes);
        if (offset >= R0FG1_HEADER_BYTES && offset < result_offset)
        {
            read_records_crc = r0fs_crc32_update(read_records_crc, record, bytes);
        }
        if (offset >= R0FG1_WORLD_OFFSET)
        {
            read_worlds_crc = r0fs_crc32_update(read_worlds_crc, record, bytes);
        }
        offset += bytes;
    }
    if (read_records_crc != records_crc || read_worlds_crc != worlds_crc)
    {
        return 0u;
    }
    put32(record, ~crc);
    if (!r0fg1_trace_write(trace_bytes - 4u, record, 4u))
    {
        return 0u;
    }
    // CRC32 of any valid CRC32-appended stream has this fixed residue.
    return r0fg1_transport_prepare(trace_bytes, 0x2144df1cul);
}
