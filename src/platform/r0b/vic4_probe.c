#include <stdint.h>
#include <mega65.h>

/*
 * Narrow target probe only.  It verifies that the documented FCM/CHR16 bits
 * latch through the VIC-IV register interface and restores the prior state.
 * It deliberately does not assert a visible FCM layout, swap, DMA, or IRQ.
 */
uint8_t r0b_vic4_fcm_register_probe(void) {
  uint8_t saved;
  uint8_t observed;
  const uint8_t fcm_bits = (uint8_t)(VIC4_CHR16_MASK | VIC4_FCLRLO_MASK | VIC4_FCLRHI_MASK);

  VICIV.key = 0x47u;
  VICIV.key = 0x53u;
  saved = VICIV.ctrlc;
  VICIV.ctrlc = (uint8_t)(saved | fcm_bits);
  observed = VICIV.ctrlc;
  VICIV.ctrlc = saved;
  return (uint8_t)((observed & fcm_bits) == fcm_bits);
}
