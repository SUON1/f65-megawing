#include <stdint.h>
#include "r0b_interfaces.h"

/*
 * This is an admission gate, deliberately not a VIC-IV register latch. It
 * performs no VIC-IV I/O: the previous state-changing control-C experiment is
 * not safe enough to include in this resident evidence disk. The caller must
 * report DEFERRED until an isolated physical restore proof exists.
 */
uint8_t r0b_vic4_fcm_safe_gate(void) {
  return (uint8_t)(R0B_DISPLAY_CANDIDATE_COUNT == 2u &&
                   R0B_DISPLAY_CANDIDATE_FCM_320X200_WIDTH == 320u &&
                   R0B_DISPLAY_CANDIDATE_FCM_320X200_HEIGHT == 200u);
}
