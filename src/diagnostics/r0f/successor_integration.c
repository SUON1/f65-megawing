#include <stdint.h>

#include "combined_platform.h"
#include "r0f_successor_integration.h"
#include "successor_lifecycle.h"

// Owns the private T03 workload/storage lifecycle and result record.
#define PROTECTED_DATA __attribute__((section(".r0fs_protected_data")))

#define DOS_TO_KERNAL_BACKUP 0u
#define DOS_TO_APPLICATION_BACKUP 1u
#define APPLICATION_BACKUP_TO_DOS 2u
#define KERNAL_BACKUP_TO_DOS 3u
#define DOS_TO_LOCAL 4u
#define LOCAL_TO_DOS 5u

extern uint8_t r0fs_storage(void);
extern uint8_t r0fs_context_read(void);
extern void r0fs_context_invalidate(void);
extern uint8_t r0f_pf_flat_copy(void);
extern uint8_t r0f_pf_enter(void);
extern void r0f_pf_start_irq(void);
extern void r0f_pf_stop_irq(void);
extern uint8_t r0fc_rom_toggle(void);
extern volatile uint8_t r0f_pf_copy_request[9];
extern volatile uint8_t r0f_pf_cpu_port;
extern volatile uint8_t r0f_pf_stack_high;
extern volatile uint8_t r0fc_trap_flags;
extern volatile uint8_t r0fc_trap_base;

volatile uint8_t r0fsi_permit PROTECTED_DATA;
volatile uint8_t r0fsi_storage_phase PROTECTED_DATA;
volatile uint8_t r0fsi_storage_error PROTECTED_DATA;
volatile uint8_t r0fsi_storage_returned PROTECTED_DATA;
volatile uint8_t r0fsi_storage_denied PROTECTED_DATA;
volatile uint8_t r0fsi_input PROTECTED_DATA;
volatile uint8_t r0fsi_output PROTECTED_DATA;
volatile uint8_t r0fsi_input_end PROTECTED_DATA;
volatile uint8_t r0fsi_output_end PROTECTED_DATA;
volatile uint8_t r0fsi_token[R0FSI_STORAGE_FILE_BYTES] PROTECTED_DATA;
volatile uint8_t r0fsi_read[R0FSI_STORAGE_FILE_BYTES] PROTECTED_DATA;
volatile uint8_t r0fsi_payload[R0FSI_STORAGE_FILE_BYTES] PROTECTED_DATA;
volatile uint8_t r0fsi_end[4] PROTECTED_DATA;
volatile uint8_t r0fsi_app_sp PROTECTED_DATA;
volatile uint16_t r0fsi_context_offset PROTECTED_DATA;
volatile uint8_t r0fsi_context_length PROTECTED_DATA;
volatile uint8_t r0fsi_context_region PROTECTED_DATA;
volatile uint8_t r0fsi_context_copy_ok PROTECTED_DATA;
volatile uint8_t r0fsi_context_buffer[R0FSI_CONTEXT_CHUNK_BYTES]
    PROTECTED_DATA;

static r0fc_model model;
static r0fc_snapshots snapshots;
static uint8_t transfer[255];
static uint8_t display_pixels[64];
static uint8_t display_saved[15];
static const uint16_t display_registers[15] = {
    0xd011u, 0xd031u, 0xd054u, 0xd058u, 0xd059u,
    0xd05au, 0xd05bu, 0xd05eu, 0xd060u, 0xd061u,
    0xd062u, 0xd063u, 0xd064u, 0xd065u, 0xd07bu,
};
static uint8_t lifecycle_state;
static uint8_t display_front;
static uint8_t display_ready;
static uint8_t display_slot;
static uint8_t display_frame;
static uint8_t display_started;
static uint8_t display_suspended;
static uint8_t display_suspended_d011;
static uint8_t application_dma_outstanding;
static uint16_t display_clear_at;
static uint16_t display_services;
static uint32_t display_snapshot_crc;
static uint32_t context_crc_expected;
static uint32_t next_deadline;
static uint32_t low_before_record;
static uint32_t low_after_record;
static uint32_t dos_before_record;
static uint32_t dos_after_record;
static uint32_t checksum_before_record;
static uint16_t tick_before_record;
static uint8_t context_invalidated_record;

static void lockout(uint8_t fault);

static void result_u16(uint16_t offset, uint16_t value)
{
    cfresult[offset] = (uint8_t)value;
    cfresult[offset + 1u] = (uint8_t)(value >> 8u);
}

static void result_u32(uint16_t offset, uint32_t value)
{
    uint8_t index;

    for (index = 0u; index < 4u; index++)
    {
        cfresult[offset + index] = (uint8_t)value;
        value >>= 8u;
    }
}

static uint32_t result_get_u32(uint16_t offset)
{
    uint8_t index = 4u;
    uint32_t value = 0u;

    while (index != 0u)
    {
        value = (value << 8u) | cfresult[offset + --index];
    }
    return value;
}

static uint32_t crc_update(uint32_t crc, const volatile uint8_t *bytes,
                           uint16_t length)
{
    while (length-- != 0u)
    {
        uint8_t bit;

        crc ^= *bytes++;
        for (bit = 0u; bit < 8u; bit++)
        {
            crc = (crc >> 1u)
                ^ ((crc & 1u) != 0u ? 0xedb88320ul : 0u);
        }
    }
    return crc;
}

static uint8_t context_read(uint8_t region, uint16_t offset, uint8_t length)
{
    r0fsi_context_region = region;
    r0fsi_context_offset = offset;
    r0fsi_context_length = length;
    return r0fs_context_read();
}

static uint32_t context_crc(void)
{
    uint16_t offset = 0u;
    uint32_t crc = 0xfffffffful;

    while (offset < R0FS_KERNAL_CONTEXT_BYTES)
    {
        uint16_t remaining = (uint16_t)(R0FS_KERNAL_CONTEXT_BYTES - offset);
        uint8_t length = remaining > R0FSI_CONTEXT_CHUNK_BYTES
            ? R0FSI_CONTEXT_CHUNK_BYTES : (uint8_t)remaining;

        if (!context_read(1u, offset, length))
        {
            return 0u;
        }
        crc = crc_update(crc, r0fsi_context_buffer, length);
        offset = (uint16_t)(offset + length);
    }
    return ~crc;
}

static uint8_t context_valid(uint32_t expected_crc)
{
    uint8_t index;

    if (!context_read(0u, 0u, R0FS_KERNAL_CONTEXT_GUARD_BYTES))
    {
        return 0u;
    }
    for (index = 0u; index < R0FS_KERNAL_CONTEXT_GUARD_BYTES; index++)
    {
        if (r0fsi_context_buffer[index] != R0FS_KERNAL_CONTEXT_GUARD)
        {
            return 0u;
        }
    }
    if (!context_read(2u, 0u, R0FS_KERNAL_CONTEXT_GUARD_BYTES))
    {
        return 0u;
    }
    for (index = 0u; index < R0FS_KERNAL_CONTEXT_GUARD_BYTES; index++)
    {
        if (r0fsi_context_buffer[index] != R0FS_KERNAL_CONTEXT_GUARD)
        {
            return 0u;
        }
    }
    return (uint8_t)(context_crc() == expected_crc);
}

static uint8_t fixed_physical_copy(uint32_t source, uint32_t destination,
                                   uint8_t length)
{
    uint8_t index;

    for (index = 0u; index < 4u; index++)
    {
        r0f_pf_copy_request[index] = (uint8_t)(source >> (index * 8u));
        r0f_pf_copy_request[4u + index] =
            (uint8_t)(destination >> (index * 8u));
    }
    r0f_pf_copy_request[8] = length;
    return r0f_pf_flat_copy();
}

static uint8_t dos_copy(uint8_t action)
{
    uint16_t offset = 0u;

    while (offset < R0FS_DOS_CONTEXT_BYTES)
    {
        uint16_t remaining = (uint16_t)(R0FS_DOS_CONTEXT_BYTES - offset);
        uint8_t length = remaining > 255u ? 255u : (uint8_t)remaining;
        uint32_t source;
        uint32_t destination;

        if (action == DOS_TO_KERNAL_BACKUP)
        {
            source = R0FS_DOS_CONTEXT + offset;
            destination = R0FS_DOS_KERNAL_ENTRY_BACKUP + offset;
        }
        else if (action == DOS_TO_APPLICATION_BACKUP)
        {
            source = R0FS_DOS_CONTEXT + offset;
            destination = R0FS_DOS_APPLICATION_BACKUP + offset;
        }
        else if (action == APPLICATION_BACKUP_TO_DOS)
        {
            source = R0FS_DOS_APPLICATION_BACKUP + offset;
            destination = R0FS_DOS_CONTEXT + offset;
        }
        else if (action == KERNAL_BACKUP_TO_DOS)
        {
            source = R0FS_DOS_KERNAL_ENTRY_BACKUP + offset;
            destination = R0FS_DOS_CONTEXT + offset;
        }
        else if (action == DOS_TO_LOCAL)
        {
            source = R0FS_DOS_CONTEXT + offset;
            destination = (uint32_t)(uintptr_t)transfer;
        }
        else if (action == LOCAL_TO_DOS)
        {
            source = (uint32_t)(uintptr_t)transfer;
            destination = R0FS_DOS_CONTEXT + offset;
        }
        else
        {
            return 0u;
        }
        if (!fixed_physical_copy(source, destination, length))
        {
            return 0u;
        }
        offset = (uint16_t)(offset + length);
    }
    return 1u;
}

static uint32_t dos_crc(uint8_t write_pattern)
{
    uint16_t offset = 0u;
    uint32_t crc = 0xfffffffful;

    while (offset < R0FS_DOS_CONTEXT_BYTES)
    {
        uint16_t remaining = (uint16_t)(R0FS_DOS_CONTEXT_BYTES - offset);
        uint8_t length = remaining > 255u ? 255u : (uint8_t)remaining;
        uint16_t index;

        if (write_pattern)
        {
            for (index = 0u; index < length; index++)
            {
                uint16_t position = (uint16_t)(offset + index);

                transfer[index] =
                    (uint8_t)(position ^ (position >> 8u) ^ 0x93u);
            }
            if (!fixed_physical_copy((uint32_t)(uintptr_t)transfer,
                                     R0FS_DOS_CONTEXT + offset, length))
            {
                return 0u;
            }
        }
        if (!fixed_physical_copy(R0FS_DOS_CONTEXT + offset,
                                 (uint32_t)(uintptr_t)transfer, length))
        {
            return 0u;
        }
        crc = crc_update(crc, transfer, length);
        offset = (uint16_t)(offset + length);
    }
    return ~crc;
}

static uint8_t low_application_copy(uint8_t restore)
{
    uint16_t offset = 0u;

    while (offset < R0FS_LOW_APPLICATION_BYTES)
    {
        uint16_t remaining =
            (uint16_t)(R0FS_LOW_APPLICATION_BYTES - offset);
        uint8_t length = remaining > 255u ? 255u : (uint8_t)remaining;

        if (!cfcopy(R0FS_LOW_APPLICATION_BACKUP + offset,
                    (uint8_t *)(uintptr_t)(R0FS_LOW_APPLICATION_START + offset),
                    length, (uint8_t)!restore))
        {
            return 0u;
        }
        offset = (uint16_t)(offset + length);
    }
    return 1u;
}

static void display_configure(void)
{
    CFREG(0xd031u) &= 0x7fu;
    CFREG(0xd054u) |= 7u;
    CFREG(0xd058u) = 80u;
    CFREG(0xd059u) = 0u;
    CFREG(0xd05eu) = 40u;
    CFREG(0xd060u) = 0u;
    CFREG(0xd061u) = 0xc0u;
    CFREG(0xd062u) = 1u;
    CFREG(0xd063u) = 0u;
    CFREG(0xd064u) = 0u;
    CFREG(0xd065u) = 0u;
    CFREG(0xd07bu) = 25u;
    display_frame = CFREG(0xd7fau);
}

static uint8_t application_dma(uint32_t source, uint32_t destination,
                               uint16_t length)
{
    uint8_t ok;

    if (application_dma_outstanding)
    {
        cffault = 89u;
        return 0u;
    }
    application_dma_outstanding = 1u;
    ok = cfdma(source, destination, length);
    application_dma_outstanding = 0u;
    return ok;
}

static void display_begin(void)
{
    uint8_t index;
    uint32_t offset;

    for (index = 0u; index < 15u; index++)
    {
        display_saved[index] = CFREG(display_registers[index]);
    }
    CFREG(0xd011u) &= 0xefu;
    for (index = 0u; index < 255u; index++)
    {
        transfer[index] = 1u;
    }
    for (offset = 0u; offset < 4096u; offset += 255u)
    {
        uint32_t remaining = 4096u - offset;
        uint8_t length = remaining > 255u ? 255u : (uint8_t)remaining;

        (void)cfcopy(R0FC_STAGING + offset, transfer, length, 1u);
    }
    display_front = 0u;
    display_ready = 0u;
    display_slot = R0FC_SNAPSHOT_COUNT;
    display_clear_at = 0u;
    display_services = 0u;
    display_suspended = 0u;
    application_dma_outstanding = 0u;
    display_started = 1u;
    display_configure();
    CFREG(0xd011u) = display_saved[0];
}

static void display_restore(void)
{
    uint8_t index;

    CFREG(0xd011u) &= 0xefu;
    for (index = 1u; index < 15u; index++)
    {
        CFREG(display_registers[index]) = display_saved[index];
    }
    CFREG(0xd011u) = display_saved[0];
}

static void display_quantum(void)
{
    uint8_t index;
    uint8_t frame = CFREG(0xd7fau);
    uint32_t destination = display_front ? R0FC_ROM : R0FC_ROM + 0x10000ul;

    if (frame != display_frame)
    {
        display_frame = frame;
        if (display_ready)
        {
            uint32_t screen = display_front ? R0FC_ROM : R0FC_ROM + 0x10000ul;

            CFREG(0xd060u) = (uint8_t)screen;
            CFREG(0xd061u) = (uint8_t)(screen >> 8u);
            CFREG(0xd062u) = (uint8_t)(screen >> 16u);
            display_front ^= 1u;
            display_ready = 0u;
        }
    }
    if (display_ready)
    {
        return;
    }
    if (display_slot == R0FC_SNAPSHOT_COUNT)
    {
        display_slot = r0fc_acquire(&snapshots);
        if (display_slot == R0FC_SNAPSHOT_COUNT)
        {
            return;
        }
        display_snapshot_crc =
            cfcrc(snapshots.data[display_slot], R0FC_SNAPSHOT_BYTES);
        display_clear_at = 0u;
    }
    if (display_clear_at < R0FSI_DISPLAY_BUFFER_BYTES)
    {
        if (!application_dma(R0FC_STAGING, destination + display_clear_at,
                             R0FSI_DISPLAY_QUANTUM_BYTES))
        {
            return;
        }
        display_clear_at =
            (uint16_t)(display_clear_at + R0FSI_DISPLAY_QUANTUM_BYTES);
        return;
    }
    for (index = 0u; index < sizeof(display_pixels); index++)
    {
        display_pixels[index] =
            snapshots.data[display_slot][index] == 0u ? 1u : 5u;
    }
    for (index = 0u; index < 9u; index++)
    {
        uint32_t offset = (uint32_t)index * 64u;

        if (!cfcopy(destination + offset, display_pixels,
                    sizeof(display_pixels), 1u))
        {
            return;
        }
    }
    if (cfcrc(snapshots.data[display_slot], R0FC_SNAPSHOT_BYTES)
        != display_snapshot_crc)
    {
        cffault = 70u;
        return;
    }
    r0fc_release(&snapshots);
    display_slot = R0FC_SNAPSHOT_COUNT;
    display_ready = 1u;
    display_services++;
}

static uint8_t display_drain(void)
{
    uint8_t quanta;

    for (quanta = 0u; quanta < 17u
         && display_slot != R0FC_SNAPSHOT_COUNT; quanta++)
    {
        display_quantum();
    }
    return (uint8_t)(display_slot == R0FC_SNAPSHOT_COUNT && !cffault);
}

static uint8_t display_suspend(void)
{
    if (display_slot != R0FC_SNAPSHOT_COUNT
        || application_dma_outstanding || display_suspended)
    {
        return 0u;
    }
    display_suspended_d011 = CFREG(0xd011u);
    CFREG(0xd011u) = (uint8_t)(display_suspended_d011 & 0xefu);
    display_suspended = 1u;
    return 1u;
}

static uint8_t display_resume(void)
{
    if (!display_suspended || application_dma_outstanding)
    {
        return 0u;
    }
    display_configure();
    CFREG(0xd011u) = display_suspended_d011;
    display_suspended = 0u;
    return 1u;
}

static uint8_t restore_rom_after_display_suspend(void)
{
    if (!display_suspended || application_dma_outstanding)
    {
        return 0u;
    }
    return cfrom_restore();
}

static void display_abandon_and_suspend(void)
{
    if (display_slot < R0FC_SNAPSHOT_COUNT)
    {
        r0fc_release(&snapshots);
        display_slot = R0FC_SNAPSHOT_COUNT;
    }
    display_ready = 0u;
    if (!display_suspended)
    {
        display_suspended_d011 = CFREG(0xd011u);
        CFREG(0xd011u) = (uint8_t)(display_suspended_d011 & 0xefu);
        display_suspended = 1u;
    }
}

static uint8_t run_authoritative_tick(void)
{
    uint32_t now;
    uint8_t snapshot;

    if (r0f_pf_nmi_seen)
    {
        lockout(90u);
        return 0u;
    }
    do
    {
        now = cfnow();
        if ((int32_t)(now - next_deadline) < 0)
        {
            display_quantum();
            cfinput();
            cfaudio_service(0u);
            if (r0f_pf_nmi_seen)
            {
                lockout(91u);
                return 0u;
            }
        }
    }
    while ((int32_t)(now - next_deadline) < 0 && !cffault);
    if (cffault)
    {
        return 0u;
    }
    cfinput_tick(0u);
    r0fc_tick(&model);
    snapshot = r0fc_publish(&snapshots, &model);
    if (snapshot < R0FC_SNAPSHOT_COUNT)
    {
        (void)cfcopy(R0FC_SNAPSHOTS
                     + (uint32_t)snapshot * R0FC_SNAPSHOT_BYTES,
                     snapshots.data[snapshot], R0FC_SNAPSHOT_BYTES, 1u);
    }
    display_quantum();
    cfinput();
    cfaudio_service(0u);
    if (r0f_pf_nmi_seen)
    {
        lockout(92u);
        return 0u;
    }
    next_deadline += cfperiod >> 16u;
    return (uint8_t)!cffault;
}

static uint8_t run_ticks(uint8_t count)
{
    uint8_t index;

    for (index = 0u; index < count; index++)
    {
        if (!run_authoritative_tick())
        {
            return 0u;
        }
    }
    return 1u;
}

static uint8_t reclaim_after_storage(void)
{
    uint8_t features = r0fc_rom_toggle();

    if (!(r0fc_trap_flags & 1u) || r0fc_trap_base != 2u
        || (features & 4u) != 0u)
    {
        return 0u;
    }
    cfreclaimed = 1u;
    return 1u;
}

static void lockout(uint8_t fault)
{
    cffault = fault;
    lifecycle_state = R0FS_S_LOCKOUT;
    cfaudio_stop();
    r0f_pf_stop_irq();
}

static uint8_t transition(uint8_t event)
{
    lifecycle_state = r0fs_transition(lifecycle_state, event);
    if (lifecycle_state == R0FS_S_LOCKOUT)
    {
        lockout(71u);
        return 0u;
    }
    return 1u;
}

static uint8_t storage_transition(void)
{
    uint16_t tick_before = model.tick;
    uint32_t checksum_before = model.checksum;
    uint32_t low_before;
    uint32_t low_after;
    uint32_t dos_before;
    uint32_t dos_after;
    uint8_t index;

    if (!display_drain() || !display_suspend()
        || !transition(R0FS_E_QUIESCE))
    {
        return 0u;
    }
    cfaudio_stop();
    r0f_pf_stop_irq();
    if (r0f_pf_nmi_seen)
    {
        lockout(72u);
        return 0u;
    }
    if (!restore_rom_after_display_suspend()
        || !transition(R0FS_E_RESTORE_ROM))
    {
        lockout(73u);
        return 0u;
    }
    if (!context_valid(context_crc_expected))
    {
        lockout(74u);
        return 0u;
    }
    low_before = cfcrc((const volatile uint8_t *)(uintptr_t)
                       R0FS_LOW_APPLICATION_START,
                       R0FS_LOW_APPLICATION_BYTES);
    dos_before = dos_crc(0u);
    if (!low_application_copy(0u)
        || !dos_copy(DOS_TO_APPLICATION_BACKUP)
        || !dos_copy(KERNAL_BACKUP_TO_DOS)
        || !transition(R0FS_E_SAVE_APPLICATION))
    {
        lockout(75u);
        return 0u;
    }
    if (!r0fs_storage_allowed(lifecycle_state, 1u, 1u, 1u, 1u,
                              r0f_pf_nmi_seen)
        || !transition(R0FS_E_ENTER_KERNAL))
    {
        lockout(76u);
        return 0u;
    }
    for (index = 0u; index < R0FSI_STORAGE_FILE_BYTES; index++)
    {
        r0fsi_payload[index] =
            (uint8_t)((checksum_before >> ((index & 3u) * 8u)) ^ index);
    }
    r0fsi_permit = R0FSI_STORAGE_PERMIT;
    (void)r0fs_storage();
    if (r0fsi_storage_phase != 5u || r0fsi_storage_error != 0u
        || !r0fsi_storage_returned || r0fsi_input != 0u
        || r0fsi_output != 3u || r0fsi_input_end != 0u
        || r0fsi_output_end != 3u || r0f_pf_nmi_seen)
    {
        lockout(77u);
        return 0u;
    }
    for (index = 0u; index < R0FSI_STORAGE_FILE_BYTES; index++)
    {
        if (r0fsi_read[index] != r0fsi_payload[index]
            || r0fsi_token[index] != (uint8_t)(index ^ 0x65u))
        {
            lockout(78u);
            return 0u;
        }
    }
    if (!transition(R0FS_E_FINISH_STORAGE)
        || !context_valid(context_crc_expected)
        || !transition(R0FS_E_RESTORE_KERNAL_CONTEXT)
        || !dos_copy(APPLICATION_BACKUP_TO_DOS)
        || !low_application_copy(1u)
        || !transition(R0FS_E_RESTORE_APPLICATION))
    {
        lockout(79u);
        return 0u;
    }
    low_after = cfcrc((const volatile uint8_t *)(uintptr_t)
                      R0FS_LOW_APPLICATION_START,
                      R0FS_LOW_APPLICATION_BYTES);
    dos_after = dos_crc(0u);
    if (low_before != low_after || dos_before != dos_after
        || model.tick != tick_before || model.checksum != checksum_before
        || r0f_pf_enter() != 2u || r0f_pf_cpu_port != 0x35u)
    {
        lockout(80u);
        return 0u;
    }
    r0fs_context_invalidate();
    context_invalidated_record = 1u;
    if (r0f_pf_nmi_seen
        || !r0fs_resume_allowed(lifecycle_state, 1u, 1u, 0u)
        || !transition(R0FS_E_RESUME_SERVICES)
        || !reclaim_after_storage())
    {
        lockout(81u);
        return 0u;
    }
    if (!display_resume())
    {
        lockout(93u);
        return 0u;
    }
    cfaudio_begin();
    if (!cfclock_begin())
    {
        lockout(82u);
        return 0u;
    }
    if (r0f_pf_nmi_seen)
    {
        lockout(94u);
        return 0u;
    }
    next_deadline = cfnow() + (cfperiod >> 16u);
    tick_before_record = tick_before;
    checksum_before_record = checksum_before;
    low_before_record = low_before;
    low_after_record = low_after;
    dos_before_record = dos_before;
    dos_after_record = dos_after;
    return 1u;
}

int main(void)
{
    uint16_t index;
    uint32_t reserve_before = 0u;
    uint32_t reserve_after;
    uint32_t rom_crc;
    uint32_t restore_crc;
    uint32_t input_before = 0u;
    uint32_t input_after = 0u;
    uint32_t audio_before = 0u;
    uint32_t audio_after = 0u;
    uint32_t snapshots_before = 0u;
    uint32_t snapshots_after = 0u;
    uint16_t irq_before = 0u;
    uint16_t irq_after = 0u;
    uint16_t dma_before = 0u;
    uint16_t dma_after = 0u;
    uint16_t display_before = 0u;
    uint16_t display_after = 0u;
    uint8_t stage = 1u;
    uint8_t resumed_service_mask = 0u;

    for (index = 0u; index < R0FSI_RESULT_BYTES; index++)
    {
        cfresult[index] = 0u;
    }
    cfresult[0] = 'R';
    cfresult[1] = 'S';
    cfresult[2] = 'I';
    cfresult[3] = '1';
    if (!cfentry())
    {
        lockout(83u);
        goto finish;
    }
    lifecycle_state = R0FS_S_PRE_C_CAPTURED;
    cfscreen();
    context_crc_expected = context_crc();
    if (!context_crc_expected || !context_valid(context_crc_expected)
        || !dos_copy(DOS_TO_KERNAL_BACKUP) || !dos_crc(1u)
        || !transition(R0FS_E_ACTIVATE))
    {
        lockout(84u);
        goto finish;
    }
    reserve_before = cfphysical_crc(R0FS_MEASURED_RESERVE,
                                    R0FS_MEASURED_RESERVE_BYTES);
    if (!cfrom_begin() || !cfclock_begin() || !cfcalibrate(0u))
    {
        lockout(85u);
        goto finish;
    }
    r0fc_reset(&model);
    r0fc_snap_reset(&snapshots);
    display_begin();
    cfaudio_begin();
    next_deadline = cfnow() + (cfperiod >> 16u);
    stage = 2u;
    if (!run_ticks(R0FSI_PRE_STORAGE_TICKS))
    {
        lockout(86u);
        goto finish;
    }
    irq_before = r0f_pf_irq_count;
    dma_before = (uint16_t)cfget32(R0FC_O_DMA_JOBS);
    input_before = cfget32(R0FC_O_INPUT_SAMPLES);
    audio_before = cfget32(R0FC_O_AUDIO_SERVICES);
    snapshots_before = snapshots.published;
    display_before = display_services;
    stage = 3u;
    if (!storage_transition())
    {
        goto finish;
    }
    stage = 4u;
    if (!run_ticks(R0FSI_POST_STORAGE_TICKS))
    {
        lockout(87u);
        goto finish;
    }
    irq_after = r0f_pf_irq_count;
    dma_after = (uint16_t)cfget32(R0FC_O_DMA_JOBS);
    input_after = cfget32(R0FC_O_INPUT_SAMPLES);
    audio_after = cfget32(R0FC_O_AUDIO_SERVICES);
    snapshots_after = snapshots.published;
    display_after = display_services;
    if (display_after > display_before)
    {
        resumed_service_mask |= R0FSI_SERVICE_DISPLAY;
    }
    if (audio_after > audio_before)
    {
        resumed_service_mask |= R0FSI_SERVICE_AUDIO;
    }
    if (input_after > input_before)
    {
        resumed_service_mask |= R0FSI_SERVICE_INPUT;
    }
    if (irq_after > irq_before)
    {
        resumed_service_mask |= R0FSI_SERVICE_IRQ;
    }
    if (dma_after > dma_before)
    {
        resumed_service_mask |= R0FSI_SERVICE_DMA;
    }
    stage = 5u;

finish:
    cfaudio_stop();
    r0f_pf_stop_irq();
    if (cfreclaimed)
    {
        display_abandon_and_suspend();
        (void)restore_rom_after_display_suspend();
    }
    if (display_started)
    {
        display_restore();
    }
    reserve_after = cfphysical_crc(R0FS_MEASURED_RESERVE,
                                   R0FS_MEASURED_RESERVE_BYTES);
    rom_crc = cfget32(R0FC_O_ROM_CRC);
    restore_crc = cfget32(R0FC_O_RESTORE_CRC);
    for (index = 0u; index < R0FSI_RESULT_BYTES; index++)
    {
        cfresult[index] = 0u;
    }
    cfresult[0] = 'R';
    cfresult[1] = 'S';
    cfresult[2] = 'I';
    cfresult[3] = '1';
    cfresult[R0FSI_O_VERSION] = 1u;
    cfresult[R0FSI_O_STAGE] = stage;
    result_u16(R0FSI_O_TICK_BEFORE, tick_before_record);
    result_u16(R0FSI_O_TICK_AFTER, model.tick);
    result_u32(R0FSI_O_CHECKSUM_BEFORE, checksum_before_record);
    result_u32(R0FSI_O_CHECKSUM_AFTER, model.checksum);
    result_u32(R0FSI_O_CONTEXT_CRC, context_crc_expected);
    result_u32(R0FSI_O_ROM_CRC, rom_crc);
    result_u32(R0FSI_O_RESTORE_CRC, restore_crc);
    result_u32(R0FSI_O_RESERVE_BEFORE, reserve_before);
    result_u32(R0FSI_O_RESERVE_AFTER, reserve_after);
    result_u32(R0FSI_O_LOW_BEFORE, low_before_record);
    result_u32(R0FSI_O_LOW_AFTER, low_after_record);
    result_u32(R0FSI_O_DOS_BEFORE, dos_before_record);
    result_u32(R0FSI_O_DOS_AFTER, dos_after_record);
    cfresult[R0FSI_O_STORAGE_PHASE] = r0fsi_storage_phase;
    cfresult[R0FSI_O_STORAGE_ERROR] = r0fsi_storage_error;
    cfresult[R0FSI_O_STORAGE_RETURNED] = r0fsi_storage_returned;
    cfresult[R0FSI_O_STORAGE_DENIED] = r0fsi_storage_denied;
    result_u16(R0FSI_O_IRQ_BEFORE, irq_before);
    result_u16(R0FSI_O_IRQ_AFTER, irq_after);
    result_u16(R0FSI_O_DMA_BEFORE, dma_before);
    result_u16(R0FSI_O_DMA_AFTER, dma_after);
    result_u32(R0FSI_O_INPUT_BEFORE, input_before);
    result_u32(R0FSI_O_INPUT_AFTER, input_after);
    result_u32(R0FSI_O_AUDIO_BEFORE, audio_before);
    result_u32(R0FSI_O_AUDIO_AFTER, audio_after);
    result_u32(R0FSI_O_SNAPSHOTS_BEFORE, snapshots_before);
    result_u32(R0FSI_O_SNAPSHOTS_AFTER, snapshots_after);
    cfresult[R0FSI_O_CANONICAL_BASE_PAGE] = r0f_pf_enter();
    cfresult[R0FSI_O_CANONICAL_PORT] = r0f_pf_cpu_port;
    cfresult[R0FSI_O_CONTEXT_INVALIDATED] = context_invalidated_record;
    cfresult[R0FSI_O_RESUMED_SERVICE_MASK] = resumed_service_mask;
    cfresult[R0FSI_O_NMI_STICKY] = r0f_pf_nmi_seen;
    cfresult[R0FSI_O_LIFECYCLE] = lifecycle_state;
    cfresult[R0FSI_O_FAULT] = cffault;
    if (reserve_before == reserve_after
        && r0fs_completion_allowed(
            lifecycle_state, r0f_pf_nmi_seen, cffault,
            resumed_service_mask,
            R0FSI_SERVICE_DISPLAY | R0FSI_SERVICE_AUDIO
                | R0FSI_SERVICE_INPUT | R0FSI_SERVICE_IRQ
                | R0FSI_SERVICE_DMA)
        && model.tick == R0FSI_PRE_STORAGE_TICKS
                         + R0FSI_POST_STORAGE_TICKS)
    {
        cfresult[R0FSI_O_STAGE] = 127u;
    }
    else if (!cffault)
    {
        lockout(88u);
        cfresult[R0FSI_O_FAULT] = cffault;
        cfresult[R0FSI_O_LIFECYCLE] = lifecycle_state;
    }
    result_u32(R0FSI_O_CRC32,
               cfcrc(cfresult, R0FSI_O_CRC32));
    cffinal_screen();
    cfscreen();
    cfline(5u, cffault ? "SUCCESSOR LOCKOUT - NO ACCEPTANCE"
                       : "SUCCESSOR HOST/STATIC IMAGE - RUNTIME UNVERIFIED");
    cfline(7u, "NO D81 / XEMU / SD / HARDWARE / R0-F ACCEPTANCE");
    cfhex(9u, 0u, cffault, 2u);
    cfhex(9u, 8u, lifecycle_state, 2u);
    cfhex(9u, 16u, model.tick, 4u);
    cfhex(9u, 24u, result_get_u32(R0FSI_O_CRC32), 8u);
    for (;;)
    {
    }
}
