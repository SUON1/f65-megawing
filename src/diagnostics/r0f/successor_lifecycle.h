#ifndef R0F_SUCCESSOR_LIFECYCLE_H
#define R0F_SUCCESSOR_LIFECYCLE_H

#include <stdint.h>

#include "r0f_successor.h"

uint8_t r0fs_transition(uint8_t state, uint8_t event);
uint8_t r0fs_storage_allowed(uint8_t state, uint8_t rom_restored,
                             uint8_t snapshot_valid, uint8_t dma_empty,
                             uint8_t irq_masked, uint8_t nmi_seen);
uint8_t r0fs_resume_allowed(uint8_t state, uint8_t canonical_restored,
                            uint8_t snapshot_invalidated, uint8_t fault);
uint8_t r0fs_context_range_valid(uint16_t offset, uint16_t length);
uint8_t r0fs_context_mailbox_valid(uint8_t region, uint16_t offset,
                                   uint8_t length);
uint8_t r0fs_completion_allowed(uint8_t state, uint8_t nmi_seen,
                                uint8_t fault, uint8_t resumed_mask,
                                uint8_t required_mask);
uint8_t r0fs_final_fault(uint8_t state, uint8_t nmi_seen,
                         uint8_t existing_fault, uint8_t resumed_mask,
                         uint8_t required_mask, uint8_t reserve_equal,
                         uint8_t ticks_equal);
uint8_t r0fs_post_storage_tick_fault(uint8_t existing_fault);
uint32_t r0fs_crc32(const uint8_t *bytes, uint16_t length);
uint8_t r0fs_snapshot_valid(const uint8_t *leading_guard,
                            const uint8_t *payload,
                            const uint8_t *trailing_guard,
                            uint32_t expected_crc);

#endif
