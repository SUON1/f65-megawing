#ifndef R0FG1_TRANSPORT_H
#define R0FG1_TRANSPORT_H
#include <stdint.h>

// Bounded private trace/capsule adapter. No workload or measurement policy.
// PF flat-copy ABI, B=2, no MAP/DMA changes. Only admitted trace can be written.
// Before terminal ownership this byte is a monotonic preparation marker.
// Only the stopped terminal path advances it; the exporter replaces it.
extern volatile uint8_t r0fg1_export_status;

// Measured MOS volatile C increment costs seven bytes; INC absolute costs
// three. Terminal IRQs are stopped. Preserve A/X/Y/Z/B and declare flags and
// memory clobbered; no MAP, base-page, DMA or hardware-register access.
static inline void r0fg1_terminal_checkpoint(void)
{
#ifdef __mos__
    __asm__ volatile ("inc r0fg1_export_status" : : : "cc", "memory");
#else
    r0fg1_export_status++;
#endif
}

uint8_t r0fg1_transport_init(void);
uint8_t r0fg1_trace_write(uint32_t offset, const uint8_t *data, uint8_t bytes);
uint8_t r0fg1_trace_read(uint32_t offset, uint8_t *data, uint8_t bytes);
uint8_t r0fg1_transport_prepare(uint32_t bytes, uint32_t expected_crc);
#endif
