#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "combined_model.h"
#include "r0f_successor_integration.h"
#include "successor_lifecycle.h"

int main(void)
{
    r0fc_model integrated;
    r0fc_model uninterrupted;
    r0fc_model saved;
    r0fc_snapshots snapshots;
    uint32_t checks = 0u;
    uint16_t event;
    uint16_t length;
    uint16_t offset;
    uint16_t state;
    uint8_t lifecycle = R0FS_S_PRE_C_CAPTURED;
    uint8_t tick;
    uint8_t leading[R0FS_KERNAL_CONTEXT_GUARD_BYTES];
    uint8_t payload[R0FS_KERNAL_CONTEXT_BYTES];
    uint8_t payload_copy[R0FS_KERNAL_CONTEXT_BYTES];
    uint8_t trailing[R0FS_KERNAL_CONTEXT_GUARD_BYTES];

    for (state = 0u; state < 256u; state++)
    {
        for (event = 0u; event < 256u; event++)
        {
            uint8_t expected = R0FS_S_LOCKOUT;

            if (state < R0FS_S_SERVICES_RESUMED && event == state)
            {
                expected = (uint8_t)(state + 1u);
            }
            assert(r0fs_transition((uint8_t)state, (uint8_t)event)
                   == expected);
            checks++;
        }
    }

    r0fc_reset(&integrated);
    r0fc_reset(&uninterrupted);
    r0fc_snap_reset(&snapshots);
    lifecycle = r0fs_transition(lifecycle, R0FS_E_ACTIVATE);
    assert(lifecycle == R0FS_S_WORKLOAD_ACTIVE);
    for (tick = 0u; tick < R0FSI_PRE_STORAGE_TICKS; tick++)
    {
        uint8_t slot;

        r0fc_tick(&integrated);
        r0fc_tick(&uninterrupted);
        slot = r0fc_publish(&snapshots, &integrated);
        if (slot < R0FC_SNAPSHOT_COUNT)
        {
            assert(r0fc_acquire(&snapshots) == slot);
            r0fc_release(&snapshots);
        }
        checks += 3u;
    }
    saved = integrated;
    lifecycle = r0fs_transition(lifecycle, R0FS_E_QUIESCE);
    lifecycle = r0fs_transition(lifecycle, R0FS_E_RESTORE_ROM);
    lifecycle = r0fs_transition(lifecycle, R0FS_E_SAVE_APPLICATION);
    assert(r0fs_storage_allowed(lifecycle, 1u, 1u, 1u, 1u, 0u));
    lifecycle = r0fs_transition(lifecycle, R0FS_E_ENTER_KERNAL);
    assert(!memcmp(&saved, &integrated, sizeof(saved)));
    lifecycle = r0fs_transition(lifecycle, R0FS_E_FINISH_STORAGE);
    lifecycle = r0fs_transition(lifecycle, R0FS_E_RESTORE_KERNAL_CONTEXT);
    lifecycle = r0fs_transition(lifecycle, R0FS_E_RESTORE_APPLICATION);
    assert(r0fs_resume_allowed(lifecycle, 1u, 1u, 0u));
    lifecycle = r0fs_transition(lifecycle, R0FS_E_RESUME_SERVICES);
    assert(lifecycle == R0FS_S_SERVICES_RESUMED);
    assert(integrated.tick == R0FSI_PRE_STORAGE_TICKS);
    checks += 12u;

    for (tick = 0u; tick < R0FSI_POST_STORAGE_TICKS; tick++)
    {
        r0fc_tick(&integrated);
        r0fc_tick(&uninterrupted);
        checks += 2u;
    }
    assert(integrated.tick == uninterrupted.tick);
    assert(integrated.checksum == uninterrupted.checksum);
    assert(!memcmp(integrated.x, uninterrupted.x, sizeof(integrated.x)));
    assert(!memcmp(integrated.y, uninterrupted.y, sizeof(integrated.y)));
    assert(!memcmp(integrated.z, uninterrupted.z, sizeof(integrated.z)));
    assert(!memcmp(integrated.command, uninterrupted.command,
                   sizeof(integrated.command)));
    assert(!memcmp(integrated.next, uninterrupted.next,
                   sizeof(integrated.next)));
    assert(integrated.tick
           == R0FSI_PRE_STORAGE_TICKS + R0FSI_POST_STORAGE_TICKS);
    checks += 2u;

    for (state = 0u; state < 256u; state++)
    {
        uint8_t rom;
        uint8_t snapshot;
        uint8_t dma;
        uint8_t irq;
        uint8_t nmi;

        for (rom = 0u; rom < 2u; rom++)
        {
            for (snapshot = 0u; snapshot < 2u; snapshot++)
            {
                for (dma = 0u; dma < 2u; dma++)
                {
                    for (irq = 0u; irq < 2u; irq++)
                    {
                        for (nmi = 0u; nmi < 2u; nmi++)
                        {
                            uint8_t expected =
                                (uint8_t)(state == R0FS_S_APPLICATION_SAVED
                                          && rom && snapshot && dma && irq
                                          && !nmi);

                            assert(r0fs_storage_allowed((uint8_t)state, rom,
                                                        snapshot, dma, irq,
                                                        nmi) == expected);
                            checks++;
                        }
                    }
                }
            }
        }
    }
    assert(!r0fs_resume_allowed(R0FS_S_APPLICATION_RESTORED, 0u, 1u, 0u));
    assert(!r0fs_resume_allowed(R0FS_S_APPLICATION_RESTORED, 1u, 0u, 0u));
    assert(!r0fs_resume_allowed(R0FS_S_APPLICATION_RESTORED, 1u, 1u, 1u));
    checks += 3u;

    for (offset = 0u; offset <= R0FS_KERNAL_CONTEXT_BYTES + 1u; offset++)
    {
        for (length = 0u; length <= R0FSI_CONTEXT_CHUNK_BYTES; length++)
        {
            uint8_t expected =
                (uint8_t)(length != 0u
                          && offset <= R0FS_KERNAL_CONTEXT_BYTES - length);

            assert(r0fs_context_range_valid(offset, length) == expected);
            checks++;
        }
    }
    assert(r0fs_context_range_valid(0u, R0FS_KERNAL_CONTEXT_BYTES));
    assert(!r0fs_context_range_valid(1u, R0FS_KERNAL_CONTEXT_BYTES));
    checks += 2u;

    assert(!r0fs_context_mailbox_valid(1u, 0xffffu, 1u));
    assert(!r0fs_context_mailbox_valid(1u, 0xff80u, 255u));
    assert(!r0fs_context_mailbox_valid(
        1u, R0FS_KERNAL_CONTEXT_BYTES, 1u));
    assert(!r0fs_context_mailbox_valid(
        1u, R0FS_KERNAL_CONTEXT_BYTES - 1u, 2u));
    assert(r0fs_context_mailbox_valid(1u, 0u, 1u));
    assert(r0fs_context_mailbox_valid(
        1u, R0FS_KERNAL_CONTEXT_BYTES - 1u, 1u));
    assert(r0fs_context_mailbox_valid(
        0u, 0u, R0FS_KERNAL_CONTEXT_GUARD_BYTES));
    assert(r0fs_context_mailbox_valid(
        2u, 0u, R0FS_KERNAL_CONTEXT_GUARD_BYTES));
    assert(!r0fs_context_mailbox_valid(0u, 1u, 1u));
    assert(!r0fs_context_mailbox_valid(
        2u, 0u, R0FS_KERNAL_CONTEXT_GUARD_BYTES + 1u));
    checks += 10u;

    for (offset = 0u; offset < R0FS_KERNAL_CONTEXT_GUARD_BYTES; offset++)
    {
        leading[offset] = R0FS_KERNAL_CONTEXT_GUARD;
        trailing[offset] = R0FS_KERNAL_CONTEXT_GUARD;
    }
    for (offset = 0u; offset < R0FS_KERNAL_CONTEXT_BYTES; offset++)
    {
        payload[offset] = (uint8_t)(offset ^ (offset >> 8u) ^ 0x65u);
    }
    for (offset = 0u; offset < R0FS_KERNAL_CONTEXT_BYTES;)
    {
        uint16_t remaining =
            (uint16_t)(R0FS_KERNAL_CONTEXT_BYTES - offset);
        uint8_t chunk = remaining > R0FSI_CONTEXT_CHUNK_BYTES
            ? R0FSI_CONTEXT_CHUNK_BYTES : (uint8_t)remaining;

        assert(r0fs_context_mailbox_valid(1u, offset, chunk));
        memcpy(payload_copy + offset, payload + offset, chunk);
        offset = (uint16_t)(offset + chunk);
        checks++;
    }
    assert(r0fs_crc32(payload_copy, R0FS_KERNAL_CONTEXT_BYTES)
           == r0fs_crc32(payload, R0FS_KERNAL_CONTEXT_BYTES));
    checks++;
    {
        uint32_t context_crc =
            r0fs_crc32(payload, R0FS_KERNAL_CONTEXT_BYTES);

        assert(r0fs_snapshot_valid(leading, payload, trailing, context_crc));
        leading[0] ^= 1u;
        assert(!r0fs_snapshot_valid(leading, payload, trailing, context_crc));
        leading[0] ^= 1u;
        trailing[R0FS_KERNAL_CONTEXT_GUARD_BYTES - 1u] ^= 1u;
        assert(!r0fs_snapshot_valid(leading, payload, trailing, context_crc));
        trailing[R0FS_KERNAL_CONTEXT_GUARD_BYTES - 1u] ^= 1u;
        payload[0] ^= 1u;
        assert(!r0fs_snapshot_valid(leading, payload, trailing, context_crc));
        checks += 4u;
    }

    assert(r0fs_completion_allowed(
        R0FS_S_SERVICES_RESUMED, 0u, 0u, 31u, 31u));
    assert(!r0fs_completion_allowed(
        R0FS_S_SERVICES_RESUMED, 1u, 0u, 31u, 31u));
    assert(!r0fs_completion_allowed(
        R0FS_S_SERVICES_RESUMED, 0u, 1u, 31u, 31u));
    assert(!r0fs_completion_allowed(
        R0FS_S_SERVICES_RESUMED, 0u, 0u, 30u, 31u));
    checks += 4u;

    printf("R0-F successor T03 lifecycle/continuation/fault checks PASS: %lu\n",
           (unsigned long)checks);
    printf("T03 deterministic lineage: tick %u %08lx -> tick %u %08lx\n",
           R0FSI_PRE_STORAGE_TICKS, (unsigned long)saved.checksum,
           integrated.tick, (unsigned long)integrated.checksum);
    return 0;
}
