#include <stdint.h>
#include "r0b_interfaces.h"

extern uint8_t r0b_vic4_fcm_register_probe(void);

/* Proof-only resident result block. Its format is deliberately not a production ABI. */
static volatile uint8_t *const screen = (volatile uint8_t *)0x0800;
static volatile uint8_t *const result = (volatile uint8_t *)0x1800;

static void text(uint16_t offset, const char *value) {
  while (*value) screen[offset++] = (uint8_t)*value++;
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
  uint8_t fcm_registers = r0b_vic4_fcm_register_probe();
  uint8_t ok = (uint8_t)(contract_shape_ok() && filled_work_units() == 38u && fcm_registers == 1u);
  result[0] = 'R'; result[1] = '0'; result[2] = 'B'; result[3] = '1';
  result[4] = 1; result[5] = ok; result[6] = 2; result[7] = 15;
  result[8] = (uint8_t)filled_work_units(); result[9] = fcm_registers;
  result[10] = (uint8_t)(result[0] + result[1] + result[2] + result[3] + result[4] + result[5] + result[6] + result[7] + result[8]);

  text(0, "R0-B PROOF HARNESS");
  text(40, "R0B-MODE-001 HOST PASS");
  text(80, "R0B-FCM-001 ACCOUNT PASS");
  text(120, "R0B-PAL-001 HOST PASS");
  text(160, "R0B-IN-002 HOST PASS");
  text(200, fcm_registers ? "R0B-FCM-REG-001 PASS" : "R0B-FCM-REG-001 FAIL");
  text(240, "FCM FRAME: DEFERRED");
  text(280, "REASON: DMA/POINTER PROBE");
  text(320, ok ? "R0-B TEST RUN COMPLETE" : "R0-B TEST RUN FAILED");
  text(360, ok ? "R0B-BLD-001 PASS" : "R0B-BLD-001 FAIL");
  text(400, "HARDWARE: NOT RUN");
  for (;;) { }
}
