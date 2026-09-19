#include <stdint.h>
#ifdef R0F_CAPTURE_TEST
extern uint8_t r0f_bus_read(uint16_t address);
extern void r0f_bus_write(uint16_t address, uint8_t value);
#else
static uint8_t r0f_bus_read(uint16_t address) { return *(volatile uint8_t *)(uintptr_t)address; }
static void r0f_bus_write(uint16_t address, uint8_t value) { *(volatile uint8_t *)(uintptr_t)address = value; }
#endif
/* Post-acquisition only: docs/reports/R0-F_CAPTURE_CONTRACT.md. */
uint8_t r0f_capture_key(void) {
  uint8_t key = r0f_bus_read(0xd610u);
  if (key) r0f_bus_write(0xd610u, key);
  return key;
}
