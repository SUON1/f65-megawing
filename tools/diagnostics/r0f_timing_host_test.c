#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
volatile uint8_t r0f_host_screen[2000], r0f_host_result[256];
extern unsigned char r0f_capture[];
extern void r0f_run(void), r0f_timing_run(void);
static uint32_t clock_value = 0xffff0000u;
static unsigned reads, raster_reads, phase_calls;
static const char *mode;
static int stopped;
void r0f_host_work_hook(uint16_t tick) {
  if (tick == 16u) {
    if (!strcmp(mode,"overrun")) clock_value += 12000u;
    if (!strcmp(mode,"overflow")) clock_value += 70000u;
    if (!strcmp(mode,"clock-jump")) clock_value += 1000001u;
  }
}
uint8_t r0f_raster_low_read(void) { unsigned i = raster_reads++; return (uint8_t)(250u + ((i & 1u) ? (i/2u)*17u : 0u)); }
uint8_t r0f_raster_wait_low_phase(uint8_t p) { if (p != (uint8_t)((phase_calls++%16u)*16u)) abort(); return 1u; }
uint8_t r0f_clock_begin(void) { return (uint8_t)(strcmp(mode,"begin-fail") != 0); }
void r0f_clock_stop(void) { stopped = 1; }
uint8_t r0f_clock_now(uint32_t *v) {
  if (!strcmp(mode,"read-fail") && reads++ == 10u) return 0u;
  if (strcmp(mode,"stuck-clock")) clock_value += 100u;
  *v = clock_value;
  return 1u;
}
uint8_t r0f_frame_read(void) { return !strcmp(mode,"stuck-frame") ? 0u : (uint8_t)((clock_value - 0xffff0000u)/20000u); }
uint8_t r0f_video_read(void) { return 0u; }
uint8_t r0f_speed_read(void) { return 0x40u; }
int main(int argc, char **argv) {
  mode = argc > 1 ? argv[1] : "pass";
  r0f_run(); r0f_timing_run();
  if (!stopped) abort();
  int success = !strcmp(mode,"pass") || !strcmp(mode,"overrun");
  if (success && r0f_host_result[151] != 127u) abort();
  if (!success && (r0f_host_result[151] || !r0f_host_result[252])) abort();
  if (fwrite((const void *)r0f_host_result, 1u, 256u, stdout) != 256u) abort();
  if (fwrite(r0f_capture, 1u, 10880u, stdout) != 10880u) abort();
  return 0;
}
