#include <stdint.h>
#include "r0b_interfaces.h"

/*
 * Deterministic target counterpart to the Java-generated corpus expectation.
 * This deliberately exercises the proof accumulator only; it does not claim
 * CIA/keyboard/joystick sampling or physical input latency.
 */
uint8_t r0b_input_fixture_validate(void) {
  uint32_t state = 65067u;
  uint8_t accumulator = 0u;
  uint16_t consumed = 0u;
  uint16_t sample;

  for (sample = 0u; sample != R0B_INPUT_CORPUS_TRANSITIONS; ++sample) {
    uint8_t edge;
    state = state * 1664525u + 1013904223u;
    edge = (uint8_t)((state >> 29) & 1u);
    accumulator = (uint8_t)(accumulator | edge);
    if ((sample & 3u) == 3u) {
      consumed = (uint16_t)(consumed + accumulator);
      accumulator = 0u;
    }
  }
  consumed = (uint16_t)(consumed + accumulator);
  return (uint8_t)(consumed == R0B_INPUT_CORPUS_CONSUMED_EDGES);
}

/* Synthetic edge-to-binding fixture. It is deliberately not a CIA sample. */
uint8_t r0b_input_edge_service(void) {
  volatile uint8_t raw = 0u;
  uint8_t previous = raw;
  uint8_t pressed;
  raw = 1u;
  pressed = (uint8_t)(raw & (uint8_t)~previous);
  raw = 0u;
  return (uint8_t)(pressed == 1u && raw == 0u);
}
