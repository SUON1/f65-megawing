#ifndef R0FG1_TRANSPORT_H
#define R0FG1_TRANSPORT_H
#include <stdint.h>

// Bounded private trace/capsule adapter. No workload or measurement policy.
// PF flat-copy ABI, B=2, no MAP/DMA changes. Only admitted trace can be written.
uint8_t r0fg1_transport_init(void);
uint8_t r0fg1_trace_write(uint32_t offset, const uint8_t *data, uint8_t bytes);
uint8_t r0fg1_trace_read(uint32_t offset, uint8_t *data, uint8_t bytes);
uint8_t r0fg1_transport_prepare(uint32_t bytes, uint32_t expected_crc);
#endif
