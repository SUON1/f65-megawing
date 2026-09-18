#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "r0f_interfaces.h"
volatile uint8_t r0f_host_screen[2000];
static uint8_t data[R0F_CAPTURE_TOTAL_BYTES], original[R0F_CAPTURE_TOTAL_BYTES], saved[2000];
static uint8_t key;
static unsigned acks, summaries;
extern void r0f_capture_init(void), r0f_capture_render(uint8_t), r0f_capture_command(uint8_t);
extern uint8_t r0f_capture_key(void);
uint8_t r0f_capture_byte(uint16_t index) { assert(index < sizeof(data)); return data[index]; }
uint8_t r0f_bus_read(uint16_t address) { assert(address == 0xd610u); return key; }
void r0f_bus_write(uint16_t address, uint8_t value) { assert(address == 0xd610u && value == key && key); ++acks; key=0; }
void r0f_timing_display(void) { ++summaries; r0f_host_screen[0]=0xeeu; }
int main(void) {
  assert(fread(data, 1u, sizeof(data), stdin) == sizeof(data));
  assert(getchar() == EOF);
  memcpy(original, data, sizeof(data));
  r0f_capture_init();
  memcpy(saved, (const void *)r0f_host_screen, sizeof(saved));
  r0f_capture_command('P'); r0f_capture_command(0u); r0f_capture_command('?');
  r0f_capture_render(255u);
  assert(!memcmp(saved, (const void *)r0f_host_screen, sizeof(saved)));
  assert(r0f_capture_key()==0u && acks==0u);
  key='s'; r0f_capture_command(r0f_capture_key());
  assert(acks==1u && summaries==1u && r0f_host_screen[0]==0xeeu);
  r0f_capture_command('n'); assert(r0f_host_screen[0]==0xeeu);
  r0f_capture_command('c'); assert(!memcmp(saved, (const void *)r0f_host_screen, sizeof(saved)));
  for (unsigned page=0u; page<R0F_CAPTURE_PAGES; ++page) {
    assert(fwrite((const void *)r0f_host_screen, 1u, 2000u, stdout)==2000u);
    r0f_capture_command(page%2u ? ' ' : 'n');
  }
  memcpy(saved, (const void *)r0f_host_screen, sizeof(saved));
  r0f_capture_command('N'); assert(!memcmp(saved, (const void *)r0f_host_screen, sizeof(saved)));
  for (unsigned page=1u; page<R0F_CAPTURE_PAGES; ++page) r0f_capture_command('p');
  assert(r0f_host_screen[80u+8u]=='1');
  assert(!memcmp(data, original, sizeof(data)));
  return 0;
}
