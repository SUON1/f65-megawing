#include "group1_export.h"

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

uint8_t r0fg1_export_begin(r0fg1_export *export,
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
