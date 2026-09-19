#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
volatile uint8_t r0f_host_screen[2000], r0f_host_result[256];
static unsigned reads, phase_calls;
static int fail_phase;
extern void r0f_run(void);
uint8_t r0f_raster_low_read(void) {
  unsigned index = reads++;
  return (uint8_t)(250u + ((index & 1u) ? (index / 2u) * 17u : 0u));
}
uint8_t r0f_raster_wait_low_phase(uint8_t phase) {
  if (phase != (uint8_t)((phase_calls++ % 16u) * 16u)) abort();
  return (uint8_t)!(fail_phase && phase == 48u);
}
int main(int argc, char **argv) {
  (void)argv;
  fail_phase = argc > 1;
  r0f_run();
  if (phase_calls != 80u) abort();
  for (unsigned i = 0; i < 256u; ++i) putchar(r0f_host_result[i]);
  return 0;
}
