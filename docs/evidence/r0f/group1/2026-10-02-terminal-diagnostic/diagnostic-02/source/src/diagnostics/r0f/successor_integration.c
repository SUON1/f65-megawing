#include <stdint.h>

#include "combined_platform.h"
#include "r0f_successor_integration.h"
#include "successor_capture.h"
#include "successor_irq.h"
#include "successor_lifecycle.h"

#if defined(R0FG1_EXPORT_QUALIFICATION) || defined(R0FG1_INTEGRATION)
extern uint8_t r0fg1_export_probe_init(void);
extern uint8_t r0fg1_export_probe_prepare(void);
extern void r0fg1_terminal_export(void) __attribute__((noreturn));
#endif

#ifdef R0FG1_INTEGRATION
#include "group1_capture.h"
#include "group1_scene.h"
#define ACTIVE_PRE_TICKS (R0FG1_PHASES * R0FG1_TICKS_PER_PHASE)
#define ACTIVE_POST_TICKS ACTIVE_PRE_TICKS
#define GROUP1_SCREEN_CELLS (80u * 25u)
#define GROUP1_ROM_FONT (R0FC_ROM + 0xd000ul)
#define GROUP1_DISPLAY_COPY_BEGIN (R0FSI_DISPLAY_BUFFER_BYTES + 1u)
#define GROUP1_DISPLAY_COMPLETE (GROUP1_DISPLAY_COPY_BEGIN + R0FG1P_SCENE_COPIES)
#define GROUP1_DISPLAY_DRAIN_QUANTA (R0FSI_DISPLAY_BUFFER_BYTES \
    / R0FSI_DISPLAY_QUANTUM_BYTES + R0FG1P_SCENE_COPIES + 2u)
static uint8_t capture_epoch;
static uint16_t display_source_tick;
static r0fg1_presentation display_presentation;
static uint16_t display_request_tick, display_requests, display_cancels;
static uint8_t display_views, display_tiers;
static uint32_t display_registration_crc;
#else
#define ACTIVE_PRE_TICKS R0FSI_PRE_STORAGE_TICKS
#define ACTIVE_POST_TICKS R0FSI_POST_STORAGE_TICKS
#endif

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
#ifdef R0FG1_INTEGRATION
static uint8_t display_pixels[R0FG1P_SCENE_BYTES];
#else
static uint8_t display_pixels[64];
#endif
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
static uint8_t iec_before_record = 0xffu;
static uint8_t iec_after_record = 0xffu;
static uint8_t reclaim_features_record = 0xffu;
static uint8_t irq_observation[8] = {
    0xffu, 0xffu, 0xffu, 0xffu, 0xffu, 0xffu, 0xffu, 0xffu,
};

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

#ifndef R0FG1_INTEGRATION
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
#endif

static uint32_t crc_update(uint32_t crc, const volatile uint8_t *bytes,
                           uint16_t length)
{
    // One ordered volatile read per byte, using the shared private CRC codec.
    return r0fs_crc32_update(crc, bytes, length);
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
#ifdef R0FG1_INTEGRATION
    CFREG(0xd061u) = 0u;
    CFREG(0xd062u) = (uint8_t)((R0FC_ROM >> 16u) + display_front);
#else
    CFREG(0xd061u) = 0xc0u;
    CFREG(0xd062u) = 1u;
#endif
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

#ifdef R0FG1_INTEGRATION
static uint8_t display_seed_staging(void)
{
    for (uint8_t index = 0u; index < sizeof(transfer); index++)
    {
        transfer[index] = 1u;
    }
    for (uint16_t offset = 0u; offset < R0FSI_DISPLAY_QUANTUM_BYTES;)
    {
        uint16_t remaining = (uint16_t)(R0FSI_DISPLAY_QUANTUM_BYTES - offset);
        uint8_t length = remaining > sizeof(transfer)
            ? sizeof(transfer) : (uint8_t)remaining;
        if (!cfcopy(R0FC_STAGING + offset, transfer, length, 1u))
        {
            return 0u;
        }
        offset = (uint16_t)(offset + length);
    }
    return 1u;
}
#endif

static void display_begin(void)
{
    uint8_t index;
#ifndef R0FG1_INTEGRATION
    uint32_t offset;
#endif

    for (index = 0u; index < 15u; index++)
    {
        display_saved[index] = CFREG(display_registers[index]);
    }
    CFREG(0xd011u) &= 0xefu;
#ifdef R0FG1_INTEGRATION
    if (!display_seed_staging())
    {
        return;
    }
#else
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
#endif
    display_front = 0u;
#ifdef R0FG1_INTEGRATION
    r0fg1_presentation_init(&display_presentation);
#endif
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

#ifdef R0FG1_INTEGRATION
static void display_quantum_work(void)
#else
static void display_quantum(void)
#endif
{
#ifndef R0FG1_INTEGRATION
    uint8_t index;
#endif
    uint8_t frame = CFREG(0xd7fau);
    uint32_t destination = display_front ? R0FC_ROM : R0FC_ROM + 0x10000ul;

#ifdef R0FG1_INTEGRATION
    uint8_t view = (uint8_t)((model.tick >> R0FG1P_VIEW_TICK_SHIFT) & 1u);
    if (view != display_presentation.requested_view)
    {
        if (!r0fg1_view_request(&display_presentation, view)
            || display_requests == UINT16_MAX)
        {
            cffault = 113u;
            return;
        }
        display_request_tick = model.tick;
        display_requests++;
        if (display_presentation.busy)
        {
            if (display_cancels == UINT16_MAX)
            {
                cffault = 113u;
                return;
            }
            r0fg1_presentation_cancel(&display_presentation);
            if (display_slot < R0FC_SNAPSHOT_COUNT)
            {
                r0fc_release(&snapshots);
                display_slot = R0FC_SNAPSHOT_COUNT;
            }
            display_ready = 0u;
            display_cancels++;
        }
    }
#endif
    if (frame != display_frame)
    {
        display_frame = frame;
        if (display_ready)
        {
            uint32_t screen = display_front ? R0FC_ROM : R0FC_ROM + 0x10000ul;

#ifdef R0FG1_INTEGRATION
            if (!r0fg1_presentation_swap(&display_presentation))
            {
                cffault = 113u;
                return;
            }
#endif
            // The two stores share pointer low/mid bytes: only $D062 changes.
            // No IRQ reads the foreground registration/composition state.
            CFREG(0xd060u) = (uint8_t)screen;
            CFREG(0xd061u) = (uint8_t)(screen >> 8u);
            CFREG(0xd062u) = (uint8_t)(screen >> 16u);
#ifdef R0FG1_INTEGRATION
            const r0fg1_presentation_key *key = &display_presentation.displayed.key;
            uint8_t anchor_mask = 0u;
            for (uint8_t anchor = 0u;
                 anchor < display_presentation.displayed.anchor_count; anchor++)
            {
                uint16_t handle = display_presentation.displayed.anchors[anchor].handle;
                if (handle >= R0FG1P_SCENE_CANDIDATES)
                {
                    cffault = 113u;
                    return;
                }
                anchor_mask |= (uint8_t)(1u << handle);
            }
            display_views |= (uint8_t)(1u << key->view);
            display_tiers |= (uint8_t)(1u << key->tier);
            r0fg1_world(key->source_tick, display_request_tick,
                (uint8_t)(key->view | (uint8_t)(key->tier << 1u)
                    | (uint8_t)(key->buffer << 2u)), anchor_mask,
                display_registration_crc);
#endif
            display_front ^= 1u;
            // The swap changed front: the next clear belongs to the other
            // store, not the buffer that was just published.
            destination ^= 0x10000ul;
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
#ifdef R0FG1_INTEGRATION
        display_source_tick = (uint16_t)(snapshots.data[display_slot][0]
            | (uint16_t)snapshots.data[display_slot][1] << 8u);
        if (!r0fg1_scene_bind(&display_presentation, display_source_tick,
                             (uint8_t)(display_front ^ 1u)))
        {
            cffault = 113u;
            return;
        }
#endif
        // This owner holds ordinary RAM buffers. Reuse the qualified compact
        // CRC; volatile hardware/low-memory checks keep their existing path.
        display_snapshot_crc =
#ifdef R0FG1_INTEGRATION
            r0fs_crc32(snapshots.data[display_slot], R0FC_SNAPSHOT_BYTES);
#else
            cfcrc(snapshots.data[display_slot], R0FC_SNAPSHOT_BYTES);
#endif
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
#ifdef R0FG1_INTEGRATION
    if (display_clear_at == R0FSI_DISPLAY_BUFFER_BYTES)
    {
        if (!r0fg1_scene_encode(&display_presentation, display_pixels))
        {
            cffault = 113u;
            return;
        }
        display_registration_crc = r0fs_crc32(display_pixels, sizeof(display_pixels));
        display_clear_at++;
        return;
    }
    if (display_clear_at < GROUP1_DISPLAY_COMPLETE)
    {
        // Nine complete fixture copies; their bounds come from the contract.
        uint16_t offset = (uint16_t)((display_clear_at - GROUP1_DISPLAY_COPY_BEGIN)
            * sizeof(display_pixels));
        if (cfcopy(destination + offset, display_pixels, sizeof(display_pixels), 1u))
        {
            display_clear_at++;
        }
    }
    if (display_clear_at != GROUP1_DISPLAY_COMPLETE)
    {
        return;
    }
    // The last synchronous copy completes the buffer. Check the retained
    // snapshot and matching registration now, without an empty extra
    // quantum; publication still waits for a later frame boundary above.
#else
    for (index = 0u; index < sizeof(display_pixels); index++)
    {
        display_pixels[index] =
            snapshots.data[display_slot][index] == 0u ? 1u : 5u;
    }
    for (index = 0u; index < 9u; index++)
    {
        uint32_t offset = (uint32_t)index * sizeof(display_pixels);

        if (!cfcopy(destination + offset, display_pixels,
                    sizeof(display_pixels), 1u))
        {
            return;
        }
    }
#endif
    if (
#ifdef R0FG1_INTEGRATION
        r0fs_crc32(snapshots.data[display_slot], R0FC_SNAPSHOT_BYTES)
#else
        cfcrc(snapshots.data[display_slot], R0FC_SNAPSHOT_BYTES)
#endif
        != display_snapshot_crc)
    {
        cffault = 70u;
        return;
    }
    r0fc_release(&snapshots);
    display_slot = R0FC_SNAPSHOT_COUNT;
#ifdef R0FG1_INTEGRATION
    if (!r0fg1_presentation_complete(&display_presentation,
                                     &display_presentation.building.key, 1u))
    {
        cffault = 113u;
        return;
    }
#endif
    display_ready = 1u;
    display_services++;
}

#ifdef R0FG1_INTEGRATION
void r0fg1_display_metrics(void)
{
    r0fg1_presentation_metrics(display_presentation.anchor_high,
        display_presentation.occlusion_high, display_presentation.anchor_drops,
        display_requests, display_cancels, display_views, display_tiers);
}

static void display_quantum(void)
{
    uint32_t start = cfnow();
    display_quantum_work();
    r0fg1_service(2u, start);
}

static void group1_input_service(void)
{
    uint32_t start = cfnow();
    cfinput();
    r0fg1_service(0u, start);
}

static void group1_audio_service(void)
{
    uint32_t start = cfnow();
    cfaudio_service(0u);
    r0fg1_service(1u, start);
}

static const uint8_t group1_orders[6][3] = {
    {2u, 0u, 1u}, {2u, 1u, 0u}, {0u, 2u, 1u},
    {0u, 1u, 2u}, {1u, 2u, 0u}, {1u, 0u, 2u},
};
static uint8_t group1_order;

static void group1_service_sweep(void)
{
    for (uint8_t index = 0u; index < 3u; index++)
    {
        switch (group1_orders[group1_order][index])
        {
        case 0u:
            group1_input_service();
            break;
        case 1u:
            group1_audio_service();
            break;
        default:
            display_quantum();
            break;
        }
    }
    r0fg1_service_order(group1_order);
}
#endif

static uint8_t display_drain(void)
{
    uint8_t quanta;

    for (quanta = 0u; quanta <
#ifdef R0FG1_INTEGRATION
         GROUP1_DISPLAY_DRAIN_QUANTA
#else
         17u
#endif
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
        // Every rejecting path supplies its cause to the resume caller.
        cffault = 93u;
        return 0u;
    }
#ifdef R0FG1_INTEGRATION
    // ROM restoration destroyed both pixel stores. Discard the ready attempt
    // and display an explicit unregistered fallback, never stale registration.
    // Low-application backup is already restored; staging can be seeded again.
    r0fg1_presentation_cancel(&display_presentation);
    display_presentation.displayed_valid = 0u;
    display_ready = 0u;
    if (!display_seed_staging())
    {
        return 0u;
    }
    for (display_clear_at = 0u;
         display_clear_at < R0FSI_DISPLAY_BUFFER_BYTES;
         display_clear_at = (uint16_t)(display_clear_at + R0FSI_DISPLAY_QUANTUM_BYTES))
    {
        if (!application_dma(R0FC_STAGING,
                R0FC_ROM + (uint32_t)display_front * 0x10000ul + display_clear_at,
                R0FSI_DISPLAY_QUANTUM_BYTES))
        {
            return 0u;
        }
    }
#endif
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
    if (!r0fsi_prepare_rom_toggle())
    {
        return 0u;
    }
    return cfrom_restore();
}

static void display_abandon_and_suspend(void)
{
#ifdef R0FG1_INTEGRATION
    r0fg1_presentation_cancel(&display_presentation);
#endif
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
#ifdef R0FG1_INTEGRATION
    r0fg1_tick_open();
    uint32_t wait_iterations = 0u;
#endif
    do
    {
#ifdef R0FG1_INTEGRATION
        if (++wait_iterations > R0FG1_WAIT_LIMIT)
        {
            lockout(111u);
            return 0u;
        }
#endif
        now = cfnow();
        if ((int32_t)(now - next_deadline) < 0)
        {
#ifdef R0FG1_INTEGRATION
            group1_service_sweep();
#else
            display_quantum();
            cfinput();
            cfaudio_service(0u);
#endif
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
#ifdef R0FG1_INTEGRATION
    r0fg1_tick_start();
#else
    cfinput_tick(0u);
#endif
    r0fc_tick(&model);
#ifdef R0FG1_INTEGRATION
    r0fg1_stage_begin(21u);
#endif
    snapshot = r0fc_publish(&snapshots, &model);
    if (snapshot < R0FC_SNAPSHOT_COUNT)
    {
        (void)cfcopy(R0FC_SNAPSHOTS
                     + (uint32_t)snapshot * R0FC_SNAPSHOT_BYTES,
                     snapshots.data[snapshot], R0FC_SNAPSHOT_BYTES, 1u);
    }
#ifdef R0FG1_INTEGRATION
    r0fg1_stage_end(21u);
#endif
#ifdef R0FG1_INTEGRATION
    group1_service_sweep();
#else
    display_quantum();
    cfinput();
    cfaudio_service(0u);
#endif
    if (r0f_pf_nmi_seen)
    {
        lockout(92u);
        return 0u;
    }
#ifdef R0FG1_INTEGRATION
    uint16_t reading_tick = snapshots.reading < R0FC_SNAPSHOT_COUNT
        ? (uint16_t)(snapshots.data[snapshots.reading][0]
            | (uint16_t)snapshots.data[snapshots.reading][1] << 8u) : 0u;
    r0fg1_tick_close(model.tick, snapshots.published, reading_tick,
                     snapshots.high, model.queue_high,
                     display_presentation.displayed_valid);
    next_deadline = r0fg1_next_tick();
#else
    next_deadline += cfperiod >> 16u;
#endif
    return (uint8_t)!cffault;
}

#ifdef R0FG1_INTEGRATION
static uint8_t run_ticks(uint16_t count)
#else
static uint8_t run_ticks(uint8_t count)
#endif
{
#ifdef R0FG1_INTEGRATION
    uint16_t index;
#else
    uint8_t index;
#endif

    for (index = 0u; index < count; index++)
    {
#ifdef R0FG1_INTEGRATION
        if (index % R0FG1_TICKS_PER_PHASE == 0u)
        {
            uint8_t phase = (uint8_t)(index / R0FG1_TICKS_PER_PHASE);
            group1_order = (uint8_t)((phase + capture_epoch * 3u) % 6u);
            if (phase != 0u || capture_epoch == 0u)
            {
                next_deadline = cfframe_wait() + (cfcia_frame * phase) / R0FG1_PHASES
                    + (cfperiod >> 16u);
            }
            r0fg1_phase(capture_epoch, phase, next_deadline);
        }
#endif
        if (!run_authoritative_tick())
        {
            return 0u;
        }
#ifdef R0FG1_INTEGRATION
        if ((index + 1u) % R0FG1_TICKS_PER_PHASE == 0u)
        {
            r0fg1_phase_end();
        }
#endif
    }
    return 1u;
}

static uint8_t reclaim_after_storage(void)
{
    uint8_t features;
    uint8_t ready = r0fsi_prepare_rom_toggle();

    iec_before_record = r0fsi_iec_before;
    iec_after_record = r0fsi_iec_after;
    if (!ready)
    {
        return 0u;
    }
    features = r0fc_rom_toggle();
    reclaim_features_record = features;

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
    cffault = r0fsi_irq_fault != 0u ? r0fsi_irq_fault : fault;
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
    // Display-clear DMA reads CIA time. Restart only after canonical restore
    // and reclaim. The IRQ handler owns no display/DMA state; acquisition is
    // inactive here. Keep raster-line selection after display configuration.
    if (!cfclock_begin() || !display_resume())
    {
        // Clock and every display rejection already record the first cause.
        lockout(cffault);
        return 0u;
    }
    r0fsi_irq_select_line();
    // Audio initialization reads the CIA clock; restart it first after KERNAL.
    cfaudio_begin();
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
#ifndef R0FG1_INTEGRATION
    uint8_t capture_page = 1u;
#endif
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
    uint8_t final_fault;

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
#ifdef R0FG1_INTEGRATION
    if (!r0fg1_capture_init())
    {
        lockout(107u);
        goto finish;
    }
#endif
#ifdef R0FG1_EXPORT_QUALIFICATION
    if (!r0fg1_export_probe_init())
    {
        lockout(107u);
        goto finish;
    }
#endif
    if (!r0fsi_prepare_rom_toggle() || !cfrom_begin()
        || !cfclock_begin() || !cfcalibrate(0u))
    {
        lockout(85u);
        goto finish;
    }
#ifdef R0FG1_INTEGRATION
    r0fg1_calibration(0u);
#endif
    r0fc_reset(&model);
    r0fc_snap_reset(&snapshots);
    display_begin();
    r0fsi_irq_select_line();
    cfaudio_begin();
    next_deadline = cfnow() + (cfperiod >> 16u);
    stage = 2u;
    if (!run_ticks(ACTIVE_PRE_TICKS))
    {
#ifdef R0FG1_INTEGRATION
        // Keep the observed cause in the combined test, as on resumed ticks.
        lockout(cffault != 0u ? cffault : 86u);
#else
        lockout(86u);
#endif
        goto finish;
    }
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
    // Observe only the resumed interval; KERNAL activity cannot earn this bit.
    if (!r0fsi_irq_snapshot(&irq_before))
    {
        lockout(r0fsi_irq_fault);
        goto finish;
    }
    stage = 4u;
#ifdef R0FG1_INTEGRATION
    capture_epoch = 1u;
#endif
    if (!run_ticks(ACTIVE_POST_TICKS))
    {
        // Keep the first post-resume failure instead of hiding it with 0x57.
        lockout(r0fs_post_storage_tick_fault(cffault));
        goto finish;
    }
    if (!r0fsi_irq_snapshot(&irq_after))
    {
        lockout(r0fsi_irq_fault);
        goto finish;
    }
    // Capture before cleanup disables/acknowledges the source or restores ROM.
    // Reads are sequential; an IRQ may occur between them. Do not read CIA ICR.
    irq_observation[0] = r0fsi_irq_cpu_status();
    irq_observation[1] = CFREG(0xd019u);
    irq_observation[2] = CFREG(0xd01au);
    irq_observation[3] = CFREG(0xd06fu);
    irq_observation[4] = CFREG(0xd079u);
    irq_observation[5] = CFREG(0xd07au);
    irq_observation[6] = CFREG(0xfffeu);
    irq_observation[7] = CFREG(0xffffu);
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
    if ((uint16_t)(irq_after - irq_before) != 0u)
    {
        resumed_service_mask |= R0FSI_SERVICE_IRQ;
    }
    if (dma_after > dma_before)
    {
        resumed_service_mask |= R0FSI_SERVICE_DMA;
    }
#ifdef R0FG1_INTEGRATION
    if (cfcalibrate(1u))
    {
        r0fg1_calibration(1u);
    }
#endif
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
    if (r0fsi_irq_fault != 0u)
    {
        lockout(r0fsi_irq_fault);
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
    cfresult[R0FSI_O_IEC_OUTPUT_BEFORE] = iec_before_record;
    cfresult[R0FSI_O_IEC_OUTPUT_RELEASED] = iec_after_record;
    cfresult[R0FSI_O_RECLAIM_FEATURES] = reclaim_features_record;
    for (index = 0u; index < sizeof(irq_observation); index++)
    {
        cfresult[R0FSI_O_IRQ_CPU_STATUS + index] = irq_observation[index];
    }
    cfresult[R0FSI_O_LIFECYCLE] = lifecycle_state;
    cfresult[R0FSI_O_FAULT] = cffault;
    final_fault = r0fs_final_fault(
        lifecycle_state, r0f_pf_nmi_seen, cffault, resumed_service_mask,
        R0FSI_SERVICE_DISPLAY | R0FSI_SERVICE_AUDIO
            | R0FSI_SERVICE_INPUT | R0FSI_SERVICE_IRQ | R0FSI_SERVICE_DMA,
        (uint8_t)(reserve_before == reserve_after),
        (uint8_t)(model.tick == ACTIVE_PRE_TICKS
                              + ACTIVE_POST_TICKS));
    if (reserve_before == reserve_after
        && r0fs_completion_allowed(
            lifecycle_state, r0f_pf_nmi_seen, cffault,
            resumed_service_mask,
            R0FSI_SERVICE_DISPLAY | R0FSI_SERVICE_AUDIO
                | R0FSI_SERVICE_INPUT | R0FSI_SERVICE_IRQ
                | R0FSI_SERVICE_DMA)
        && model.tick == ACTIVE_PRE_TICKS
                         + ACTIVE_POST_TICKS)
    {
        cfresult[R0FSI_O_STAGE] = 127u;
    }
    else if (!cffault)
    {
        lockout(final_fault != 0u ? final_fault : 88u);
        cfresult[R0FSI_O_FAULT] = cffault;
        cfresult[R0FSI_O_LIFECYCLE] = lifecycle_state;
    }
    result_u32(R0FSI_O_CRC32,
               cfcrc(cfresult, R0FSI_O_CRC32));
#if defined(R0FG1_EXPORT_QUALIFICATION) || defined(R0FG1_INTEGRATION)
    if (!cffault)
    {
        CFREG(0xd011u) &= 0xefu;
        uint8_t terminal_fault = 107u;
        if (dos_copy(KERNAL_BACKUP_TO_DOS))
        {
#ifdef R0FG1_INTEGRATION
            terminal_fault = r0fg1_capture_finish_fault();
#else
            terminal_fault = r0fg1_export_probe_prepare() ? 0u : 107u;
#endif
            if (terminal_fault == 0u)
            {
                r0fg1_terminal_export();
            }
        }
        lockout(terminal_fault);
        cfresult[R0FSI_O_FAULT] = cffault;
        cfresult[R0FSI_O_LIFECYCLE] = lifecycle_state;
        result_u32(R0FSI_O_CRC32, cfcrc(cfresult, R0FSI_O_CRC32));
    }
#endif
#ifdef R0FG1_INTEGRATION
    // Successful Group 1 acquisition exits through the terminal exporter.
    // Keep failure presentation bounded; the CAP14 page viewer belongs to
    // the original photograph-based capture variant, preserved below.
    // Keep later legacy display-enable writes from replacing the precise
    // screen/font pointers. Preserve D05D's side-border bits; this is terminal.
    CFREG(0xd05du) &= 0x7fu;
    cffinal_screen();
    // The pinned ROM's restored font is readable in the admitted ROM range.
    // Do not depend on the boot-time writable character-cache contents.
    CFREG(0xd068u) = (uint8_t)GROUP1_ROM_FONT;
    CFREG(0xd069u) = (uint8_t)(GROUP1_ROM_FONT >> 8u);
    CFREG(0xd06au) = (uint8_t)(GROUP1_ROM_FONT >> 16u);
    // KERNAL/storage may leave text colors unsuitable for this final screen.
    // Reuse the admitted color range and transport; acquisition is stopped.
    for (index = 0u; index < sizeof(transfer); index++)
    {
        transfer[index] = 1u;
    }
    for (uint16_t offset = 0u; offset < GROUP1_SCREEN_CELLS;)
    {
        uint8_t bytes = GROUP1_SCREEN_CELLS - offset > sizeof(transfer)
            ? sizeof(transfer) : (uint8_t)(GROUP1_SCREEN_CELLS - offset);
        if (!cfcopy(R0FC_COLOR + offset, transfer, bytes, 1u))
        {
            break;
        }
        offset = (uint16_t)(offset + bytes);
    }
    cfscreen();
    cfline(5u, "GROUP 1 LOCKOUT - NO ACCEPTANCE");
    cfline(7u, "FAULT   STATE   TICK    MASK  NMI");
    cfhex(9u, 0u, cfresult[R0FSI_O_FAULT], 2u);
    cfhex(9u, 8u, lifecycle_state, 2u);
    cfhex(9u, 16u, model.tick, 4u);
    cfhex(9u, 24u, resumed_service_mask, 2u);
    cfhex(9u, 30u, r0f_pf_nmi_seen, 2u);
    cfline(11u, "RESET TO EXIT - RETAIN FAILURE");
    // Terminal preflight blanks display fetch. A rejected export must still
    // show its cause using the restored text configuration, after acquisition.
    CFREG(0xd011u) |= 0x10u;
    for (;;)
    {
    }
#else
    cffinal_screen();
summary:
    cfscreen();
    cfline(5u, cffault ? "SUCCESSOR LOCKOUT - NO ACCEPTANCE"
                       : "SUCCESSOR HOST/STATIC IMAGE - RUNTIME UNVERIFIED");
    cfline(7u, "FAULT   STATE   TICK    MASK  NMI");
    cfhex(9u, 0u, cffault, 2u);
    cfhex(9u, 8u, lifecycle_state, 2u);
    cfhex(9u, 16u, model.tick, 4u);
    cfhex(9u, 24u, resumed_service_mask, 2u);
    cfhex(9u, 30u, r0f_pf_nmi_seen, 2u);
    cfline(11u, "RESERVE BEFORE   RESERVE AFTER");
    cfhex(13u, 0u, reserve_before, 8u);
    cfhex(13u, 17u, reserve_after, 8u);
    cfline(15u, "RESULT CRC32");
    cfhex(17u, 0u, result_get_u32(R0FSI_O_CRC32), 8u);
    cfline(19u, "IRQ BEFORE  AFTER   IEC OUT    CLEAR  FEATURES");
    cfhex(21u, 0u, irq_before, 4u);
    cfhex(21u, 12u, irq_after, 4u);
    cfhex(21u, 20u, iec_before_record, 2u);
    cfhex(21u, 31u, iec_after_record, 2u);
    cfhex(21u, 38u, reclaim_features_record, 2u);
    cfline(22u, "CPU  VIC  EN   VIDEO CMP   MODE VECTOR  R0FCAP13");
    for (index = 0u; index < 6u; index++)
    {
        cfhex(23u, (uint8_t)(index * 5u), irq_observation[index], 2u);
    }
    cfhex(23u, 30u, (uint16_t)((uint16_t)irq_observation[7] << 8u)
                         | irq_observation[6], 4u);
    cfline(24u, "N: CAPTURE PAGES   S: SUMMARY   RESET TO EXIT");
    for (;;)
    {
        // Only poll/acknowledge the inherited ASCII queue after acquisition.
        // Do not re-enter storage, alter the result, or restart services.
        uint8_t key = CFREG(0xd610u);
        if (key == 0u)
        {
            continue;
        }
        CFREG(0xd610u) = 0u;
        key &= 0xdfu;
        if (key == 'S')
        {
            capture_page = 1u;
            goto summary;
        }
        if (key == 'N')
        {
            capture_page ^= 1u;
            r0fsi_capture_page(capture_page);
        }
    }
#endif
}
