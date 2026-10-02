#ifndef R0F_GROUP1_TIMING_H
#define R0F_GROUP1_TIMING_H

#include <stdint.h>

// Private measurement arithmetic, not a hardware clock or production scheduler.
// Compare only intervals shorter than half the 32-bit timestamp range.
typedef struct
{
    uint32_t release_counts;
    uint32_t period_q16;
    uint16_t fraction;
} r0fg1_clock;

typedef struct
{
    uint32_t execution_counts;
    uint32_t publication_counts;
    uint32_t release_lateness_counts;
    uint32_t deadline_debt_counts;
    uint32_t deadline_slack_counts;
    uint8_t verdict;
} r0fg1_tick_measurement;

enum
{
    R0FG1_INVALID = 0,
    R0FG1_WITHIN_DEADLINE = 1,
    R0FG1_DEADLINE_MISS = 2,
    R0FG1_BOUNDARY_UNCERTAIN = 3,
};

uint8_t r0fg1_clock_init(r0fg1_clock *clock, uint32_t first_release_counts,
                         uint32_t period_q16);
uint32_t r0fg1_next_release(const r0fg1_clock *clock);
void r0fg1_clock_advance(r0fg1_clock *clock);
uint8_t r0fg1_measure_tick(const r0fg1_clock *clock, uint32_t start_counts,
                          uint32_t publication_counts, uint32_t end_counts,
                          uint32_t uncertainty_counts,
                          r0fg1_tick_measurement *measurement);

#endif
