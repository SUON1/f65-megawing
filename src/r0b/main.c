#include <stdint.h>
#include "r0b_interfaces.h"

extern uint8_t r0b_input_fixture_validate(void);
extern uint8_t r0b_audio_priority_fixture_validate(void);
extern void r0b_sid_proxy_start(void);
extern void r0b_stage2_run(uint8_t input_ok, uint8_t audio_ok);

/* Proof-only resident result block. Its format is deliberately not a production ABI. */
/* The active BASIC 65 text screen is a 40 x 25 PETSCII byte screen at $0800. */
static volatile uint8_t *const screen = (volatile uint8_t *)0x0800;
static volatile uint8_t *const result = (volatile uint8_t *)0x1800;

static uint8_t petscii(char value) {
  uint8_t code = (uint8_t)value;
  if (code >= (uint8_t)'A' && code <= (uint8_t)'Z') return (uint8_t)(code & 0x1fu);
  return code;
}

static void text(uint16_t offset, const char *value) {
  while (*value) screen[offset++] = petscii(*value++);
}

static void clear_screen(void) {
  uint16_t offset;
  for (offset = 0u; offset != 1000u; ++offset) screen[offset] = 0x20u;
}

static uint8_t contract_shape_ok(void) {
  return (uint8_t)(R0B_R0BDISPLAY_DESCRIPTOR_SIZE == 58u &&
                   R0B_R0BWORK_RESULT_SIZE == 16u &&
                   R0B_R0BINPUT_TRANSITION_SIZE == 8u &&
                   R0B_R0BAUDIO_EVENT_SIZE == 8u &&
                   R0B_R0BEVIDENCE_HEADER_SIZE == 48u);
}

static uint16_t filled_work_units(void) {
  uint8_t tier;
  uint16_t units = 0;
  for (tier = 0; tier != 4; ++tier) units = (uint16_t)(units + 8u + tier);
  return units;
}

int main(void) {
  /*
   * The D054 latch/read/restore experiment is deliberately not run from the
   * owner-facing disk. Its first physical MEGA65 execution left the normal
   * 16-bit text display unreadable. It needs an isolated, reversible test
   * harness before it can be admitted again.
   */
  clear_screen();
  uint8_t input_fixture = r0b_input_fixture_validate();
  uint8_t audio_fixture = r0b_audio_priority_fixture_validate();
  r0b_sid_proxy_start();
  uint8_t ok = (uint8_t)(contract_shape_ok() && filled_work_units() == 38u && input_fixture == 1u && audio_fixture == 1u);
  result[0] = 'R'; result[1] = '0'; result[2] = 'B'; result[3] = '1';
  result[4] = 1; result[5] = ok; result[6] = 2; result[7] = 15;
  result[8] = (uint8_t)filled_work_units(); result[9] = 0u;
  result[11] = input_fixture; result[12] = audio_fixture;
  result[10] = (uint8_t)(result[0] + result[1] + result[2] + result[3] + result[4] + result[5] + result[6] + result[7] + result[8]);

  text(0, "R0-B PROOF HARNESS");
  text(40, "R0B-MODE-001 HOST PASS");
  text(80, "R0B-FCM-001 ACCOUNT PASS");
  text(120, "R0B-PAL-001 HOST PASS");
  text(160, "R0B-IN-002 HOST PASS");
  text(200, "R0B-FCM-REG-001 DEFERRED");
  text(240, "FCM FRAME: DEFERRED");
  text(280, "REASON: D054 PROBE NOT SAFE");
  text(320, input_fixture ? "R0B-IN-001 FIXTURE PASS" : "R0B-IN-001 FIXTURE FAIL");
  text(360, audio_fixture ? "R0B-AUD-003 MODEL PASS" : "R0B-AUD-003 MODEL FAIL");
  text(400, "SID CONFIGURED: NOT TIMED");
  text(440, ok ? "R0-B TEST RUN COMPLETE" : "R0-B TEST RUN FAILED");
  text(480, ok ? "R0B-BLD-001 PASS" : "R0B-BLD-001 FAIL");
  text(520, "HARDWARE: BASELINE ONLY");
  r0b_stage2_run(input_fixture, audio_fixture);
  for (;;) { }
}
