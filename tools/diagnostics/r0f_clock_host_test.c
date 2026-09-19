#include <assert.h>
#include <stdint.h>
#include <stdio.h>
extern uint8_t r0f_clock_begin(void), r0f_clock_now(uint32_t *);
extern void r0f_clock_stop(void);
static uint8_t registers[65536];
static uint32_t counter;
static unsigned writes, reads, moving, unstable;
uint8_t r0f_bus_read(uint16_t address) {
  if (address >= 0xdc04u && address <= 0xdc07u) {
    ++reads;
    if (moving) --counter;
    if (unstable && address == 0xdc07u) return (uint8_t)reads;
    return (uint8_t)(counter >> ((address-0xdc04u)*8u));
  }
  return registers[address];
}
void r0f_bus_write(uint16_t address, uint8_t value) {
  assert((address>=0xdc04u && address<=0xdc07u) || address==0xdc0eu || address==0xdc0fu);
  registers[address]=value; ++writes;
}
int main(void) {
  uint32_t value, previous;
  registers[0xd030]=1u;
  assert(!r0f_clock_begin() && writes==0u);
  r0f_clock_stop(); assert(writes==0u);
  registers[0xd030]=0x44u; registers[0xdc0e]=0xffu;
  assert(!r0f_clock_begin() && writes==0u);
  registers[0xdc0e]=0xbfu; registers[0xdc0f]=0xffu;
  assert(r0f_clock_begin() && writes==8u);
  assert(registers[0xdc0e]==0x91u && registers[0xdc0f]==0xd1u);
  for(unsigned a=0xdc04u;a<=0xdc07u;a++) assert(registers[a]==255u);
  counter=0x12345678u;
  assert(r0f_clock_now(&value) && value==0xedcba987u);
  moving=1u;
  for(unsigned test=0;test<3u;test++) {
    counter = test==0u ? 0x00010005u : test==1u ? 0x01000005u : 5u;
    previous=~counter;
    for(unsigned i=0;i<100u;i++) {
      assert(r0f_clock_now(&value));
      assert((uint32_t)(value-previous)>0u && (uint32_t)(value-previous)<256u);
      previous=value;
    }
  }
  unstable=1u; reads=0u;
  assert(!r0f_clock_now(&value) && reads==32u*8u);
  r0f_clock_stop(); assert(registers[0xdc0e]==0x80u && registers[0xdc0f]==0x80u);
  assert(writes==10u); r0f_clock_stop(); assert(writes==10u);
  puts("PASS: CIA visibility/serial guards, write ownership, cascade/byte/32-bit wraps, unstable-read bound, stop");
}
