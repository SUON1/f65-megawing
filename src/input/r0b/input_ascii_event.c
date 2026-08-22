#include <stdint.h>
#include <mega65.h>

/*
 * $D610 is the MEGA65 ASCII key-event queue.  Reading obtains one event and
 * writing that same byte acknowledges it.  No CIA port or data-direction
 * register is altered, which keeps keyboard/joystick routing under ROM/OS
 * ownership during this bounded proof.
 */
static volatile uint8_t *const ascii_event = (volatile uint8_t *)0xd610;

uint8_t r0b_input_ascii_event(void) {
  uint8_t value = *ascii_event;
  if (value != 0u) *ascii_event = value;
  return value;
}
