#ifndef R0F_GROUP1_EXPORT_H
#define R0F_GROUP1_EXPORT_H

#include <stdint.h>

#include "r0f_group1_export.h"

// Pure capability policy. Does not access hardware or choose workload cases.
typedef struct
{
    uint32_t bytes;
    uint32_t acquisition_crc;
    uint8_t state;
} r0fg1_export;

typedef struct
{
    uint8_t acquisition_stopped;
    uint8_t dma_empty;
    uint8_t display_stopped;
    uint8_t audio_stopped;
    uint8_t irq_masked;
    uint8_t rom_verified;
    uint8_t capsule_verified;
    uint8_t nmi_seen;
} r0fg1_export_readiness;

uint8_t r0fg1_export_activate(r0fg1_export *export);
uint8_t r0fg1_export_append(r0fg1_export *export, uint16_t bytes);
uint8_t r0fg1_export_freeze(r0fg1_export *export, uint32_t acquisition_crc);
uint8_t r0fg1_export_begin(r0fg1_export *export,
                          const r0fg1_export_readiness *readiness);
// Pure terminal diagnostic: zero means admitted; 70-7B identify rejection.
// The existing boolean entry interface retains exactly its prior semantics.
uint8_t r0fg1_export_begin_diagnostic(r0fg1_export *export,
                                     const r0fg1_export_readiness *readiness);
uint8_t r0fg1_export_finish(r0fg1_export *export, uint8_t transport_ok);
uint8_t r0fg1_export_read_range(const r0fg1_export *export,
                               uint32_t offset, uint16_t bytes);

#endif
