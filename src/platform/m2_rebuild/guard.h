// Pure deadline policy; units are the authoritative clock's native counts.
#pragma once
#include <stdint.h>

// Return spendable work counts after reserving entry, exit and scheduler cost.
uint16_t m2rb_guard(uint32_t now, uint32_t release,
                     uint32_t operation_bound, uint32_t guard_bound);
