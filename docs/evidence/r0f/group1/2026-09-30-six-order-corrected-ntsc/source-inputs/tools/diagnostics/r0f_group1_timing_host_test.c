#include <assert.h>
#include <stdint.h>
#include <stdio.h>

#include "group1_timing.h"

static void check_period(uint32_t period, uint32_t epoch)
{
    r0fg1_clock clock;

    assert(r0fg1_clock_init(&clock, epoch, period));
    for (uint32_t tick = 0u; tick < 100000u; tick++)
    {
        // Independent 64-bit closed form, including repeated 32-bit wraps.
        uint64_t expected = ((uint64_t)tick * period) >> 16u;

        assert(clock.release_counts == epoch + (uint32_t)expected);
        assert(clock.fraction == (uint16_t)((uint64_t)tick * period));
        r0fg1_clock_advance(&clock);
    }
}

static void check_boundaries(uint32_t epoch)
{
    r0fg1_clock clock;
    r0fg1_tick_measurement measurement;

    assert(r0fg1_clock_init(&clock, epoch, 100u << 16u));
    for (uint32_t duration = 0u; duration < 201u; duration++)
    {
        for (uint32_t uncertainty = 0u; uncertainty < 5u; uncertainty++)
        {
            uint8_t expected = R0FG1_BOUNDARY_UNCERTAIN;
            if (duration + uncertainty < 100u)
            {
                expected = R0FG1_WITHIN_DEADLINE;
            }
            else if (duration > 100u + uncertainty)
            {
                expected = R0FG1_DEADLINE_MISS;
            }
            assert(r0fg1_measure_tick(&clock, epoch, epoch + duration / 2u,
                                      epoch + duration, uncertainty,
                                      &measurement) == expected);
            assert(measurement.execution_counts == duration);
        }
    }
    // Work can be short yet miss its deadline because dispatch was late.
    assert(r0fg1_measure_tick(&clock, epoch + 99u, epoch + 100u,
                              epoch + 102u, 0u, &measurement)
           == R0FG1_DEADLINE_MISS);
    assert(measurement.deadline_debt_counts == 2u);
    assert(measurement.release_lateness_counts == 99u);
    assert(r0fg1_measure_tick(&clock, epoch - 1u, epoch, epoch + 1u,
                              0u, &measurement) == R0FG1_INVALID);
    assert(r0fg1_measure_tick(&clock, epoch, epoch + 2u, epoch + 1u,
                              0u, &measurement) == R0FG1_INVALID);
    assert(r0fg1_measure_tick(&clock, epoch, epoch,
                              epoch + 0x80000000u, 0u, &measurement)
           == R0FG1_INVALID);
    assert(r0fg1_measure_tick(&clock, epoch, epoch, epoch,
                              0x80000000u, &measurement) == R0FG1_INVALID);
}

static void check_service_phases(void)
{
    const uint16_t periods[] = {16u, 17u, 31u, 32u, 33u, 1024u, 10000u, 65535u};
    const uint32_t releases[] = {100000u, 16u};
    uint16_t edges[R0FG1_PHASE_BINS - 1u];

    assert(!r0fg1_phase_edges(15u, edges));
    assert(!r0fg1_phase_edges(16u, 0));
    assert(r0fg1_service_phase_bin(0u, 16u, 15u, edges) == R0FG1_NO_PHASE_BIN);
    assert(r0fg1_service_phase_bin(0u, 16u, 16u, 0) == R0FG1_NO_PHASE_BIN);
    for (unsigned int index = 0u; index < sizeof(periods) / sizeof(periods[0]); index++)
    {
        uint16_t period = periods[index];
        uint16_t width = (uint16_t)(period / R0FG1_PHASE_BINS);
        uint16_t wider_bins = (uint16_t)(period % R0FG1_PHASE_BINS);
        uint16_t wider_counts = (uint16_t)((width + 1u) * wider_bins);

        assert(r0fg1_phase_edges(period, edges));
        for (unsigned int epoch = 0u; epoch < sizeof(releases) / sizeof(releases[0]); epoch++)
        {
            uint32_t release = releases[epoch];

            for (uint32_t elapsed = 0u; elapsed <= period; elapsed++)
            {
                // Independent quotient calculation covers unequal bin widths,
                // exact edges and CIA subtraction across a 32-bit wrap.
                uint32_t expected = elapsed < wider_counts
                    ? elapsed / (width + 1u)
                    : wider_bins + (elapsed - wider_counts) / width;
                if (expected >= R0FG1_PHASE_BINS)
                {
                    expected = R0FG1_PHASE_BINS - 1u;
                }
                uint32_t start = release - period + elapsed;

                assert(r0fg1_service_phase_bin(start, release, period, edges)
                       == expected);
            }
            assert(r0fg1_service_phase_bin(release + 1u, release, period, edges)
                   == R0FG1_NO_PHASE_BIN);
            assert(r0fg1_service_phase_bin(release - period - 1u, release, period, edges)
                   == R0FG1_NO_PHASE_BIN);
        }
    }
}

int main(void)
{
    const uint32_t periods[] = {
        0x00010000u, 0x00010001u, 0x12348000u, 0x1234ffffu, 0xffffffffu,
    };
    r0fg1_clock clock;
    r0fg1_tick_measurement measurement;

    for (unsigned int index = 0u; index < sizeof(periods) / sizeof(periods[0]); index++)
    {
        check_period(periods[index], 0u);
        check_period(periods[index], 0xfffffff0u);
    }
    check_boundaries(0u);
    check_boundaries(0xfffffff0u);
    check_service_phases();
    assert(!r0fg1_clock_init(&clock, 0u, 0xffffu));
    assert(!r0fg1_clock_init(0, 0u, 0x10000u));
    assert(r0fg1_measure_tick(0, 0u, 0u, 0u, 0u, &measurement)
           == R0FG1_INVALID);
    assert(r0fg1_measure_tick(&clock, 0u, 0u, 0u, 0u, 0) == R0FG1_INVALID);
    puts("Group 1 timing arithmetic PASS: 1000000 releases; deadline, uncertainty, wrap and service-phase boundaries");
    return 0;
}
