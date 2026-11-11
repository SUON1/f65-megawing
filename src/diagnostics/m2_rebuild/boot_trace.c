// Reset-only CF001 trace root. The foreground ends before clock or display setup.
#include "combined_platform.h"

volatile uint8_t m2_boot_outcome;

int main(void)
{
    uint8_t passed = (uint8_t)(cfentry() && !r0f_pf_nmi_seen
        && cfrom_begin() && !cffault && !r0f_pf_nmi_seen);
    m2_boot_outcome = passed ? 1u : 255u;
    for (;;)
    {
    }
}
