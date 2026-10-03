// Exercise the actual transport against channel control/status combinations.
// Retain the previous complete set of integrity and first-fault cases.
#define main previous_transport_cases
#include "r0f_group1_readiness_host_test.c"
#undef main

int main(void)
{
    assert(previous_transport_cases() == 0);
    unsigned cases = 0u;
    for (unsigned channel = 0u; channel < 4u; channel++)
    {
        for (unsigned value = 0u; value < 256u; value++)
        {
            uint32_t crc = reset_attempt();
            registers[0xd720u + channel * 16u] = (uint8_t)value;
            // Independent allowed-value oracle: status only, never controls.
            uint8_t allowed = (uint8_t)(value == 0u || value == 4u
                || value == 8u || value == 12u);
            assert(r0fg1_transport_prepare(sizeof(trace), crc) == allowed);
            assert(r0fg1_export_permit == (allowed ? 0xa5u : 0u));
            assert(r0fg1_export_status == (allowed ? 0x6bu : 0x75u));
            cases++;
        }
    }
    // All simultaneous combinations of the two status flags on four channels.
    for (unsigned combination = 0u; combination < 256u; combination++)
    {
        uint32_t crc = reset_attempt();
        for (unsigned channel = 0u; channel < 4u; channel++)
        {
            registers[0xd720u + channel * 16u] =
                (uint8_t)(((combination >> (channel * 2u)) & 3u) * 4u);
        }
        assert(r0fg1_transport_prepare(sizeof(trace), crc));
        assert(r0fg1_export_permit == 0xa5u);
        assert(r0fg1_export_bytes == sizeof(trace));
        cases++;
    }
    printf("%u additional audio readback cases PASS\n", cases);
    return 0;
}
