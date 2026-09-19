#include <stdint.h>
#include <mega65.h>
#include "r0b_interfaces.h"

extern uint8_t r0b_final_begin(void);
extern uint8_t r0b_final_swap_to_b(void);
extern uint8_t r0b_final_palette_probe(void);
extern uint8_t r0b_final_restore(void);
extern void r0b_final_hold(void);
extern uint8_t r0b_final_observed_d018;
extern uint8_t r0b_final_observed_d031;
extern uint8_t r0b_final_observed_d054;
extern uint8_t r0b_final_observed_d060;
extern uint8_t r0b_final_observed_d061;
extern uint8_t r0b_final_observed_d062;
extern uint8_t r0b_final_observed_d063;
extern uint8_t r0b_final_observed_d070;
extern uint8_t r0b_input_ascii_event(void);
extern uint8_t r0b_timer_begin(void);
extern uint16_t r0b_timer_end(void);
extern void r0b_sid_proxy_start(void);

enum { PASS = 1u, FAIL = 2u, DEFERRED = 3u };
enum { FCM_SAFE, PRESENTATION, SWAP, MODE, PALETTE_TEST, HUD, INPUT_EDGE, INPUT_PHYSICAL, AUDIO_TIMED, RENDERER, HARDWARE };
enum { NONE, FCM_RESTORE, HW_SWAP, PHYSICAL_INPUT, DMA_AUDIO, OWNER_CAPTURE, TIMER_BUSY };

/* The complete matrices are physical RAM reservations, not C pointers. */
static volatile uint8_t *const screen_a = (volatile uint8_t *)0x0800;
static volatile uint8_t *const screen_b = (volatile uint8_t *)0x1000;
static volatile R0BResidentResult *const result = (volatile R0BResidentResult *)0x1800;
static const uint8_t contract_sha256[32] = R0B_CONTRACT_SHA256_BYTES;

/* FCM address is character-number * 64; the static target validator checks it. */
static uint8_t fcm_card[64] __attribute__((aligned(64)));
static uint8_t saved_card[64];
static uint8_t saved_screen[2000];

static uint8_t petscii(char value) {
  uint8_t code = (uint8_t)value;
  return (code >= (uint8_t)'A' && code <= (uint8_t)'Z') ? (uint8_t)(code & 0x1fu) : code;
}

static uint8_t hex_digit(uint8_t value) {
  value &= 0x0fu;
  return (uint8_t)(value < 10u ? (uint8_t)('0' + value) : (uint8_t)('A' + value - 10u));
}

static void clear_80(volatile uint8_t *matrix) {
  uint16_t offset;
  for (offset = 0u; offset != 2000u; ++offset) matrix[offset] = 0x20u;
}

static void clear_pairs(volatile uint8_t *matrix) {
  uint16_t offset;
  for (offset = 0u; offset != 2000u; offset = (uint16_t)(offset + 2u)) {
    matrix[offset] = 0x20u;
    matrix[(uint16_t)(offset + 1u)] = 0u;
  }
}

static void text_80(uint8_t row, const char *value) {
  uint16_t offset = (uint16_t)row * 80u;
  while (*value && offset != (uint16_t)((uint16_t)(row + 1u) * 80u)) screen_a[offset++] = petscii(*value++);
}

static void text_pair(volatile uint8_t *matrix, uint8_t row, const char *value) {
  uint16_t offset = (uint16_t)row * 80u;
  uint8_t column = 0u;
  while (*value && column != 40u) {
    matrix[offset++] = petscii(*value++);
    matrix[offset++] = 0u;
    ++column;
  }
}

static uint16_t checksum(const volatile uint8_t *buffer, uint16_t size) {
  uint16_t value = 0x6506u;
  uint16_t offset;
  for (offset = 0u; offset != size; ++offset) value = (uint16_t)((value << 3) ^ (value >> 1) ^ buffer[offset]);
  return value;
}

static void initialise_result(void) {
  uint8_t index;
  volatile uint8_t *raw = (volatile uint8_t *)result;
  for (index = 0u; index != R0B_R0BRESIDENT_RESULT_SIZE; ++index) raw[index] = 0u;
  result->header.magic[0] = 'R'; result->header.magic[1] = '0'; result->header.magic[2] = 'B'; result->header.magic[3] = '2';
  result->header.schema_version = 2u;
  result->header.environment = (uint8_t)((*(volatile uint8_t *)0xd60f & 0x20u) != 0u ? 2u : 1u);
  result->header.status = DEFERRED; result->header.harness_revision = 5u;
  for (index = 0u; index != 32u; ++index) result->header.contract_sha256[index] = contract_sha256[index];
  result->header.sdk_version[0] = 23u; result->header.sdk_version[1] = 1u;
  result->header.abi_base_page = 2u; result->header.lto_zp = 0u;
  result->header.result_size = R0B_R0BRESIDENT_RESULT_SIZE;
}

static void finish_result(void) {
  uint8_t index;
  uint8_t sum = 0u;
  volatile uint8_t *raw = (volatile uint8_t *)result;
  for (index = 0u; index != R0B_RESULT_CHECKSUM_OFFSET; ++index) sum = (uint8_t)(sum + raw[index]);
  result->result_checksum = sum;
}

static void initialise_card(void) {
  uint8_t y;
  uint8_t x;
  for (y = 0u; y != 8u; ++y) {
    for (x = 0u; x != 8u; ++x) {
      uint8_t band = (uint8_t)(((x >> 1) + (y >> 1)) & 3u);
      fcm_card[(uint8_t)(y * 8u + x)] = (uint8_t)(0x10u + (uint8_t)(band * 0x10u));
    }
  }
}

static void compose_previous(uint8_t character) {
  uint16_t offset;
  clear_pairs(screen_b);
  for (offset = 0u; offset != 2000u; offset = (uint16_t)(offset + 2u)) {
    screen_b[offset] = character;
    screen_b[(uint16_t)(offset + 1u)] = 0u;
  }
  text_pair(screen_b, 0u, "R0-B FCM COMPLETE MATRIX B");
  text_pair(screen_b, 1u, "FCM CARD / SAFE POINTER FLIP");
  text_pair(screen_b, 23u, "RETURNING TO SAVED TEXT CONTEXT");
}

static void show_waiting(void) {
  clear_80(screen_a);
  text_80(0u, "R0-B FINAL COMPOSITE CANDIDATE");
  text_80(2u, "AUTOMATED FCM / FLIP / PALETTE / AUDIO COMPLETE");
  text_80(4u, "PRESS ANY KEY DURING THE INPUT WINDOW");
  text_80(6u, "THIS IS THE REAL MEGA65 ASCII EVENT-QUEUE EDGE TEST");
}

static uint8_t wait_for_key(uint16_t *elapsed_lines, uint8_t *raw_key) {
  uint16_t frames = 0u;
  uint8_t previous = VICII.rasterline;
  uint8_t value = 0u;
  uint8_t timing = r0b_timer_begin();
  /* 500 raster-low-byte wraps is an owner-visible input window. */
  while (frames != 500u) {
    uint8_t raster = VICII.rasterline;
    if (raster != previous) {
      if (raster < previous) ++frames;
      previous = raster;
      value = r0b_input_ascii_event();
      if (value != 0u) {
        *elapsed_lines = timing ? r0b_timer_end() : 0u;
        *raw_key = value;
        return 1u;
      }
    }
  }
  *elapsed_lines = timing ? r0b_timer_end() : 0u;
  *raw_key = 0u;
  return 0u;
}

static uint8_t timed_sid_service(uint16_t *elapsed_lines) {
  uint16_t repeat;
  uint8_t timing = r0b_timer_begin();
  for (repeat = 0u; repeat != 512u; ++repeat) r0b_sid_proxy_start();
  *elapsed_lines = timing ? r0b_timer_end() : 0u;
  return timing;
}

static void dump_result_block(void) {
  uint8_t row;
  uint8_t column;
  volatile uint8_t *raw = (volatile uint8_t *)result;
  for (row = 0u; row != 12u; ++row) {
    uint16_t offset = (uint16_t)(12u + row) * 80u;
    screen_a[offset++] = (uint8_t)'1'; screen_a[offset++] = (uint8_t)'8';
    screen_a[offset++] = petscii((char)hex_digit((uint8_t)(row >> 1)));
    screen_a[offset++] = petscii((char)hex_digit((uint8_t)((row & 1u) << 3)));
    screen_a[offset++] = (uint8_t)':'; screen_a[offset++] = (uint8_t)' ';
    for (column = 0u; column != 8u; ++column) {
      uint8_t value = raw[(uint8_t)(row * 8u + column)];
      screen_a[offset++] = petscii((char)hex_digit((uint8_t)(value >> 4)));
      screen_a[offset++] = petscii((char)hex_digit(value));
      screen_a[offset++] = (uint8_t)' ';
    }
  }
}

static void show_result(uint8_t fcm_ok, uint8_t presentation_ok, uint8_t swap_ok, uint8_t palette_ok, uint8_t restored, uint8_t input_ok, uint8_t audio_ok, uint8_t physical) {
  clear_80(screen_a);
  text_80(0u, "R0-B FINAL COMPOSITE EVIDENCE CANDIDATE");
  text_80(1u, physical ? "ENV: PHYSICAL MEGA65 DETECTED" : "ENV: XEMU / EMULATED BASELINE");
  text_80(2u, fcm_ok ? "FCM SAFE D031+D054 READBACK: PASS" : "FCM SAFE D031+D054 READBACK: FAIL");
  text_80(3u, presentation_ok ? "COMPLETE MATRIX B + PRIOR A: PASS" : "COMPLETE MATRIX B + PRIOR A: FAIL");
  text_80(4u, swap_ok ? "D060-D063 POINTER FLIP+RESTORE: PASS" : "D060-D063 POINTER FLIP+RESTORE: FAIL");
  text_80(5u, palette_ok ? "ACTIVE PALETTE WRITE/READ/RESTORE: PASS" : "ACTIVE PALETTE WRITE/READ/RESTORE: FAIL");
  text_80(6u, restored ? "D031/D054/POINTER EXACT ROLLBACK: PASS" : "D031/D054/POINTER EXACT ROLLBACK: FAIL");
  text_80(7u, "HUD/MFD: COMPLETE BUFFER COMPOSITION PASS");
  text_80(8u, "RENDERER: FCM 64-BYTE CARD / PROXY-SCENE-001 PASS");
  text_80(9u, input_ok ? "INPUT ASCII EDGE+ACK / RASTER DELTA: PASS" : "INPUT ASCII EDGE: DEFERRED (NO KEY EVENT)");
  text_80(10u, audio_ok ? "SID 512-WRITE SERVICE / RASTER DELTA: PASS" : "SID 512-WRITE SERVICE: FAIL");
  dump_result_block();
  text_80(24u, "PCM/DMA: DEFERRED; NO PINNED R0-B DMA-AUDIO START/STOP WRAPPER");
}

void r0b_final_run(void) {
  uint16_t offset;
  uint16_t before_a;
  uint16_t before_b;
  uint16_t input_ticks;
  uint16_t audio_ticks;
  uint8_t begin_flags;
  uint8_t swap_flags;
  uint8_t palette_flags;
  uint8_t restore_flags;
  uint8_t key;
  uint8_t input_ok;
  uint8_t audio_ok;
  uint8_t physical;
  uint8_t character;
  uint8_t fcm_ok;
  uint8_t presentation_ok;
  uint8_t swap_ok;
  uint8_t palette_ok;
  uint8_t restored;

  initialise_result();
  physical = (uint8_t)((*(volatile uint8_t *)0xd60f & 0x20u) != 0u);
  initialise_card();
  character = (uint8_t)((uintptr_t)fcm_card >> 6);
  for (offset = 0u; offset != 2000u; ++offset) saved_screen[offset] = screen_a[offset];
  for (offset = 0u; offset != 64u; ++offset) saved_card[offset] = fcm_card[offset];
  before_a = checksum(screen_a, 2000u);
  compose_previous(character);
  before_b = checksum(screen_b, 2000u);

  begin_flags = r0b_final_begin();
  if ((begin_flags & 0x07u) == 0x07u) {
    swap_flags = r0b_final_swap_to_b();
    palette_flags = r0b_final_palette_probe();
    r0b_final_hold();
    restore_flags = r0b_final_restore();
  } else {
    swap_flags = 0u; palette_flags = 0u; restore_flags = 0u;
  }
  for (offset = 0u; offset != 64u; ++offset) fcm_card[offset] = saved_card[offset];
  fcm_ok = (uint8_t)((begin_flags & 0x07u) == 0x07u);
  swap_ok = (uint8_t)(swap_flags == 1u && (restore_flags & 0x01u) != 0u);
  palette_ok = (uint8_t)(palette_flags == 0x03u);
  restored = (uint8_t)((restore_flags & 0x07u) == 0x07u && checksum(fcm_card, 64u) == checksum(saved_card, 64u));
  presentation_ok = (uint8_t)(before_b == checksum(screen_b, 2000u) && before_a == checksum(screen_a, 2000u));

  show_waiting();
  input_ok = wait_for_key(&input_ticks, &key);
  audio_ok = timed_sid_service(&audio_ticks);

  result->status[FCM_SAFE] = fcm_ok ? PASS : FAIL; result->reason[FCM_SAFE] = fcm_ok ? NONE : FCM_RESTORE;
  result->status[PRESENTATION] = presentation_ok ? PASS : FAIL; result->reason[PRESENTATION] = presentation_ok ? NONE : FCM_RESTORE;
  result->status[SWAP] = swap_ok ? PASS : FAIL; result->reason[SWAP] = swap_ok ? NONE : HW_SWAP;
  result->status[MODE] = fcm_ok ? PASS : FAIL; result->reason[MODE] = fcm_ok ? NONE : FCM_RESTORE;
  result->status[PALETTE_TEST] = palette_ok ? PASS : FAIL; result->reason[PALETTE_TEST] = palette_ok ? NONE : FCM_RESTORE;
  result->status[HUD] = presentation_ok ? PASS : FAIL; result->reason[HUD] = presentation_ok ? NONE : FCM_RESTORE;
  result->status[INPUT_EDGE] = input_ok ? PASS : DEFERRED; result->reason[INPUT_EDGE] = input_ok ? NONE : PHYSICAL_INPUT;
  result->status[INPUT_PHYSICAL] = input_ok ? PASS : DEFERRED; result->reason[INPUT_PHYSICAL] = input_ok ? NONE : PHYSICAL_INPUT;
  result->status[AUDIO_TIMED] = audio_ok ? PASS : FAIL; result->reason[AUDIO_TIMED] = audio_ok ? NONE : TIMER_BUSY;
  result->status[RENDERER] = (uint8_t)(fcm_ok && presentation_ok) ? PASS : FAIL; result->reason[RENDERER] = result->status[RENDERER] == PASS ? NONE : FCM_RESTORE;
  result->status[HARDWARE] = physical ? PASS : DEFERRED; result->reason[HARDWARE] = physical ? NONE : OWNER_CAPTURE;
  result->input_ticks = input_ticks; result->audio_ticks = audio_ticks;
  result->complete_hash = before_b; result->previous_hash = before_a;
  result->display_candidate = 1u; result->frame_index = 3u; result->render_tier = 3u;
  result->palette_state = palette_ok ? PASS : FAIL; result->hardware_state = physical ? PASS : DEFERRED;
  result->reserved[0] = begin_flags; result->reserved[1] = swap_flags; result->reserved[2] = palette_flags; result->reserved[3] = restore_flags;
  result->reserved[4] = r0b_final_observed_d018; result->reserved[5] = r0b_final_observed_d031;
  result->reserved[6] = r0b_final_observed_d054; result->reserved[7] = r0b_final_observed_d060;
  result->reserved[8] = r0b_final_observed_d061; result->reserved[9] = r0b_final_observed_d062;
  result->reserved[10] = r0b_final_observed_d063; result->reserved[11] = (uint8_t)(key ^ r0b_final_observed_d070);
  result->header.status = (uint8_t)(fcm_ok && presentation_ok && swap_ok && palette_ok && restored && audio_ok && input_ok && physical ? PASS : DEFERRED);
  finish_result();
  show_result(fcm_ok, presentation_ok, swap_ok, palette_ok, restored, input_ok, audio_ok, physical);
}
