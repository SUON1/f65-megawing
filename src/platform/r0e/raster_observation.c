#include <stdint.h>
#include <mega65.h>

/*
 * Private R0-E diagnostic helper.  It reads only the VIC-II-compatible
 * raster low byte; it performs no VIC unlock or write, MAP, DMA, CIA, IRQ,
 * or NMI operation.  Its unit is intentionally only a modulo-256 raster-line
 * delta, never a CPU-cycle or end-to-end latency value.
 */
uint8_t r0e_raster_low_read(void) { return VICII.rasterline; }

uint8_t r0e_raster_wait_low_phase(uint8_t phase) {
  uint16_t attempts;
  for (attempts = 0u; attempts != 0xffffu; ++attempts)
    if (r0e_raster_low_read() == phase) return 1u;
  return 0u;
}
