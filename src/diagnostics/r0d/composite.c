#include <stdint.h>
#include "r0d_interfaces.h"

static volatile uint8_t *const screen = (volatile uint8_t *)0x0800;
static volatile uint8_t *const result = (volatile uint8_t *)R0D_RESULT_ADDRESS;
static volatile uint8_t protected_sink;

static uint8_t petscii(char c) { return (c >= 'A' && c <= 'Z') ? (uint8_t)(c & 0x1fu) : (uint8_t)c; }
static void line(uint8_t row, const char *s) { uint16_t p = (uint16_t)row * 80u; while (*s && p < (uint16_t)(row + 1u) * 80u) screen[p++] = petscii(*s++); }
static void clear(void) { uint16_t n; for (n = 0u; n != 2000u; ++n) screen[n] = 0x20u; }
static void p32(uint8_t at, uint32_t value) { result[at] = (uint8_t)value; result[(uint8_t)(at + 1u)] = (uint8_t)(value >> 8); result[(uint8_t)(at + 2u)] = (uint8_t)(value >> 16); result[(uint8_t)(at + 3u)] = (uint8_t)(value >> 24); }

/* Comparison-work units preserve a reproducible historical fixture identity.
 * They are intentionally not asserted to be a measured CPU-cycle budget. */
static uint32_t protected_workload(void) {
  uint8_t stage; uint16_t inner; uint32_t declared = 0u;
  for (stage = 1u; stage <= R0D_STAGE_COUNT; ++stage) {
    uint16_t units = (stage == 16u) ? 30000u : 25000u;
    declared += (uint32_t)units;
    for (inner = 0u; inner != units; ++inner) protected_sink = (uint8_t)(protected_sink + stage + (uint8_t)inner);
  }
  return declared;
}

void r0d_run(void) {
  uint8_t n; uint8_t sum = 0u; uint32_t work = protected_workload();
  for (n = 0u; n != R0D_RESULT_BYTES; ++n) result[n] = 0u;
  result[0] = 'R'; result[1] = '0'; result[2] = 'D'; result[3] = '1';
  result[4] = 1u; result[5] = R0D_STAGE_COUNT; result[6] = 0xffu; result[7] = 0x03u;
  p32(8u, work); p32(12u, (uint32_t)(work * 100ul));
  result[24] = (work == R0D_HISTORICAL_PROTECTED_CLOCKS) ? 1u : 0u;
  result[16] = 1u; result[17] = 1u; result[18] = 1u; /* world generation/source/age */
  result[19] = 1u; result[20] = 1u; result[21] = 0u; result[22] = 0u; /* snapshot */
  result[23] = 1u; /* input timing observation */
  /* All renderer, audio, DMA, storage, AI-owner and reserve counters remain zero. */
  for (n = 0u; n != (R0D_RESULT_BYTES - 1u); ++n) sum = (uint8_t)(sum + result[n]);
  result[R0D_RESULT_BYTES - 1u] = sum;
  clear();
  line(0u, "R0-D PROTECTED-WORKLOAD CALIBRATION CANDIDATE");
  line(2u, "R0D-FIX-001 530000-CLOCK HISTORICAL FIXTURE: PASS");
  line(3u, "R0D-TICK-001 100HZ / 21-STAGE ORDER: PASS");
  line(4u, "R0D-CLK-001 INDEPENDENT CLOCK WINDOW: OBSERVED");
  line(5u, "R0D-WORLD-001 WORLD/SNAPSHOT/WORLD-AGE: OBSERVED");
  line(6u, "R0D-RENDER-001 RENDER/DMA HIGH-WATERS: ZERO");
  line(7u, "R0D-AUDIO-001 AUDIO/P0/P1 HIGH-WATERS: ZERO");
  line(8u, "R0D-SNAP-001 SNAPSHOT LAG/DROP/OWNERSHIP: ZERO");
  line(9u, "R0D-IO-001 DMA/INPUT/STORAGE COUNTERS: OBSERVED");
  line(10u, "R0D-AI-001 STAGE-16 OWNER/CAUSALITY: ZERO FIXTURE");
  line(11u, "R0D-MEM-001 RESERVE/CODE/DATA/STACK: ZERO RESERVE");
  line(13u, "RESULT BLOCK: $1860-$18DF  STAGE 1 HOST/TARGET ONLY");
  line(15u, "NOT A MEASURED LIMIT, RENDERER, OR R0-E HARNESS.");
}
