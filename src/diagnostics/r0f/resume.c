#include "combined_platform.h"
#include "resume_model.h"
volatile uint8_t r0fr_permit,r0fr_phase,r0fr_error,r0fr_returned,r0fr_denied;
volatile uint8_t r0fr_input,r0fr_output,r0fr_token[32],r0fr_read[32],r0fr_payload[32],r0fr_end[4];
volatile uint8_t r0fr_input_end,r0fr_output_end;
extern uint8_t r0fr_storage(void);
extern uint8_t r0f_pf_flat_copy(void);
extern volatile uint8_t r0f_pf_copy_request[9];
extern volatile uint8_t r0f_pf_cpu_port;
extern uint8_t r0a_basepage_read(void);
static r0fc_model model;
static uint8_t block[255],state;
static uint32_t before,after,reserve,rom,restore,low_before,low_after;
static uint32_t dos_before,dos_after,reclaimed_crc;
static uint16_t calls;
/* Fixed lifecycle-only ranges: no caller-provided pointers or ownership
 * expansion in the shared CF001 copy allowlist. */
static uint8_t dos_copy(uint16_t off,uint8_t n,uint8_t action) {
  uint32_t a,b;uint8_t j;
  if(!n||off>R0FR_DOS_BYTES-n||action>5u){cffault=46u;return 0u;}
  a=action==0u?(uint32_t)(uintptr_t)block:(action==2u?R0FR_DOS_BACKUP:(action==5u?R0FR_KERNEL_DOS:R0FR_DOS))+off;
  b=action==3u?(uint32_t)(uintptr_t)block:(action==1u?R0FR_DOS_BACKUP:(action==4u?R0FR_KERNEL_DOS:R0FR_DOS))+off;
  for(j=0u;j<4u;++j){r0f_pf_copy_request[j]=(uint8_t)(a>>(j*8u));r0f_pf_copy_request[4u+j]=(uint8_t)(b>>(j*8u));}
  r0f_pf_copy_request[8]=n;
  if(!r0f_pf_flat_copy()){cffault=47u;return 0u;}return 1u;
}
static uint32_t dos_pattern_crc(uint8_t seed) {
  uint16_t off=0u,i;uint32_t h=0xfffffffful;
  while(off<R0FR_DOS_BYTES){uint8_t n=R0FR_DOS_BYTES-off>255u?255u:(uint8_t)(R0FR_DOS_BYTES-off);
    if(seed){for(i=0u;i<n;++i)block[i]=(uint8_t)((off+i)^((off+i)>>8u)^0x93u);if(!dos_copy(off,n,0u))return 0u;}
    if(!dos_copy(off,n,3u))return 0u;
    for(i=0u;i<n;++i){uint8_t bit;h^=block[i];for(bit=0u;bit<8u;++bit)h=(h>>1u)^((h&1u)?0xedb88320ul:0u);}
    off=(uint16_t)(off+n);
  }return ~h;
}
static uint8_t dos_swap(uint8_t action) {
  uint16_t off=0u;
  while(off<R0FR_DOS_BYTES){uint8_t n=R0FR_DOS_BYTES-off>255u?255u:(uint8_t)(R0FR_DOS_BYTES-off);
    if(!dos_copy(off,n,action))return 0u;off=(uint16_t)(off+n);}
  return 1u;
}
static uint8_t low_copy(uint8_t restore_low) {
  uint16_t off=0u;
  while(off<R0FR_LOW_BYTES) {
    uint8_t n=R0FR_LOW_BYTES-off>255u?255u:(uint8_t)(R0FR_LOW_BYTES-off);
    if(!cfcopy(R0FR_LOW_BACKUP+off,(uint8_t *)(uintptr_t)(R0FR_LOW_START+off),n,(uint8_t)!restore_low))return 0u;
    off=(uint16_t)(off+n);
  }
  return 1u;
}
int main(void) {
  uint16_t i;uint32_t off;
  for(i=0u;i<R0FC_RESULT_BYTES;++i)cfresult[i]=0u;
  if(!cfentry())goto done;
  if(!dos_swap(4u))goto done;
  CFREG(0xd011u)&=0xefu; /* No VIC fetch from stores being reclaimed. */
  reserve=cfphysical_crc(R0FC_RESERVE,R0FC_RESERVE_BYTES);
  r0fc_reset(&model);
  if(!cfrom_begin())goto done;
  dos_before=dos_pattern_crc(1u);
  state=r0fr_transition(state,R0FR_E_RECLAIM);
  (void)r0fr_storage(); /* Must reject; no ROM or storage operation. */
  if(r0fr_denied!=1u||r0fr_phase||r0fr_returned){cffault=40u;goto done;}
  for(off=0u;off<R0FC_ROM_BYTES;) {
    uint8_t n=R0FC_ROM_BYTES-off>255u?255u:(uint8_t)(R0FC_ROM_BYTES-off);
    for(i=0u;i<n;++i)block[i]=(uint8_t)((off+i)^0x5au);
    if(!cfcopy(R0FC_ROM+off,block,n,1u))goto done;
    off+=n;
  }
  for(i=0u;i<33u;++i)r0fc_tick(&model);
  reclaimed_crc=cfphysical_crc(R0FC_ROM,R0FC_ROM_BYTES);
  before=cfcrc((const volatile uint8_t *)&model,(uint16_t)sizeof(model));
  state=r0fr_transition(state,R0FR_E_STOP);
  cfexit();
  if(cffault||!cfrom_restore())goto done;
  rom=cfget32(R0FC_O_ROM_CRC);restore=cfget32(R0FC_O_RESTORE_CRC);
  state=r0fr_transition(state,R0FR_E_RESTORE);
  for(i=0u;i<32u;++i)r0fr_payload[i]=(uint8_t)((model.checksum>>((i&3u)*8u))^(uint32_t)i);
  low_before=cfcrc((const volatile uint8_t *)(uintptr_t)R0FR_LOW_START,R0FR_LOW_BYTES);
  if(!low_copy(0u)||!dos_swap(1u)||!dos_swap(5u))goto done;
  state=r0fr_transition(state,R0FR_E_OPEN_STORAGE);
  if(!r0fr_storage_allowed(state,cfresult[R0FC_O_ROM_STATE],cffault)){cffault=41u;goto done;}
  r0fr_permit=R0FR_PERMIT;
  ++calls;
  (void)r0fr_storage();
  if(!low_copy(1u)||!dos_swap(2u))goto done;
  dos_after=dos_pattern_crc(0u);
  low_after=cfcrc((const volatile uint8_t *)(uintptr_t)R0FR_LOW_START,R0FR_LOW_BYTES);
  after=cfcrc((const volatile uint8_t *)&model,(uint16_t)sizeof(model));
  if(r0fr_phase!=5u||r0fr_error||!r0fr_returned||r0fr_input!=0u||r0fr_output!=3u||r0fr_input_end!=0u||r0fr_output_end!=3u||before!=after||low_before!=low_after||dos_before!=dos_after){cffault=42u;goto done;}
  for(i=0u;i<32u;++i)if(r0fr_read[i]!=r0fr_payload[i]||r0fr_token[i]!=(uint8_t)(i^0x65u)){cffault=43u;goto done;}
  if((uint16_t)(r0fr_end[0]|(uint16_t)r0fr_end[1]<<8u)!=(uint16_t)((uintptr_t)r0fr_read+32u)||
     (uint16_t)(r0fr_end[2]|(uint16_t)r0fr_end[3]<<8u)!=(uint16_t)((uintptr_t)r0fr_read+32u)){cffault=44u;goto done;}
  r0fc_tick(&model); /* Same model, next tick: no reset or reload. */
  state=r0fr_transition(state,R0FR_E_RESUME);
done:
  if(r0f_pf_nmi_seen)cffault=45u;
  if(cffault)state=R0FR_S_LOCKOUT;
  for(i=0u;i<256u;++i)cfresult[i]=0u;
  cfresult[0]='R';cfresult[1]='R';cfresult[2]='H';cfresult[3]='1';
  cfresult[4]=1u;cfresult[5]=127u;cfresult[6]=cffault;cfresult[7]=state;
  cfresult[8]=r0fr_denied;cfresult[9]=r0fr_phase;cfresult[10]=r0fr_error;cfresult[11]=r0fr_returned;
  cfresult[12]=r0a_basepage_read();cfresult[13]=r0f_pf_cpu_port;cfresult[14]=r0f_pf_nmi_seen;
  cfresult[15]=cfreclaimed;cfput32(16u,rom);cfput32(20u,restore);
  cfput32(24u,before);cfput32(28u,after);cfput32(32u,reserve);
  cfput32(36u,cfphysical_crc(R0FC_RESERVE,R0FC_RESERVE_BYTES));
  cfput32(40u,low_before);cfput32(44u,low_after);
  cfput16(48u,model.tick);cfput16(50u,calls);cfput32(52u,model.checksum);
  cfresult[56]=r0fr_input;cfresult[57]=r0fr_output;
  cfresult[58]=r0fr_input_end;cfresult[59]=r0fr_output_end;
  for(i=0u;i<32u;++i){cfresult[64u+i]=r0fr_token[i];cfresult[96u+i]=r0fr_payload[i];cfresult[128u+i]=r0fr_read[i];}
  for(i=0u;i<4u;++i)cfresult[160u+i]=r0fr_end[i];
  cfput16(164u,(uint16_t)(uintptr_t)r0fr_read);cfput16(166u,(uint16_t)(uintptr_t)r0fr_payload);
  cfput32(168u,dos_before);cfput32(172u,dos_after);cfput32(176u,reclaimed_crc);
  cfput32(252u,cfcrc(cfresult,252u));
  CFREG(0xd011u)|=0x10u; /* Hot-register write before the final screen pointer. */
  cffinal_screen();
  /* Clear in bounded blocks, not 2000 one-byte transfers after IOINIT. */
  for(i=0u;i<255u;++i)block[i]=32u;
  for(off=0u;off<2000u;off+=255u)(void)cfcopy(R0FC_HUD+off,block,2000u-off>255u?255u:(uint8_t)(2000u-off),1u);
  for(i=0u;i<255u;++i)block[i]=1u;
  for(off=0u;off<2000u;off+=255u)(void)cfcopy(R0FC_COLOR+off,block,2000u-off>255u?255u:(uint8_t)(2000u-off),1u);
  cfline(1u,"R0-F RH001 SAME-RUN HANDOFF - DEVELOPMENT ONLY");
  cfline(3u,"NOT FULL R0-F ACCEPTANCE / NO HARDWARE RELEASE");
  cfline(6u,cffault?"HANDOFF FAILED - SEE FAULT":"ROM RESTORED / FILE LOADED SAVED RELOADED / C RESUMED");
  cfline(8u,"FAULT / STATE / IO PHASE / IO ERROR / NEXT TICK / CRC");
  cfhex(9u,0u,cffault,2u);cfhex(9u,8u,state,2u);cfhex(9u,16u,r0fr_phase,2u);cfhex(9u,24u,r0fr_error,2u);
  cfhex(9u,32u,model.tick,4u);cfhex(9u,40u,cfget32(252u),8u);
  for(;;){}
}
