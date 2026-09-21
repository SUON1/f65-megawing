#include <stdint.h>

#include "successor_lifecycle.h"

extern void r0fs_canonical_restore_marker(void);

volatile uint8_t r0fs_admission_state;
volatile uint8_t r0f_pf_cpu_port;
volatile uint8_t r0f_pf_stack_high;
volatile uint8_t r0f_pf_irq_seq;
volatile uint8_t r0f_pf_irq_seen;
volatile uint8_t r0f_pf_nmi_seen;
volatile uint8_t r0f_pf_copy_request[9];
volatile uint8_t r0f_pf_copy_ok;
volatile uint8_t r0f_pf_probe_regs[7];
volatile uint16_t r0f_pf_irq_count;
volatile uint16_t r0f_pf_probe_timeout;

int main(void)
{
    r0fs_admission_state = r0fs_transition(R0FS_S_PRE_C_CAPTURED,
                                           R0FS_E_ACTIVATE);
    r0fs_canonical_restore_marker();

    for (;;)
    {
    }
}
