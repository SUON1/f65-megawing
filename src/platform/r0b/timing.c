#include <stdint.h>
#include <mega65.h>

/*
 * Read-only VIC-II-compatible raster timestamp. It reads D012 only and
 * performs no VIC unlock, mode write, raster IRQ, CIA, or DMA operation. The
 * delta is an 8-bit raster-line elapsed-time value, not a CPU-cycle or physical
 * input/audio-output latency result.
 */
static uint8_t start_tick;

uint8_t r0b_timer_begin(void) {
  start_tick = VICII.rasterline;
  return 1u;
}

uint16_t r0b_timer_end(void) {
  return (uint16_t)(uint8_t)(VICII.rasterline - start_tick);
}
