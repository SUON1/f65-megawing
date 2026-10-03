#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "group1_export.h"
uint8_t baseline_begin(r0fg1_export *export,
                          const r0fg1_export_readiness *readiness)
{
    if (export == 0 || export->state != R0FG1X_S_FROZEN)
    {
        return 0u;
    }
    if (readiness == 0 || readiness->acquisition_stopped != 1u
        || readiness->dma_empty != 1u || readiness->display_stopped != 1u
        || readiness->audio_stopped != 1u || readiness->irq_masked != 1u
        || readiness->rom_verified != 1u || readiness->capsule_verified != 1u
        || readiness->nmi_seen != 0u || export->bytes == 0u
        || export->bytes > R0FG1X_TRACE_CAPACITY)
    {
        export->state = R0FG1X_S_FAILED;
        return 0u;
    }
    // Consumed before storage, including when transport later fails.
    export->state = R0FG1X_S_EXPORTING;
    return 1u;
}

static unsigned long cases;

static void check(uint8_t state, uint32_t bytes,
                  r0fg1_export_readiness *readiness)
{
    r0fg1_export before = {
        .state = state, .bytes = bytes, .acquisition_crc = 0x12345678u
    };
    r0fg1_export old = before;
    r0fg1_export current = before;
    r0fg1_export diagnostic = before;
    uint8_t expected = baseline_begin(&old, readiness);

    assert(r0fg1_export_begin(&current, readiness) == expected);
    uint8_t reason = r0fg1_export_begin_diagnostic(&diagnostic, readiness);
    assert((reason == 0u) == expected);
    assert(old.state == current.state && old.state == diagnostic.state);
    assert(current.bytes == bytes && diagnostic.bytes == bytes);
    assert(current.acquisition_crc == before.acquisition_crc);
    assert(diagnostic.acquisition_crc == before.acquisition_crc);
    if (state != R0FG1X_S_FROZEN)
    {
        assert(reason == 0x70u);
    }
    else if (!readiness)
    {
        assert(reason == 0x71u);
    }
    else
    {
        uint8_t wanted = 0u;
        const unsigned char *fields = (const unsigned char *)readiness;
        for (unsigned index = 0u; index < 8u; index++)
        {
            if (fields[index] != (index == 7u ? 0u : 1u))
            {
                wanted = (uint8_t)(0x72u + index);
                break;
            }
        }
        if (!wanted && !bytes)
        {
            wanted = 0x7au;
        }
        if (!wanted && bytes > R0FG1X_TRACE_CAPACITY)
        {
            wanted = 0x7bu;
        }
        assert(reason == wanted);
    }
    cases++;
}

int main(void)
{
    const uint32_t lengths[] = {
        0u, 1u, R0FG1X_TRACE_CAPACITY, R0FG1X_TRACE_CAPACITY + 1u, UINT32_MAX
    };
    r0fg1_export_readiness valid = {1u, 1u, 1u, 1u, 1u, 1u, 1u, 0u};

    assert(!baseline_begin(0, &valid));
    assert(!r0fg1_export_begin(0, &valid));
    assert(r0fg1_export_begin_diagnostic(0, &valid) == 0x70u);
    for (unsigned state = 0u; state < 256u; state++)
    {
        for (unsigned size = 0u; size < 5u; size++)
        {
            check((uint8_t)state, lengths[size], 0);
            check((uint8_t)state, lengths[size], &valid);
            for (unsigned field = 0u; field < 8u; field++)
            {
                for (unsigned value = 0u; value < 256u; value++)
                {
                    r0fg1_export_readiness ready = valid;
                    ((unsigned char *)&ready)[field] = (unsigned char)value;
                    check((uint8_t)state, lengths[size], &ready);
                }
            }
        }
    }
    for (unsigned mask = 0u; mask < 256u; mask++)
    {
        r0fg1_export_readiness ready = valid;
        for (unsigned index = 0u; index < 8u; index++)
        {
            if (mask & (1u << index))
            {
                ((unsigned char *)&ready)[index] ^= 1u;
            }
        }
        check(R0FG1X_S_FROZEN, 1u, &ready);
    }
    printf("%lu policy comparisons and first-rejection cases PASS\n", cases);
    return 0;
}
