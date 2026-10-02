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
    assert(!r0fg1_clock_init(&clock, 0u, 0xffffu));
    assert(!r0fg1_clock_init(0, 0u, 0x10000u));
    assert(r0fg1_measure_tick(0, 0u, 0u, 0u, 0u, &measurement)
           == R0FG1_INVALID);
    assert(r0fg1_measure_tick(&clock, 0u, 0u, 0u, 0u, 0) == R0FG1_INVALID);
    puts("Group 1 timing arithmetic PASS: 1000000 releases; deadline, uncertainty and wrap boundaries");
    return 0;
}
