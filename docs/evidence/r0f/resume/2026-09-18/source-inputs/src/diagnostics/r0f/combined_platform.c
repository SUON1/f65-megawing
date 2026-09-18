#include "combined_platform.h"
volatile uint8_t *const cfresult=(volatile uint8_t *)R0FC_RESULT;
uint8_t cffault,cfreclaimed;
uint32_t cfperiod,cfcia_frame,cfcycles_frame;
volatile uint8_t r0f_pf_irq_seq,r0f_pf_irq_seen,r0f_pf_nmi_seen,r0f_pf_stack_high;
volatile uint8_t r0f_pf_cpu_port,r0f_pf_probe_regs[7],r0f_pf_copy_request[9],r0f_pf_copy_ok;
volatile uint16_t r0f_pf_irq_count,r0f_pf_probe_timeout;
volatile uint8_t r0fc_features,r0fc_trap_flags,r0fc_trap_base;
volatile uint8_t r0fc_hardware_seed,r0fc_hardware_low;
volatile uint16_t r0fc_software_seed,r0fc_software_low;
extern uint8_t r0f_pf_enter(void),r0f_pf_flat_copy(void),r0fc_rom_toggle(void);
extern void r0f_pf_start_irq(void),r0f_pf_stop_irq(void),r0fc_stack_seed(void),r0fc_stack_measure(void);
uint8_t cfworkspace[255];
#define check cfworkspace
static uint8_t block[255],list[17],features_open,backup_valid;
static r0fc_edges keys[8],scripted;
static uint8_t keys_valid,pcm_last,pcm_on,input_frame,audio_frame;
static uint32_t service_last;
static uint8_t final_screen;
void cfput16(uint16_t at,uint16_t v){cfresult[at]=(uint8_t)v;cfresult[at+1u]=(uint8_t)(v>>8u);}
void cfput32(uint16_t at,uint32_t v){uint8_t i;for(i=0u;i<4u;++i){cfresult[at+i]=(uint8_t)v;v>>=8u;}}
uint32_t cfget32(uint16_t at){uint8_t i=4u;uint32_t v=0u;while(i)v=(v<<8u)|cfresult[at+--i];return v;}
void cfadd(uint16_t at,uint32_t v){cfput32(at,cfget32(at)+v);}
static uint32_t crc_byte(uint32_t h,uint8_t v){uint8_t j;h^=v;for(j=0u;j<8u;++j)h=(h>>1u)^((h&1u)?0xedb88320ul:0u);return h;}
uint32_t cfcrc(const volatile uint8_t *p,uint16_t n){uint32_t h=0xfffffffful;while(n--)h=crc_byte(h,*p++);return ~h;}
static void screen_byte(uint16_t at,uint8_t v){
  if(final_screen){block[0]=v;(void)cfcopy(R0FC_HUD+at,block,1u,1u);}else CFREG((uint16_t)(0x800u+at))=v;
}
void cffinal_screen(void){final_screen=1u;CFREG(0xd060u)=0u;CFREG(0xd061u)=0u;CFREG(0xd062u)=4u;CFREG(0xd063u)=0u;CFREG(0xd064u)=0u;CFREG(0xd065u)=0u;}
void cfline(uint8_t row,const char *s){uint8_t n=0u;
  while(*s&&n<80u){uint8_t c=(uint8_t)*s++;screen_byte((uint16_t)(80u*row+n++),(c>='A'&&c<='Z')?(uint8_t)(c&31u):c);}}
void cfhex(uint8_t row,uint8_t col,uint32_t v,uint8_t digits){static const char a[]="0123456789ABCDEF";
  while(digits){uint8_t c=(uint8_t)a[v&15u];screen_byte((uint16_t)(80u*row+col+--digits),c>='A'?(uint8_t)(c&31u):c);v>>=4u;}}
void cfscreen(void){uint16_t i;for(i=0u;i<2000u;++i)screen_byte(i,32u);
  cfline(1u,"R0-F COMBINED EXPERIMENT CF001 / F65BLK02");cfline(3u,"DEVELOPMENT EVIDENCE - NOT R0-F ACCEPTANCE");}
uint8_t cfcopy(uint32_t physical,uint8_t *local,uint8_t n,uint8_t to_chip){uint32_t a,b;uint8_t i;
  if(!r0fc_range(physical,n,to_chip,cfreclaimed)||(to_chip&&physical>=R0FC_BACKUP&&physical<R0FC_BACKUP+R0FC_ROM_BYTES&&backup_valid)) {cffault=21u;return 0u;}
  a=to_chip?(uint32_t)(uintptr_t)local:physical;b=to_chip?physical:(uint32_t)(uintptr_t)local;
  for(i=0u;i<4u;++i){r0f_pf_copy_request[i]=(uint8_t)(a>>(i*8u));r0f_pf_copy_request[4u+i]=(uint8_t)(b>>(i*8u));}
  r0f_pf_copy_request[8]=n;if(!r0f_pf_flat_copy()){cffault=22u;return 0u;}return 1u;
}
uint32_t cfphysical_crc(uint32_t start,uint32_t bytes){uint32_t h=0xfffffffful;uint8_t i;
  while(bytes){uint8_t n=bytes>255u?255u:(uint8_t)bytes;
    if(!cfcopy(start,block,n,0u))return 0u;
    for(i=0u;i<n;++i)h=crc_byte(h,block[i]);start+=n;bytes-=n;
  }return ~h;
}
uint8_t cfentry(void){uint8_t i;cfresult[R0FC_O_BASE_PAGE]=r0f_pf_enter();
  cfresult[R0FC_O_CPU_PORT]=r0f_pf_cpu_port;cfresult[R0FC_O_VIDEO]=CFREG(0xd06fu);
  CFREG(0xd054u)|=0x40u;cfresult[R0FC_O_SPEED]=CFREG(0xd054u);
  cfresult[R0FC_O_REFERENCE]=(CFREG(0xd60fu)&32u)?2u:1u;
  cfresult[R0FC_O_MODEL]=CFREG(0xd629u);
  for(i=0u;i<4u;++i)cfresult[R0FC_O_CORE_ID+i]=CFREG((uint16_t)(0xd632u+i));
  if(cfresult[R0FC_O_BASE_PAGE]!=2u||r0f_pf_stack_high!=1u||r0f_pf_cpu_port!=0x35u||(CFREG(0xd030u)&0xb9u)) {cffault=1u;return 0u;}
  r0fc_stack_seed();return 1u;
}
uint8_t cfrom_begin(void){uint32_t off=0u;uint8_t i;
  cfline(6u,"VERIFYING IMMUTABLE ROM BACKUP - DO NOT PRESS RESTORE");
  while(off<R0FC_ROM_BYTES){uint8_t n=R0FC_ROM_BYTES-off>255u?255u:(uint8_t)(R0FC_ROM_BYTES-off);
    if(!cfcopy(R0FC_ROM+off,block,n,0u)||!cfcopy(R0FC_BACKUP+off,block,n,1u)||!cfcopy(R0FC_BACKUP+off,check,n,0u))return 0u;
    for(i=0u;i<n;++i)if(block[i]!=check[i]){cffault=23u;return 0u;}off+=n;
  }
  backup_valid=1u;cfput32(R0FC_O_ROM_CRC,cfphysical_crc(R0FC_BACKUP,R0FC_ROM_BYTES));
  features_open=r0fc_rom_toggle();cfresult[R0FC_O_FEATURES]=features_open;cfresult[R0FC_O_TRAP_FLAGS]=r0fc_trap_flags;
  if(!(r0fc_trap_flags&1u)||r0fc_trap_base!=2u||(features_open&4u)){
    if((r0fc_trap_flags&1u)&&(features_open&4u))(void)r0fc_rom_toggle();cffault=24u;return 0u;}
  cfreclaimed=1u;cfresult[R0FC_O_ROM_STATE]=1u;
  /* Storage admission rejects while reclaimed, without touching any I/O. */
  cfput16(R0FC_O_STORAGE_REJECTS,1u);return 1u;
}
uint8_t cfrom_restore(void){uint32_t off=0u;uint8_t i;
  if(!cfreclaimed)return 0u;
  while(off<R0FC_ROM_BYTES){uint8_t n=R0FC_ROM_BYTES-off>255u?255u:(uint8_t)(R0FC_ROM_BYTES-off);
    if(!cfcopy(R0FC_BACKUP+off,block,n,0u)||!cfcopy(R0FC_ROM+off,block,n,1u)||!cfcopy(R0FC_ROM+off,check,n,0u))return 0u;
    for(i=0u;i<n;++i)if(block[i]!=check[i]){cffault=25u;return 0u;}off+=n;
  }
  cfput32(R0FC_O_RESTORE_MATCHES,off);cfput32(R0FC_O_RESTORE_CRC,cfphysical_crc(R0FC_ROM,R0FC_ROM_BYTES));
  if(cfphysical_crc(R0FC_BACKUP,R0FC_ROM_BYTES)!=cfget32(R0FC_O_ROM_CRC)||cfget32(R0FC_O_RESTORE_CRC)!=cfget32(R0FC_O_ROM_CRC)){cffault=26u;return 0u;}
  if(r0fc_rom_toggle()!=(uint8_t)(features_open|4u)||!(r0fc_trap_flags&1u)||r0fc_trap_base!=2u){cffault=27u;return 0u;}
  cfreclaimed=0u;cfresult[R0FC_O_ROM_STATE]=2u;return 1u;
}
uint8_t cfclock_begin(void){if(CFREG(0xdc0eu)&0x40u){cffault=2u;return 0u;}
  CFREG(0xdc0eu)=0u;CFREG(0xdc0fu)=0u;CFREG(0xdc04u)=255u;CFREG(0xdc05u)=255u;CFREG(0xdc06u)=255u;CFREG(0xdc07u)=255u;
  CFREG(0xdc0fu)=0x51u;CFREG(0xdc0eu)=0x11u;r0f_pf_start_irq();return 1u;}
uint32_t cfnow(void){uint8_t n;for(n=0u;n<32u;++n){uint8_t bh=CFREG(0xdc07u),bl=CFREG(0xdc06u),bh2=CFREG(0xdc07u);
    uint8_t ah=CFREG(0xdc05u),al=CFREG(0xdc04u),ah2=CFREG(0xdc05u),bl2=CFREG(0xdc06u),bh3=CFREG(0xdc07u);
    if(bh==bh2&&bh==bh3&&bl==bl2&&ah==ah2&&!(ah==255u&&al>=240u))return ~((uint32_t)bh<<24u|(uint32_t)bl<<16u|(uint16_t)ah<<8u|al);
  }cffault=3u;return 0u;}
uint32_t cfframe_wait(void){uint8_t old=CFREG(0xd7fau);uint32_t n;
  for(n=0u;n<200000ul;++n){uint8_t f=CFREG(0xd7fau);
    if(cfresult[5]==5u){cfinput();cfaudio_service(0u);}
    if(f!=old){if((uint8_t)(f-old)!=1u)cffault=4u;return cfnow();}}
  cffault=5u;return 0u;}
uint32_t cfcycles(uint32_t counts){return cfratio(counts,cfcycles_frame,cfcia_frame,0u);}
uint8_t cfcalibrate(uint8_t after){uint32_t sum=0u,min=0xfffffffful,max=0u,previous,now,cycles=0u;uint8_t i;
  (void)cfframe_wait();previous=cfframe_wait();
  for(i=0u;i<16u&&!cffault;++i){uint32_t d;uint8_t frame;
    now=cfframe_wait();d=now-previous;previous=now;if(d<1000u||d>100000u){cffault=6u;break;}
    sum+=d;if(d<min)min=d;if(d>max)max=d;
    cfput32((uint16_t)((after?1536u:176u)+i*4u),d);
    frame=CFREG(0xd7fau);cycles=(uint32_t)CFREG(0xd7f2u)|(uint32_t)CFREG(0xd7f3u)<<8u|(uint32_t)CFREG(0xd7f4u)<<16u|(uint32_t)CFREG(0xd7f5u)<<24u;
    if(frame!=CFREG(0xd7fau)){cffault=7u;break;}
    if(!after)cfput32((uint16_t)(1600u+i*4u),cycles);
  }
  if(cffault)return 0u;
  if(after){uint32_t v=sum/16u;cfput32(R0FC_O_AFTER_CIA_FRAME,v);cfput32(R0FC_O_CLOCK_DRIFT,v>cfcia_frame?v-cfcia_frame:cfcia_frame-v);
    if((CFREG(0xd06fu)!=cfresult[R0FC_O_VIDEO])||!(CFREG(0xd054u)&0x40u)||r0f_pf_nmi_seen)cffault=8u;
    return (uint8_t)!cffault;}
  cfcia_frame=sum/16u;
  if(cfresult[R0FC_O_REFERENCE]==1u){/* pinned Xemu scanline integer truncation */
    cfcycles_frame=(cfresult[R0FC_O_VIDEO]&128u)?676962ul:808704ul;
  }else {if(cycles<600000ul||cycles>900000ul||(CFREG(0xd06fu)&64u)){cffault=9u;return 0u;}cfcycles_frame=cycles;}
  cfput32(R0FC_O_CIA_PER_FRAME,cfcia_frame);cfput32(R0FC_O_CYCLES_PER_FRAME,cfcycles_frame);
  /* Q16 CIA counts per nominal 10ms. Split before shift to avoid overflow. */
  cfperiod=cfratio(405000ul,cfcia_frame,cfcycles_frame,16u);
  cfput32(R0FC_O_PERIOD_Q16,cfperiod);
  cfput32(R0FC_O_FRAME_SPREAD,max-min);cfput16(R0FC_O_CALIBRATION_SAMPLES,16u);
  now=cfnow();previous=cfnow();cfput32(R0FC_O_CLOCK_OVERHEAD,previous-now);return 1u;
}
uint8_t cfdma(uint32_t src,uint32_t dst,uint16_t n){uint32_t a,b;
  if(!r0fc_dma_encode(list,src,dst,n,cfreclaimed)){cffault=30u;return 0u;}
  if(!cfcopy(R0FC_DMA_LIST,list,17u,1u))return 0u;
  a=cfnow();CFREG(0xd702u)=5u;CFREG(0xd704u)=0u;CFREG(0xd701u)=0x60u;CFREG(0xd705u)=0u;b=cfnow();
  {uint16_t jobs=(uint16_t)(cfresult[R0FC_O_DMA_JOBS]|(uint16_t)cfresult[R0FC_O_DMA_JOBS+1u]<<8u);cfput16(R0FC_O_DMA_JOBS,(uint16_t)(jobs+1u));}
  if(b-a>cfget32(R0FC_O_DMA_MAX))cfput32(R0FC_O_DMA_MAX,b-a);
  return (uint8_t)!cffault;
}
void cfaudio_stop(void){CFREG(0xd720u)=0u;CFREG(0xd730u)=0u;CFREG(0xd740u)=0u;CFREG(0xd750u)=0u;CFREG(0xd711u)=0u;CFREG(0xd404u)=0u;CFREG(0xd418u)=0u;pcm_on=0u;}
void cfaudio_begin(void){uint8_t i;cfaudio_stop();for(i=0u;i<255u;++i)block[i]=(uint8_t)(112u+(i&31u));
  if(!cfcopy(R0FC_AUDIO,block,255u,1u))return;
  CFREG(0xd711u)=0x80u;CFREG(0xd721u)=0u;CFREG(0xd722u)=0x30u;CFREG(0xd723u)=5u;
  CFREG(0xd72au)=0u;CFREG(0xd72bu)=0x30u;CFREG(0xd72cu)=5u;
  CFREG(0xd727u)=255u;CFREG(0xd728u)=0x30u;CFREG(0xd729u)=16u;CFREG(0xd71cu)=16u;
  CFREG(0xd724u)=0u;CFREG(0xd725u)=16u;CFREG(0xd726u)=0u;
  CFREG(0xd72du)=0u;CFREG(0xd72eu)=0u;CFREG(0xd72fu)=0u;CFREG(0xd720u)=0xe2u;
  pcm_on=1u;pcm_last=CFREG(0xd72au);service_last=cfnow();
  CFREG(0xd400u)=0x40u;CFREG(0xd401u)=0x12u;CFREG(0xd405u)=0x11u;CFREG(0xd406u)=0xf1u;CFREG(0xd404u)=0x21u;CFREG(0xd418u)=2u;
}
void cfaudio_service(uint8_t warning){uint32_t now;uint8_t p,f=CFREG(0xd7fau);
  if(f==audio_frame&&warning==(uint8_t)!pcm_on)return;
  audio_frame=f;now=cfnow();p=CFREG(0xd72au);
  if(pcm_on&&p!=pcm_last)cfadd(R0FC_O_PCM_PROGRESS,1u);pcm_last=p;
  if(now-service_last>cfget32(R0FC_O_SERVICE_GAP))cfput32(R0FC_O_SERVICE_GAP,now-service_last);service_last=now;
  if(warning&&pcm_on){CFREG(0xd720u)=0u;pcm_on=0u;cfadd(R0FC_O_PREEMPTIONS,1u);CFREG(0xd401u)=0x24u;}
  else if(!warning&&!pcm_on){CFREG(0xd720u)=0xe2u;pcm_on=1u;CFREG(0xd401u)=0x12u;}
  cfadd(R0FC_O_AUDIO_SERVICES,1u);
}
void cfinput(void){uint8_t row,total=0u,f=CFREG(0xd7fau);if(keys_valid&&f==input_frame)return;input_frame=f;
  for(row=0u;row<8u;++row){uint8_t v;CFREG(0xd614u)=row;v=(uint8_t)~CFREG(0xd613u);
    if(keys_valid)total=(uint8_t)(total+r0fc_edge_sample(&keys[row],v));else keys[row].state=v;}
  if(total)cfadd(R0FC_O_INPUT_EDGES,total);
  keys_valid=1u;cfadd(R0FC_O_INPUT_SAMPLES,1u);}
void cfinput_tick(uint8_t state){uint8_t row,total=0u;
  for(row=0u;row<8u;++row)total=(uint8_t)(total+r0fc_edge_consume(&keys[row]));
  if(total)cfadd(R0FC_O_CONSUMED_EDGES,total);
  total=r0fc_edge_sample(&scripted,state);if(total)cfadd(R0FC_O_INJECTED_EDGES,total);
  total=r0fc_edge_consume(&scripted);if(total)cfadd(R0FC_O_INJECTED_CONSUMED,total);
}
void cfexit(void){cfaudio_stop();r0f_pf_stop_irq();CFREG(0xdc0eu)=0u;CFREG(0xdc0fu)=0u;
  cfput16(R0FC_O_IRQ_COUNT,r0f_pf_irq_count);cfresult[R0FC_O_NMI]=r0f_pf_nmi_seen;if(r0f_pf_nmi_seen)cffault=10u;
  r0fc_stack_measure();cfput16(R0FC_O_HARDWARE_STACK,(uint16_t)(256u-r0fc_hardware_low));cfput16(R0FC_O_SOFTWARE_STACK,(uint16_t)(0xd000u-r0fc_software_low));
  if(r0fc_hardware_low==0u||r0fc_software_low==0xc000u)cffault=11u;
}
