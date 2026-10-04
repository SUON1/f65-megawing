// Private synchronous foreground PF encoder; callers retain admission policy.
#ifndef R0FG2_COPY_H
#define R0FG2_COPY_H
#include <stdint.h>
uint8_t r0fg2_copy(uint32_t source, uint32_t destination, uint8_t bytes);
#endif
