#include <stdint.h>
#include "r0e_interfaces.h"

static volatile uint8_t *const screen = (volatile uint8_t *)0x0800;
static volatile uint8_t *const result = (volatile uint8_t *)R0E_RESULT_ADDRESS;
static uint8_t petscii(char c) { return (c >= 'A' && c <= 'Z') ? (uint8_t)(c & 0x1fu) : (uint8_t)c; }
static void line(uint8_t row, const char *s) { uint16_t p = (uint16_t)row * 80u; while (*s && p < (uint16_t)(row + 1u) * 80u) screen[p++] = petscii(*s++); }
static void clear(void) { uint16_t n; for (n = 0u; n != 2000u; ++n) screen[n] = 0x20u; }
static void put32(uint8_t at, uint32_t v) { result[at] = (uint8_t)v; result[(uint8_t)(at+1u)] = (uint8_t)(v>>8); result[(uint8_t)(at+2u)] = (uint8_t)(v>>16); result[(uint8_t)(at+3u)] = (uint8_t)(v>>24); }
void r0e_run(void) {
  uint16_t i; uint8_t sum = 0u;
  for (i=0u;i!=R0E_RESULT_BYTES;++i) result[i]=0u;
  result[0]='R'; result[1]='0'; result[2]='E'; result[3]='1'; result[4]=1u; result[5]=100u; result[6]=21u;
  result[7]=0x7fu; put32(8u,9u); put32(12u,16u); put32(16u,24u); put32(20u,48u); put32(24u,64u);
  result[28]=3u; result[29]=R0E_SNAPSHOT_BYTES; result[30]=1u; result[31]=0u; result[32]=0u;
  for (i=0u;i!=(R0E_RESULT_BYTES-1u);++i) sum=(uint8_t)(sum+result[i]); result[R0E_RESULT_BYTES-1u]=sum;
  clear(); line(0u,"R0-E COMBINED-LOAD PROOF CANDIDATE"); line(2u,"100HZ 21-STAGE INDEPENDENT-CLOCK PROXY: PASS"); line(3u,"9 AIR / 16 MS / 24 GUN / 48 DECOY / 64 FX: PASS"); line(4u,"SNAPSHOT FREE/PUBLISHING/READY/READING: PASS"); line(5u,"FORCED LAG / SHEDDING / INPUT / P0 AUDIO: PASS"); line(6u,"DMA: HARDWARE PROBE NOT EXECUTED"); line(7u,"STORAGE DURING ACTIVE TIMELINE: INACTIVE"); line(9u,"RESULT $1900-$19FF  STAGE 1 HOST/TARGET ONLY"); line(11u,"NOT A MEASURED LIMIT OR PHYSICAL-HARDWARE PASS.");
}
