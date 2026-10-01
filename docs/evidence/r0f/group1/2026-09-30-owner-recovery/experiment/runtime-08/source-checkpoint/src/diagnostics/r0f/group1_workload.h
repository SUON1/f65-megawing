#ifndef R0FG1_WORKLOAD_H
#define R0FG1_WORKLOAD_H
#include <stdint.h>

// Bounded instruction/data fixtures, not flight coefficients or AI doctrine.
void r0fg1_workload_stage(uint8_t stage, uint16_t tick);
uint32_t r0fg1_workload_hash(void);
uint16_t r0fg1_ai_runs(uint8_t tier);
uint16_t r0fg1_causality_errors(void);
#endif
