#ifndef R0FG1_CAPTURE_H
#define R0FG1_CAPTURE_H
#include <stdint.h>
#include "r0f_group1_trace.h"

uint8_t r0fg1_capture_init(void);
void r0fg1_calibration(uint8_t after);
void r0fg1_phase(uint8_t epoch, uint8_t phase, uint32_t release);
void r0fg1_phase_end(void);
void r0fg1_tick_open(void);
void r0fg1_tick_start(void);
void r0fg1_stage_begin(uint8_t stage);
void r0fg1_stage_end(uint8_t stage);
void r0fg1_service(uint8_t service, uint32_t start);
void r0fg1_dma(uint32_t start);
void r0fg1_world(uint16_t source_tick);
void r0fg1_tick_close(uint16_t tick, uint16_t published,
                      uint16_t reading_tick, uint8_t snapshot_high,
                      uint8_t queue_high);
uint32_t r0fg1_next_tick(void);
uint8_t r0fg1_capture_finish(void);
#endif
