// Narrow Platform seam. Graphics never receives a physical address or register.
#pragma once
#include <stdint.h>

// Copy failure is terminal for the candidate; the front store is untouched.
uint8_t m2rb_io_write(uint8_t store, uint16_t offset,
                       const uint8_t *bytes, uint8_t count);
// 0: deferred with no hardware change, 1: latched, -1: uncertain/terminal.
int8_t m2rb_io_commit(uint8_t store);
