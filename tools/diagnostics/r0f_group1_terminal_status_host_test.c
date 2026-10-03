// Actual terminal transport functions with explicit physical/register mocks.
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "group1_export.h"
#include "group1_transport.h"
#include "successor_lifecycle.h"

static uint8_t registers[65536];
#define CFREG(address) registers[address]
static uint8_t result[512];
static volatile uint8_t *const cfresult = result;
static uint8_t cffault, cfreclaimed, r0f_pf_nmi_seen;
volatile uint8_t r0fg1_export_status;
static uint8_t r0fg1_export_permit;
static uint32_t r0fg1_export_bytes;
static uint8_t buffer[R0FG1X_COPY_CHUNK_BYTES];
static uint32_t capsule_crc;
static r0fg1_export export;
static uint8_t capsule[R0FG1X_CAPSULE_BYTES];
static uint8_t trace[32];
static uint8_t fail_trace, fail_capsule, irq_status;

static uint8_t r0fsi_irq_cpu_status(void)
{
    return irq_status;
}

static uint8_t transfer(uint8_t is_trace, uint32_t offset,
                        uint8_t bytes, uint8_t write)
{
    assert(!write);
    assert(bytes <= sizeof(buffer));
    assert(offset + bytes <= (is_trace ? sizeof(trace) : sizeof(capsule)));
    if ((is_trace && fail_trace) || (!is_trace && fail_capsule))
    {
        return 0u;
    }
    memcpy(buffer, (is_trace ? trace : capsule) + offset, bytes);
    return 1u;
}

#include "terminal_transport_under_test.inc"

static uint32_t reset_attempt(void)
{
    memset(registers, 0, sizeof(registers));
    memset(result, 0, sizeof(result));
    memset(&export, 0, sizeof(export));
    memset(capsule, R0FG1X_GUARD_VALUE, sizeof(capsule));
    for (uint32_t index = 0u; index < sizeof(trace); index++)
    {
        trace[index] = (uint8_t)(index ^ 0x5au);
    }
    cffault = cfreclaimed = r0f_pf_nmi_seen = 0u;
    fail_trace = fail_capsule = r0fg1_export_permit = 0u;
    r0fg1_export_bytes = 0u;
    r0fg1_export_status = 0x6du;
    irq_status = 4u;
    result[5] = 127u;
    assert(validate_capsule(1u));
    assert(r0fg1_export_activate(&export));
    return ~r0fs_crc32_update(0xfffffffful, trace, sizeof(trace));
}

int main(void)
{
    // Cases retain the real policy and capsule checks; only edges are mocked.
    for (uint8_t test = 0u; test < 16u; test++)
    {
        uint32_t crc = reset_attempt();
        switch (test)
        {
            case 1: cffault = 3u; break;
            case 2: result[5] = 1u; break;
            case 3: cfreclaimed = 1u; break;
            case 4: fail_trace = 1u; break;
            case 5: export.state = R0FG1X_S_COLD; break;
            case 6: crc ^= 1u; break;
            case 7: registers[0xd011] = 0x10u; break;
            case 8: registers[0xd720] = 1u; break;
            case 9: registers[0xd730] = 1u; break;
            case 10: registers[0xd740] = 1u; break;
            case 11: registers[0xd750] = 1u; break;
            case 12: irq_status = 0u; break;
            case 13: capsule[0] ^= 1u; break;
            case 14: capsule[R0FG1X_GUARD_BYTES + 5u] ^= 1u; break;
            case 15: r0f_pf_nmi_seen = 1u; break;
            default: break;
        }
        uint8_t ok = r0fg1_transport_prepare(sizeof(trace), crc);
        assert(ok == (test == 0u));
        assert(r0fg1_export_status == (test >= 1u && test <= 6u ? 0x6eu : 0x6fu));
        assert(r0fg1_export_permit == (test == 0u ? 0xa5u : 0u));
        if (test == 0u)
        {
            assert(r0fg1_export_bytes == sizeof(trace));
            assert(export.state == R0FG1X_S_EXPORTING);
        }
    }
    uint32_t crc = reset_attempt();
    fail_capsule = 1u;
    assert(!r0fg1_transport_prepare(sizeof(trace), crc));
    assert(r0fg1_export_status == 0x6fu && !r0fg1_export_permit);
    puts("17 terminal transport cases: success, precondition/read/CRC, all audio channels, display, IRQ, capsule guard/CRC/copy and NMI; exact markers and permit gating PASS");
    return 0;
}
