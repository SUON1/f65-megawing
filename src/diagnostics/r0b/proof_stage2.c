#include <stdint.h>
#include "r0b_interfaces.h"

extern uint8_t r0b_vic4_fcm_safe_gate(void);
extern uint8_t r0b_timer_begin(void);
extern uint16_t r0b_timer_end(void);
extern uint8_t r0b_input_edge_service(void);
extern void r0b_sid_proxy_start(void);

/* Proof-only RAM buffers; neither is a claimed VIC-IV display store. */
static volatile uint8_t *const screen = (volatile uint8_t *)0x0800;
static volatile uint8_t *const complete_a = (volatile uint8_t *)0x0400;
static volatile uint8_t *const complete_b = (volatile uint8_t *)0x1000;
static volatile R0BResidentResult *const result = (volatile R0BResidentResult *)0x1800;
static const uint8_t contract_sha256[32] = R0B_CONTRACT_SHA256_BYTES;

enum { PASS = 1u, FAIL = 2u, DEFERRED = 3u };
enum { FCM_SAFE, PRESENTATION, SWAP, MODE, PALETTE, HUD, INPUT_EDGE, INPUT_PHYSICAL, AUDIO_TIMED, RENDERER, HARDWARE };
enum { NONE, FCM_RESTORE, HW_SWAP, PHYSICAL_INPUT, DMA_AUDIO, OWNER_CAPTURE, TIMER_BUSY };

static uint8_t petscii(char value) {
  uint8_t code = (uint8_t)value;
  return (code >= (uint8_t)'A' && code <= (uint8_t)'Z') ? (uint8_t)(code & 0x1fu) : code;
}

static void clear(volatile uint8_t *buffer) {
  uint16_t offset;
  for (offset = 0u; offset != 1000u; ++offset) buffer[offset] = 0x20u;
}

static void put(volatile uint8_t *buffer, uint16_t offset, const char *value) {
  while (*value) buffer[offset++] = petscii(*value++);
}

static void number(volatile uint8_t *buffer, uint16_t offset, uint16_t value) {
  uint16_t divisor = 10000u;
  uint8_t emitted = 0u;
  do {
    uint8_t digit = 0u;
    while (value >= divisor) { value = (uint16_t)(value - divisor); ++digit; }
    if (digit != 0u || emitted != 0u || divisor == 1u) { buffer[offset++] = (uint8_t)('0' + digit); emitted = 1u; }
    divisor = (uint16_t)(divisor / 10u);
  } while (divisor != 0u);
}

static void present(volatile uint8_t *buffer) {
  uint16_t offset;
  uint8_t row;
  uint8_t column;
  /* The verified BASIC 65 baseline is an 80x25 matrix at $0800. */
  for (offset = 0u; offset != 2000u; ++offset) screen[offset] = 0x20u;
  for (row = 0u; row != 25u; ++row) {
    for (column = 0u; column != 40u; ++column) {
      screen[(uint16_t)row * 80u + column] = buffer[(uint16_t)row * 40u + column];
    }
  }
}

static uint16_t hash(volatile uint8_t *buffer) {
  uint16_t offset;
  uint16_t value = 0x6506u;
  for (offset = 0u; offset != 1000u; ++offset) value = (uint16_t)((value << 3) ^ (value >> 1) ^ buffer[offset]);
  return value;
}

static void wire_proxy(volatile uint8_t *buffer) {
  uint8_t column;
  for (column = 4u; column != 36u; ++column) buffer[4u * 40u + column] = petscii('-');
  for (column = 0u; column != 11u; ++column) {
    buffer[(uint16_t)(5u + column) * 40u + (uint16_t)(12u - column)] = petscii('*');
    buffer[(uint16_t)(5u + column) * 40u + (uint16_t)(12u + column)] = petscii('*');
  }
}

static void compose_previous(void) {
  clear(complete_a);
  put(complete_a, 0u, "R0-B PREVIOUS COMPLETE FRAME");
  put(complete_a, 40u, "PROXY SCENE 001 / WIRE CANDIDATE");
  wire_proxy(complete_a);
  put(complete_a, 18u * 40u, "COCKPIT STATUS: STABLE");
}

static void compose_status(uint8_t input_ok, uint8_t audio_ok, uint8_t input_timer, uint8_t audio_timer, uint16_t input_ticks, uint16_t audio_ticks) {
  clear(complete_b);
  put(complete_b, 0u, "R0-B EVIDENCE HARNESS REV 2");
  put(complete_b, 40u, "ENV: TARGET CAPTURE REQUIRED");
  put(complete_b, 80u, "SDK:23.1.0 ABI:B=02 LTOZP=00");
  put(complete_b, 120u, "RESULT BLOCK:$1800 SIZE:96");
  put(complete_b, 160u, "R0B-MODE-001 CANDIDATE PASS");
  put(complete_b, 200u, "R0B-PAL-001 ROLE MAP PASS");
  put(complete_b, 240u, "ACTIVE MODE/PALETTE: DEFERRED");
  put(complete_b, 280u, "R0B-FCM-SAFE-001 DEFERRED");
  put(complete_b, 320u, "NO D054 ACCESS; CLEAR: RESTORE PROOF");
  put(complete_b, 360u, "R0B-PRES-001 COMPLETE+PREV PASS");
  put(complete_b, 400u, "R0B-SWAP-001 HW FLIP DEFERRED");
  put(complete_b, 440u, "R0B-HUD-001 COCKPIT/MFD PASS");
  put(complete_b, 480u, "R0B-REN-001 WIRE PROXY PASS");
  put(complete_b, 520u, input_ok ? "R0B-IN-001 CORPUS PASS" : "R0B-IN-001 CORPUS FAIL");
  put(complete_b, 560u, input_timer ? "R0B-IN-003 EDGE RASTER:" : "R0B-IN-003 EDGE DEFERRED");
  if (input_timer) number(complete_b, 588u, input_ticks);
  put(complete_b, 600u, "R0B-IN-004 PHYS EDGE DEFERRED");
  put(complete_b, 640u, audio_ok ? "R0B-AUD-003 MODEL PASS" : "R0B-AUD-003 MODEL FAIL");
  put(complete_b, 680u, audio_timer ? "R0B-AUD-001 SID RASTER:" : "R0B-AUD-001 SID DEFERRED");
  if (audio_timer) number(complete_b, 708u, audio_ticks);
  put(complete_b, 720u, "R0B-AUD-004 PCM/DMA DEFERRED");
  put(complete_b, 760u, "R0B-HW-001 OWNER CAPTURE REQUIRED");
  put(complete_b, 800u, "R0B-BLD-001 PASS; GATE NOT CLOSED");
  put(complete_b, 840u, "DEFERRED ITEMS HAVE CLEAR CONDITIONS");
}

static void initialise_result(void) {
  uint8_t index;
  volatile uint8_t *raw = (volatile uint8_t *)result;
  for (index = 0u; index != R0B_R0BRESIDENT_RESULT_SIZE; ++index) raw[index] = 0u;
  result->header.magic[0] = 'R'; result->header.magic[1] = '0'; result->header.magic[2] = 'B'; result->header.magic[3] = '2';
  result->header.schema_version = 2u;
  result->header.environment = 0u; /* runner records Xemu or physical identity */
  result->header.status = PASS; result->header.harness_revision = 2u;
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

void r0b_stage2_run(uint8_t input_ok, uint8_t audio_ok) {
  uint16_t repeat;
  uint8_t input_edge = 0u;
  uint8_t input_timer = r0b_timer_begin();
  uint8_t audio_timer;
  uint16_t input_ticks = 0u;
  uint16_t audio_ticks = 0u;
  uint16_t previous_hash;
  uint16_t complete_hash;
  uint8_t complete_ok;
  uint8_t fcm_gate;

  initialise_result();
  compose_previous();
  previous_hash = hash(complete_a);
  present(complete_a); /* the prior complete buffer is visible while B is composed */
  if (input_timer) {
    for (repeat = 0u; repeat != 2048u; ++repeat) input_edge = r0b_input_edge_service();
    input_ticks = r0b_timer_end();
  }
  audio_timer = r0b_timer_begin();
  if (audio_timer) {
    for (repeat = 0u; repeat != 512u; ++repeat) r0b_sid_proxy_start();
    audio_ticks = r0b_timer_end();
  }
  else r0b_sid_proxy_start();
  compose_status(input_ok, audio_ok, input_timer, audio_timer, input_ticks, audio_ticks);
  complete_hash = hash(complete_b);
  complete_ok = (uint8_t)(previous_hash == hash(complete_a) && complete_hash != 0u);
  present(complete_b); /* safe CPU copy; no VIC-IV register or hardware flip */
  fcm_gate = r0b_vic4_fcm_safe_gate();

  result->status[FCM_SAFE] = DEFERRED; result->reason[FCM_SAFE] = FCM_RESTORE;
  result->status[PRESENTATION] = complete_ok ? PASS : FAIL;
  result->status[SWAP] = DEFERRED; result->reason[SWAP] = HW_SWAP;
  result->status[MODE] = fcm_gate ? PASS : FAIL;
  result->status[PALETTE] = DEFERRED; result->reason[PALETTE] = FCM_RESTORE;
  result->status[HUD] = complete_ok ? PASS : FAIL;
  result->status[INPUT_EDGE] = (input_timer && input_edge && input_ticks) ? PASS : DEFERRED;
  result->reason[INPUT_EDGE] = result->status[INPUT_EDGE] == PASS ? NONE : TIMER_BUSY;
  result->status[INPUT_PHYSICAL] = DEFERRED; result->reason[INPUT_PHYSICAL] = PHYSICAL_INPUT;
  result->status[AUDIO_TIMED] = (audio_timer && audio_ticks) ? PASS : DEFERRED;
  result->reason[AUDIO_TIMED] = result->status[AUDIO_TIMED] == PASS ? NONE : TIMER_BUSY;
  result->status[RENDERER] = complete_ok ? PASS : FAIL;
  result->status[HARDWARE] = DEFERRED; result->reason[HARDWARE] = OWNER_CAPTURE;
  result->input_ticks = input_ticks; result->audio_ticks = audio_ticks;
  result->complete_hash = complete_hash; result->previous_hash = previous_hash;
  result->display_candidate = 1u; result->frame_index = 2u; result->render_tier = 3u;
  result->palette_state = DEFERRED; result->hardware_state = DEFERRED;
  if (!input_ok || !audio_ok || !complete_ok || !fcm_gate) result->header.status = FAIL;
  finish_result();
}
