#include <stdint.h>
#include "r0f_interfaces.h"

#ifdef R0F_HOST_TEST
extern volatile uint8_t r0f_host_screen[2000], r0f_host_result[256];
#define screen r0f_host_screen
#define result r0f_host_result
#else
static volatile uint8_t *const screen = (volatile uint8_t *)0x0800;
static volatile uint8_t *const result = (volatile uint8_t *)R0F_RESULT_ADDRESS;
#endif
extern uint8_t r0f_clock_begin(void), r0f_clock_now(uint32_t *value);
extern uint8_t r0f_frame_read(void), r0f_video_read(void), r0f_speed_read(void);
extern void r0f_clock_stop(void), r0f_fixture_reset(void);
extern uint8_t r0f_fixture_tick(uint8_t flags, uint16_t tick);

typedef struct { uint16_t duration, lateness; } tick_sample;
struct capture {
  tick_sample ticks[R0F_SWEEP_CASES][R0F_SWEEP_SAMPLES];
  uint32_t spans[R0F_SWEEP_CASES][R0F_SWEEP_PHASES];
} r0f_capture;
_Static_assert(sizeof(r0f_capture) == R0F_RAW_CAPTURE_BYTES, "capture layout");
static uint16_t sorted[R0F_SWEEP_SAMPLES];
static uint32_t last_clock;
static uint8_t fault, high_water;
static const uint8_t case_flags[5] = {0u, 1u, 2u, 4u, 8u};

static void p16(uint8_t at, uint16_t v) { result[at] = (uint8_t)v; result[(uint8_t)(at+1u)] = (uint8_t)(v >> 8u); }
static void p32(uint8_t at, uint32_t v) { p16(at, (uint16_t)v); p16((uint8_t)(at+2u), (uint16_t)(v >> 16u)); }
static uint8_t now(uint32_t *v) {
  if (!r0f_clock_now(v)) { fault = 2u; return 0u; }
  if ((uint32_t)(*v - last_clock) > 1000000ul) { fault = 3u; return 0u; }
  last_clock = *v;
  return 1u;
}
static uint8_t wait_until(uint32_t target, uint32_t *v) {
  uint16_t tries;
  for (tries = 0u; tries != R0F_POLL_LIMIT; ++tries) {
    if (!now(v)) return 0u;
    if ((uint32_t)(*v - target) < 0x80000000ul) return 1u;
  }
  fault = 4u; return 0u;
}
static uint8_t frame_edge(uint32_t *v) {
  uint8_t before = r0f_frame_read();
  uint16_t tries;
  for (tries = 0u; tries != R0F_POLL_LIMIT; ++tries) {
    uint8_t after;
    if (!now(v)) return 0u;
    after = r0f_frame_read();
    if (after != before) {
      if ((uint8_t)(after - before) != 1u) { fault = 5u; return 0u; }
      return now(v);
    }
  }
  fault = 6u; return 0u;
}
static uint8_t calibrate(uint32_t *counts) {
  uint32_t first, end = 0u;
  uint8_t frame;
  if (!frame_edge(&first)) return 0u;
  for (frame = 0u; frame != R0F_CALIBRATION_FRAMES; ++frame)
    if (!frame_edge(&end)) return 0u;
  *counts = end - first;
  /* Acquisition/encoding guard, not a production performance threshold. */
  if (*counts < 8000ul * R0F_CALIBRATION_FRAMES ||
      *counts > 60000ul * R0F_CALIBRATION_FRAMES) { fault = 7u; return 0u; }
  return 1u;
}
static uint8_t sweep_case(uint8_t id, uint32_t frame_counts) {
  uint8_t phase;
  uint16_t index = 0u, mask = 0u;
  for (phase = 0u; phase != R0F_SWEEP_PHASES; ++phase) {
    uint32_t edge, release, start, end = 0u, origin;
    uint16_t tick;
    r0f_fixture_reset();
    if (!frame_edge(&edge)) return 0u;
    release = edge + (frame_counts * phase) / R0F_SWEEP_PHASES;
    origin = release;
    for (tick = 1u; tick <= R0F_SWEEP_TICKS; ++tick) {
      uint32_t duration, late;
      uint8_t ready;
      if (!wait_until(release, &start)) return 0u;
      ready = r0f_fixture_tick(case_flags[id], tick);
      if (!now(&end)) return 0u;
      if (ready > high_water) high_water = ready;
      duration = end - start;
      late = end - (release + R0F_PERIOD_COUNTS);
      if (late >= 0x80000000ul) late = 0u;
      if (duration > 65535ul || late > 65535ul) { fault = 8u; return 0u; }
      r0f_capture.ticks[id][index].duration = (uint16_t)duration;
      r0f_capture.ticks[id][index].lateness = (uint16_t)late;
      ++index;
      release += R0F_PERIOD_COUNTS;
    }
    r0f_capture.spans[id][phase] = end - origin;
    mask |= (uint16_t)(1u << phase);
    p16((uint8_t)(170u + id * 16u), mask);
  }
  return 1u;
}
static void summarize(uint8_t id) {
  uint16_t i, j, late = 0u, misses = 0u;
  uint32_t span = 0u;
  uint8_t at = (uint8_t)(160u + id * 16u);
  for (i = 0u; i != R0F_SWEEP_SAMPLES; ++i) {
    tick_sample sample = r0f_capture.ticks[id][i];
    sorted[i] = sample.duration;
    if (sample.lateness) ++misses;
    if (sample.lateness > late) late = sample.lateness;
  }
  for (i = 1u; i != R0F_SWEEP_SAMPLES; ++i) {
    uint16_t v = sorted[i];
    j = i;
    while (j && sorted[j-1u] > v) { sorted[j] = sorted[j-1u]; --j; }
    sorted[j] = v;
  }
  for (i = 0u; i != R0F_SWEEP_PHASES; ++i)
    if (r0f_capture.spans[id][i] > span) span = r0f_capture.spans[id][i];
  p16(at, sorted[(R0F_SWEEP_SAMPLES+1u)/2u-1u]);
  p16((uint8_t)(at+2u), sorted[(R0F_SWEEP_SAMPLES*95u+99u)/100u-1u]);
  p16((uint8_t)(at+4u), sorted[R0F_SWEEP_SAMPLES-1u]);
  p16((uint8_t)(at+6u), late); p16((uint8_t)(at+8u), misses);
  p32((uint8_t)(at+12u), span);
}
static void text(uint8_t row, const char *s) {
  uint16_t at = (uint16_t)row * 80u;
  while (*s) { uint8_t c = (uint8_t)*s++; screen[at++] = (c >= 'A' && c <= 'Z') ? (uint8_t)(c & 31u) : c; }
}
static void hex(uint8_t row, uint8_t col, uint32_t v, uint8_t digits) {
  uint16_t at = (uint16_t)row * 80u + col + digits;
  while (digits--) { uint8_t n = (uint8_t)(v & 15u); screen[--at] = n < 10u ? (uint8_t)('0'+n) : (uint8_t)(1u+n-10u); v >>= 4u; }
}
static uint16_t r16(uint8_t at) { return (uint16_t)((uint16_t)result[at] | (uint16_t)((uint16_t)result[(uint8_t)(at+1u)] << 8u)); }
static uint32_t r32(uint8_t at) { return (uint32_t)r16(at) | (uint32_t)r16((uint8_t)(at+2u)) << 16u; }
void r0f_timing_display(void) {
  uint16_t i;
  uint8_t id;
  for (i = 0u; i != 2000u; ++i) screen[i] = 32u;
#ifdef R0F_RAW_CAPTURE
  text(0u, "R0-F CIA COUNT SWEEP - F65R0F5");
  text(23u, "C RETURNS TO RAW CAPTURE PAGES");
#else
  text(0u, "R0-F CIA COUNT SWEEP - F65R0F4");
#endif
  text(2u, result[7] == 127u ? "INHERITED FUNCTIONAL FIXTURE: PASS" : "FUNCTIONAL FIXTURE: FAIL");
  text(3u, fault ? "ACQUISITION: FAILED - DO NOT USE TIMING" : "ACQUISITION: COMPLETE - NOT R0-F ACCEPTANCE");
  text(4u, "UNITS: RAW CIA COUNTS. ALL NUMBERS BELOW HEX.");
  text(5u, "CASE    P50  P95  MAX  LATE MISS MASK SPAN33");
  for (id = 0u; id != 5u; ++id) {
    uint8_t row = (uint8_t)(6u+id), at = (uint8_t)(160u+id*16u), n;
    static const char *const names[5] = {"NORMAL", "LAG", "SHED", "FAULT", "PRESS"};
    text(row, names[id]);
    for (n = 0u; n != 6u; ++n) hex(row, (uint8_t)(8u+n*5u), r16((uint8_t)(at+n*2u)), 4u);
    hex(row, 38u, r32((uint8_t)(at+12u)), 8u);
  }
  text(12u, "16-FRAME COUNTS BEFORE/AFTER:"); hex(12u, 29u, r32(152u), 8u); hex(12u, 39u, r32(240u), 8u);
  text(13u, "PERIOD=10000 COUNTS; 16 PHASES X 33 TICKS X 5 CASES");
  text(14u, "NO CALIBRATED HZ/US, CPU CYCLES, INPUT/AUDIO LATENCY");
  text(15u, "IRQ MASKED. DMA NOT RUN. RESET REQUIRED AFTER TEST.");
  text(16u, "FAULT / READY HIGH-WATER / VIDEO / SPEED:");
  hex(16u, 41u, fault, 2u); hex(16u, 45u, high_water, 2u);
  hex(16u, 49u, result[158], 2u); hex(16u, 53u, result[159], 2u);
  text(18u, "RAW CAPTURE ADDRESS/LENGTH:"); hex(18u, 28u, r16(248u), 4u); hex(18u, 34u, r16(250u), 4u);
}
void r0f_timing_run(void) {
  uint16_t i;
  uint8_t id, sum = 0u;
  uint32_t before = 0u, after = 0u;
  fault = 0u; high_water = 0u;
  for (i = 144u; i != 256u; ++i) result[i] = 0u;
  for (i = 0u; i != sizeof(r0f_capture); ++i) ((uint8_t *)&r0f_capture)[i] = 0u;
  result[4] = 2u;
  result[144]='C'; result[145]='T'; result[146]=1u; result[147]=16u;
  result[148]=33u; result[149]=5u; result[150]=16u;
  p16(156u, R0F_CALIBRATION_FRAMES); result[158]=r0f_video_read(); result[159]=r0f_speed_read();
  p32(244u, R0F_PERIOD_COUNTS); p16(250u, R0F_RAW_CAPTURE_BYTES);
#ifdef R0F_HOST_TEST
  p16(248u, 0x4000u); /* Native address is not a target address. */
#else
  p16(248u, (uint16_t)(uintptr_t)&r0f_capture);
#endif
  text(20u, "CIA TIMING SWEEP RUNNING - DO NOT PRESS RESTORE");
  if (!r0f_clock_begin()) fault = 1u;
  else if (!r0f_clock_now(&last_clock)) fault = 2u;
  else if (calibrate(&before)) {
    p32(152u, before);
    for (id = 0u; id != R0F_SWEEP_CASES; ++id) {
      if (!sweep_case(id, before / R0F_CALIBRATION_FRAMES)) break;
      summarize(id);
    }
    if (!fault && calibrate(&after)) p32(240u, after);
  }
  r0f_clock_stop();
  result[151] = fault ? 0u : 127u; result[252] = fault; result[253] = high_water;
  for (i = 0u; i != 255u; ++i) sum = (uint8_t)(sum + result[i]);
  result[255] = sum;
  r0f_timing_display();
}
#ifdef R0F_RAW_CAPTURE
uint8_t r0f_capture_byte(uint16_t index) {
  if (index < R0F_RESULT_BYTES) return result[index];
  index = (uint16_t)(index - R0F_RESULT_BYTES);
  return index < R0F_RAW_CAPTURE_BYTES ? ((const uint8_t *)&r0f_capture)[index] : 0u;
}
#endif
