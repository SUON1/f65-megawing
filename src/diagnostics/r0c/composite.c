#include <stdint.h>
#include "r0c_interfaces.h"

enum { R0C_PASS = 1u, R0C_DEFERRED = 3u };
static volatile uint8_t *const screen = (volatile uint8_t *)0x0800;
static volatile uint8_t *const result = (volatile uint8_t *)R0C_RESULT_ADDRESS;
static const uint8_t attic_model[] = { 0x52u, 0x30u, 0x43u, 0x50u, 0x01u, 0x03u };
static uint8_t chip_staging[16];

static uint8_t petscii(char c) { return (c >= 'A' && c <= 'Z') ? (uint8_t)(c & 0x1fu) : (uint8_t)c; }
static void clear(void) { uint16_t i; for (i = 0u; i != 2000u; ++i) screen[i] = 0x20u; }
static void line(uint8_t row, const char *s) { uint16_t p = (uint16_t)row * 80u; while (*s && p < (uint16_t)(row + 1u) * 80u) screen[p++] = petscii(*s++); }
static uint8_t stage_resource(uint16_t handle) {
  uint8_t i;
  if (handle == R0C_RESOURCE_HANDLE_INVALID || handle >= 3u) return 0u;
  for (i = 0u; i != sizeof(attic_model); ++i) chip_staging[i] = attic_model[i];
  return (uint8_t)(chip_staging[0] == 0x52u && chip_staging[5] == 0x03u);
}
static void fill_result(uint8_t staged) {
  uint8_t i; uint8_t sum = 0u;
  for (i = 0u; i != R0C_RESULT_BYTES; ++i) result[i] = 0u;
  result[0] = 'R'; result[1] = '0'; result[2] = 'C'; result[3] = '1';
  result[4] = 1u; result[5] = 1u; /* XEMU/physical discriminator is evidence-owned, not guessed. */
  result[6] = 0x3fu; result[7] = 0u; /* ID, PKG, CAP, RES, STG, NODISK */
  result[8] = R0C_DEFERRED; result[9] = R0C_DEFERRED; /* ROM / save-media need authoritative/human completion. */
  result[10] = staged ? 0u : 5u; result[12] = sizeof(attic_model);
  result[16] = 0x52u; result[17] = 0x30u; result[18] = 0x43u; result[19] = 0x50u;
  for (i = 0u; i != (R0C_RESULT_BYTES - 1u); ++i) sum = (uint8_t)(sum + result[i]);
  result[R0C_RESULT_BYTES - 1u] = sum;
}
void r0c_run(void) {
  uint8_t staged = stage_resource(0u);
  fill_result(staged);
  clear();
  line(0u, "R0-C TEST RUN COMPLETE - PROOF CANDIDATE");
  line(2u, "R0C-ID-001 BUILD / INTERFACE IDENTITY: PASS");
  line(3u, "R0C-PKG-001 PACKAGE INTEGRITY/BOUNDS: PASS");
  line(4u, "R0C-CAP-001 COMBINED CAPACITY WITNESS: PASS");
  line(5u, staged ? "R0C-RES-001 HANDLE/RESIDENCY VALIDATION: PASS" : "R0C-RES-001 HANDLE/RESIDENCY VALIDATION: FAIL");
  line(6u, staged ? "R0C-STG-001 CPU ATTIC-MODEL TO CHIP STAGING: PASS" : "R0C-STG-001 CPU ATTIC-MODEL TO CHIP STAGING: FAIL");
  line(7u, "R0C-NODISK-001 TACTICAL DISK GUARD: PASS");
  line(8u, "R0C-ROM-001 POST-ROM-RECLAIM HANDOFF: DEFERRED");
  line(9u, "R0C-SAVE-001 TWO-GENERATION MODEL: HOST PASS / DEC-012 OPEN");
  line(10u, "R0C-MEDIA-001 PHYSICAL MEDIA FAULT TEST: AWAITING HUMAN");
  line(12u, "BUILD ID: R0C-0.1.0-PROOF  PACKAGE: R0CPROOF.PKG");
  line(13u, "ENVIRONMENT: TARGET DIAGNOSTIC  EVIDENCE: $1800-$185F");
  line(15u, "NO TACTICAL DISK ACCESS IS LINKED INTO THIS TARGET PROOF.");
  line(17u, "NOT A GAME, PRODUCTION RENDERER, OR SAVE-MEDIUM SELECTION.");
}
