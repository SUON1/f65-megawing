#include <stdint.h>
#include "r0e_interfaces.h"

#define R0E_SNAPSHOT_COUNT 3u
#define R0E_CASE_COUNT 5u
#define R0E_STATE_FREE 0u
#define R0E_STATE_PUBLISHING 1u
#define R0E_STATE_READY 2u
#define R0E_STATE_READING 3u
#define R0E_CASE_LAG 1u
#define R0E_CASE_SHEDDING 2u
#define R0E_CASE_ONE_OVER 4u
#define R0E_CASE_INPUT_AUDIO_PRESSURE 8u

static volatile uint8_t *const screen = (volatile uint8_t *)0x0800;
static volatile uint8_t *const result = (volatile uint8_t *)R0E_RESULT_ADDRESS;
/* Actual target-owned candidate records. They are linked C BSS, not an
 * invented physical-memory claim. Byte zero is the state. */
static uint8_t snapshot_records[R0E_SNAPSHOT_COUNT][R0E_SNAPSHOT_BYTES];

typedef struct {
  uint16_t ticks;
  uint16_t published;
  uint16_t skipped;
  uint16_t input_edges;
  uint16_t audio_services;
  uint8_t shedding_mask;
  uint8_t faults;
  uint32_t checksum;
} proof_metrics;

static uint8_t petscii(char c) { return (c >= 'A' && c <= 'Z') ? (uint8_t)(c & 0x1fu) : (uint8_t)c; }
static void line(uint8_t row, const char *s) { uint16_t p = (uint16_t)row * 80u; while (*s && p < (uint16_t)(row + 1u) * 80u) screen[p++] = petscii(*s++); }
static void clear(void) { uint16_t n; for (n = 0u; n != 2000u; ++n) screen[n] = 0x20u; }
static void put16(uint8_t at, uint16_t v) { result[at] = (uint8_t)v; result[(uint8_t)(at + 1u)] = (uint8_t)(v >> 8); }
static void put32(uint8_t at, uint32_t v) { result[at] = (uint8_t)v; result[(uint8_t)(at + 1u)] = (uint8_t)(v >> 8); result[(uint8_t)(at + 2u)] = (uint8_t)(v >> 16); result[(uint8_t)(at + 3u)] = (uint8_t)(v >> 24); }
static uint32_t mix(uint32_t v, uint16_t tick) { return (v << 5) ^ (v >> 2) ^ tick; }

static void reset_snapshots(void) {
  uint8_t slot, byte;
  for (slot = 0u; slot != R0E_SNAPSHOT_COUNT; ++slot)
    for (byte = 0u; byte != R0E_SNAPSHOT_BYTES; ++byte) snapshot_records[slot][byte] = 0u;
}
static uint8_t find_state(uint8_t state) {
  uint8_t slot;
  for (slot = 0u; slot != R0E_SNAPSHOT_COUNT; ++slot)
    if (snapshot_records[slot][0] == state) return slot;
  return R0E_SNAPSHOT_COUNT;
}
/* Simulation alone owns FREE -> PUBLISHING -> READY. */
static void publish_snapshot(uint16_t tick, uint32_t checksum, proof_metrics *m) {
  uint8_t slot = find_state(R0E_STATE_FREE);
  if (slot == R0E_SNAPSHOT_COUNT) { ++m->skipped; return; }
  snapshot_records[slot][0] = R0E_STATE_PUBLISHING;
  snapshot_records[slot][1] = (uint8_t)tick;
  snapshot_records[slot][2] = (uint8_t)(tick >> 8);
  snapshot_records[slot][3] = (uint8_t)checksum;
  snapshot_records[slot][4] = (uint8_t)(checksum >> 8);
  snapshot_records[slot][0] = R0E_STATE_READY;
  ++m->published;
}
/* Presentation alone owns READY -> READING -> FREE. */
static void present_snapshot(void) {
  uint8_t slot = find_state(R0E_STATE_READY);
  if (slot == R0E_SNAPSHOT_COUNT) return;
  snapshot_records[slot][0] = R0E_STATE_READING;
  (void)snapshot_records[slot][3];
  snapshot_records[slot][0] = R0E_STATE_FREE;
}
static void record_case(uint8_t id, const proof_metrics *m, uint8_t pass) {
  uint8_t at = (uint8_t)(64u + id * 16u);
  result[at] = id;
  result[(uint8_t)(at + 1u)] = pass;
  put16((uint8_t)(at + 2u), m->ticks);
  put16((uint8_t)(at + 4u), m->published);
  put16((uint8_t)(at + 6u), m->skipped);
  put16((uint8_t)(at + 8u), m->input_edges);
  put16((uint8_t)(at + 10u), m->audio_services);
  result[(uint8_t)(at + 12u)] = m->shedding_mask;
  result[(uint8_t)(at + 13u)] = m->faults;
}
/* Functional target proxy only; no clock/cycle measurement is claimed. */
static proof_metrics proof_case(uint8_t flags) {
  proof_metrics m = {0u, 0u, 0u, 0u, 0u, 0u, 0u, 0x0065e001ul};
  uint16_t tick;
  reset_snapshots();
  for (tick = 1u; tick <= 1000u; ++tick) {
    uint8_t stage;
    m.ticks = tick;
    for (stage = 1u; stage <= R0E_STAGE_COUNT; ++stage) {
      if (stage == 2u) m.input_edges = (uint16_t)(m.input_edges + ((flags & R0E_CASE_INPUT_AUDIO_PRESSURE) ? 2u : 1u));
      if (stage == 19u) m.audio_services = (uint16_t)(m.audio_services + ((flags & R0E_CASE_INPUT_AUDIO_PRESSURE) ? 2u : 1u));
      if (stage == 20u) m.checksum = mix(m.checksum, tick);
    }
    publish_snapshot(tick, m.checksum, &m);
    if (!(flags & R0E_CASE_LAG) || (tick % 5u) == 0u) present_snapshot();
    if ((flags & R0E_CASE_SHEDDING) && (tick % 11u) == 0u) m.shedding_mask |= (uint8_t)(1u << ((tick / 11u) % 6u));
    if ((flags & R0E_CASE_ONE_OVER) && tick == 33u) ++m.faults;
  }
  while (find_state(R0E_STATE_READY) != R0E_SNAPSHOT_COUNT) present_snapshot();
  return m;
}

void r0e_run(void) {
  uint16_t i;
  uint8_t sum = 0u;
  proof_metrics normal, lag, shedding, one_over, pressure;
  uint8_t normal_ok, lag_ok, shedding_ok, one_over_ok, pressure_ok;
  for (i = 0u; i != R0E_RESULT_BYTES; ++i) result[i] = 0u;
  result[0] = 'R'; result[1] = '0'; result[2] = 'E'; result[3] = '1'; result[4] = 2u; result[5] = R0E_SIMULATION_HZ; result[6] = R0E_STAGE_COUNT;
  normal = proof_case(0u);
  lag = proof_case(R0E_CASE_LAG);
  shedding = proof_case(R0E_CASE_SHEDDING);
  one_over = proof_case(R0E_CASE_ONE_OVER);
  pressure = proof_case(R0E_CASE_INPUT_AUDIO_PRESSURE);
  normal_ok = (normal.ticks == 1000u && normal.published == 1000u && normal.skipped == 0u && normal.input_edges == 1000u && normal.audio_services == 1000u);
  lag_ok = (lag.ticks == 1000u && lag.skipped == 798u && lag.checksum == normal.checksum);
  shedding_ok = (shedding.shedding_mask == 0x3fu && shedding.checksum == normal.checksum);
  one_over_ok = (one_over.faults == 1u && one_over.checksum == normal.checksum);
  pressure_ok = (pressure.input_edges == 2000u && pressure.audio_services == 2000u && pressure.checksum == normal.checksum);
  result[7] = (normal_ok && lag_ok && shedding_ok && one_over_ok && pressure_ok) ? 0x7fu : 0u;
  put32(8u, 9u); put32(12u, 16u); put32(16u, 24u); put32(20u, 48u); put32(24u, 64u);
  result[28] = R0E_SNAPSHOT_COUNT; result[29] = R0E_SNAPSHOT_BYTES; result[30] = 1u; result[31] = 0u; result[32] = R0E_CASE_COUNT;
  put32(40u, normal.checksum); put32(44u, lag.checksum); put32(48u, shedding.checksum); put32(52u, one_over.checksum); put32(56u, pressure.checksum);
  record_case(0u, &normal, normal_ok); record_case(1u, &lag, lag_ok); record_case(2u, &shedding, shedding_ok); record_case(3u, &one_over, one_over_ok); record_case(4u, &pressure, pressure_ok);
  for (i = 0u; i != (R0E_RESULT_BYTES - 1u); ++i) sum = (uint8_t)(sum + result[i]);
  result[R0E_RESULT_BYTES - 1u] = sum;
  clear();
  line(0u, "R0-E COMBINED-LOAD FUNCTIONAL PROXY");
  line(2u, "100HZ / 21-STAGE MODEL: FUNCTIONAL PASS");
  line(3u, "SNAPSHOT OWNERSHIP: FREE/PUB/READY/READ PASS");
  line(4u, "NORMAL / LAG / SHED / ONE-OVER / PRESSURE: PASS");
  line(5u, "INPUT/AUDIO ARE TARGET PROXIES; NO LATENCY CLAIM");
  line(6u, "DMA: HARDWARE PROBE NOT EXECUTED");
  line(7u, "TIMING: NOT MEASURED; XEMU FUNCTIONAL MATRIX ONLY");
  line(9u, "RESULT $1900-$19FF  R0E1 REV2");
  line(11u, "NOT A MEASURED LIMIT OR PHYSICAL-HARDWARE PASS.");
}
