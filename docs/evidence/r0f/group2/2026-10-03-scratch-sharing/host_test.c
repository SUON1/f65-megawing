// Execute exact copied owner definitions; emulate only physical I/O and ROM trap.
#define R0FG1_INTEGRATION
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "combined_platform.h"
#include "group1_export.h"
#include "r0f_group2_scratch.h"
#include "r0f_successor_integration.h"
#include "successor_lifecycle.h"

#define DOS_TO_KERNAL_BACKUP 0u
#define DOS_TO_APPLICATION_BACKUP 1u
#define APPLICATION_BACKUP_TO_DOS 2u
#define KERNAL_BACKUP_TO_DOS 3u
#define DOS_TO_LOCAL 4u
#define LOCAL_TO_DOS 5u
#define GROUP1_SCREEN_CELLS (80u * 25u)

uint8_t r0fg2_foreground_scratch[R0FG2_SCRATCH_BYTES];
static uint8_t block[255], features_open, backup_valid;
static uint8_t result_bytes[512];
volatile uint8_t *const cfresult = result_bytes;
uint8_t cffault, cfreclaimed;
static uint8_t r0fc_trap_flags, r0fc_trap_base;
static volatile uint8_t r0f_pf_copy_request[9];
static uint32_t capsule_crc;
static r0fg1_export export;
static uint8_t rom[R0FC_ROM_BYTES], backup[R0FC_ROM_BYTES];
static uint8_t dos[R0FS_DOS_CONTEXT_BYTES];
static uint8_t dos_kernal[R0FS_DOS_CONTEXT_BYTES];
static uint8_t dos_application[R0FS_DOS_CONTEXT_BYTES];
static uint8_t staging[8192], color[2000];
static uint8_t capsule[R0FG1X_CAPSULE_BYTES], trace[R0FG1X_TRACE_CAPACITY];
static unsigned copies, fail_at, corrupt_at, checks;

struct region
{
    uint32_t address;
    uint8_t *data;
    size_t bytes;
};

static uint8_t *resolve(uint32_t address, uint8_t bytes)
{
    struct region regions[] = {
        {R0FC_ROM, rom, sizeof(rom)}, {R0FC_BACKUP, backup, sizeof(backup)},
        {R0FS_DOS_CONTEXT, dos, sizeof(dos)},
        {R0FS_DOS_KERNAL_ENTRY_BACKUP, dos_kernal, sizeof(dos_kernal)},
        {R0FS_DOS_APPLICATION_BACKUP, dos_application, sizeof(dos_application)},
        {R0FC_STAGING, staging, sizeof(staging)}, {R0FC_COLOR, color, sizeof(color)},
        {R0FG1X_CAPSULE_START, capsule, sizeof(capsule)},
        {R0FG1X_TRACE_START, trace, sizeof(trace)},
        {(uint32_t)(uintptr_t)block, block, sizeof(block)},
        {(uint32_t)(uintptr_t)r0fg2_foreground_scratch,
         r0fg2_foreground_scratch, sizeof(r0fg2_foreground_scratch)}
    };
    uint8_t *found = NULL;
    for (size_t i = 0; i < sizeof(regions) / sizeof(regions[0]); i++)
    {
        if (address >= regions[i].address
            && (uint64_t)address + bytes <= (uint64_t)regions[i].address + regions[i].bytes)
        {
            assert(found == NULL);
            found = regions[i].data + (address - regions[i].address);
        }
    }
    assert(found != NULL);
    return found;
}

static uint8_t r0f_pf_flat_copy(void)
{
    uint32_t source = 0, destination = 0;
    for (uint8_t i = 0; i < 4; i++)
    {
        source |= (uint32_t)r0f_pf_copy_request[i] << (8 * i);
        destination |= (uint32_t)r0f_pf_copy_request[4 + i] << (8 * i);
    }
    uint8_t bytes = r0f_pf_copy_request[8];
    assert(bytes != 0);
    uint8_t *from = resolve(source, bytes);
    uint8_t *to = resolve(destination, bytes);
    assert(from != to);
    copies++;
    if (copies == fail_at)
    {
        return 0;
    }
    memcpy(to, from, bytes);
    if (copies == corrupt_at)
    {
        to[bytes - 1] ^= 1;
    }
    return 1;
}

static uint8_t r0fc_rom_toggle(void)
{
    r0fc_trap_flags = 1;
    r0fc_trap_base = 2;
    return cfreclaimed ? 4 : 0;
}

void cfline(uint8_t row, const char *text)
{
    (void)row;
    (void)text;
}

#include "actual_owners.h"

// Independent bitwise checksum; does not call the production codec.
static uint32_t expected_crc(const uint8_t *data, size_t bytes)
{
    uint32_t value = UINT32_MAX;
    for (size_t i = 0; i < bytes; i++)
    {
        value ^= data[i];
        for (unsigned bit = 0; bit < 8; bit++)
        {
            value = value & 1 ? (value >> 1) ^ 0xedb88320u : value >> 1;
        }
    }
    return ~value;
}

static void handoff(void)
{
    memset(r0fg2_foreground_scratch, 0xda, sizeof(r0fg2_foreground_scratch));
    fail_at = corrupt_at = copies = 0;
    checks++;
}

static void reset_rom(void)
{
    handoff();
    cffault = cfreclaimed = backup_valid = 0;
    memset(result_bytes, 0, sizeof(result_bytes));
    for (size_t i = 0; i < sizeof(rom); i++)
    {
        rom[i] = (uint8_t)(i ^ (i >> 8));
    }
}

int main(void)
{
    reset_rom();
    assert(cfrom_begin());
    assert(memcmp(rom, backup, sizeof(rom)) == 0);
    assert(cfget32(R0FC_O_ROM_CRC) == expected_crc(rom, sizeof(rom)));
    unsigned begin_copies = copies;
    handoff();
    assert(dos_crc(1) == expected_crc(dos, sizeof(dos)));
    for (size_t i = 0; i < sizeof(dos); i++)
    {
        assert(dos[i] == (uint8_t)(i ^ (i >> 8) ^ 0x93));
    }
    handoff();
    assert(display_seed_staging());
    for (size_t i = 0; i < R0FSI_DISPLAY_QUANTUM_BYTES; i++)
    {
        assert(staging[i] == 1);
    }
    handoff();
    memset(rom, 0x73, sizeof(rom));
    assert(cfrom_restore());
    assert(memcmp(rom, backup, sizeof(rom)) == 0);
    assert(!cfreclaimed && !cffault);
    unsigned restore_copies = copies;

    const unsigned begin_failures[] = {1, 2, 3, begin_copies / 2};
    for (size_t i = 0; i < sizeof(begin_failures) / sizeof(begin_failures[0]); i++)
    {
        reset_rom();
        fail_at = begin_failures[i];
        assert(!cfrom_begin() && cffault == 22);
        assert(copies == fail_at);
    }
    reset_rom();
    corrupt_at = 3;
    assert(!cfrom_begin() && cffault == 23 && copies == 3);
    const unsigned restore_failures[] = {1, 2, 3, restore_copies / 2};
    for (size_t i = 0; i < sizeof(restore_failures) / sizeof(restore_failures[0]); i++)
    {
        reset_rom();
        assert(cfrom_begin());
        handoff();
        fail_at = restore_failures[i];
        assert(!cfrom_restore() && cffault == 22 && cfreclaimed);
        assert(copies == fail_at);
    }
    reset_rom();
    assert(cfrom_begin());
    handoff();
    corrupt_at = 3;
    assert(!cfrom_restore() && cffault == 25 && cfreclaimed);
    handoff();
    assert(cfrom_restore());
    assert(!cfcopy(R0FC_BACKUP, block, 1, 1) && cffault == 21);
    cffault = 0;

    for (uint8_t action = 0; action < 6; action++)
    {
        handoff();
        memset(dos, 0x17, sizeof(dos));
        memset(dos_kernal, 0x28, sizeof(dos_kernal));
        memset(dos_application, 0x39, sizeof(dos_application));
        assert(dos_copy(action));
        unsigned count = copies;
        if (action == DOS_TO_KERNAL_BACKUP) assert(dos_kernal[0] == 0x17);
        if (action == DOS_TO_APPLICATION_BACKUP) assert(dos_application[0] == 0x17);
        if (action == APPLICATION_BACKUP_TO_DOS) assert(dos[0] == 0x39);
        if (action == KERNAL_BACKUP_TO_DOS) assert(dos[0] == 0x28);
        if (action == DOS_TO_LOCAL) assert(r0fg2_foreground_scratch[0] == 0x17);
        if (action == LOCAL_TO_DOS) assert(dos[0] == 0xda);
        for (unsigned failure = 1; failure <= count; failure++)
        {
            handoff();
            fail_at = failure;
            assert(!dos_copy(action) && copies == failure);
        }
    }
    assert(!dos_copy(255));
    for (uint8_t write = 0; write < 2; write++)
    {
        handoff();
        assert(dos_crc(write) == expected_crc(dos, sizeof(dos)));
        unsigned count = copies;
        for (unsigned failure = 1; failure <= count; failure++)
        {
            handoff();
            fail_at = failure;
            assert(dos_crc(write) == 0 && copies == failure);
        }
    }
    handoff();
    assert(display_seed_staging());
    unsigned display_copies = copies;
    for (unsigned failure = 1; failure <= display_copies; failure++)
    {
        handoff();
        fail_at = failure;
        assert(!display_seed_staging() && cffault == 22 && copies == failure);
    }
    handoff();
    terminal_colors();
    for (size_t i = 0; i < sizeof(color); i++) assert(color[i] == 1);
    unsigned color_copies = copies;
    for (unsigned failure = 1; failure <= color_copies; failure++)
    {
        handoff();
        fail_at = failure;
        terminal_colors();
        assert(copies == failure && cffault == 22);
    }

    handoff();
    memset(capsule, R0FG1X_GUARD_VALUE, sizeof(capsule));
    for (size_t i = 0; i < R0FG1X_CONTEXT_BYTES; i++) capsule[16 + i] = (uint8_t)i;
    assert(r0fg1_transport_init());
    unsigned capsule_copies = copies;
    for (unsigned failure = 1; failure <= capsule_copies; failure++)
    {
        handoff();
        fail_at = failure;
        assert(!validate_capsule(0) && copies == failure);
    }
    for (unsigned corruption = 1; corruption <= capsule_copies; corruption++)
    {
        handoff();
        corrupt_at = corruption;
        assert(!validate_capsule(0));
    }
    for (unsigned length = 1; length <= 255; length++)
    {
        uint8_t input[255], output[255];
        for (unsigned i = 0; i < length; i++) input[i] = (uint8_t)(i ^ length);
        handoff();
        assert(r0fg1_trace_write(R0FG1X_TRACE_CAPACITY - length, input, length));
        handoff();
        assert(r0fg1_trace_read(R0FG1X_TRACE_CAPACITY - length, output, length));
        assert(memcmp(input, output, length) == 0);
        handoff();
        assert(!r0fg1_trace_write(R0FG1X_TRACE_CAPACITY - length + 1, input, length));
        assert(copies == 0);
        fail_at = 1;
        assert(!r0fg1_trace_write(0, input, length) && copies == 1);
        handoff();
        fail_at = 1;
        memset(output, 0x77, sizeof(output));
        assert(!r0fg1_trace_read(0, output, length));
        for (unsigned i = 0; i < sizeof(output); i++) assert(output[i] == 0x77);
    }
    handoff();
    assert(!transfer(0, 0, 1, 1));
    assert(!transfer(1, UINT32_MAX, 1, 0));
    assert(!transfer(1, 0, 0, 0));
    assert(copies == 0);
    assert(validate_capsule(0));
    printf("PASS: %u poisoned handoffs; ROM, DOS, staging, terminal colors, capsule and trace owners\n", checks);
    return 0;
}
