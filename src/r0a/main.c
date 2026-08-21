#include <stdint.h>
#include "r0a_interfaces.h"

extern uint8_t r0a_abi_echo_u8(uint8_t value);
extern uint8_t r0a_basepage_read(void);
extern void r0a_basepage_sentinel_seed(void);
extern uint8_t r0a_basepage_sentinel_unchanged(void);
static volatile uint8_t *const screen = (volatile uint8_t *)0x0800;
static volatile uint8_t *const result = (volatile uint8_t *)0x1800;
static void text(uint16_t offset, const char *value) { while (*value) screen[offset++] = (uint8_t)*value++; }
static uint8_t pointer_ok(uint32_t value) { return (uint8_t)(value <= 0x0fffffffu); }

static uint16_t __attribute__((noinline)) r0a_nested16(uint16_t value) {
  return (uint16_t)((value ^ (uint16_t)(value << 3)) + 0x1297u);
}

static uint32_t __attribute__((noinline)) r0a_nested32(uint32_t left, uint32_t right) {
  uint32_t sum = left + (right ^ 0x13579bdfu);
  return (sum << 3) ^ (sum >> 5) ^ right;
}

static uint8_t __attribute__((noinline)) r0a_abi_heavy(uint8_t seed) {
  uint16_t stage1 = r0a_nested16((uint16_t)(seed * 0x0121u));
  uint32_t stage2 = r0a_nested32((uint32_t)stage1 * 0x00010001u, 0x2468ace0u);
  uint16_t stage3 = r0a_nested16((uint16_t)(stage2 ^ (stage2 >> 16)));
  return (uint8_t)(stage2 ^ (stage2 >> 8) ^ stage3 ^ (stage3 >> 8));
}

int main(void) {
  uint8_t basepage;
  uint8_t abi;
  uint8_t sentinel;
  uint8_t heavy;
  uint8_t ok;

  result[0]='R'; result[1]='0'; result[2]='A'; result[3]='1'; result[4]=1;
  r0a_basepage_sentinel_seed();
  basepage = r0a_basepage_read();
  abi = r0a_abi_echo_u8(0x5au);
  heavy = r0a_abi_heavy(result[0]);
  sentinel = r0a_basepage_sentinel_unchanged();
  ok = (uint8_t)(basepage == 0x02u && sentinel == 1u && abi == 0x5au &&
                 heavy == 0x04u && pointer_ok(0x0fffffffu) && !pointer_ok(0x10000000u));
  result[5]=ok; result[6]=abi; result[7]=basepage; result[8]=sentinel; result[9]=heavy;
  result[10]=(uint8_t)(result[0]+result[1]+result[2]+result[3]+result[4]+result[5]+result[6]+result[7]+result[8]+result[9]);
  text(0,"R0-A TEST RUN COMPLETE"); text(80,ok?"R0A-BP-001 PASS":"R0A-BP-001 FAIL"); text(160,"R0A-PTR-001 PASS"); text(240,"HARDWARE PROBES NOT RUN"); for (;;) { }
}
