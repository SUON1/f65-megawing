#include <stdint.h>
#include "r0f_platform.h"

#define REG(a) (*(volatile uint8_t *)(uintptr_t)(a))
static volatile uint8_t *const result=(volatile uint8_t *)R0FP_RESULT_ADDRESS;
volatile uint8_t r0f_pf_irq_seq, r0f_pf_irq_seen, r0f_pf_nmi_seen, r0f_pf_stack_high;
volatile uint8_t r0f_pf_cpu_port;
volatile uint16_t r0f_pf_irq_count, r0f_pf_probe_timeout;
volatile uint8_t r0f_pf_probe_regs[7], r0f_pf_copy_request[9], r0f_pf_copy_ok;
static uint8_t buffer[R0FP_MAX_COPY], returned[R0FP_MAX_COPY], list[R0FP_LIST_BYTES];
static uint8_t fault;
extern uint8_t r0f_pf_enter(void), r0f_pf_flat_copy(void);
extern void r0f_pf_start_irq(void), r0f_pf_stop_irq(void), r0f_pf_register_probe(void);
extern uint8_t r0f_pf_dma_encode(uint8_t *,uint32_t,uint32_t,uint16_t);
extern uint32_t r0f_pf_crc(const volatile uint8_t *,uint16_t);

static void put16(uint16_t at,uint16_t v) { result[at]=(uint8_t)v;result[at+1u]=(uint8_t)(v>>8u); }
static void put32(uint16_t at,uint32_t v) {
  uint8_t i;for(i=0u;i<4u;++i)result[at+i]=(uint8_t)(v>>(i*8u));
}
static void line(uint8_t row,const char *s) {
  volatile uint8_t *p=(volatile uint8_t *)(uintptr_t)(0x800u+80u*row);
  while(*s) { uint8_t c=(uint8_t)*s++;*p++=(c>='A'&&c<='Z')?(uint8_t)(c&31u):c; }
}
static void hex(uint8_t row,uint8_t column,uint32_t v,uint8_t digits) {
  static const char alphabet[]="0123456789ABCDEF";
  while(digits) { uint8_t c=(uint8_t)alphabet[v&15u];
    REG((uint16_t)(0x800u+80u*row+column+--digits))=(c>='A')?(uint8_t)(c&31u):c;v>>=4u; }
}
static void screen(void) {
  uint16_t i;
  for(i=0u;i<2000u;++i) REG((uint16_t)(0x800u+i))=32u;
  line(1u,"R0-F PLATFORM QUALIFICATION PF001 - DEVELOPMENT ONLY");
  line(3u,"CANONICAL MAP / RASTER IRQ / REAL DMA / PCM PROGRESS");
  line(5u,"NOT THE FULL COMBINED WORKLOAD. NOT R0-F ACCEPTANCE.");
  line(7u,"RAW CIA COUNTS ONLY. NO SI OR CPU-CYCLE CALIBRATION.");
  line(20u,"RESET REQUIRED. DO NOT PRESS RESTORE DURING RUN.");
}

/* Delayed CIA B-underflow boundary: refuse the first 16 A counts after
 * reload in addition to stable high/low/high reads. This guard is not a
 * calibration tolerance and does not modify the retained F5 wrapper. */
static uint8_t clock_now(uint32_t *v) {
  uint8_t n;
  for(n=0u;n<32u;++n) {
    uint8_t bh=REG(0xdc07u),bl=REG(0xdc06u),bh2=REG(0xdc07u);
    uint8_t ah=REG(0xdc05u),al=REG(0xdc04u),ah2=REG(0xdc05u);
    uint8_t bl2=REG(0xdc06u),bh3=REG(0xdc07u);
    if(bh==bh2&&bh==bh3&&bl==bl2&&ah==ah2&&!(ah==255u&&al>=240u)) {
      *v=~((uint32_t)bh<<24u|(uint32_t)bl<<16u|(uint32_t)ah<<8u|al);return 1u;
    }
  }
  fault=2u;return 0u;
}
static void clock_begin(void) {
  REG(0xdc0eu)=0u;REG(0xdc0fu)=0u;
  REG(0xdc04u)=255u;REG(0xdc05u)=255u;REG(0xdc06u)=255u;REG(0xdc07u)=255u;
  REG(0xdc0fu)=0x51u;REG(0xdc0eu)=0x11u;
}
static uint8_t irq_count(uint16_t *v) {
  uint8_t n;
  for(n=0u;n<32u;++n) {
    uint8_t a=r0f_pf_irq_seq;uint16_t b=r0f_pf_irq_count;
    if(!(a&1u)&&a==r0f_pf_irq_seq) {*v=b;return 1u;}
  }
  fault=3u;return 0u;
}
static uint8_t frame_wait(uint32_t *t) {
  uint8_t initial=REG(0xd7fau);
  uint32_t loops;
  for(loops=0u;loops<200000u;++loops) {
    uint8_t frame=REG(0xd7fau);
    if(frame!=initial) {
      if((uint8_t)(frame-initial)!=1u) {fault=4u;return 0u;}
      return clock_now(t);
    }
  }
  fault=5u;return 0u;
}
static uint8_t frame_sample(uint16_t at) {
  uint32_t previous,now;uint8_t i;
  if(!frame_wait(&previous))return 0u;
  for(i=0u;i<R0FP_FRAME_SAMPLES;++i) {
    if(!frame_wait(&now))return 0u;
    if(now-previous==0u||now-previous>100000u){fault=6u;return 0u;}
    put32((uint16_t)(at+i*4u),now-previous);previous=now;
  }
  return 1u;
}
static uint8_t copy_allowed(uint32_t p,uint8_t n) {
  if(p>=R0FP_COPY_SOURCE&&p<=R0FP_COPY_SOURCE+512u-n)return 1u;
  if(p>=R0FP_AUDIO_START&&p<=R0FP_AUDIO_START+256u-n)return 1u;
  if(n<=R0FP_LIST_BYTES&&p>=R0FP_LIST_ADDRESS&&p<=R0FP_LIST_ADDRESS+R0FP_LIST_BYTES-n)return 1u;
  return 0u;
}
static uint8_t flat_copy(uint32_t physical,uint8_t *local,uint8_t n,uint8_t to_chip) {
  uint32_t a,b;uint8_t i;
  if(!n||!copy_allowed(physical,n)){fault=7u;return 0u;}
  /* local is only one of the three linked private arrays, never caller input. */
  a=to_chip?(uint32_t)(uintptr_t)local:physical;
  b=to_chip?physical:(uint32_t)(uintptr_t)local;
  for(i=0u;i<4u;++i){r0f_pf_copy_request[i]=(uint8_t)(a>>(i*8u));
    r0f_pf_copy_request[4u+i]=(uint8_t)(b>>(i*8u));}
  r0f_pf_copy_request[8]=n;
  if(!r0f_pf_flat_copy()){fault=8u;return 0u;}return 1u;
}
static uint8_t dma_test(void) {
  uint8_t i;uint32_t start,end;
  for(i=0u;i<R0FP_MAX_COPY;++i)buffer[i]=(uint8_t)(i^0x5au);
  if(!flat_copy(R0FP_COPY_SOURCE,buffer,R0FP_MAX_COPY,1u))return 0u;
  for(i=0u;i<R0FP_MAX_COPY;++i)returned[i]=0u;
  if(!flat_copy(R0FP_COPY_DEST,returned,R0FP_MAX_COPY,1u))return 0u;
  if(!r0f_pf_dma_encode(list,R0FP_COPY_SOURCE,R0FP_COPY_DEST,R0FP_MAX_COPY)){fault=9u;return 0u;}
  if(!flat_copy(R0FP_LIST_ADDRESS,list,R0FP_LIST_BYTES,1u)||!clock_now(&start))return 0u;
  /* Sole DMAService trigger site; IRQ never submits jobs or touches list. */
  REG(0xd702u)=5u;REG(0xd704u)=0u;REG(0xd701u)=0x60u;REG(0xd705u)=0u;
  if(!clock_now(&end))return 0u;
  put32(R0FP_O_DMA_COUNTS,end-start);put16(R0FP_O_DMA_JOBS,1u);
  if(end-start>100000u){fault=10u;return 0u;}
  if(!flat_copy(R0FP_COPY_DEST,returned,R0FP_MAX_COPY,0u))return 0u;
  for(i=0u;i<R0FP_MAX_COPY;++i)if(buffer[i]!=returned[i]){fault=11u;return 0u;}
  put16(R0FP_O_DMA_MATCHES,R0FP_MAX_COPY);return 1u;
}
static void audio_stop(void) {
  REG(0xd720u)=0u;REG(0xd730u)=0u;REG(0xd740u)=0u;REG(0xd750u)=0u;
  REG(0xd711u)=0u;REG(0xd404u)=0u;REG(0xd418u)=0u;
}
static uint8_t pcm_test(void) {
  uint8_t i,previous,changed=0u;uint32_t t;
  for(i=0u;i<255u;++i)buffer[i]=(uint8_t)(112u+(i&31u));
  if(!flat_copy(R0FP_AUDIO_START,buffer,R0FP_MAX_COPY,1u))return 0u;
  audio_stop();
  REG(0xd711u)=0x80u;
  REG(0xd721u)=0u;REG(0xd722u)=0x30u;REG(0xd723u)=5u;
  REG(0xd72au)=0u;REG(0xd72bu)=0x30u;REG(0xd72cu)=5u;
  REG(0xd727u)=0xffu;REG(0xd728u)=0x30u;
  REG(0xd729u)=16u;REG(0xd71cu)=16u;
  REG(0xd724u)=(uint8_t)R0FP_PCM_INCREMENT;
  REG(0xd725u)=(uint8_t)(R0FP_PCM_INCREMENT>>8u);
  REG(0xd726u)=(uint8_t)((uint32_t)R0FP_PCM_INCREMENT>>16u);
  REG(0xd72du)=0u;REG(0xd72eu)=0u;REG(0xd72fu)=0u;
  REG(0xd720u)=0xe2u;
  previous=REG(0xd72au);
  for(i=0u;i<8u;++i){uint8_t now;
    if(!frame_wait(&t))return 0u;
    now=REG(0xd72au);if(now!=previous)++changed;previous=now;
  }
  result[R0FP_O_PCM_PROGRESS]=changed;
  if(!changed){fault=12u;return 0u;}
  REG(0xd720u)=0u;
  /* Let any already-issued memory fetch finish before observing stopped state. */
  if(!frame_wait(&t))return 0u;
  previous=REG(0xd72au);
  for(i=0u;i<3u;++i){if(!frame_wait(&t))return 0u;
    if(REG(0xd72au)!=previous||(REG(0xd720u)&0x80u)){fault=13u;return 0u;}}
  result[R0FP_O_PCM_STOPPED]=1u;audio_stop();return 1u;
}
int main(void) {
  uint16_t i,count=0u;uint32_t a=0u,b=0u;
  for(i=0u;i<R0FP_RESULT_BYTES;++i)result[i]=0u;
  result[0]='R';result[1]='P';result[2]='F';result[3]='1';result[R0FP_O_VERSION]=1u;
  result[R0FP_O_STAGE]=1u;result[R0FP_O_BASE_PAGE]=r0f_pf_enter();
  result[R0FP_O_STACK_HIGH]=r0f_pf_stack_high;
  result[R0FP_O_CPU_PORT]=r0f_pf_cpu_port;result[R0FP_O_D030]=REG(0xd030u);
  result[R0FP_O_VIDEO]=REG(0xd06fu);result[R0FP_O_SPEED]=REG(0xd054u);
  screen();
  if(result[R0FP_O_BASE_PAGE]!=2u||r0f_pf_stack_high!=1u||
     (result[R0FP_O_CPU_PORT]&7u)!=5u||(result[R0FP_O_D030]&0xb9u))fault=1u;
  /* Do not enable inherited CIA serial-output operation. No gameplay NMI. */
  if(REG(0xdc0eu)&0x40u)fault=14u;
  if(!fault) {
    clock_begin();r0f_pf_start_irq();result[R0FP_O_STAGE]=2u;
    if(clock_now(&a)&&clock_now(&b))put32(R0FP_O_READ_OVERHEAD,b-a);
    r0f_pf_register_probe();
    for(i=0u;i<7u;++i)result[R0FP_O_IRQ_REGISTERS+i]=r0f_pf_probe_regs[i];
    if(r0f_pf_probe_regs[0]!=0xa5u||r0f_pf_probe_regs[1]!=0x5au||
       r0f_pf_probe_regs[2]!=0xc3u||r0f_pf_probe_regs[3]!=0x3cu||
       r0f_pf_probe_regs[4]!=2u||(r0f_pf_probe_regs[5]&9u)||r0f_pf_probe_regs[6]!=0x80u)fault=15u;
    else result[R0FP_O_REGISTER_PROBE]=1u;
    if(!fault&&frame_sample(R0FP_O_BEFORE_FRAMES)) {
      result[R0FP_O_STAGE]=3u;
      if(dma_test()) {result[R0FP_O_STAGE]=4u;
        if(pcm_test()) {result[R0FP_O_STAGE]=5u;(void)frame_sample(R0FP_O_AFTER_FRAMES);}}
    }
    if(irq_count(&count))put16(R0FP_O_IRQ_COUNT,count);
  }
  audio_stop();r0f_pf_stop_irq();REG(0xdc0eu)=0u;REG(0xdc0fu)=0u;
  result[R0FP_O_NMI]=r0f_pf_nmi_seen;if(r0f_pf_nmi_seen)fault=16u;
  result[R0FP_O_FAULT]=fault;if(!fault)result[R0FP_O_STAGE]=127u;
  put32(R0FP_O_CRC32,r0f_pf_crc(result,R0FP_O_CRC32));
  line(10u,fault?"PLATFORM TEST STOPPED - NOT QUALIFIED":"PLATFORM PRIMITIVES OBSERVED - FULL WORKLOAD STILL OPEN");
  line(12u,"STAGE / FAULT / IRQ / DMA MATCHED / PCM MOVED:");
  hex(13u,0u,result[R0FP_O_STAGE],2u);hex(13u,8u,fault,2u);
  hex(13u,16u,count,4u);hex(13u,24u,result[R0FP_O_DMA_MATCHES],2u);
  hex(13u,32u,result[R0FP_O_PCM_PROGRESS],2u);
  line(15u,"RESULT BLOCK: $1900-$19FF. CRC32:");
  hex(15u,33u,r0f_pf_crc(result,R0FP_O_CRC32),8u);
  for(;;){}
}
