// Host-only harness: compile the real adapter with fake registers and primitives.
#include <assert.h>
#include <inttypes.h>
#include <stdio.h>
#include <string.h>
#include "combined_platform.h"
#include "guard.h"

static uint8_t registers[65536];
static uint8_t result_bytes[R0FC_RESULT_BYTES];
volatile uint8_t *const cfresult = result_bytes;
uint8_t cffault;
volatile uint8_t r0f_pf_nmi_seen;
volatile uint16_t r0fc_software_low;
volatile uint8_t r0fc_hardware_low;
static unsigned scenario;
static unsigned calls;
static uint32_t samples[18];
static uint8_t reads[256];
static unsigned read_count;
static unsigned read_index;

static volatile uint8_t *host_register(uint16_t address)
{
    if (address == 0xd7fau)
    {
        if (scenario != 6u)
        {
            registers[address] += scenario == 5u ? 2u : 1u;
        }
    }
    if (address >= 0xdc04u && address <= 0xdc07u)
    {
        static const uint16_t order[8] = {
            0xdc07u, 0xdc06u, 0xdc07u, 0xdc05u,
            0xdc04u, 0xdc05u, 0xdc06u, 0xdc07u
        };
        assert(read_index < read_count && address == order[read_index % 8u]);
        return &reads[read_index++];
    }
    return &registers[address];
}

#undef CFREG
#define CFREG(address) (*host_register(address))
#define cfnow frozen_cfnow
#include "sampler.inc"
#undef cfnow

uint8_t cfentry(void)
{
    cfresult[R0FC_O_REFERENCE] = scenario == 7u ? 0u : 1u;
    return 1u;
}

uint8_t cfrom_begin(void) { return 1u; }
uint8_t cfclock_begin(void) { return (uint8_t)(scenario != 1u); }

uint32_t cfnow(void)
{
    assert(calls < 18u);
    if (scenario == 2u || (scenario == 9u && calls == 17u))
    {
        cffault = 3u;
    }
    if (scenario == 3u)
    {
        r0f_pf_nmi_seen = 1u;
    }
    return samples[calls++];
}

uint8_t cfcopy(uint32_t address, uint8_t *bytes, uint8_t count, uint8_t to_chip)
{
    (void)address; (void)bytes; (void)count; (void)to_chip;
    assert(0 && "Clock fixture must not call physical copy");
    return 0u;
}

void cfput16(uint16_t at, uint16_t value) { (void)at; (void)value; }
void r0fc_stack_measure(void) { assert(0 && "No target stack measurement"); }

#include "../../../src/platform/m1/m1_platform.c"

int main(void)
{
    M1Clock local = {0};
    char command;
    while (scanf(" %c", &command) == 1)
    {
        if (command == 'r' || command == 'z')
        {
            if (command == 'r') { m1_clock_reset(&local); }
            else { memset(&local, 0, sizeof(local)); }
            puts("RESET");
        }
        else if (command == 's')
        {
            uint32_t raw;
            unsigned fault;
            assert(scanf("%" SCNu32 " %u", &raw, &fault) == 2);
            uint32_t value = m1_clock_sample(&local, raw, (uint8_t)fault);
            printf("%" PRIu32 " %u %u\n", value, local.fault, local.state);
        }
        else if (command == 'a')
        {
            unsigned video;
            assert(scanf("%u %u", &video, &scenario) == 2);
            for (unsigned i = 0; i < 18; ++i)
            {
                assert(scanf("%" SCNu32, &samples[i]) == 1);
            }
            memset(registers, 0, sizeof(registers));
            registers[0xd06f] = (uint8_t)video;
            cffault = r0f_pf_nmi_seen = 0u;
            calls = 0u;
            uint8_t ok = m1_platform_begin();
            if (scenario == 10u) { cffault = 3u; }
            if (scenario == 11u) { r0f_pf_nmi_seen = 1u; }
            uint32_t now = m1_platform_now();
            printf("%u %" PRIu32 " %" PRIu32 " %u %u\n",
                ok, m1_platform_period(), now, m1_platform_fault(), calls);
        }
        else if (command == 'q')
        {
            assert(scanf("%u", &read_count) == 1 && read_count <= 256u);
            for (unsigned i = 0; i < read_count; ++i)
            {
                unsigned value;
                assert(scanf("%u", &value) == 1 && value <= 255u);
                reads[i] = (uint8_t)value;
            }
            read_index = cffault = 0u;
            uint32_t raw = frozen_cfnow();
            printf("%" PRIu32 " %u %u\n", raw, cffault, read_index);
        }
        else if (command == 'g')
        {
            uint32_t now, release, operation, guard;
            assert(scanf("%" SCNu32 " %" SCNu32 " %" SCNu32 " %" SCNu32,
                         &now, &release, &operation, &guard) == 4);
            printf("%u\n", m2rb_guard(now, release, operation, guard));
        }
        else if (command == 't')
        {
            uint32_t period, release, now;
            unsigned ticks;
            uint16_t fraction = 0u;
            assert(scanf("%" SCNu32 " %" SCNu32 " %u %" SCNu32,
                         &period, &release, &ticks, &now) == 4);
            for (unsigned i = 0; i < ticks; ++i)
            {
                #include "release.inc"
            }
            uint8_t due = (uint8_t)
                #include "due.inc"
                ;
            printf("%" PRIu32 " %u %u\n", release, fraction, due);
        }
        else if (command == 'm')
        {
            printf("%zu %zu\n", sizeof(M1Clock), sizeof(local.phase)
                + sizeof(local.elapsed) + sizeof(local.state) + sizeof(local.fault));
        }
        else { assert(0 && "Unknown host command"); }
    }
    return 0;
}
