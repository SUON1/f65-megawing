#include <assert.h>
#include <stdint.h>
#include <stdio.h>

#include "successor_lifecycle.h"

int main(void)
{
    uint8_t leading[R0FS_KERNAL_CONTEXT_GUARD_BYTES];
    uint8_t payload[R0FS_KERNAL_CONTEXT_BYTES];
    uint8_t trailing[R0FS_KERNAL_CONTEXT_GUARD_BYTES];
    uint32_t checks = 0u;
    uint16_t index;
    uint16_t state;
    uint16_t event;

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

    assert(r0fs_storage_allowed(R0FS_S_APPLICATION_SAVED, 1u, 1u, 1u,
                                1u, 0u));
    assert(!r0fs_storage_allowed(R0FS_S_APPLICATION_SAVED, 0u, 1u, 1u,
                                 1u, 0u));
    assert(!r0fs_storage_allowed(R0FS_S_APPLICATION_SAVED, 1u, 0u, 1u,
                                 1u, 0u));
    assert(!r0fs_storage_allowed(R0FS_S_APPLICATION_SAVED, 1u, 1u, 0u,
                                 1u, 0u));
    assert(!r0fs_storage_allowed(R0FS_S_APPLICATION_SAVED, 1u, 1u, 1u,
                                 0u, 0u));
    assert(!r0fs_storage_allowed(R0FS_S_APPLICATION_SAVED, 1u, 1u, 1u,
                                 1u, 1u));
    checks += 6u;

    assert(r0fs_resume_allowed(R0FS_S_APPLICATION_RESTORED, 1u, 1u, 0u));
    assert(!r0fs_resume_allowed(R0FS_S_APPLICATION_RESTORED, 0u, 1u, 0u));
    assert(!r0fs_resume_allowed(R0FS_S_APPLICATION_RESTORED, 1u, 0u, 0u));
    assert(!r0fs_resume_allowed(R0FS_S_APPLICATION_RESTORED, 1u, 1u, 1u));
    checks += 4u;

    assert(!r0fs_context_range_valid(0u, 0u));
    assert(r0fs_context_range_valid(0u, 1u));
    assert(r0fs_context_range_valid(R0FS_KERNAL_CONTEXT_BYTES - 1u, 1u));
    assert(r0fs_context_range_valid(0u, R0FS_KERNAL_CONTEXT_BYTES));
    assert(!r0fs_context_range_valid(1u, R0FS_KERNAL_CONTEXT_BYTES));
    assert(!r0fs_context_range_valid(R0FS_KERNAL_CONTEXT_BYTES, 1u));
    assert(!r0fs_context_range_valid(65535u, 2u));
    checks += 7u;

    for (index = 0u; index < R0FS_KERNAL_CONTEXT_GUARD_BYTES; index++)
    {
        leading[index] = R0FS_KERNAL_CONTEXT_GUARD;
        trailing[index] = R0FS_KERNAL_CONTEXT_GUARD;
    }
    for (index = 0u; index < R0FS_KERNAL_CONTEXT_BYTES; index++)
    {
        payload[index] = (uint8_t)(index ^ (index >> 8u) ^ 0x65u);
    }

    {
        uint32_t crc = r0fs_crc32(payload, R0FS_KERNAL_CONTEXT_BYTES);

        assert(r0fs_snapshot_valid(leading, payload, trailing, crc));
        payload[0] ^= 1u;
        assert(!r0fs_snapshot_valid(leading, payload, trailing, crc));
        payload[0] ^= 1u;
        payload[R0FS_KERNAL_CONTEXT_BYTES - 1u] ^= 1u;
        assert(!r0fs_snapshot_valid(leading, payload, trailing, crc));
        payload[R0FS_KERNAL_CONTEXT_BYTES - 1u] ^= 1u;
        leading[0] ^= 1u;
        assert(!r0fs_snapshot_valid(leading, payload, trailing, crc));
        leading[0] ^= 1u;
        trailing[R0FS_KERNAL_CONTEXT_GUARD_BYTES - 1u] ^= 1u;
        assert(!r0fs_snapshot_valid(leading, payload, trailing, crc));
        checks += 5u;
    }

    printf("R0-F successor lifecycle/guard/CRC checks PASS: %lu\n",
           (unsigned long)checks);
    return 0;
}
