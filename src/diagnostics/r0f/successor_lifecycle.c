#include "successor_lifecycle.h"

uint8_t r0fs_transition(uint8_t state, uint8_t event)
{
    if (state < R0FS_S_SERVICES_RESUMED && event == state)
    {
        return (uint8_t)(state + 1u);
    }

    return R0FS_S_LOCKOUT;
}

uint8_t r0fs_storage_allowed(uint8_t state, uint8_t rom_restored,
                             uint8_t snapshot_valid, uint8_t dma_empty,
                             uint8_t irq_masked, uint8_t nmi_seen)
{
    return (uint8_t)(state == R0FS_S_APPLICATION_SAVED
                     && rom_restored == 1u
                     && snapshot_valid == 1u
                     && dma_empty == 1u
                     && irq_masked == 1u
                     && nmi_seen == 0u);
}

uint8_t r0fs_resume_allowed(uint8_t state, uint8_t canonical_restored,
                            uint8_t snapshot_invalidated, uint8_t fault)
{
    return (uint8_t)(state == R0FS_S_APPLICATION_RESTORED
                     && canonical_restored == 1u
                     && snapshot_invalidated == 1u
                     && fault == 0u);
}

uint8_t r0fs_context_range_valid(uint16_t offset, uint16_t length)
{
    return (uint8_t)(length != 0u
                     && length <= R0FS_KERNAL_CONTEXT_BYTES
                     && offset <= R0FS_KERNAL_CONTEXT_BYTES - length);
}

uint8_t r0fs_context_mailbox_valid(uint8_t region, uint16_t offset,
                                   uint8_t length)
{
    uint16_t end;

    if (length == 0u || region > 2u)
    {
        return 0u;
    }
    if (region != 1u)
    {
        return (uint8_t)(offset == 0u
                         && length <= R0FS_KERNAL_CONTEXT_GUARD_BYTES);
    }
    end = (uint16_t)(offset + length);
    return (uint8_t)(offset < R0FS_KERNAL_CONTEXT_BYTES
                     && end >= offset
                     && end <= R0FS_KERNAL_CONTEXT_BYTES);
}

uint8_t r0fs_completion_allowed(uint8_t state, uint8_t nmi_seen,
                                uint8_t fault, uint8_t resumed_mask,
                                uint8_t required_mask)
{
    return (uint8_t)(state == R0FS_S_SERVICES_RESUMED
                     && nmi_seen == 0u
                     && fault == 0u
                     && resumed_mask == required_mask);
}

uint32_t r0fs_crc32(const uint8_t *bytes, uint16_t length)
{
    uint32_t crc = 0xfffffffful;

    while (length-- != 0u)
    {
        uint8_t bit;

        crc ^= *bytes++;
        for (bit = 0u; bit < 8u; bit++)
        {
            crc = (crc >> 1u) ^ ((crc & 1u) != 0u ? 0xedb88320ul : 0u);
        }
    }

    return ~crc;
}

uint8_t r0fs_snapshot_valid(const uint8_t *leading_guard,
                            const uint8_t *payload,
                            const uint8_t *trailing_guard,
                            uint32_t expected_crc)
{
    uint8_t index;

    for (index = 0u; index < R0FS_KERNAL_CONTEXT_GUARD_BYTES; index++)
    {
        if (leading_guard[index] != R0FS_KERNAL_CONTEXT_GUARD
            || trailing_guard[index] != R0FS_KERNAL_CONTEXT_GUARD)
        {
            return 0u;
        }
    }

    return (uint8_t)(r0fs_crc32(payload, R0FS_KERNAL_CONTEXT_BYTES)
                     == expected_crc);
}
