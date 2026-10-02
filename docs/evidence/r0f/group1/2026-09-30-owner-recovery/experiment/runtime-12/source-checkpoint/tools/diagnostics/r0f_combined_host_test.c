#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "combined_model.h"
int main(void){r0fc_model m;r0fc_snapshots s;uint8_t saved[64],encoded[17],old[17];unsigned n,t;
  {r0fc_edges e={0u,0u,0u};uint32_t observed=0u,consumed=0u;
    for(n=0u;n<10000u;++n){uint8_t bit=(uint8_t)(1u<<(n&7u));
      observed+=r0fc_edge_sample(&e,bit);assert(!r0fc_edge_sample(&e,bit));
      observed+=r0fc_edge_sample(&e,0u);consumed+=r0fc_edge_consume(&e);
      assert(!r0fc_edge_consume(&e));}
    assert(observed==20000u&&consumed==observed);
    assert(r0fc_edge_sample(&e,255u)==8u);assert(r0fc_edge_sample(&e,0u)==8u);assert(r0fc_edge_consume(&e)==16u);
    puts("10000 short/held/repeated edge pairs and simultaneous bitmask PASS (not semantic-command corpus)");}
  r0fc_reset(&m);r0fc_snap_reset(&s);
  for(t=1;t<=33;++t){r0fc_tick(&m);assert(m.tick==t);assert(m.queue_high==64u);}
  printf("CF001 33-tick golden: %08lx\n",(unsigned long)m.checksum);
  for(n=0;n<64;++n)assert(r0fc_event(&m,(uint8_t)(n%9u)));
  assert(!r0fc_event(&m,0u));assert(m.event_count==64u);
  assert(r0fc_publish(&s,&m)==0u);assert(r0fc_acquire(&s)==0u);memcpy(saved,s.data[0],64);
  r0fc_tick(&m);assert(r0fc_publish(&s,&m)==1u);r0fc_tick(&m);assert(r0fc_publish(&s,&m)==2u);
  assert(r0fc_publish(&s,&m)==3u);assert(!memcmp(saved,s.data[0],64));assert(s.high==3u);
  r0fc_release(&s);assert(r0fc_acquire(&s)==2u);assert(s.state[1]==0u);r0fc_release(&s);
  memset(encoded,0xa5,17);memcpy(old,encoded,17);
  assert(!r0fc_dma_encode(encoded,R0FC_STAGING,R0FC_STAGING,1u,1u));assert(!memcmp(old,encoded,17));
  for(n=1;n<=255;++n){assert(r0fc_dma_encode(encoded,R0FC_STAGING,R0FC_STAGING+256u,(uint16_t)n,0u));
    assert(encoded[7]==n);assert(r0fc_range(R0FC_ROM+R0FC_ROM_BYTES-n,(uint16_t)n,1u,1u));
    if(n>1u)assert(!r0fc_range(R0FC_ROM+R0FC_ROM_BYTES-n+1u,(uint16_t)n,1u,1u));}
  assert(!r0fc_range(R0FC_RESERVE,1u,1u,1u));assert(r0fc_range(R0FC_RESERVE,255u,0u,0u));
  assert(!r0fc_range(R0FC_ROM,1u,1u,0u));assert(!r0fc_range(0xfffffffful,2u,1u,1u));
  assert(!r0fc_dma_encode(encoded,R0FC_STAGING,R0FC_ROM,255u,0u));
  for(n=1;n<=4096;++n){assert(r0fc_dma_encode(encoded,R0FC_STAGING,R0FC_STAGING+4096u,(uint16_t)n,1u));
    assert((unsigned)(encoded[7]|(unsigned)encoded[8]<<8)==n);}
  assert(!r0fc_dma_encode(encoded,R0FC_STAGING,R0FC_ROM,4097u,1u));
  assert(!r0fc_dma_encode(encoded,R0FC_STAGING,R0FC_RESERVE,1u,1u));
  {uint32_t seed=0x65cf1234u;unsigned accepted=0u;
    for(n=0u;n<10000u;++n){uint32_t a,b,d;uint8_t shift;uint64_t expected;
      seed=seed*1664525u+1013904223u;a=seed%530001u;
      seed=seed*1664525u+1013904223u;b=seed%900001u;
      seed=seed*1664525u+1013904223u;d=1000u+seed%899000u;shift=(uint8_t)((n&1u)?16u:0u);
      expected=((uint64_t)a*b<<shift)/d;
      if(expected<=0xffffffffu){assert(cfratio(a,b,d,shift)==expected);++accepted;}}
    assert(accepted>5000u);printf("Exact ratio vectors PASS: %u\n",accepted);}
  puts("CF001 native model/snapshot/range/DMA boundary tests PASS");return 0;
}
