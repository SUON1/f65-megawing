#include <stdint.h>
#include <mega65.h>

/*
 * Proof-only scheduling model. A priority-zero warning must win the next
 * service slot; this function does not claim an interrupt cadence or latency.
 */
uint8_t r0b_audio_priority_fixture_validate(void) {
  const uint8_t arrivals[8] = {2u, 2u, 1u, 2u, 0u, 1u, 0u, 0u};
  uint8_t pending = 0u;
  uint8_t service;
  uint8_t priority_zero_services = 0u;

  for (service = 0u; service != 8u; ++service) {
    uint8_t event = arrivals[service];
    pending = (uint8_t)(pending | (uint8_t)(1u << event));
    if ((pending & 1u) != 0u) {
      pending = (uint8_t)(pending & (uint8_t)~1u);
      ++priority_zero_services;
    } else if ((pending & 2u) != 0u) {
      pending = (uint8_t)(pending & (uint8_t)~2u);
    } else if ((pending & 4u) != 0u) {
      pending = (uint8_t)(pending & (uint8_t)~4u);
    }
  }
  return (uint8_t)(priority_zero_services == 3u);
}

/*
 * A continuous, audible SID proxy for later owner testing. It is intentionally
 * not a latency result: no audio capture, service interrupt, or threshold is
 * inferred from this configuration write.
 */
void r0b_sid_proxy_start(void) {
  SID1.v1.freq = 0x0160u;
  SID1.v1.pw = 0x0800u;
  SID1.v1.ad = 0x24u;
  SID1.v1.sr = 0xa8u;
  SID1.v1.ctrl = 0x41u;
  SID1.amp = 0x0fu;
}
