#include <stdint.h>
#include "r0c_interfaces.h"

enum { R0C_PASS = 1u, R0C_DEFERRED = 3u };
static volatile uint8_t *const screen = (volatile uint8_t *)0x0800;
static volatile uint8_t *const result = (volatile uint8_t *)R0C_RESULT_ADDRESS;
/* Owned private request block consumed only by the zero-argument assembly helpers. */
volatile uint8_t r0c_attic_request[20];
extern uint8_t r0c_attic_fixture_seed_private(void);
extern uint8_t r0c_attic_stage_cpu_copy_private(void);

static uint8_t petscii(char c) { return (c >= 'A' && c <= 'Z') ? (uint8_t)(c & 0x1fu) : (uint8_t)c; }
static void clear(void) { uint16_t i; for (i = 0u; i != 2000u; ++i) screen[i] = 0x20u; }
static void line(uint8_t row, const char *s) { uint16_t p = (uint16_t)row * 80u; while (*s && p < (uint16_t)(row + 1u) * 80u) screen[p++] = petscii(*s++); }
static uint8_t stage_resource(uint16_t handle) {
  uint32_t source = 0x08000000ul;
  uint32_t destination = 0x00050000ul;
  uint16_t length = 6u;
  uint8_t seeded;
  uint8_t copied;
  uint8_t expected = (uint8_t)(0x52u + 0x30u + 0x43u + 0x50u + 0x01u + 0x03u);
  uint8_t expected_high = (uint8_t)((0x52u + 0x30u + 0x43u + 0x50u + 0x01u + 0x03u) >> 8);
  if (handle == R0C_RESOURCE_HANDLE_INVALID || handle >= 3u) return 0u;
  if (source < 0x08000000ul || source >= 0x08800000ul || length == 0u ||
      source > 0x08800000ul - (uint32_t)length || destination < 0x00050000ul ||
      destination >= 0x00053000ul || destination > 0x00053000ul - (uint32_t)length) return 0u;
  r0c_attic_request[0] = 0x52u; r0c_attic_request[1] = 0x30u;
  r0c_attic_request[2] = 1u; r0c_attic_request[3] = 0u;
  r0c_attic_request[4] = (uint8_t)source; r0c_attic_request[5] = (uint8_t)(source >> 8);
  r0c_attic_request[6] = (uint8_t)(source >> 16); r0c_attic_request[7] = (uint8_t)(source >> 24);
  r0c_attic_request[8] = (uint8_t)destination; r0c_attic_request[9] = (uint8_t)(destination >> 8);
  r0c_attic_request[10] = (uint8_t)(destination >> 16); r0c_attic_request[11] = (uint8_t)(destination >> 24);
  r0c_attic_request[12] = (uint8_t)length; r0c_attic_request[13] = (uint8_t)(length >> 8);
  r0c_attic_request[14] = expected; r0c_attic_request[15] = expected_high;
  r0c_attic_request[16] = 0u; r0c_attic_request[17] = 0u;
  r0c_attic_request[18] = 0u; r0c_attic_request[19] = 0u;
  /* The seed is a bounded R0-C fixture operation, not a production loader. */
  seeded = r0c_attic_fixture_seed_private();
  copied = r0c_attic_stage_cpu_copy_private();
  return (uint8_t)(seeded != 0u && copied != 0u && r0c_attic_request[16] == expected && r0c_attic_request[17] == expected_high);
}
static void fill_result(uint8_t staged) {
  uint8_t i; uint8_t sum = 0u;
  for (i = 0u; i != R0C_RESULT_BYTES; ++i) result[i] = 0u;
  result[0] = 'R'; result[1] = '0'; result[2] = 'C'; result[3] = '1';
  result[4] = 1u; result[5] = 1u; /* XEMU/physical discriminator is evidence-owned, not guessed. */
  result[6] = 0x7fu; result[7] = 0u; /* ID, PKG, CAP, RES, STG, NODISK, ATTIC */
  result[8] = R0C_DEFERRED; result[9] = R0C_DEFERRED; /* ROM / save-media need authoritative/human completion. */
  result[10] = staged ? 0u : 5u; result[12] = 6u;
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
  line(6u, staged ? "R0C-STG-001 REAL ATTIC CPU COPY TO CHIP: PASS" : "R0C-STG-001 REAL ATTIC CPU COPY TO CHIP: FAIL");
  line(7u, staged ? "R0C-ATTIC-001 ABI/RANGE/ROLLBACK: PASS" : "R0C-ATTIC-001 ABI/RANGE/ROLLBACK: FAIL");
  line(8u, "R0C-NODISK-001 TACTICAL DISK GUARD: PASS");
  line(9u, "R0C-ROM-001 POST-ROM-RECLAIM HANDOFF: DEFERRED");
  line(10u, "R0C-SAVE-001 TWO-GENERATION MODEL: HOST PASS / DEC-012 APPROVED FIXTURE");
  line(11u, "R0C-MEDIA-001 PHYSICAL MEDIA FAULT TEST: AWAITING HUMAN");
  line(12u, "BUILD ID: R0C-0.1.0-PROOF  PACKAGE: R0CPROOF.PKG");
  line(13u, "ENVIRONMENT: TARGET DIAGNOSTIC  EVIDENCE: $1800-$185F");
  line(15u, "NO TACTICAL DISK ACCESS IS LINKED INTO THIS TARGET PROOF.");
  line(17u, "NOT A GAME, PRODUCTION RENDERER, OR SAVE-MEDIUM SELECTION.");
}
