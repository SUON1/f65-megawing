#include "combined_platform.h"

static r0fc_model model;
static r0fc_snapshots snapshots __attribute__((section(".r0fc_hot")));
static uint16_t durations[R0FC_SAMPLES] __attribute__((section(".r0fc_capture")));
static uint16_t sorted[R0FC_TICKS];
static volatile uint16_t work[32] __attribute__((section(".r0fc_hot")));
extern uint8_t cfworkspace[255];
#define pixels cfworkspace
static uint8_t matrix[80] __attribute__((section(".r0fc_hot")));
static uint8_t display_saved[15];
static const uint16_t display_regs[15]={0xd011u,0xd031u,0xd054u,0xd058u,0xd059u,0xd05au,0xd05bu,0xd05eu,
  0xd060u,0xd061u,0xd062u,0xd063u,0xd064u,0xd065u,0xd07bu};
static uint8_t front,ready,render_stage,object,tier,bound_tier,frame;
static uint8_t depth_order[9];
static uint16_t clear_at,kernel_n,render_x,render_y;
static uint32_t bound_hash;

/* Calibration kernel is C, finite and observable. No NOP padding or literal
 * cycle labels. Each batch mutates all 32 SoA-like work values. */
static void kernel(uint16_t batches){uint16_t k;uint8_t i;
  for(k=0u;k<batches;++k)for(i=0u;i<32u;++i){uint16_t v=work[i];
    v=(uint16_t)(v+(uint16_t)(work[(i+7u)&31u]>>2u)+i+1u);
    work[i]=(v&1u)?(uint16_t)(v^0x65a5u):(uint16_t)((v<<1u)|(v>>15u));
  }
}
static void kernel_calibrate(void){uint32_t a,b,target,base;uint8_t i;
  for(i=0u;i<32u;++i)work[i]=(uint16_t)(i*13u+1u);
  r0fc_reset(&model);a=cfnow();for(i=0u;i<33u;++i)r0fc_tick(&model);b=cfnow();
  base=((b-a)/33u)*10u/3u;cfput32(1664u,base);
  a=cfnow();kernel(8u);b=cfnow();
  if(b<=a||b-a>100000u){cffault=40u;return;}
  target=cfratio(R0FC_COMPARISON_CYCLES,cfcia_frame,cfcycles_frame,0u);
  kernel_n=target>base?(uint16_t)(((target-base)*8u)/(b-a)):0u;if(kernel_n>4096u){cffault=41u;return;}
  a=cfnow();kernel(kernel_n);b=cfnow();cfput16(R0FC_O_KERNEL_ITERATIONS,kernel_n);
  cfput32(R0FC_O_KERNEL_COUNTS,b-a+base);target=cfcycles(b-a+base);cfput32(R0FC_O_KERNEL_CYCLES,target);
  cfput32(R0FC_O_KERNEL_ERROR,target>530000ul?target-530000ul:530000ul-target);
}
static void metadata(uint8_t bank){uint8_t row,col;uint16_t cell=0u;
  for(row=0u;row<25u;++row){for(col=0u;col<40u;++col){uint16_t card;
      if(row==24u)card=(uint16_t)(R0FC_HUD/64u+col);
      else card=(uint16_t)((bank?0x30000ul:0x20000ul)/64u+cell);
      matrix[col*2u]=(uint8_t)card;matrix[col*2u+1u]=(uint8_t)(card>>8u);++cell;
    }(void)cfcopy(R0FC_DISPLAY_META+(uint32_t)bank*2000u+(uint16_t)row*80u,matrix,80u,1u);}
}
static void display_begin(void){uint8_t i;uint32_t off;
  for(i=0u;i<15u;++i)display_saved[i]=CFREG(display_regs[i]);CFREG(0xd011u)&=0xefu;
  for(i=0u;i<255u;++i)pixels[i]=1u;
  for(off=0u;off<4096u;off+=255u)(void)cfcopy(R0FC_STAGING+off,pixels,4096u-off>255u?255u:(uint8_t)(4096u-off),1u);
  (void)cfdma(R0FC_STAGING,R0FC_STAGING+4096u,4096u);
  if(cfphysical_crc(R0FC_STAGING,4096u)!=cfphysical_crc(R0FC_STAGING+4096u,4096u))cffault=49u;
  for(off=0u;off<131072ul&&!cffault;off+=4096u){uint16_t n=4096u;
    (void)cfdma(R0FC_STAGING,R0FC_ROM+off,n);}
  metadata(0u);metadata(1u);
  for(i=0u;i<255u;++i)pixels[i]=0u;
  for(off=0u;off<2000u&&!cffault;off+=255u)(void)cfcopy(R0FC_COLOR+off,pixels,2000u-off>255u?255u:(uint8_t)(2000u-off),1u);
  for(i=0u;i<255u;++i)pixels[i]=5u;
  for(off=0u;off<2560u&&!cffault;off+=255u)(void)cfcopy(R0FC_HUD+off,pixels,2560u-off>255u?255u:(uint8_t)(2560u-off),1u);
  CFREG(0xd031u)&=0x7fu;CFREG(0xd054u)|=7u;CFREG(0xd058u)=80u;CFREG(0xd059u)=0u;
  CFREG(0xd05eu)=40u;CFREG(0xd060u)=0u;CFREG(0xd061u)=0xc0u;CFREG(0xd062u)=1u;CFREG(0xd063u)=0u;
  CFREG(0xd064u)=0u;CFREG(0xd065u)=0u;CFREG(0xd07bu)=25u;
  CFREG(0xd011u)=display_saved[0];front=ready=render_stage=0u;frame=CFREG(0xd7fau);
}
static void display_restore(void){uint8_t i;CFREG(0xd011u)&=0xefu;
  for(i=1u;i<15u;++i)CFREG(display_regs[i])=display_saved[i];
  /* Restore simple readable text colors without touching CIA I/O aliases. */
  for(i=0u;i<255u;++i)pixels[i]=1u;
  {uint32_t off;for(off=0u;off<2000u;off+=255u)(void)cfcopy(R0FC_COLOR+off,pixels,2000u-off>255u?255u:(uint8_t)(2000u-off),1u);}
  CFREG(0xd011u)=display_saved[0];
}
static uint16_t le16(const uint8_t *p){return (uint16_t)(p[0]|(uint16_t)p[1]<<8u);}
static void render_quantum(uint8_t lag){uint8_t slot=snapshots.reading,i;uint32_t dest;
  uint8_t current=CFREG(0xd7fau);
  if(current!=frame){frame=current;
    if(ready){uint32_t p=R0FC_DISPLAY_META+(uint32_t)(front^1u)*2000u;
      /* The frame counter has just changed; only a completed store is offered. */
      CFREG(0xd060u)=(uint8_t)p;CFREG(0xd061u)=(uint8_t)(p>>8u);CFREG(0xd062u)=(uint8_t)(p>>16u);
      front^=1u;ready=0u;cfadd(R0FC_O_SWAPS,1u);}
  }
  if(ready)return;
  if(!render_stage){slot=r0fc_acquire(&snapshots);if(slot==3u)return;
    bound_hash=cfcrc(snapshots.data[slot],64u);bound_tier=tier;clear_at=0u;render_stage=1u;object=0u;
    for(i=0u;i<9u;++i){uint8_t j=i;while(j&&le16(&snapshots.data[slot][10u+depth_order[j-1u]*6u])<le16(&snapshots.data[slot][10u+i*6u])){depth_order[j]=depth_order[j-1u];--j;}depth_order[j]=i;}}
  if(lag&&(model.tick%8u)!=0u)return;
  dest=(front?0x20000ul:0x30000ul);
  if(render_stage==1u){uint16_t n=4096u;
    (void)cfdma(R0FC_STAGING,dest+clear_at,n);clear_at=(uint16_t)(clear_at+n);
    if(clear_at==61440u)render_stage=2u;return;}
  /* Bounded painter-ordered synthetic triangles; coordinates come only from
   * the acquired immutable record. Projection uses widened integer division. */
  if(render_stage==2u&&object<9u){const uint8_t *p=&snapshots.data[slot][6u+depth_order[object]*6u];
    int16_t x=(int16_t)((le16(p)&255u)-128),y=(int16_t)((le16(p+2u)&127u)-64);
    uint16_t z=(uint16_t)(257u+(le16(p+4u)&1023u));
    int32_t sx=160+(int32_t)x*128/z,sy=96+(int32_t)y*128/z;
    if(sx<0||sx>=312||sy<0||sy>=176){++object;return;}
    render_x=(uint16_t)sx&0xfff8u;render_y=(uint16_t)sy&0xfff8u;render_stage=3u;
  }
  if(render_stage==3u){uint32_t at=(uint32_t)(render_y>>3u)*2560u+(render_x>>3u)*64u;
    /* The candidate quantizes tiny synthetic triangles to an 8x8 card. One
     * bounded object quantum generates eight top-left-inclusive spans. */
    for(i=0u;i<64u;++i){uint8_t y=(uint8_t)(i>>3u),x=(uint8_t)(i&7u),lo=(uint8_t)(y>>1u);
      uint8_t on=(uint8_t)(x>=lo);
      if(bound_tier==1u)on=(uint8_t)(x>=2u&&x<=5u&&y>=2u&&y<=5u&&x>=lo);
      if(bound_tier==2u)on=(uint8_t)(on&&(y==0u||x==lo||x==7u));
      if(bound_tier==3u)on=(uint8_t)(x>=2u&&x<6u&&y>=2u&&y<6u);
      pixels[i]=on?(uint8_t)(2u+object):1u;}
    (void)cfcopy(dest+at,pixels,64u,1u);++object;render_stage=2u;
  }
  if(object==9u){if(cfcrc(snapshots.data[slot],64u)!=bound_hash){cffault=42u;return;}
    cfadd(R0FC_O_RENDERED,1u);ready=1u;render_stage=0u;r0fc_release(&snapshots);}
}
static void hud(uint16_t tick){uint8_t i;for(i=0u;i<64u;++i)pixels[i]=(uint8_t)(((tick+i)&8u)?5u:2u);
  (void)cfcopy(R0FC_HUD,pixels,64u,1u);}
static void record_phase(uint8_t cohort,uint16_t sample,uint16_t late,uint32_t span_count){uint8_t i,j;uint32_t sum=0u;uint16_t at=(uint16_t)(R0FC_RECORD+(uint16_t)cohort*16u);
  for(i=0u;i<33u;++i){uint16_t v=durations[sample+i];sorted[i]=v;sum+=v;}
  for(i=1u;i<33u;++i){uint16_t v=sorted[i];j=i;while(j&&sorted[j-1u]>v){sorted[j]=sorted[j-1u];--j;}sorted[j]=v;}
  cfinput();cfaudio_service(0u);
  cfput16(at,sorted[16]);cfput16(at+2u,sorted[31]);cfput16(at+4u,sorted[32]);cfput16(at+6u,late);
  cfput32(at+8u,sum);cfput32(at+12u,span_count);
}
static void sweep(void){uint8_t kind,phase;uint16_t sample=0u;uint32_t golden=0u;
  for(kind=0u;kind<5u&&!cffault;++kind)for(phase=0u;phase<16u&&!cffault;++phase){
    uint8_t tick;uint16_t fraction=0u,late_max=0u,first_sample=sample,credit=0u;
    uint32_t deadline,start,end,phase_start,swaps_start=cfget32(R0FC_O_SWAPS);
    r0fc_reset(&model);r0fc_snap_reset(&snapshots);render_stage=ready=0u;
    phase_start=cfframe_wait();deadline=phase_start+((cfperiod>>16u)*phase)/16u;
    for(tick=1u;tick<=33u&&!cffault;++tick){uint32_t now;
      do {now=cfnow();if((int32_t)(now-deadline)<0){render_quantum((uint8_t)(kind==1u));cfinput();cfaudio_service((uint8_t)(kind==4u&&tick>=16u&&tick<24u));}}
      while((int32_t)(now-deadline)<0&&!cffault);
      start=cfnow();now=start-deadline;if(now>65535u){cffault=43u;break;}if(now>late_max)late_max=(uint16_t)now;
      if(now>(cfperiod>>16u)*8u){cffault=44u;break;}
      cfinput_tick((uint8_t)(kind==4u&&tick>=8u&&tick<16u));r0fc_tick(&model);
      /* Measured comparison batch spread at 30 batches per 100 ticks, never
       * driven by raster. Its work state is excluded from authority. */
      credit=(uint16_t)(credit+kernel_n*3u);kernel((uint16_t)(credit/10u));credit=(uint16_t)(credit%10u);
      {uint8_t slot=r0fc_publish(&snapshots,&model);if(slot<3u)(void)cfcopy(R0FC_SNAPSHOTS+(uint16_t)slot*64u,snapshots.data[slot],64u,1u);}
      if(kind==3u&&tick==17u){uint8_t n;for(n=0u;n<64u;++n)(void)r0fc_event(&model,0u);
        if(r0fc_event(&model,0u)){cffault=45u;break;}cfresult[R0FC_O_CONTROLLED_FAULTS]++;model.event_count=0u;}
      cfinput();cfaudio_service((uint8_t)(kind==4u&&tick>=16u&&tick<24u));hud(tick);
      tier=kind==2u?(uint8_t)((tick/8u)&3u):0u;cfresult[R0FC_O_TIER_MASK]|=(uint8_t)(1u<<tier);
      end=cfnow();if(end-start>65535u){cffault=46u;break;}durations[sample++]=(uint16_t)(end-start);
      deadline+=cfperiod>>16u;{uint16_t old=fraction;fraction=(uint16_t)(fraction+(uint16_t)cfperiod);if(fraction<old)++deadline;}
      cfadd(R0FC_O_TOTAL_TICKS,1u);
    }
    if(cffault)break;
    if(!golden)golden=model.checksum;else if(model.checksum!=golden){cffault=47u;break;}
    cfput32(R0FC_O_LAST_CHECKSUM,model.checksum);cfadd(R0FC_O_SKIPPED,snapshots.skipped);
    if(snapshots.high>cfresult[R0FC_O_SNAPSHOT_HIGH])cfresult[R0FC_O_SNAPSHOT_HIGH]=snapshots.high;
    cfresult[R0FC_O_QUEUE_HIGH]=model.queue_high;
    record_phase((uint8_t)(kind*16u+phase),first_sample,late_max,end-phase_start);
    cfresult[R0FC_O_PHASE_SWAPS+kind*16u+phase]=(uint8_t)(cfget32(R0FC_O_SWAPS)-swaps_start);
  }
  cfput16(R0FC_O_DURATION_BYTES,(uint16_t)(sample*2u));
}
int main(void){uint16_t i;uint8_t display=0u,page=255u;
  for(i=0u;i<R0FC_RESULT_BYTES;++i)cfresult[i]=0u;
  cfresult[0]='R';cfresult[1]='C';cfresult[2]='F';cfresult[3]='1';cfresult[4]=1u;cfresult[5]=1u;
  cfscreen();if(cfentry()){
    cfput32(R0FC_O_RESERVE_BEFORE,cfphysical_crc(R0FC_RESERVE,R0FC_RESERVE_BYTES));
    cfresult[5]=2u;
    if(cfrom_begin()&&cfclock_begin()&&cfcalibrate(0u)){
      cfresult[5]=3u;kernel_calibrate();
      if(!cffault){cfresult[5]=4u;display_begin();display=1u;cfaudio_begin();
        if(!cffault){cfresult[5]=5u;sweep();}
        if(!cffault){cfresult[5]=6u;(void)cfcalibrate(1u);}
      }
    }
  }
  cfexit();if(display)CFREG(0xd011u)&=0xefu;
  if(cfreclaimed){cfresult[5]=7u;(void)cfrom_restore();}
  if(display)display_restore();
  cfput32(R0FC_O_RESERVE_AFTER,cfphysical_crc(R0FC_RESERVE,R0FC_RESERVE_BYTES));
  if(cfget32(R0FC_O_RESERVE_BEFORE)!=cfget32(R0FC_O_RESERVE_AFTER))cffault=48u;
  cfput16(R0FC_O_DURATION_ADDRESS,(uint16_t)(uintptr_t)durations);
  cfput32(R0FC_O_DURATION_CRC,cfcrc((const volatile uint8_t *)durations,5280u));
  cfput16(R0FC_O_ACTIVE_SLOTS,187u);cfresult[6]=cffault;if(!cffault)cfresult[5]=127u;
  cfput32(R0FC_O_CRC32,cfcrc(cfresult,R0FC_O_CRC32));cffinal_screen();
summary:
  cfscreen();
  cfline(5u,cffault?"EXPERIMENT STOPPED - NO ACCEPTANCE":"ACQUISITION COMPLETE - PHYSICAL REVIEW STILL REQUIRED");
  cfline(7u,"FAULT / REFERENCE / ROM RESTORED / TICKS / CRC32");
  cfhex(8u,0u,cffault,2u);cfhex(8u,8u,cfresult[7],2u);cfhex(8u,16u,cfresult[12],2u);
  cfhex(8u,24u,cfget32(R0FC_O_TOTAL_TICKS),8u);cfhex(8u,36u,cfget32(R0FC_O_CRC32),8u);
  cfline(10u,"KERNEL CLOCK ESTIMATE / CALIBRATION ERROR / CLOCK FRAME");
  cfhex(11u,0u,cfget32(R0FC_O_KERNEL_CYCLES),8u);cfhex(11u,12u,cfget32(R0FC_O_KERNEL_ERROR),8u);cfhex(11u,24u,cfcycles_frame,8u);
  cfline(13u,"DMA JOBS / PCM MOVES / REAL KEY EDGES / WORLD SWAPS");
  cfhex(14u,0u,(uint16_t)(cfresult[78]|(uint16_t)cfresult[79]<<8u),4u);cfhex(14u,12u,cfget32(R0FC_O_PCM_PROGRESS),8u);
  cfhex(14u,24u,cfget32(R0FC_O_INPUT_EDGES),8u);cfhex(14u,36u,cfget32(R0FC_O_SWAPS),8u);
  cfline(17u,"REF 01=XEMU MODEL. 02=NOMINAL HARDWARE COUNTERS.");
  cfline(18u,"NO TRACEABLE SI / EXTERNAL LATENCY / R0-F ACCEPTANCE.");
  cfline(20u,"ROM STATE 02=RESTORED. RESET REQUIRED.");
  cfline(21u,"N: RAW CAPTURE. RESET REQUIRED. NO DISK WRITES.");
  for(;;){uint8_t key=CFREG(0xd610u);if(!key)continue;CFREG(0xd610u)=0u;key&=0xdfu;
    if(key=='S'){page=255u;goto summary;}
    if(key=='N'||key==0u)page=page>=13u?0u:(uint8_t)(page+1u);
    else if(key=='P')page=page==0u||page==255u?13u:(uint8_t)(page-1u);else continue;
    cfscreen();cfline(3u,"RAW: 14 PAGES. N/NEXT P/PREV S/SUMMARY. FIELDS HEX.");
    cfhex(4u,0u,(uint8_t)(page+1u),2u);cfhex(4u,8u,(uint16_t)page*512u,4u);
    cfhex(4u,16u,page==13u?416u:512u,4u);cfhex(4u,24u,cfget32(R0FC_O_CRC32),8u);cfhex(4u,36u,cfget32(R0FC_O_DURATION_CRC),8u);
    for(i=0u;i<512u;++i){uint16_t at=(uint16_t)((uint16_t)page*512u+i);uint8_t v=0u;
      if(at<1792u)v=cfresult[at];else if(at<7072u)v=((const uint8_t *)durations)[at-1792u];
      cfhex((uint8_t)(6u+(i>>5u)),(uint8_t)((i&31u)*2u),v,2u);}
  }
}
