#include <stddef.h>

#include "group1_export.h"

// This private readiness object is inspected as bytes only after proving
// every member offset. No public or generated layout is duplicated.
_Static_assert(offsetof(r0fg1_export_readiness, acquisition_stopped) == 0u,
               "readiness byte layout");
_Static_assert(offsetof(r0fg1_export_readiness, dma_empty) == 1u,
               "readiness byte layout");
_Static_assert(offsetof(r0fg1_export_readiness, display_stopped) == 2u,
               "readiness byte layout");
_Static_assert(offsetof(r0fg1_export_readiness, audio_stopped) == 3u,
               "readiness byte layout");
_Static_assert(offsetof(r0fg1_export_readiness, irq_masked) == 4u,
               "readiness byte layout");
_Static_assert(offsetof(r0fg1_export_readiness, rom_verified) == 5u,
               "readiness byte layout");
_Static_assert(offsetof(r0fg1_export_readiness, capsule_verified) == 6u,
               "readiness byte layout");
_Static_assert(offsetof(r0fg1_export_readiness, nmi_seen) == 7u,
               "readiness byte layout");
_Static_assert(sizeof(r0fg1_export_readiness) == 8u, "readiness size");

uint8_t r0fg1_export_activate(r0fg1_export *export)
{
    if (export == 0 || export->state != R0FG1X_S_COLD)
    {
        return 0u;
    }
    export->bytes = 0u;
    export->acquisition_crc = 0u;
    export->state = R0FG1X_S_ACQUIRING;
    return 1u;
}

uint8_t r0fg1_export_append(r0fg1_export *export, uint16_t bytes)
{
    if (export == 0 || export->state != R0FG1X_S_ACQUIRING)
    {
        return 0u;
    }
    if (bytes == 0u || export->bytes > R0FG1X_TRACE_CAPACITY
        || bytes > R0FG1X_TRACE_CAPACITY - export->bytes)
    {
        export->state = R0FG1X_S_FAILED;
        return 0u;
    }
    export->bytes += bytes;
    return 1u;
}

uint8_t r0fg1_export_freeze(r0fg1_export *export, uint32_t acquisition_crc)
{
    if (export == 0 || export->state != R0FG1X_S_ACQUIRING)
    {
        return 0u;
    }
    if (export->bytes == 0u || export->bytes > R0FG1X_TRACE_CAPACITY)
    {
        export->state = R0FG1X_S_FAILED;
        return 0u;
    }
    // Zero is a legitimate CRC. Its value is evidence, never an authority flag.
    export->acquisition_crc = acquisition_crc;
    export->state = R0FG1X_S_FROZEN;
    return 1u;
}

uint8_t r0fg1_export_begin_diagnostic(r0fg1_export *export,
                                     const r0fg1_export_readiness *readiness)
{
    if (export == 0 || export->state != R0FG1X_S_FROZEN)
    {
        return 0x70u;
    }
    uint8_t reason = 0u;
    if (readiness == 0)
    {
        reason = 0x71u;
    }
    else
    {
        // Unsigned-character access to object representation is permitted C.
        // Check every readiness field in the original short-circuit order.
        const unsigned char *fields = (const unsigned char *)readiness;
        for (uint8_t index = 0u; index < 8u; index++)
        {
            uint8_t expected = index == 7u ? 0u : 1u;
            if (fields[index] != expected)
            {
                reason = (uint8_t)(0x72u + index);
                break;
            }
        }
        if (reason == 0u)
        {
            if (export->bytes == 0u)
            {
                reason = 0x7au;
            }
            else if (export->bytes > R0FG1X_TRACE_CAPACITY)
            {
                reason = 0x7bu;
            }
        }
    }
    if (reason != 0u)
    {
        export->state = R0FG1X_S_FAILED;
        return reason;
    }
    // Consumed before storage, including when transport later fails.
    export->state = R0FG1X_S_EXPORTING;
    return 0u;
}

uint8_t r0fg1_export_begin(r0fg1_export *export,
                          const r0fg1_export_readiness *readiness)
{
    return (uint8_t)(r0fg1_export_begin_diagnostic(export, readiness) == 0u);
}

uint8_t r0fg1_export_finish(r0fg1_export *export, uint8_t transport_ok)
{
    if (export == 0 || export->state != R0FG1X_S_EXPORTING)
    {
        return 0u;
    }
    export->state = transport_ok == 1u ? R0FG1X_S_EXPORTED : R0FG1X_S_FAILED;
    return (uint8_t)(transport_ok == 1u);
}

uint8_t r0fg1_export_read_range(const r0fg1_export *export,
                               uint32_t offset, uint16_t bytes)
{
    return (uint8_t)(export != 0 && export->state == R0FG1X_S_EXPORTING
                     && export->bytes <= R0FG1X_TRACE_CAPACITY
                     && bytes != 0u && offset <= export->bytes
                     && bytes <= export->bytes - offset);
}
