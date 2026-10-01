#include <assert.h>
#include <stdint.h>
#include <stdio.h>

#include "group1_export.h"

static r0fg1_export frozen_trace(void)
{
    r0fg1_export export = {0};

    assert(r0fg1_export_activate(&export));
    assert(r0fg1_export_append(&export, 512u));
    assert(r0fg1_export_freeze(&export, 0u));
    return export;
}

int main(void)
{
    r0fg1_export_readiness ready = {1u, 1u, 1u, 1u, 1u, 1u, 1u, 0u};

    for (uint16_t mask = 0u; mask < 256u; mask++)
    {
        r0fg1_export export = frozen_trace();
        r0fg1_export_readiness flags = {
            (uint8_t)(mask & 1u), (uint8_t)((mask >> 1u) & 1u),
            (uint8_t)((mask >> 2u) & 1u), (uint8_t)((mask >> 3u) & 1u),
            (uint8_t)((mask >> 4u) & 1u), (uint8_t)((mask >> 5u) & 1u),
            (uint8_t)((mask >> 6u) & 1u), (uint8_t)((mask >> 7u) & 1u),
        };
        uint8_t allowed = (uint8_t)(mask == 127u);

        assert(r0fg1_export_begin(&export, &flags) == allowed);
        assert(export.state == (allowed ? R0FG1X_S_EXPORTING : R0FG1X_S_FAILED));
        assert(!r0fg1_export_begin(&export, &ready));
        assert(!r0fg1_export_activate(&export));
        assert(!r0fg1_export_append(&export, 1u));
        assert(!r0fg1_export_freeze(&export, 1u));
        assert(export.acquisition_crc == 0u && export.bytes == 512u);
    }
    for (uint8_t outcome = 0u; outcome < 3u; outcome++)
    {
        r0fg1_export export = frozen_trace();

        assert(!r0fg1_export_finish(&export, 1u));
        assert(!r0fg1_export_read_range(&export, 0u, 1u));
        assert(r0fg1_export_begin(&export, &ready));
        for (uint32_t offset = 0u; offset <= 513u; offset++)
        {
            for (uint16_t bytes = 0u; bytes <= 513u; bytes++)
            {
                uint8_t allowed = (uint8_t)(bytes > 0u && offset <= 512u
                                            && bytes <= 512u - offset);
                assert(r0fg1_export_read_range(&export, offset, bytes) == allowed);
            }
        }
        assert(!r0fg1_export_read_range(&export, 0xffffffffu, 1u));
        assert(r0fg1_export_finish(&export, outcome) == (outcome == 1u));
        assert(export.state == (outcome == 1u ? R0FG1X_S_EXPORTED : R0FG1X_S_FAILED));
        assert(!r0fg1_export_begin(&export, &ready));
        assert(!r0fg1_export_activate(&export));
        assert(!r0fg1_export_finish(&export, 1u));
        assert(export.acquisition_crc == 0u && export.bytes == 512u);
    }
    {
        r0fg1_export export = {0};
        assert(r0fg1_export_activate(&export));
        assert(!r0fg1_export_freeze(&export, 123u));
        assert(export.state == R0FG1X_S_FAILED);
    }
    {
        r0fg1_export export = {0};
        assert(r0fg1_export_activate(&export));
        for (uint32_t offset = 0u; offset < R0FG1X_TRACE_CAPACITY; offset += 512u)
        {
            assert(r0fg1_export_append(&export, 512u));
        }
        assert(!r0fg1_export_append(&export, 1u));
        assert(export.state == R0FG1X_S_FAILED);
    }
    {
        r0fg1_export export = frozen_trace();
        assert(!r0fg1_export_begin(&export, 0));
        assert(export.state == R0FG1X_S_FAILED);
    }
    assert(!r0fg1_export_activate(0));
    assert(!r0fg1_export_append(0, 1u));
    assert(!r0fg1_export_freeze(0, 0u));
    assert(!r0fg1_export_begin(0, &ready));
    assert(!r0fg1_export_finish(0, 1u));
    assert(!r0fg1_export_read_range(0, 0u, 1u));
    puts("Group 1 export policy PASS: 256 readiness cases, bounded reads, one-use and transport isolation");
    return 0;
}
