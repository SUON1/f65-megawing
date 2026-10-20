// Development-only adapter. Physical access is not exposed to runtime owners.
#pragma once
#include "m1_development.h"

uint8_t m1_platform_begin(void);
uint32_t m1_platform_now(void);
uint32_t m1_platform_period(void);
uint8_t m1_platform_key(void);
uint8_t m1_platform_frame(void);
uint8_t m1_platform_row(uint8_t store, uint8_t row, uint8_t *bytes);
uint8_t m1_platform_color_row(uint8_t row, uint8_t *bytes);
void m1_platform_palette(uint8_t border, uint8_t background);
uint8_t m1_platform_swap(uint8_t store);
uint8_t m1_platform_fault(void);
void m1_platform_measure(void);

void m1_platform_alarm(void);
