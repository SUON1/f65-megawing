#ifndef R0FS_IRQ_H
#define R0FS_IRQ_H

#include <stdint.h>

// Private successor handoff diagnostics; no public or physical-memory ABI.
extern uint8_t r0fsi_irq_fault;
extern uint8_t r0fsi_iec_before;
extern uint8_t r0fsi_iec_after;

uint8_t r0fsi_prepare_rom_toggle(void);
uint8_t r0fsi_irq_snapshot(uint16_t *count);
void r0fsi_irq_select_line(void);
uint8_t r0fsi_irq_cpu_status(void);

#endif
