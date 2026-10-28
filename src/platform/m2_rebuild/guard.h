// Pure deadline policy; units are the authoritative clock's native counts.
#pragma once
#include <stdint.h>

uint8_t m2rb_guard(uint32_t now, uint32_t release,
                    uint32_t operation_bound, uint32_t guard_bound);
