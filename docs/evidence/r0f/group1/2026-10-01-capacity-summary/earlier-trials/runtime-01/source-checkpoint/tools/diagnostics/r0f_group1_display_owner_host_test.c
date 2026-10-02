#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "combined_model.h"
#include "group1_pool_owners.h"
#include "group1_scene.h"
#include "r0f_successor_integration.h"
#include "successor_lifecycle.h"

// Actual owner and acquire/release functions are extracted verbatim. Only
// hardware copy/register and trace edges are mocked; no target timing claim.
#define GROUP1_DISPLAY_COPY_BEGIN (R0FSI_DISPLAY_BUFFER_BYTES + 1u)
#define GROUP1_DISPLAY_COMPLETE (GROUP1_DISPLAY_COPY_BEGIN + R0FG1P_SCENE_COPIES)
#define CFREG(address) registers[address]
static uint8_t registers[65536], stores[2][65536];
static r0fc_model model;
static r0fc_snapshots snapshots;
static r0fg1_presentation display_presentation;
static uint16_t display_source_tick, display_request_tick;
static uint16_t display_requests, display_cancels, display_clear_at;
static uint16_t display_services;
static uint8_t display_views, display_tiers, display_pixels[R0FG1P_SCENE_BYTES];
static uint8_t display_front, display_ready, display_slot, display_frame;
static uint32_t display_registration_crc, display_snapshot_crc;
static unsigned clears, copies, worlds, jobs, front_clear_faults;
static uint8_t copy_ok, dma_ok;
uint8_t cffault;

static uint8_t *physical(uint32_t address, uint16_t length)
{
    assert(address >= R0FC_ROM && address + length <= R0FC_ROM + R0FC_ROM_BYTES);
    uint32_t offset = address - R0FC_ROM;
    assert((offset & 65535u) + length <= 65536u);
    return stores[offset >> 16u] + (offset & 65535u);
}

static uint8_t application_dma(uint32_t source, uint32_t destination, uint16_t length)
{
    jobs++;
    assert(source == R0FC_STAGING && length == R0FSI_DISPLAY_QUANTUM_BYTES);
    assert((destination & 65535u) + length <= R0FSI_DISPLAY_BUFFER_BYTES);
    if (!dma_ok)
    {
        return 0u;
    }
    if (destination >> 16u == (R0FC_ROM >> 16u) + display_front)
    {
        front_clear_faults++;
    }
    memset(physical(destination, length), 1, length);
    clears++;
    return 1u;
}

static uint8_t cfcopy(uint32_t destination, uint8_t *bytes, uint8_t length, uint8_t to_chip)
{
    jobs++;
    assert(length == R0FG1P_SCENE_BYTES && to_chip == 1u);
    assert((destination & 65535u) % length == 0u);
    assert((destination & 65535u) / length < R0FG1P_SCENE_COPIES);
    assert(destination >> 16u == (R0FC_ROM >> 16u) + (display_front ^ 1u));
    if (!copy_ok)
    {
        return 0u;
    }
    memcpy(physical(destination, length), bytes, length);
    copies++;
    return 1u;
}

static uint32_t cfcrc(const uint8_t *bytes, uint16_t length)
{
    return r0fs_crc32(bytes, length);
}

static void r0fg1_world(uint16_t source_tick, uint16_t request_tick,
                        uint8_t flags, uint8_t anchors, uint32_t crc)
{
    assert(source_tick == display_presentation.displayed.key.source_tick);
    assert(request_tick == display_request_tick && anchors == 60u);
    assert(flags >> 2u == (display_front ^ 1u));
    uint32_t front_address = (uint32_t)CFREG(0xd062u) << 16u;
    for (unsigned index = 0u; index < R0FG1P_SCENE_COPIES; index++)
    {
        assert(memcmp(physical(front_address + index * R0FG1P_SCENE_BYTES,
                                R0FG1P_SCENE_BYTES), display_pixels,
                      R0FG1P_SCENE_BYTES) == 0);
    }
    assert(crc == cfcrc(display_pixels, sizeof(display_pixels)));
    worlds++;
}

#include "snapshot_owner_under_test.inc"
#include "display_owner_under_test.inc"

static void publish(uint16_t tick)
{
    assert(snapshots.state[0] != 3u);
    snapshots.state[0] = 2u;
    snapshots.data[0][0] = (uint8_t)tick;
    snapshots.data[0][1] = (uint8_t)(tick >> 8u);
}

static void reset(uint8_t front, uint16_t tick)
{
    memset(registers, 0, sizeof(registers));
    memset(stores, 0xcc, sizeof(stores));
    memset(&snapshots, 0, sizeof(snapshots));
    snapshots.reading = R0FC_SNAPSHOT_COUNT;
    display_front = front;
    display_slot = R0FC_SNAPSHOT_COUNT;
    display_ready = display_frame = display_views = display_tiers = cffault = 0u;
    display_clear_at = display_services = display_requests = display_cancels = 0u;
    clears = copies = worlds = jobs = front_clear_faults = 0u;
    copy_ok = dma_ok = 1u;
    r0fg1_presentation_init(&display_presentation);
    assert(r0fg1_owners_begin());
    model.tick = tick;
    publish(tick);
}

static void quantum(void)
{
    unsigned before = jobs;
    display_quantum_work();
    assert(jobs - before <= 1u);
}

static void complete(uint8_t legacy)
{
    for (unsigned index = 0u; index < R0FSI_DISPLAY_BUFFER_BYTES
         / R0FSI_DISPLAY_QUANTUM_BYTES; index++)
    {
        quantum();
        assert(!display_ready && !worlds);
    }
    quantum();
    assert(!display_ready && !copies);
    for (unsigned index = 0u; index < R0FG1P_SCENE_COPIES; index++)
    {
        quantum();
        assert(!worlds);
        if (index + 1u < R0FG1P_SCENE_COPIES)
        {
            assert(!display_ready);
        }
    }
    assert(display_ready == !legacy);
    if (legacy)
    {
        quantum();
    }
    assert(display_ready && snapshots.reading == R0FC_SNAPSHOT_COUNT);
    assert(display_services == 1u && !cffault);
}

int main(int argc, char **argv)
{
    uint8_t legacy = (uint8_t)(argc == 2 && strcmp(argv[1], "--baseline") == 0);
    for (uint8_t front = 0u; front < 2u; front++)
    {
        reset(front, 1u);
        complete(legacy);
        assert(clears == 15u && copies == 9u);
        quantum();
        assert(!worlds && clears == 15u);
        publish(2u);
        model.tick = 2u;
        CFREG(0xd7fau) = 1u;
        quantum();
        assert(worlds == 1u && display_front == (front ^ 1u));
        assert(front_clear_faults == legacy);
        assert(display_presentation.building.key.buffer == front);
    }
    if (legacy)
    {
        puts("Baseline reproduced: completion-only extra quantum and clearing just-published front store");
        return 0;
    }
    // Cancel at every unfinished quantum and while ready. The old displayed
    // generation stays untouched; no obsolete view reaches a frame swap.
    for (unsigned progress = 0u; progress <= 25u; progress++)
    {
        reset(0u, 127u);
        for (unsigned index = 0u; index < progress; index++)
        {
            quantum();
        }
        if (snapshots.reading != R0FC_SNAPSHOT_COUNT)
        {
            snapshots.state[1] = 2u;
            snapshots.data[1][0] = 128u;
        }
        else
        {
            publish(128u);
        }
        model.tick = 128u;
        CFREG(0xd7fau) = 1u;
        quantum();
        assert(!worlds && !display_ready && !cffault);
        assert(display_requests == 1u && display_cancels == (progress != 0u));
        assert(display_presentation.building.key.view == 1u);
        assert(display_presentation.building.key.source_tick == 128u);
        assert(!display_presentation.displayed_valid);
        for (unsigned index = 0u; index < 24u; index++)
        {
            quantum();
        }
        assert(display_ready && !cffault);
        CFREG(0xd7fau) = 2u;
        quantum();
        assert(worlds == 1u && display_presentation.displayed.key.view == 1u);
        assert(!front_clear_faults);
    }
    reset(0u, 1u);
    dma_ok = 0u;
    quantum();
    assert(!clears && !display_clear_at && !display_ready);
    dma_ok = 1u;
    for (unsigned index = 0u; index < 24u; index++)
    {
        quantum();
    }
    assert(copies == 8u && !display_ready);
    copy_ok = 0u;
    quantum();
    assert(copies == 8u && !display_ready && snapshots.reading != R0FC_SNAPSHOT_COUNT);
    copy_ok = 1u;
    quantum();
    assert(copies == 9u && display_ready && !cffault);
    reset(0u, 1u);
    for (unsigned index = 0u; index < 24u; index++)
    {
        quantum();
    }
    snapshots.data[0][4] ^= 1u;
    quantum();
    assert(cffault == 70u && !display_ready && !worlds);
    assert(snapshots.reading != R0FC_SNAPSHOT_COUNT);
    puts("Actual display owner: complete-copy, frame gating, backbuffer ownership, 26 cancellation boundaries, DMA/copy retry and snapshot CRC failure PASS");
    return 0;
}
