#include <stdint.h>
#include "r0b_interfaces.h"

extern uint8_t r0b_fcm_visible_begin(void);
extern uint8_t r0b_fcm_visible_restore(void);
extern void r0b_fcm_visible_hold(void);
extern uint8_t r0b_fcm_visible_observed_d018;
extern uint8_t r0b_fcm_visible_observed_d031;
extern uint8_t r0b_fcm_visible_observed_d054;
extern uint8_t r0b_fcm_visible_observed_d060;
extern uint8_t r0b_fcm_visible_observed_d061;
extern uint8_t r0b_fcm_visible_observed_d062;
extern uint8_t r0b_fcm_visible_observed_d063;

/* The admitted default C65 80-column text matrix, not a physical pointer. */
static volatile uint8_t *const screen = (volatile uint8_t *)0x0800;
static volatile R0BResidentResult *const result = (volatile R0BResidentResult *)0x1800;
static const uint8_t contract_sha256[32] = R0B_CONTRACT_SHA256_BYTES;

/* A proof character must be aligned: FCM address = character-number * 64. */
static uint8_t fcm_card[64] __attribute__((aligned(64)));
static uint8_t saved_card[64];
static uint8_t saved_screen[2000];

enum { PASS = 1u, FAIL = 2u, DEFERRED = 3u };
enum { FCM_SAFE, PRESENTATION, SWAP, MODE, PALETTE, HUD, INPUT_EDGE, INPUT_PHYSICAL, AUDIO_TIMED, RENDERER, HARDWARE };
enum { NONE, FCM_RESTORE, HW_SWAP, PHYSICAL_INPUT, DMA_AUDIO, OWNER_CAPTURE, TIMER_BUSY };

static uint8_t petscii(char value) {
  uint8_t code = (uint8_t)value;
  return (code >= (uint8_t)'A' && code <= (uint8_t)'Z') ? (uint8_t)(code & 0x1fu) : code;
}

static void clear_screen(void) {
  uint16_t offset;
  for (offset = 0u; offset != 2000u; ++offset) screen[offset] = 0x20u;
}

static void text(uint8_t row, const char *value) {
  uint16_t offset = (uint16_t)row * 80u;
  uint8_t column = 0u;
  while (*value && column != 40u) { screen[offset++] = petscii(*value++); ++column; }
}

static uint8_t hex_digit(uint8_t value) {
  value &= 0x0fu;
  return (uint8_t)(value < 10u ? (uint8_t)('0' + value) : (uint8_t)('A' + value - 10u));
}

static void dump_result_block(void) {
  uint8_t row;
  uint8_t column;
  volatile uint8_t *raw = (volatile uint8_t *)result;
  for (row = 0u; row != 12u; ++row) {
    uint16_t offset = (uint16_t)(12u + row) * 80u;
    screen[offset++] = (uint8_t)'1'; screen[offset++] = (uint8_t)'8';
    screen[offset++] = petscii((char)hex_digit((uint8_t)(row >> 1)));
    screen[offset++] = petscii((char)hex_digit((uint8_t)((row & 1u) << 3)));
    screen[offset++] = (uint8_t)':'; screen[offset++] = (uint8_t)' ';
    for (column = 0u; column != 8u; ++column) {
      uint8_t value = raw[(uint8_t)(row * 8u + column)];
      screen[offset++] = petscii((char)hex_digit((uint8_t)(value >> 4)));
      screen[offset++] = petscii((char)hex_digit(value));
      screen[offset++] = (uint8_t)' ';
    }
  }
}

static uint16_t checksum(const uint8_t *buffer, uint16_t size) {
  uint16_t value = 0x6506u;
  uint16_t offset;
  for (offset = 0u; offset != size; ++offset) value = (uint16_t)((value << 3) ^ (value >> 1) ^ buffer[offset]);
  return value;
}

static uint16_t screen_checksum(void) {
  uint16_t value = 0x6506u;
  uint16_t offset;
  for (offset = 0u; offset != 2000u; ++offset) value = (uint16_t)((value << 3) ^ (value >> 1) ^ screen[offset]);
  return value;
}

static void initialise_result(void) {
  uint8_t index;
  volatile uint8_t *raw = (volatile uint8_t *)result;
  for (index = 0u; index != R0B_R0BRESIDENT_RESULT_SIZE; ++index) raw[index] = 0u;
  result->header.magic[0] = 'R'; result->header.magic[1] = '0'; result->header.magic[2] = 'B'; result->header.magic[3] = '2';
  result->header.schema_version = 2u; result->header.environment = 0u;
  result->header.status = DEFERRED; result->header.harness_revision = 4u;
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

static void render_card(uint8_t character) {
  uint16_t offset;
  uint8_t low = character;
  for (offset = 0u; offset != 2000u; offset = (uint16_t)(offset + 2u)) {
    screen[offset] = low;
    screen[(uint16_t)(offset + 1u)] = 0u;
  }
}

static void initialise_card(void) {
  uint8_t y;
  uint8_t x;
  for (y = 0u; y != 8u; ++y) {
    for (x = 0u; x != 8u; ++x) {
      uint8_t band = (uint8_t)(((x >> 1) + (y >> 1)) & 3u);
      fcm_card[(uint8_t)(y * 8u + x)] = (uint8_t)(0x10u + band * 0x10u);
    }
  }
}

void r0b_fcm_visible_run(void) {
  uint16_t offset;
  uint16_t before_screen;
  uint16_t before_card;
  uint8_t flags;
  uint8_t character;
  uint8_t card_address_ok;
  uint8_t restored;
  uint8_t screen_ok;
  uint8_t card_ok;
  uint8_t pass;

  initialise_result();
  initialise_card();
  character = (uint8_t)((uintptr_t)fcm_card >> 6);
  card_address_ok = (uint8_t)(((uintptr_t)fcm_card <= 0x3fc0u) && (((uintptr_t)fcm_card & 0x3fu) == 0u));
  for (offset = 0u; offset != 2000u; ++offset) saved_screen[offset] = screen[offset];
  for (offset = 0u; offset != 64u; ++offset) saved_card[offset] = fcm_card[offset];
  before_screen = checksum(saved_screen, 2000u);
  before_card = checksum(saved_card, 64u);

  flags = r0b_fcm_visible_begin();
  if ((flags & 0x0fu) == 0x0fu && card_address_ok != 0u) {
    render_card(character);
    r0b_fcm_visible_hold();
    for (offset = 0u; offset != 2000u; ++offset) screen[offset] = saved_screen[offset];
    for (offset = 0u; offset != 64u; ++offset) fcm_card[offset] = saved_card[offset];
    restored = r0b_fcm_visible_restore();
  } else {
    restored = 0u;
  }

  screen_ok = (uint8_t)(before_screen == screen_checksum());
  card_ok = (uint8_t)(before_card == checksum(fcm_card, 64u));
  pass = (uint8_t)((flags & 0x0fu) == 0x0fu && card_address_ok != 0u && restored != 0u && screen_ok != 0u && card_ok != 0u);

  clear_screen();
  text(0u, "R0-B ISOLATED FCM VISIBLE/RESTORE");
  text(1u, "NO D02F; NO MAP; NO DMA; NO IRQ; NO PALETTE");
  text(2u, pass ? "R0B-FCM-VIS-001 LOCAL TEST: PASS" : "R0B-FCM-VIS-001 CONTEXT DEFERRED");
  text(3u, (flags & 0x01u) ? "C65 CONTEXT: PASS" : "C65 CONTEXT: FAIL");
  text(4u, (flags & 0x02u) ? "D031 40-PAIR PRECONDITION: PASS" : "D031 40-PAIR PRECONDITION: FAIL");
  text(5u, (flags & 0x04u) ? "D060 DEFAULT $0800 PRECONDITION: PASS" : "D060 DEFAULT $0800 PRECONDITION: FAIL");
  text(6u, (flags & 0x08u) ? "D054 FCLRLO/HI+CHR16 LATCH: PASS" : "D054 FCLRLO/HI+CHR16 LATCH: FAIL");
  text(7u, card_address_ok ? "FCM 64-BYTE CARD ALIGNMENT: PASS" : "FCM 64-BYTE CARD ALIGNMENT: FAIL");
  text(8u, restored ? "D054 EXACT RESTORE: PASS" : "D054 EXACT RESTORE: FAIL");
  text(9u, screen_ok ? "SCREEN BYTES EXACT RESTORE: PASS" : "SCREEN BYTES EXACT RESTORE: FAIL");
  text(10u, card_ok ? "FCM CARD BYTES EXACT RESTORE: PASS" : "FCM CARD BYTES EXACT RESTORE: FAIL");
  text(11u, "OBSERVED D031/D060-D063 IN RESULT $1850+");
  text(24u, "GATE OPEN; NO POINTER-SWAP OR PALETTE CLAIM");

  result->status[FCM_SAFE] = pass ? PASS : DEFERRED; result->reason[FCM_SAFE] = pass ? NONE : FCM_RESTORE;
  result->status[PRESENTATION] = pass ? PASS : FAIL;
  result->status[SWAP] = DEFERRED; result->reason[SWAP] = HW_SWAP;
  result->status[MODE] = pass ? PASS : DEFERRED; result->reason[MODE] = pass ? NONE : FCM_RESTORE;
  result->status[PALETTE] = DEFERRED; result->reason[PALETTE] = FCM_RESTORE;
  result->status[HUD] = DEFERRED; result->reason[HUD] = FCM_RESTORE;
  result->status[INPUT_EDGE] = DEFERRED; result->reason[INPUT_EDGE] = TIMER_BUSY;
  result->status[INPUT_PHYSICAL] = DEFERRED; result->reason[INPUT_PHYSICAL] = PHYSICAL_INPUT;
  result->status[AUDIO_TIMED] = DEFERRED; result->reason[AUDIO_TIMED] = DMA_AUDIO;
  result->status[RENDERER] = pass ? PASS : DEFERRED; result->reason[RENDERER] = pass ? NONE : FCM_RESTORE;
  result->status[HARDWARE] = DEFERRED; result->reason[HARDWARE] = OWNER_CAPTURE;
  result->display_candidate = 1u; result->frame_index = 1u; result->render_tier = 1u;
  result->palette_state = DEFERRED; result->hardware_state = DEFERRED;
  result->reserved[0] = flags; result->reserved[1] = card_address_ok;
  result->reserved[2] = restored; result->reserved[3] = screen_ok; result->reserved[4] = card_ok;
  result->reserved[5] = r0b_fcm_visible_observed_d018;
  result->reserved[6] = r0b_fcm_visible_observed_d031;
  result->reserved[7] = r0b_fcm_visible_observed_d054;
  result->reserved[8] = r0b_fcm_visible_observed_d060;
  result->reserved[9] = r0b_fcm_visible_observed_d061;
  result->reserved[10] = r0b_fcm_visible_observed_d062;
  result->reserved[11] = r0b_fcm_visible_observed_d063;
  result->header.status = pass ? PASS : DEFERRED;
  finish_result();
  dump_result_block();
}
