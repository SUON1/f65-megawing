#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "r0f_platform.h"
extern uint8_t r0f_pf_dma_encode(uint8_t *, uint32_t, uint32_t, uint16_t);
extern uint32_t r0f_pf_crc(const volatile uint8_t *, uint16_t);
int main(void) {
  uint8_t list[R0FP_LIST_BYTES], old[R0FP_LIST_BYTES];
  static const uint32_t invalid[]={0u,0x4ffffu,0x53000u,0x56000u,0x58000u,
                                 0xffd0000u,0xffffffffu};
  unsigned i;
  for(i=1u;i<=255u;++i) {
    assert(r0f_pf_dma_encode(list,0x50000u,0x50100u,(uint16_t)i));
    assert(list[0]==10u && list[6]==0u && list[7]==i && !list[8]);
    assert(list[11]==5u && list[14]==5u && !list[15] && !list[16]);
  }
  memset(list,0xa5,sizeof list); memcpy(old,list,sizeof list);
  for(i=0u;i<sizeof invalid/sizeof invalid[0];++i) {
    assert(!r0f_pf_dma_encode(list,invalid[i],0x50100u,1u));
    assert(!r0f_pf_dma_encode(list,0x50000u,invalid[i],1u));
  }
  assert(!r0f_pf_dma_encode(list,0x50000u,0x50100u,0u));
  assert(!r0f_pf_dma_encode(list,0x50000u,0x50100u,256u));
  assert(!r0f_pf_dma_encode(list,0x50000u,0x500feu,255u));
  assert(!r0f_pf_dma_encode(list,0x500feu,0x50000u,255u));
  assert(!r0f_pf_dma_encode(list,0x52fffu,0x50000u,2u));
  assert(!r0f_pf_dma_encode(list,0x50000u,0x52fffu,2u));
  assert(!memcmp(list,old,sizeof list));
  assert(r0f_pf_dma_encode(list,0x52fffu,0x50000u,1u));
  assert(r0f_pf_dma_encode(list,0x50000u,0x52fffu,1u));
  assert(r0f_pf_crc((const uint8_t *)"123456789",9u)==0xcbf43926u);
  puts("PF-001 host PASS: 255 lengths, range/overlap/overflow rejections, no-write failures, CRC golden");
}
