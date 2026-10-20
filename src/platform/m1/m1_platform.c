// Narrow development dependency on unchanged CF001/PF001 platform primitives.
// No storage, ROM return, DMA submission or audio service is exposed to M1.
#include <string.h>

#include "combined_platform.h"
#include "m1_platform.h"

extern void r0fc_stack_measure(void);
extern volatile uint16_t r0fc_software_low;
extern volatile uint8_t r0fc_hardware_low;

#define M1_FRAME_COUNTER 0xd7fau
#define M1_VIDEO_STANDARD 0xd06fu
#define M1_BORDER_COLOR 0xd020u
#define M1_BACKGROUND_COLOR 0xd021u
#define M1_KEYBOARD_ROW 0xd614u
#define M1_KEYBOARD_BITS 0xd613u
#define M1_SCREEN_POINTER_LOW 0xd060u
#define M1_SCREEN_POINTER_MIDDLE 0xd061u
#define M1_SCREEN_POINTER_BANK 0xd062u
#define M1_SCREEN_POINTER_HIGH 0xd063u
#define M1_COLOR_POINTER_LOW 0xd064u
#define M1_COLOR_POINTER_HIGH 0xd065u

static uint32_t period_q16;
static uint8_t frame;

uint8_t m1_platform_begin(void)
{
    memset((void *)cfresult, 0, R0FC_RESULT_BYTES);
    // cfrom_begin also writes its retained startup message at $09E0-$0A14.
    // This initialization-only dependency is source-pinned in the M1 ledger.
    if (!cfentry() || !cfrom_begin() || !cfclock_begin())
    {
        return 0u;
    }
    // Retain CF001's measured nominal ratio, without its workload or audio path.
    uint32_t start = 0u;
    uint32_t elapsed = 0u;
    uint8_t previous = CFREG(M1_FRAME_COUNTER);
    uint8_t frames = 0u;
    uint32_t polls = 0u;
    while (frames < 17u && polls++ < 4000000ul)
    {
        uint8_t next = CFREG(M1_FRAME_COUNTER);
        if (next != previous)
        {
            if ((uint8_t)(next - previous) != 1u)
            {
                return 0u;
            }
            previous = next;
            uint32_t now = cfnow();
            if (frames == 0u)
            {
                start = now;
            }
            elapsed = now - start;
            ++frames;
        }
    }
    if (frames != 17u || elapsed < 16000ul || elapsed > 1600000ul)
    {
        return 0u;
    }
    // Pinned Xemu uses scanline-truncated CPU/CIA accounting (CF001 contract).
    // This profile is emulator-only; reject a reported physical machine.
    if (cfresult[R0FC_O_REFERENCE] != 1u)
    {
        return 0u;
    }
    uint32_t cycles = (CFREG(M1_VIDEO_STANDARD) & 128u) ? 676962ul : 808704ul;
    period_q16 = cfratio(R0FC_CPU_HZ / M1_TICK_HZ, elapsed / 16u, cycles, 16u);
    if (period_q16 == 0u || cffault != 0u)
    {
        return 0u;
    }
    frame = CFREG(M1_FRAME_COUNTER);
    return 1u;
}

uint32_t m1_platform_now(void)
{
    return cfnow();
}

uint32_t m1_platform_period(void)
{
    return period_q16;
}

uint8_t m1_platform_key(void)
{
    CFREG(M1_KEYBOARD_ROW) = 7u;
    return (uint8_t)((CFREG(M1_KEYBOARD_BITS) & 16u) == 0u);
}

uint8_t m1_platform_frame(void)
{
    uint8_t next = CFREG(M1_FRAME_COUNTER);
    if (next == frame)
    {
        return 0u;
    }
    frame = next;
    return 1u;
}

uint8_t m1_platform_row(uint8_t store, uint8_t row, uint8_t *bytes)
{
    if (store > 1u || row >= M1_ROWS)
    {
        return 0u;
    }
    uint32_t address = store ? M1_DISPLAY_B : M1_DISPLAY_A;
    return cfcopy(address + (uint32_t)row * M1_COLUMNS, bytes, M1_COLUMNS, 1u);
}

uint8_t m1_platform_color_row(uint8_t row, uint8_t *bytes)
{
    if (row >= M1_ROWS)
    {
        return 0u;
    }
    return cfcopy(M1_COLOR + (uint32_t)row * M1_COLUMNS,
                  bytes, M1_COLUMNS, 1u);
}

void m1_platform_palette(uint8_t border, uint8_t background)
{
    CFREG(M1_BORDER_COLOR) = border;
    CFREG(M1_BACKGROUND_COLOR) = background;
}

uint8_t m1_platform_swap(uint8_t store)
{
    if (store > 1u)
    {
        return 0u;
    }
    // Both stores share low pointer bytes. The generation selection is one byte.
    CFREG(M1_SCREEN_POINTER_LOW) = 0u;
    CFREG(M1_SCREEN_POINTER_MIDDLE) = 0u;
    CFREG(M1_SCREEN_POINTER_HIGH) = 0u;
    CFREG(M1_COLOR_POINTER_LOW) = 0u;
    CFREG(M1_COLOR_POINTER_HIGH) = 0u;
    uint8_t bank = (uint8_t)((store ? M1_DISPLAY_B : M1_DISPLAY_A) >> 16u);
    CFREG(M1_SCREEN_POINTER_BANK) = bank;
    return CFREG(M1_SCREEN_POINTER_BANK) == bank;
}

uint8_t m1_platform_fault(void)
{
    return (uint8_t)(cffault != 0u || r0f_pf_nmi_seen != 0u);
}

void m1_platform_measure(void)
{
    r0fc_stack_measure();
    cfput16(R0FC_O_HARDWARE_STACK, (uint16_t)(M1_HARDWARE_STACK_END_EXCLUSIVE
              - M1_HARDWARE_STACK_START - r0fc_hardware_low));
    cfput16(R0FC_O_SOFTWARE_STACK,
            (uint16_t)(M1_SOFTWARE_STACK_END_EXCLUSIVE - r0fc_software_low));
}

// Reset-only fatal indicator; no attempt to continue through a broken seam.
void m1_platform_alarm(void)
{
    CFREG(M1_BORDER_COLOR) = 2u;
}
