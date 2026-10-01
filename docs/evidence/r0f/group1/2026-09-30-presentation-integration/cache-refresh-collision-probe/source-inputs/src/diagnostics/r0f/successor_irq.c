#include <stdint.h>

#include "r0f_successor_integration.h"
#include "successor_irq.h"

// Owns the successor-only IEC quiescence guard and coherent IRQ observation.
#define CIA1_CONTROL_A 0xdc0eu
#define CIA2_PORT_A 0xdd00u
#define CIA_SERIAL_OUTPUT 0x40u
#define IEC_OUTPUT_MASK 0x38u
#define IRQ_SNAPSHOT_ATTEMPTS 32u
#define VIC_CONTROL_1 0xd011u
#define VIC_RASTER_COMPARE 0xd012u

#ifdef R0FS_IRQ_HOST_TEST
uint8_t r0fsi_test_read(uint16_t address);
void r0fsi_test_write(uint16_t address, uint8_t value);
uint8_t r0fsi_test_irq_byte(uint8_t index);
#define read_register r0fsi_test_read
#define write_register r0fsi_test_write
#define read_irq_byte r0fsi_test_irq_byte
#else
extern volatile uint8_t r0f_pf_irq_seq;
extern volatile uint16_t r0f_pf_irq_count;

static uint8_t read_register(uint16_t address)
{
    return *(volatile uint8_t *)(uintptr_t)address;
}

static void write_register(uint16_t address, uint8_t value)
{
    *(volatile uint8_t *)(uintptr_t)address = value;
}

static uint8_t read_irq_byte(uint8_t index)
{
    if (index == 0u)
    {
        return r0f_pf_irq_seq;
    }
    return ((volatile uint8_t *)&r0f_pf_irq_count)[index - 1u];
}
#endif

uint8_t r0fsi_irq_fault;
uint8_t r0fsi_iec_before;
uint8_t r0fsi_iec_after;

// PF001 starts on logical line zero. The pinned core resets the NTSC
// logical counter to seven and saturates at its maximum, so zero need not
// occur. Select an interior line after display setup: above every six-bit
// RASLINE0 value and below both PAL/NTSC maxima, including one-line delay.
// Preserve display control bits; D011/D012 select the legacy raster source.
// Caller already owns raster IRQ. No SEI/CLI, acknowledgment, MAP or DMA.
void r0fsi_irq_select_line(void)
{
    write_register(VIC_CONTROL_1,
                   (uint8_t)(read_register(VIC_CONTROL_1) & 0x7fu));
    write_register(VIC_RASTER_COMPARE, R0FSI_IRQ_RASTER_LINE);
}

// Caller owns the idle storage boundary: no KERNAL transaction, application
// IRQ stopped, canonical MAP/B=2/port=$35. Release only CIA2 ATN/CLK/DATA;
// preserve VIC-bank bits, DDRs and CIA1 timer/serial state. The retained HYPPO
// ROM toggle copies D67D read bit 6 (IEC active) to write bit 6 (IRQ defer).
// The pinned Xemu does not model IEC/defer status. Do not treat its feature
// byte as hardware proof: the existing real IRQ-count advancement check is
// still authoritative, and a remaining hardware owner still causes lockout.
// No DMA/MAP, timer reset, hardware-IEC reset or direct D67D write.
uint8_t r0fsi_prepare_rom_toggle(void)
{
    uint8_t port = read_register(CIA2_PORT_A);

    r0fsi_iec_before = port & IEC_OUTPUT_MASK;
    r0fsi_iec_after = r0fsi_iec_before;
    if ((read_register(CIA1_CONTROL_A) & CIA_SERIAL_OUTPUT) != 0u)
    {
        // Do not steal SRQ ownership from a serial-output user.
        r0fsi_irq_fault = R0FSI_FAULT_IEC_SERIAL_OWNED;
        return 0u;
    }
    write_register(CIA2_PORT_A, (uint8_t)(port & (uint8_t)~IEC_OUTPUT_MASK));
    r0fsi_iec_after = 0u;
    return 1u;
}

// PF001's IRQ writer brackets the two-byte count with an odd/even sequence.
// Read without SEI/CLI, including rollover; refuse a persistently torn read.
uint8_t r0fsi_irq_snapshot(uint16_t *count)
{
    uint8_t attempt;

    for (attempt = 0u; attempt < IRQ_SNAPSHOT_ATTEMPTS; attempt++)
    {
        uint8_t sequence = read_irq_byte(0u);
        uint8_t low;
        uint8_t high;

        if ((sequence & 1u) != 0u)
        {
            continue;
        }
        low = read_irq_byte(1u);
        high = read_irq_byte(2u);
        if (sequence == read_irq_byte(0u))
        {
            *count = (uint16_t)((uint16_t)high << 8u) | low;
            return 1u;
        }
    }
    r0fsi_irq_fault = R0FSI_FAULT_IRQ_SNAPSHOT;
    return 0u;
}
