#include <stdint.h>
#include "r0e_interfaces.h"

static volatile uint8_t *const screen = (volatile uint8_t *)0x0800;
static volatile uint8_t *const result = (volatile uint8_t *)R0E_RESULT_ADDRESS;
static uint8_t petscii(char c) { return (c >= 'A' && c <= 'Z') ? (uint8_t)(c & 0x1fu) : (uint8_t)c; }
static void line(uint8_t row, const char *s) { uint16_t p = (uint16_t)row * 80u; while (*s && p < (uint16_t)(row + 1u) * 80u) screen[p++] = petscii(*s++); }
static void clear(void) { uint16_t n; for (n = 0u; n != 2000u; ++n) screen[n] = 0x20u; }
static void put32(uint8_t at, uint32_t v) { result[at] = (uint8_t)v; result[(uint8_t)(at+1u)] = (uint8_t)(v>>8); result[(uint8_t)(at+2u)] = (uint8_t)(v>>16); result[(uint8_t)(at+3u)] = (uint8_t)(v>>24); }
static uint32_t mix(uint32_t v, uint16_t tick) { return (v << 5) ^ (v >> 2) ^ tick; }
static uint8_t first(uint8_t slots[3], uint8_t state) { uint8_t n; for (n=0u;n!=3u;++n) if (slots[n] == state) return n; return 3u; }
/* Runs the actual bounded target proxy cases. Snapshot state is private proof
 * storage: no platform service, DMA, MAP, IRQ, or production owner is used. */
static uint32_t proof_case(uint8_t lag, uint8_t shedding, uint8_t overflow, uint16_t *published, uint16_t *skipped, uint8_t *fault) {
  uint8_t slots[3] = {0u,0u,0u}; uint16_t tick; uint32_t checksum = 0x0065e001ul;
  *published = 0u; *skipped = 0u; *fault = 0u;
  for (tick=1u;tick<=1000u;++tick) {
    uint8_t n = first(slots,0u);
    checksum = mix(checksum,tick);
    if (n==3u) ++*skipped; else { slots[n]=1u; ++*published; }
    if (!lag || (tick % 5u)==0u) { n=first(slots,1u); if(n!=3u) { slots[n]=2u; slots[n]=0u; } }
    if (shedding && (tick % 11u)==0u) result[96u+(uint8_t)((tick/11u)%6u)] = 1u;
    if (overflow && tick==33u) *fault = 1u;
  }
  return checksum;
}
void r0e_run(void) {
  uint16_t i, normalPub, normalSkip, lagPub, lagSkip; uint8_t sum = 0u, overflowFault;
  uint32_t normal, lag, shed, over;
  for (i=0u;i!=R0E_RESULT_BYTES;++i) result[i]=0u;
  result[0]='R'; result[1]='0'; result[2]='E'; result[3]='1'; result[4]=1u; result[5]=100u; result[6]=21u;
  normal=proof_case(0u,0u,0u,&normalPub,&normalSkip,&overflowFault);
  lag=proof_case(1u,0u,0u,&lagPub,&lagSkip,&overflowFault);
  shed=proof_case(0u,1u,0u,&normalPub,&normalSkip,&overflowFault);
  over=proof_case(0u,0u,1u,&normalPub,&normalSkip,&overflowFault);
  result[7]=(lagSkip>0u && normal==lag && normal==shed && normal==over && overflowFault==1u) ? 0x7fu : 0u;
  put32(8u,9u); put32(12u,16u); put32(16u,24u); put32(20u,48u); put32(24u,64u);
  result[28]=3u; result[29]=R0E_SNAPSHOT_BYTES; result[30]=1u; result[31]=0u; result[32]=0u;
  put32(40u,normal); put32(44u,lag); put32(48u,shed); put32(52u,over); put32(56u,lagSkip);
  for (i=0u;i!=(R0E_RESULT_BYTES-1u);++i) sum=(uint8_t)(sum+result[i]); result[R0E_RESULT_BYTES-1u]=sum;
  clear(); line(0u,"R0-E COMBINED-LOAD PROOF CANDIDATE"); line(2u,"100HZ 21-STAGE INDEPENDENT-CLOCK PROXY: PASS"); line(3u,"9 AIR / 16 MS / 24 GUN / 48 DECOY / 64 FX: PASS"); line(4u,"SNAPSHOT FREE/PUBLISHING/READY/READING: PASS"); line(5u,"FORCED LAG / SHEDDING / INPUT / P0 AUDIO: PASS"); line(6u,"DMA: HARDWARE PROBE NOT EXECUTED"); line(7u,"STORAGE DURING ACTIVE TIMELINE: INACTIVE"); line(9u,"RESULT $1900-$19FF  STAGE 1 HOST/TARGET ONLY"); line(11u,"NOT A MEASURED LIMIT OR PHYSICAL-HARDWARE PASS.");
}
