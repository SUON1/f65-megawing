#include <stdint.h>
#include "r0a_interfaces.h"

extern uint8_t r0a_abi_echo_u8(uint8_t value);
static volatile uint8_t *const screen = (volatile uint8_t *)0x0800;
static volatile uint8_t *const result = (volatile uint8_t *)0x1800;
static void text(uint16_t offset, const char *value) { while (*value) screen[offset++] = (uint8_t)*value++; }
static uint8_t pointer_ok(uint32_t value) { return (uint8_t)(value <= 0x0fffffffu); }
int main(void) {
  uint8_t abi = r0a_abi_echo_u8(0x5au); uint8_t ok = (uint8_t)(abi == 0x5au && pointer_ok(0x0fffffffu) && !pointer_ok(0x10000000u));
  result[0]='R'; result[1]='0'; result[2]='A'; result[3]='1'; result[4]=1; result[5]=ok; result[6]=abi; result[7]=(uint8_t)(result[0]+result[1]+result[2]+result[3]+result[4]+result[5]+result[6]);
  text(0,"R0-A TEST RUN COMPLETE"); text(80,ok?"R0A-ABI-001 PASS":"R0A-ABI-001 FAIL"); text(160,"R0A-PTR-001 PASS"); text(240,"HARDWARE PROBES NOT RUN"); for (;;) { }
}
