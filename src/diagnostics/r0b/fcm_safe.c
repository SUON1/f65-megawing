#include <stdint.h>
#include "r0b_interfaces.h"

extern uint8_t r0b_fcm_restore_probe(void);

/* This is a proof-only result block; its layout is generated from the R0-B contract. */
static volatile uint8_t *const screen = (volatile uint8_t *)0x0800;
static volatile R0BResidentResult *const result = (volatile R0BResidentResult *)0x1800;
static const uint8_t contract_sha256[32] = R0B_CONTRACT_SHA256_BYTES;

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
  while (*value && column != 40u) {
    screen[offset++] = petscii(*value++);
    ++column;
  }
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

static uint8_t sentinel_unchanged(void) {
  static const char sentinel[] = "TEXT RESTORE SENTINEL";
  uint8_t index = 0u;
  while (sentinel[index]) {
    if (screen[(uint16_t)2u * 80u + index] != petscii(sentinel[index])) return 0u;
    ++index;
  }
  return 1u;
}

static void initialise_result(void) {
  uint8_t index;
  volatile uint8_t *raw = (volatile uint8_t *)result;
  for (index = 0u; index != R0B_R0BRESIDENT_RESULT_SIZE; ++index) raw[index] = 0u;
  result->header.magic[0] = 'R'; result->header.magic[1] = '0'; result->header.magic[2] = 'B'; result->header.magic[3] = '2';
  result->header.schema_version = 2u;
  result->header.environment = 0u; /* runner records Xemu or physical identity outside the target */
  result->header.status = DEFERRED;
  result->header.harness_revision = 3u;
  for (index = 0u; index != 32u; ++index) result->header.contract_sha256[index] = contract_sha256[index];
  result->header.sdk_version[0] = 23u; result->header.sdk_version[1] = 1u;
  result->header.abi_base_page = 2u; result->header.lto_zp = 0u;
  result->header.result_size = R0B_R0BRESIDENT_RESULT_SIZE;
}

static void finish_result(void) {
  uint8_t index;
  uint8_t checksum = 0u;
  volatile uint8_t *raw = (volatile uint8_t *)result;
  for (index = 0u; index != R0B_RESULT_CHECKSUM_OFFSET; ++index) checksum = (uint8_t)(checksum + raw[index]);
  result->result_checksum = checksum;
}

void r0b_fcm_safe_run(void) {
  uint8_t flags;
  uint8_t text_ok;
  uint8_t pass;

  initialise_result();
  clear_screen();
  text(0u, "R0-B ISOLATED FCM SAFE/RESTORE");
  text(1u, "NO D02F KEY; NO DMA; NO MAP; NO IRQ");
  text(2u, "TEXT RESTORE SENTINEL");

  flags = r0b_fcm_restore_probe();
  text_ok = sentinel_unchanged();
  pass = (uint8_t)((flags & 0x07u) == 0x07u && text_ok != 0u);

  text(5u, pass ? "R0B-FCM-SAFE-002 XEMU/TARGET PASS" : "R0B-FCM-SAFE-002 DEFERRED/FAIL");
  text(6u, (flags & 0x01u) ? "C65 CONTEXT: PASS" : "C65 CONTEXT: NOT OBSERVED");
  text(7u, (flags & 0x02u) ? "D054 LATCH READBACK: PASS" : "D054 LATCH READBACK: FAIL");
  text(8u, (flags & 0x04u) ? "D054 EXACT RESTORE: PASS" : "D054 EXACT RESTORE: FAIL");
  text(9u, text_ok ? "TEXT SENTINEL: PASS" : "TEXT SENTINEL: FAIL");
  text(10u, "OWNER PHOTO + $1800 DUMP REQUIRED");
  text(11u, "RESULT HEX $1800-$185F BELOW");
  text(24u, "GATE OPEN; FCM FRAME/SWAP NOT ENABLED");

  result->status[FCM_SAFE] = pass ? PASS : DEFERRED;
  result->reason[FCM_SAFE] = pass ? NONE : FCM_RESTORE;
  result->status[PRESENTATION] = text_ok ? PASS : FAIL;
  result->status[SWAP] = DEFERRED; result->reason[SWAP] = HW_SWAP;
  result->status[MODE] = DEFERRED; result->reason[MODE] = FCM_RESTORE;
  result->status[PALETTE] = DEFERRED; result->reason[PALETTE] = FCM_RESTORE;
  result->status[HUD] = DEFERRED; result->reason[HUD] = FCM_RESTORE;
  result->status[INPUT_EDGE] = DEFERRED; result->reason[INPUT_EDGE] = TIMER_BUSY;
  result->status[INPUT_PHYSICAL] = DEFERRED; result->reason[INPUT_PHYSICAL] = PHYSICAL_INPUT;
  result->status[AUDIO_TIMED] = DEFERRED; result->reason[AUDIO_TIMED] = DMA_AUDIO;
  result->status[RENDERER] = DEFERRED; result->reason[RENDERER] = FCM_RESTORE;
  result->status[HARDWARE] = DEFERRED; result->reason[HARDWARE] = OWNER_CAPTURE;
  result->display_candidate = 1u;
  result->hardware_state = DEFERRED;
  result->reserved[0] = flags;
  result->reserved[1] = text_ok;
  result->header.status = pass ? PASS : DEFERRED;
  finish_result();
  dump_result_block();
}
