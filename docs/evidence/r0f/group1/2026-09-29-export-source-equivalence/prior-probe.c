#include <stdint.h>

#include "combined_platform.h"
#include "group1_transport.h"
#include "successor_lifecycle.h"

// The development builder selects the length; the transport owns no test case.
#ifndef R0FG1_PROBE_BYTES
#error R0FG1_PROBE_BYTES must be supplied by the development probe builder
#endif
static uint8_t buffer[255];

uint8_t r0fg1_export_probe_init(void)
{
    return r0fg1_transport_init();
}

uint8_t r0fg1_export_probe_prepare(void)
{
    uint32_t crc = 0xfffffffful;
    for (uint32_t offset = 0u; offset < R0FG1_PROBE_BYTES;)
    {
        uint32_t remaining = R0FG1_PROBE_BYTES - offset;
        uint8_t bytes = remaining > sizeof(buffer) ? sizeof(buffer) : (uint8_t)remaining;
        for (uint8_t index = 0u; index < bytes; index++)
        {
            uint32_t position = offset + index;
            buffer[index] = position < 512u ? cfresult[position]
                : (uint8_t)(position ^ (position >> 8u) ^ 0x71u);
        }
        crc = r0fs_crc32_update(crc, buffer, bytes);
        if (!r0fg1_trace_write(offset, buffer, bytes))
        {
            return 0u;
        }
        offset += bytes;
    }
    return r0fg1_transport_prepare(R0FG1_PROBE_BYTES, ~crc);
}
