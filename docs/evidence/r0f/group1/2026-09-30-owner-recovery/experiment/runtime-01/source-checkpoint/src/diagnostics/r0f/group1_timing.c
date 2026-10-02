#include "group1_timing.h"

#define HALF_TIMESTAMP_RANGE 0x80000000ul

uint8_t r0fg1_clock_init(r0fg1_clock *clock, uint32_t first_release_counts,
                         uint32_t period_q16)
{
    if (clock == 0 || (period_q16 >> 16u) == 0u)
    {
        return 0u;
    }
    clock->release_counts = first_release_counts;
    clock->period_q16 = period_q16;
    clock->fraction = 0u;
    return 1u;
}

uint32_t r0fg1_next_release(const r0fg1_clock *clock)
{
    uint32_t fraction = (uint32_t)clock->fraction
                         + (clock->period_q16 & 0xfffful);

    return clock->release_counts + (clock->period_q16 >> 16u)
           + (fraction >> 16u);
}

void r0fg1_clock_advance(r0fg1_clock *clock)
{
    clock->release_counts = r0fg1_next_release(clock);
    clock->fraction = (uint16_t)((uint32_t)clock->fraction
                                + (clock->period_q16 & 0xfffful));
}

uint8_t r0fg1_measure_tick(const r0fg1_clock *clock, uint32_t start_counts,
                          uint32_t publication_counts, uint32_t end_counts,
                          uint32_t uncertainty_counts,
                          r0fg1_tick_measurement *measurement)
{
    uint32_t deadline;
    uint32_t distance;

    if (measurement == 0)
    {
        return R0FG1_INVALID;
    }
    *measurement = (r0fg1_tick_measurement){0};
    if (clock == 0 || (clock->period_q16 >> 16u) == 0u
        || uncertainty_counts >= HALF_TIMESTAMP_RANGE)
    {
        return R0FG1_INVALID;
    }
    measurement->release_lateness_counts = start_counts - clock->release_counts;
    measurement->publication_counts = publication_counts - start_counts;
    measurement->execution_counts = end_counts - start_counts;
    // An early start, reversed event, or ambiguous wrap invalidates acquisition.
    if (measurement->release_lateness_counts >= HALF_TIMESTAMP_RANGE
        || measurement->execution_counts >= HALF_TIMESTAMP_RANGE
        || measurement->publication_counts > measurement->execution_counts
        || end_counts - clock->release_counts >= HALF_TIMESTAMP_RANGE)
    {
        return R0FG1_INVALID;
    }
    deadline = r0fg1_next_release(clock);
    distance = end_counts - deadline;
    if (distance < HALF_TIMESTAMP_RANGE)
    {
        measurement->deadline_debt_counts = distance;
        measurement->verdict = distance <= uncertainty_counts
            ? R0FG1_BOUNDARY_UNCERTAIN : R0FG1_DEADLINE_MISS;
    }
    else
    {
        distance = deadline - end_counts;
        measurement->deadline_slack_counts = distance;
        measurement->verdict = distance <= uncertainty_counts
            ? R0FG1_BOUNDARY_UNCERTAIN : R0FG1_WITHIN_DEADLINE;
    }
    return measurement->verdict;
}

uint8_t r0fg1_phase_edges(uint16_t period_counts,
                           uint16_t edges[R0FG1_PHASE_BINS - 1])
{
    if (period_counts < R0FG1_PHASE_BINS || edges == 0)
    {
        return 0u;
    }
    uint16_t base = (uint16_t)(period_counts >> 4u);
    uint8_t remainder = (uint8_t)(period_counts & 15u);
    uint16_t boundary = 0u;
    for (uint8_t bin = 0u; bin < R0FG1_PHASE_BINS - 1u; bin++)
    {
        boundary = (uint16_t)(boundary + base + (bin < remainder));
        edges[bin] = boundary;
    }
    return 1u;
}

uint8_t r0fg1_service_phase_bin(uint32_t start_counts,
                                 uint32_t release_counts,
                                 uint16_t period_counts,
                                 const uint16_t edges[R0FG1_PHASE_BINS - 1])
{
    if (period_counts < R0FG1_PHASE_BINS || edges == 0)
    {
        return R0FG1_NO_PHASE_BIN;
    }
    uint32_t distance = release_counts - start_counts;
    if (distance > period_counts)
    {
        // A post-release call or a call outside this cohort is not a
        // pre-release service start. Subtraction is safe across CIA wrap.
        return R0FG1_NO_PHASE_BIN;
    }
    uint16_t elapsed = (uint16_t)(period_counts - distance);
    for (uint8_t bin = 0u; bin < R0FG1_PHASE_BINS - 1u; bin++)
    {
        if (elapsed < edges[bin])
        {
            return bin;
        }
    }
    return R0FG1_PHASE_BINS - 1u;
}
