#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "r0f_successor_integration.h"
#include "successor_irq.h"
#include "successor_lifecycle.h"

// Test the target guard itself, with the pinned core's IEC/defer semantics.
// This is a hardware model, not evidence of the installed physical core.
static uint8_t registers[65536];
static uint8_t hardware_iec_busy;
static uint16_t writes;
static uint8_t irq_sequence;
static uint16_t irq_count;
static uint8_t interrupt_during_read;
static uint8_t tear_every_read;

static uint8_t bus_active(void)
{
    return (uint8_t)(hardware_iec_busy
                     || (registers[0xdd00] & registers[0xdd02] & 0x30u));
}

uint8_t r0fsi_test_read(uint16_t address)
{
    assert(address == 0xdd00u || address == 0xdc0eu || address == 0xd011u);
    return registers[address];
}

void r0fsi_test_write(uint16_t address, uint8_t value)
{
    // No timer, DDR, acknowledge, D7F1 or hypervisor writes are admitted.
    assert(address == 0xdd00u || address == 0xd011u || address == 0xd012u);
    writes++;
    registers[address] = value;
}

uint8_t r0fsi_test_irq_byte(uint8_t index)
{
    uint8_t value;

    assert(index < 3u);
    if (index == 0u)
    {
        return irq_sequence;
    }
    value = index == 1u ? (uint8_t)irq_count : (uint8_t)(irq_count >> 8u);
    if (index == 1u && (interrupt_during_read || tear_every_read))
    {
        irq_sequence = (uint8_t)(irq_sequence + 2u);
        irq_count++;
        interrupt_during_read = 0u;
    }
    return value;
}

static void reset(void)
{
    memset(registers, 0, sizeof(registers));
    registers[0xdc0e] = 0x11u;
    hardware_iec_busy = 0u;
    writes = 0u;
    r0fsi_irq_fault = 0u;
    irq_sequence = 0u;
    irq_count = 0u;
    interrupt_during_read = 0u;
    tear_every_read = 0u;
}

int main(void)
{
    uint32_t checks = 0u;
    uint16_t port;
    uint16_t ddr;
    uint16_t count;
    uint8_t defer_request;

    // The former unguarded RMW can latch defer even though ROM protection
    // toggles correctly. The CPU keeps reloading defer while this bit is set.
    reset();
    registers[0xdd00] = 0x30u;
    registers[0xdd02] = 0x30u;
    defer_request = (uint8_t)(((bus_active() ? 0x40u : 0u) ^ 4u) & 0x40u);
    assert(defer_request != 0u);
    assert(r0fsi_prepare_rom_toggle());
    defer_request = (uint8_t)(((bus_active() ? 0x40u : 0u) ^ 4u) & 0x40u);
    assert(defer_request == 0u);
    assert(r0fsi_iec_before == 0x30u && r0fsi_iec_after == 0u);
    checks += 4u;

    // Exhaustively preserve every non-IEC port bit and the complete DDR.
    for (port = 0u; port < 256u; port++)
    {
        for (ddr = 0u; ddr < 256u; ddr++)
        {
            reset();
            registers[0xdd00] = (uint8_t)port;
            registers[0xdd02] = (uint8_t)ddr;
            assert(r0fsi_prepare_rom_toggle());
            assert(registers[0xdd00] == (uint8_t)(port & 0xc7u));
            assert(registers[0xdd02] == ddr);
            assert(registers[0xdc0e] == 0x11u);
            assert(r0fsi_iec_before == (port & 0x38u));
            assert(r0fsi_iec_after == 0u && !bus_active());
            assert(writes == 1u);
            assert(r0fsi_irq_fault == 0u);
            checks += 8u;
        }
    }

    reset();
    hardware_iec_busy = 1u;
    assert(r0fsi_prepare_rom_toggle());
    assert(bus_active());
    // A different hardware owner is not reset. If IRQ service remains absent,
    // the unmodified final acceptance decision must still report fault 65.
    assert(r0fs_final_fault(R0FS_S_SERVICES_RESUMED, 0u, 0u,
                           0x17u, 0x1fu, 1u, 1u) == R0FSI_FAULT_FINAL_IRQ);
    reset();
    registers[0xdc0e] = 0x51u;
    registers[0xdd00] = 0xffu;
    assert(!r0fsi_prepare_rom_toggle());
    assert(writes == 0u && registers[0xdd00] == 0xffu);
    assert(registers[0xdc0e] == 0x51u);
    assert(r0fsi_irq_fault == R0FSI_FAULT_IEC_SERIAL_OWNED);
    checks += 7u;

    reset();
    irq_count = 0x1234u;
    assert(r0fsi_irq_snapshot(&count) && count == 0x1234u);
    irq_count = 0x00ffu;
    interrupt_during_read = 1u;
    assert(r0fsi_irq_snapshot(&count) && count == 0x0100u);
    irq_count = 0xffffu;
    irq_sequence = 0xfeu;
    interrupt_during_read = 1u;
    assert(r0fsi_irq_snapshot(&count) && count == 0u);
    assert((uint16_t)(count - 0xffffu) == 1u);
    count = 0x5678u;
    irq_sequence = 1u;
    assert(!r0fsi_irq_snapshot(&count) && count == 0x5678u);
    assert(r0fsi_irq_fault == R0FSI_FAULT_IRQ_SNAPSHOT);
    reset();
    tear_every_read = 1u;
    count = 0x5678u;
    assert(!r0fsi_irq_snapshot(&count) && count == 0x5678u);
    assert(r0fsi_irq_fault == R0FSI_FAULT_IRQ_SNAPSHOT);
    checks += 8u;

    // Actual target selector preserves all seven display-control bits and
    // clears the comparator's ninth bit, regardless of current raster MSB.
    for (port = 0u; port < 256u; port++)
    {
        reset();
        registers[0xd011] = (uint8_t)port;
        r0fsi_irq_select_line();
        assert(registers[0xd011] == (port & 0x7fu));
        assert(registers[0xd012] == 128u);
        assert(writes == 2u);
        checks += 3u;
    }
    // Pinned VIC-IV source: frame reset to RASLINE0, increment then saturate
    // at mode maximum. This source-derived reachability model is deliberately
    // not Xemu (which resets its logical raster to zero). Check every allowed
    // start, both delay settings and both maxima. It reproduces the old
    // zero-line failure for nonzero starts without claiming physical proof.
    for (port = 0u; port < 64u; port++)
    {
        for (ddr = 0u; ddr < 4u; ddr++)
        {
            uint16_t maximum = (ddr & 2u) ? 312u : 262u;
            uint16_t delay = ddr & 1u;
            uint16_t line;
            uint8_t old_seen = 0u;
            uint8_t new_seen = 0u;

            for (line = port; line <= maximum; line++)
            {
                old_seen |= (uint8_t)(line == delay);
                new_seen |= (uint8_t)(line == registers[0xd012] + delay);
            }
            assert(new_seen);
            assert(old_seen == (uint8_t)(port <= delay));
            checks += 2u;
        }
    }

    printf("R0-F successor IRQ handoff host PASS: %lu checks\n",
           (unsigned long)checks);
    return 0;
}
