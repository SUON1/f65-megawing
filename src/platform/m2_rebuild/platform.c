// Platform alone touches hardware. Reset-only, no ROM return or DMA submission.
// Copy uses PF001: A result; X/Y/Z/B/P/SP preserved; Q overlaps A. Physical
// pointer scratch is $0222-$0229 under canonical B=$02, MAP/MB zero. IRQ masked;
// PF001 NMI preserves A, performs no C calls/copies, and sets its sticky fault.
// Display initialization is pre-timeline; service and commit remain UNPROVEN.
#include <string.h>

#include "combined_platform.h"
#include "io.h"
#include "m1_platform.h"
#include "m2_rebuild_input.h"
#include "m2_rebuild_profile.h"
#include "platform.h"

#define REG_CONTROL_1 0xd011u
#define REG_CONTROL_2 0xd016u
#define REG_SPRITES 0xd015u
#define REG_BORDER 0xd020u
#define REG_BACKGROUND 0xd021u
#define REG_MODE_3 0xd031u
#define REG_TOP 0xd048u
#define REG_BOTTOM 0xd04au
#define REG_TEXT_X 0xd04cu
#define REG_TEXT_Y 0xd04eu
#define REG_CHAR_MODE 0xd054u
#define REG_STRIDE 0xd058u
#define REG_X_SCALE 0xd05au
#define REG_Y_SCALE 0xd05bu
#define REG_SIDE_BORDER 0xd05cu
#define REG_COLUMNS 0xd05eu
#define REG_SCREEN_LOW 0xd060u
#define REG_SCREEN_MIDDLE 0xd061u
#define REG_SCREEN_BANK 0xd062u
#define REG_SCREEN_HIGH 0xd063u
#define REG_COLOR_LOW 0xd064u
#define REG_COLOR_HIGH 0xd065u
#define REG_VIDEO 0xd06fu
#define REG_PALETTE_BANK 0xd070u
#define REG_ROWS 0xd07bu
#define REG_RED 0xd100u
#define REG_GREEN 0xd200u
#define REG_BLUE 0xd300u
#define REG_KEY_ROW 0xd614u
#define REG_KEY_BITS 0xd613u
#define REG_PHYSICAL_RASTER_LOW 0xd052u
#define REG_PHYSICAL_RASTER_HIGH 0xd053u
#define DISPLAY_ENABLE 0x10u
#define STORE_A 0x020000UL
#define STORE_B 0x030000UL

extern volatile uint8_t r0f_pf_copy_request[9];
extern uint8_t r0f_pf_flat_copy(void);

static uint8_t initialized;
static uint8_t enabled;
static uint8_t front;
static uint16_t top;
static uint8_t buffer[64];

// Near-source ranges are checked without wrapping; output classes are selected
// by public functions, never accepted as arbitrary physical caller addresses.
static uint8_t copy(uint32_t destination, const uint8_t *source, uint8_t count)
{
    uintptr_t near = (uintptr_t)source;
    if (source == 0 || count == 0u || count > sizeof(buffer)
        || near < M1_RESIDENT_START || near >= M1_SOFTWARE_STACK_END_EXCLUSIVE
        || (uint32_t)near + count > M1_SOFTWARE_STACK_END_EXCLUSIVE
        || m1_platform_fault())
    {
        return 0u;
    }
    for (uint8_t i = 0u; i < 4u; ++i)
    {
        r0f_pf_copy_request[i] = (uint8_t)((uint32_t)near >> (i * 8u));
        r0f_pf_copy_request[i + 4u] = (uint8_t)(destination >> (i * 8u));
    }
    r0f_pf_copy_request[8] = count;
    return (uint8_t)(r0f_pf_flat_copy() && !m1_platform_fault());
}

static uint32_t store_base(uint8_t store)
{
    return store ? STORE_B : STORE_A;
}

uint8_t m2rb_io_write(uint8_t store, uint16_t offset,
                       const uint8_t *bytes, uint8_t count)
{
    if (!initialized || store > 1u || (enabled && store == front)
        || offset < M2RB_TILE_OFFSET || (uint32_t)offset + count > M2RB_BLANK_OFFSET)
    {
        return 0u;
    }
    return copy(store_base(store) + offset, bytes, count);
}

static void word(uint16_t address, uint16_t value, uint8_t high_mask)
{
    CFREG(address) = (uint8_t)value;
    CFREG((uint16_t)(address + 1u)) = (uint8_t)
        ((CFREG((uint16_t)(address + 1u)) & (uint8_t)~high_mask)
        | ((uint8_t)(value >> 8u) & high_mask));
}

static uint8_t initialize_store(uint8_t store)
{
    uint32_t base = store_base(store);
    // 1000 two-byte screen cells. The final row names an immutable black tile.
    for (uint16_t cell = 0u; cell < 1000u; cell += 32u)
    {
        uint8_t cells = cell > 968u ? (uint8_t)(1000u - cell) : 32u;
        for (uint8_t i = 0u; i < cells; ++i)
        {
            uint16_t tile = (uint16_t)(cell + i);
            uint32_t address = base + (tile < 960u
                ? M2RB_TILE_OFFSET + tile * M2RB_TILE_BYTES : M2RB_BLANK_OFFSET);
            uint16_t character = (uint16_t)(address / 64u);
            buffer[2u * i] = (uint8_t)character;
            buffer[2u * i + 1u] = (uint8_t)(character >> 8u);
        }
        if (!copy(base + cell * 2u, buffer, (uint8_t)(cells * 2u)))
        {
            return 0u;
        }
    }
    memset(buffer, M2RB_BLACK, sizeof(buffer));
    for (uint16_t offset = (uint16_t)M2RB_TILE_OFFSET;
         offset < M2RB_STORE_BYTES; offset = (uint16_t)(offset + 64u))
    {
        if (!copy(base + offset, buffer, 64u))
        {
            return 0u;
        }
    }
    return 1u;
}

uint8_t m2rb_platform_init(void)
{
    initialized = 0u;
    enabled = 0u;
    front = 0u;
    CFREG(REG_CONTROL_1) &= (uint8_t)~DISPLAY_ENABLE;
    if (!initialize_store(0u) || !initialize_store(1u))
    {
        return 0u;
    }
    memset(buffer, 0, sizeof(buffer));
    for (uint16_t offset = 0u; offset < M2RB_COLOR_BYTES; offset += 64u)
    {
        uint8_t count = (uint8_t)(M2RB_COLOR_BYTES - offset > 64u
            ? 64u : M2RB_COLOR_BYTES - offset);
        if (!copy(M2RB_COLOR_BASE + offset, buffer, count))
        {
            return 0u;
        }
    }
    // No inherited bitmap, multicolor, bitplane, RRB, attributes or sprites.
    CFREG(REG_CONTROL_1) = (uint8_t)((CFREG(REG_CONTROL_1) & 0x80u) | 0x08u);
    CFREG(REG_CONTROL_2) = 0x08u;
    CFREG(REG_SPRITES) = 0u;
    CFREG(REG_MODE_3) &= 0x27u;
    CFREG(REG_CHAR_MODE) = (uint8_t)((CFREG(REG_CHAR_MODE) & 0x40u) | 0x07u);
    CFREG(0xd051u) &= 0x3fu;
    CFREG(0xd07au) &= 0xefu;
    CFREG(REG_SIDE_BORDER + 1u) &= 0x7fu;
    word(REG_STRIDE, 80u, 255u);
    CFREG(REG_COLUMNS) = 40u;
    CFREG(REG_ROWS) = 25u;
    // Pinned VIC-IV source: H640=0, X scale=120 gives half-source step.
    // V200 duplicates physical scanlines; Y scale=1 is the reset convention.
    CFREG(REG_X_SCALE) = 120u;
    CFREG(REG_Y_SCALE) = 1u;
    top = (CFREG(REG_VIDEO) & 0x80u) ? 64u : 112u;
    word(REG_TOP, top, 15u);
    word(REG_BOTTOM, (uint16_t)(top + 400u), 15u);
    word(REG_TEXT_X, 80u, 15u);
    word(REG_TEXT_Y, top, 15u);
    word(REG_SIDE_BORDER, 80u, 63u);
    CFREG(REG_SCREEN_LOW) = 0u;
    CFREG(REG_SCREEN_MIDDLE) = 0u;
    CFREG(REG_SCREEN_BANK) = 2u;
    CFREG(REG_SCREEN_HIGH) = 0u;
    CFREG(REG_COLOR_LOW) = 0u;
    CFREG(REG_COLOR_HIGH) = 0u;
    CFREG(REG_BORDER) = M2RB_BLACK;
    CFREG(REG_BACKGROUND) = M2RB_BLACK;
    // Palette 0 is shared by world and telemetry, no palette ownership changes.
    CFREG(REG_PALETTE_BANK) = 0u;
    static const uint8_t rgb[4][3] = {
        {0u, 0u, 0u}, {0u, 5u, 15u}, {0u, 10u, 2u}, {15u, 15u, 15u}
    };
    for (uint8_t i = 0u; i < 4u; ++i)
    {
        CFREG(REG_RED + i + 1u) = rgb[i][0];
        CFREG(REG_GREEN + i + 1u) = rgb[i][1];
        CFREG(REG_BLUE + i + 1u) = rgb[i][2];
    }
    initialized = 1u;
    return (uint8_t)!m1_platform_fault();
}

static uint16_t raster(void)
{
    uint8_t first;
    uint8_t last;
    uint8_t low;
    // One retry is bounded. Inconsistency returns a value outside the window.
    first = CFREG(REG_PHYSICAL_RASTER_HIGH);
    low = CFREG(REG_PHYSICAL_RASTER_LOW);
    last = CFREG(REG_PHYSICAL_RASTER_HIGH);
    if ((first & 3u) != (last & 3u))
    {
        return 0xffffu;
    }
    return (uint16_t)(low | ((uint16_t)(last & 3u) << 8u));
}

int8_t m2rb_io_commit(uint8_t store)
{
    if (!initialized || store > 1u || (enabled && store == front)
        || m1_platform_fault())
    {
        return -1;
    }
    // Early top border only. Actual worst-case completion/prefetch bound is
    // UNPROVEN, so the composition root's zero COMMIT grant prevents execution.
    uint16_t line = raster();
    if (line < 4u || line > (uint16_t)(top - 16u))
    {
        return 0;
    }
    uint8_t bank = store ? 3u : 2u;
    CFREG(REG_SCREEN_BANK) = bank;
    if (CFREG(REG_SCREEN_BANK) != bank || m1_platform_fault())
    {
        return -1;
    }
    front = store;
    if (!enabled)
    {
        CFREG(REG_CONTROL_1) |= DISPLAY_ENABLE;
        enabled = 1u;
    }
    return 1;
}

uint16_t m2rb_platform_keys(void)
{
    static const uint8_t rows[13] = {1,1,2,1,2,2,7,1,4,4,4,5,6};
    static const uint8_t masks[13] = {2,32,4,4,2,32,64,64,2,32,4,4,8};
    uint16_t down = 0u;
    for (uint8_t i = 0u; i < 13u; ++i)
    {
        CFREG(REG_KEY_ROW) = rows[i];
        if ((CFREG(REG_KEY_BITS) & masks[i]) == 0u)
        {
            down |= (uint16_t)(1u << i);
        }
    }
    return down;
}
