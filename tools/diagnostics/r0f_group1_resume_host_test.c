// Native boundary test: actual extracted C, with physical register/copy edges
// mocked. The stopped CIA example demonstrates the hazard, not P05 causality.
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "r0f_combined.h"
#include "r0f_successor.h"
#include "r0f_successor_integration.h"
#include "successor_lifecycle.h"

static uint8_t registers[65536], result_bytes[2048], list[17], transfer[255];
static uint8_t *const cfresult = result_bytes;
#define CFREG(address) registers[(uint16_t)(address)]

static uint8_t cffault, cfreclaimed, application_dma_outstanding;
static uint8_t display_suspended, display_suspended_d011, display_ready, display_front;
static uint16_t display_clear_at, tick_before_record;
static uint32_t cfperiod = 655360ul, next_deadline, checksum_before_record;
static uint32_t low_before_record, low_after_record, dos_before_record, dos_after_record;
static uint8_t lifecycle_state, context_invalidated_record, r0f_pf_nmi_seen, r0fsi_irq_fault;
static uint8_t context_invalidated, irq_enabled, selected_line, audio_started;
static uint8_t bad_state, copy_fault, dma_clock_fault, dma_encoding_fault, reclaim_fault;
static unsigned int dma_jobs, staging_copies;
typedef struct
{
    uint8_t displayed_valid;
} mock_presentation;
static mock_presentation display_presentation;

static void r0fs_context_invalidate(void)
{
    context_invalidated = 1u;
}

static uint8_t reclaim_after_storage(void)
{
    assert(context_invalidated && lifecycle_state == R0FS_S_SERVICES_RESUMED);
    if (reclaim_fault)
    {
        return 0u;
    }
    cfreclaimed = 1u;
    if (bad_state)
    {
        display_suspended = 0u;
    }
    return 1u;
}

static void r0f_pf_start_irq(void)
{
    assert(context_invalidated && cfreclaimed);
    assert(lifecycle_state == R0FS_S_SERVICES_RESUMED && !audio_started);
    irq_enabled = 1u;
    // Model time progressing after the real initializer programs the timers.
    if (!dma_clock_fault)
    {
        registers[0xdc04] = 0u;
        registers[0xdc05] = 128u;
    }
}

static void r0f_pf_stop_irq(void)
{
    irq_enabled = 0u;
}

static void cfaudio_stop(void)
{
    audio_started = 0u;
}

static void cfaudio_begin(void)
{
    assert(irq_enabled && selected_line && !display_suspended);
    audio_started = 1u;
}

static void r0fsi_irq_select_line(void)
{
    assert(irq_enabled && !display_suspended && dma_jobs == 15u);
    selected_line = 1u;
}

static void display_configure(void)
{
    assert(dma_jobs == 15u);
}

static void r0fg1_presentation_cancel(mock_presentation *presentation)
{
    (void)presentation;
}

static uint8_t cfcopy(uint32_t physical, uint8_t *bytes, uint8_t length, uint8_t to_chip)
{
    (void)bytes;
    assert(cfreclaimed && to_chip && length);
    if (copy_fault)
    {
        cffault = copy_fault;
        return 0u;
    }
    if (physical != R0FC_DMA_LIST)
    {
        assert(physical >= R0FC_STAGING);
        assert(physical + length <= R0FC_STAGING + R0FSI_DISPLAY_QUANTUM_BYTES);
        staging_copies++;
    }
    return 1u;
}

static uint8_t r0fc_dma_encode(uint8_t *bytes, uint32_t source,
                              uint32_t destination, uint16_t length, uint8_t reclaimed)
{
    (void)bytes;
    assert(reclaimed && source == R0FC_STAGING);
    assert(destination == R0FC_ROM + dma_jobs * R0FSI_DISPLAY_QUANTUM_BYTES);
    assert(length == R0FSI_DISPLAY_QUANTUM_BYTES);
    if (dma_encoding_fault)
    {
        return 0u;
    }
    dma_jobs++;
    return 1u;
}

static void cfput16(uint16_t at, uint16_t value)
{
    result_bytes[at] = (uint8_t)value;
    result_bytes[at + 1u] = (uint8_t)(value >> 8u);
}

static void cfput32(uint16_t at, uint32_t value)
{
    for (uint8_t index = 0u; index < 4u; index++)
    {
        result_bytes[at + index] = (uint8_t)(value >> (index * 8u));
    }
}

static uint32_t cfget32(uint16_t at)
{
    uint32_t value = 0u;
    for (uint8_t index = 0u; index < 4u; index++)
    {
        value |= (uint32_t)result_bytes[at + index] << (index * 8u);
    }
    return value;
}

static void r0fg1_dma(uint32_t start)
{
    (void)start;
    // Acquisition is inactive between epochs; no trace record is modified.
}

#include "resume_under_test.inc"

static void reset(void)
{
    memset(registers, 0, sizeof(registers));
    memset(result_bytes, 0, sizeof(result_bytes));
    memset(registers + 0xdc04, 255, 4u);
    cffault = cfreclaimed = application_dma_outstanding = 0u;
    context_invalidated = context_invalidated_record = irq_enabled = 0u;
    selected_line = audio_started = r0f_pf_nmi_seen = r0fsi_irq_fault = 0u;
    bad_state = copy_fault = dma_clock_fault = dma_encoding_fault = reclaim_fault = 0u;
    display_suspended = 1u;
    display_suspended_d011 = 0x1bu;
    display_ready = display_presentation.displayed_valid = 1u;
    display_front = 0u;
    lifecycle_state = R0FS_S_APPLICATION_RESTORED;
    dma_jobs = staging_copies = 0u;
}

static void expect_failure(uint8_t fault)
{
    assert(!resume_boundary());
    assert(cffault == fault && lifecycle_state == R0FS_S_LOCKOUT);
    assert(!irq_enabled && !audio_started && !selected_line);
}

int main(void)
{
    reset();
#if TEST_BASELINE
    expect_failure(93u);
    assert(dma_jobs == 1u && staging_copies == 17u);
    assert(cfnow() == 0u && cffault == 3u);
    puts("Baseline stopped-CIA model: inner 03 hidden by 5D PASS");
#else
    assert(resume_boundary());
    assert(!cffault && irq_enabled && audio_started && selected_line);
    assert(!display_suspended && !display_presentation.displayed_valid);
    assert(dma_jobs == 15u && staging_copies == 17u);
    assert(tick_before_record == 1600u && checksum_before_record == 0x6b765fdbul);
    assert(registers[0xd011] == 0x1bu);
    reset();
    bad_state = 1u;
    expect_failure(93u);
    reset();
    application_dma_outstanding = 1u;
    expect_failure(93u);
    for (uint8_t fault = 21u; fault <= 22u; fault++)
    {
        reset();
        copy_fault = fault;
        expect_failure(fault);
    }
    reset();
    dma_clock_fault = 1u;
    expect_failure(3u);
    reset();
    dma_encoding_fault = 1u;
    expect_failure(30u);
    reset();
    registers[0xdc0e] = 0x40u;
    expect_failure(2u);
    assert(dma_jobs == 0u);
    reset();
    reclaim_fault = 1u;
    expect_failure(81u);
    reset();
    r0f_pf_nmi_seen = 1u;
    expect_failure(81u);
    reset();
    dma_clock_fault = 1u;
    r0fsi_irq_fault = 105u;
    expect_failure(105u);
    puts("Candidate ordering, 15 clears, state/copy/DMA/clock faults and lockout PASS");
#endif
    return 0;
}
