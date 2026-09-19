#include <stdint.h>
#include "r0f_interfaces.h"
#ifdef R0F_CLOCK_TEST
extern uint8_t r0f_bus_read(uint16_t address);
extern void r0f_bus_write(uint16_t address, uint8_t value);
#else
static uint8_t r0f_bus_read(uint16_t address) { return *(volatile uint8_t *)(uintptr_t)address; }
static void r0f_bus_write(uint16_t address, uint8_t value) { *(volatile uint8_t *)(uintptr_t)address = value; }
#endif
static uint8_t saved_a, saved_b;
static uint8_t owned;

/* Private reset-only contract: docs/reports/R0-F_CIA_TIMING_CONTRACT.md. */
uint8_t r0f_clock_begin(void) {
  uint8_t control;
  if (r0f_bus_read(0xd030) & 1u) return 0u;
  control = r0f_bus_read(0xdc0e);
  if (control & 0x40u) return 0u; /* Timer A would clock an inherited serial output. */
  saved_a = (uint8_t)(control & 0x80u);
  saved_b = (uint8_t)(r0f_bus_read(0xdc0f) & 0x80u);
  r0f_bus_write(0xdc0e, saved_a); r0f_bus_write(0xdc0f, saved_b);
  r0f_bus_write(0xdc04, 255u); r0f_bus_write(0xdc05, 255u);
  r0f_bus_write(0xdc06, 255u); r0f_bus_write(0xdc07, 255u);
  r0f_bus_write(0xdc0f, (uint8_t)(saved_b | 0x51u));
  r0f_bus_write(0xdc0e, (uint8_t)(saved_a | 0x11u));
  owned = 1u;
  return 1u;
}
void r0f_clock_stop(void) {
  if (owned) { r0f_bus_write(0xdc0e, saved_a); r0f_bus_write(0xdc0f, saved_b); owned = 0u; }
}
uint8_t r0f_clock_now(uint32_t *value) {
  uint8_t tries;
  for (tries = 0u; tries != 32u; ++tries) {
    uint8_t bh = r0f_bus_read(0xdc07), bl = r0f_bus_read(0xdc06);
    uint8_t bh2 = r0f_bus_read(0xdc07);
    uint8_t ah = r0f_bus_read(0xdc05), al = r0f_bus_read(0xdc04);
    uint8_t ah2 = r0f_bus_read(0xdc05), bl2 = r0f_bus_read(0xdc06), bh3 = r0f_bus_read(0xdc07);
    if (bh == bh2 && bh == bh3 && bl == bl2 && ah == ah2) {
      *value = ~((uint32_t)bh << 24u | (uint32_t)bl << 16u |
                 (uint32_t)ah << 8u | al);
      return 1u;
    }
  }
  return 0u;
}
uint8_t r0f_frame_read(void) { return r0f_bus_read(0xd7fa); }
uint8_t r0f_video_read(void) { return r0f_bus_read(0xd06f); }
uint8_t r0f_speed_read(void) { return r0f_bus_read(0xd054); }
