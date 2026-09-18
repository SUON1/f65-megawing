#include "combined_model.h"

static uint8_t bits(uint8_t v){uint8_t n=0u;while(v){++n;v=(uint8_t)(v&(uint8_t)(v-1u));}return n;}
uint8_t r0fc_edge_sample(r0fc_edges *e,uint8_t state){
  /* Keep the three byte updates distinct for the pinned MOS allocator. */
  volatile r0fc_edges *p=e;uint8_t change=(uint8_t)(p->state^state);
  p->pressed=(uint8_t)(p->pressed|(uint8_t)(change&state));
  p->released=(uint8_t)(p->released|(uint8_t)(change&p->state));p->state=state;return bits(change);}
uint8_t r0fc_edge_consume(r0fc_edges *e){uint8_t n=(uint8_t)(bits(e->pressed)+bits(e->released));
  e->pressed=e->released=0u;return n;}

uint32_t cfratio(uint32_t a,uint32_t b,uint32_t d,uint8_t shift){
  /* Exact quotient/remainder multiplication without a 64-bit target runtime.
   * Private preconditions: 0<d<1000000, shift<=16, quotient fits uint32. */
  uint32_t q=a/d,r=a%d,s=0u,t=0u;
  while(b){if(b&1u){s+=q;t+=r;if(t>=d){t-=d;++s;}}b>>=1u;
    if(b){q<<=1u;r<<=1u;if(r>=d){r-=d;++q;}}}
  while(shift--){s<<=1u;t<<=1u;if(t>=d){t-=d;++s;}}
  return s;
}

uint32_t r0fc_hash(uint32_t h, uint16_t v) {
  return ((h << 5u) | (h >> 27u)) ^ (uint32_t)v;
}
void r0fc_reset(r0fc_model *m) {
  uint8_t i;
  for(i=0u;i<R0FC_ENTITIES;++i) {
    m->x[i]=(uint16_t)(i*17u+3u);m->y[i]=(uint16_t)(i*13u+5u);
    m->z[i]=(uint16_t)(i*7u+257u);
  }
  for(i=0u;i<9u;++i)m->command[i]=m->next[i]=0u;
  for(i=0u;i<R0FC_EFFECTS;++i)m->effects[i]=i;
  m->tick=0u;m->environment=0u;m->checksum=0x0065cf01ul;
  m->event_count=m->queue_high=m->rejected=0u;
}
uint8_t r0fc_event(r0fc_model *m,uint8_t entity) {
  if(entity>=9u||m->event_count==R0FC_QUEUE_CAPACITY) {m->rejected=1u;return 0u;}
  m->events[m->event_count++]=entity;
  if(m->event_count>m->queue_high)m->queue_high=m->event_count;
  return 1u;
}
/* Non-gameplay instruction/data-access fixture in the specified stage order.
 * No coefficient below is an aircraft, sensor, weapon or AI model. */
void r0fc_tick(r0fc_model *m) {
  static const uint8_t table[16]={3u,7u,2u,11u,5u,13u,1u,9u,4u,15u,6u,12u,8u,14u,10u,0u};
  uint8_t stage,i;
  for(stage=1u;stage<=21u;++stage) {
    if(stage==1u)++m->tick;
    else if(stage==2u) { /* fixed tick-tagged input corpus, not human input */
      m->environment=(uint16_t)(m->tick&7u);
    } else if(stage==3u) {for(i=0u;i<9u;++i)m->command[i]=m->next[i];}
    else if(stage==4u)m->environment=(uint16_t)(m->environment+table[m->tick&15u]);
    else if(stage>=5u&&stage<=10u) {
      for(i=0u;i<9u;++i) {
        uint16_t v=(uint16_t)(m->x[i]+m->command[i]+m->environment+stage);
        m->x[i]=(uint16_t)(v^(uint16_t)(m->y[i]>>3u));
        m->y[i]=(uint16_t)(m->y[i]+table[v&15u]);
        m->z[i]=(uint16_t)(257u+((m->z[i]+i+stage)&1023u));
      }
    } else if(stage==11u) {m->event_count=0u;}
    else if(stage==12u) { /* all 16 + 24 + 48 existing synthetic slots */
      for(i=9u;i<97u;++i) {
        m->x[i]=(uint16_t)(m->x[i]+table[(i+m->tick)&15u]);
        m->y[i]=(uint16_t)(m->y[i]^(uint16_t)(m->x[i]>>2u));
        m->z[i]=(uint16_t)(257u+((m->z[i]+3u)&1023u));
      }
    } else if(stage==13u) {
      for(i=0u;i<R0FC_QUEUE_CAPACITY;++i)(void)r0fc_event(m,(uint8_t)(i%9u));
    } else if(stage==14u) {
      for(i=0u;i<m->event_count;++i)m->y[m->events[i]]=(uint16_t)(m->y[m->events[i]]+1u);
    } else if(stage==15u) {
      for(i=113u;i<123u;++i) {
        m->x[i]=(uint16_t)(m->x[i]+m->x[(i-113u)%9u]);
        m->y[i]=(uint16_t)(m->y[i]^m->tick);
      }
    } else if(stage==16u) {
      for(i=0u;i<9u;++i)m->next[i]=(uint16_t)((m->x[113u+i]^m->tick)&15u);
    } else if(stage==17u) {
      for(i=97u;i<113u;++i)m->x[i]=(uint16_t)(m->x[i]+m->environment+1u);
    } else if(stage==18u) {m->event_count=0u;}
    else if(stage==19u) {
      for(i=0u;i<R0FC_EFFECTS;++i)m->effects[i]=(uint16_t)((m->effects[i]+m->tick+i)&255u);
    } else if(stage==20u) {
      uint32_t h=r0fc_hash(0x0065cf01ul,m->tick);
      for(i=0u;i<R0FC_ENTITIES;++i) {h=r0fc_hash(h,m->x[i]);h=r0fc_hash(h,m->y[i]);h=r0fc_hash(h,m->z[i]);}
      for(i=0u;i<9u;++i){h=r0fc_hash(h,m->command[i]);h=r0fc_hash(h,m->next[i]);}
      m->checksum=h;
    }
    /* Stage 21 is the bounded publication call made by the owner after this
     * function; no presentation pointer ever aliases m. */
  }
}
void r0fc_snap_reset(r0fc_snapshots *s) {
  uint8_t i,j;for(i=0u;i<3u;++i) {s->state[i]=0u;for(j=0u;j<64u;++j)s->data[i][j]=0u;}
  s->skipped=s->published=s->acquired=0u;s->high=0u;s->reading=3u;
}
uint8_t r0fc_publish(r0fc_snapshots *s,const r0fc_model *m) {
  uint8_t i,j,used=0u;
  for(i=0u;i<3u&&s->state[i];++i){}
  if(i==3u){++s->skipped;return 3u;}
  s->state[i]=1u;
  s->data[i][0]=(uint8_t)m->tick;s->data[i][1]=(uint8_t)(m->tick>>8u);
  for(j=0u;j<4u;++j)s->data[i][2u+j]=(uint8_t)(m->checksum>>(j*8u));
  for(j=0u;j<9u;++j) {
    uint8_t k=(uint8_t)(6u+j*6u);uint16_t v=m->x[j];
    s->data[i][k]=(uint8_t)v;s->data[i][k+1u]=(uint8_t)(v>>8u);
    v=m->y[j];s->data[i][k+2u]=(uint8_t)v;s->data[i][k+3u]=(uint8_t)(v>>8u);
    v=m->z[j];s->data[i][k+4u]=(uint8_t)v;s->data[i][k+5u]=(uint8_t)(v>>8u);
  }
  s->state[i]=2u;++s->published;
  for(j=0u;j<3u;++j)if(s->state[j])++used;
  if(used>s->high)s->high=used;
  return i;
}
uint8_t r0fc_acquire(r0fc_snapshots *s) {
  uint8_t i,best=3u;uint16_t newest=0u;
  if(s->reading!=3u)return s->reading;
  for(i=0u;i<3u;++i)if(s->state[i]==2u) {
    uint16_t tick=(uint16_t)(s->data[i][0]|(uint16_t)s->data[i][1]<<8u);
    if(best==3u||tick>newest){best=i;newest=tick;}
  }
  if(best!=3u) {
    for(i=0u;i<3u;++i)if(s->state[i]==2u)s->state[i]=0u;
    s->state[best]=3u;s->reading=best;++s->acquired;
  }
  return best;
}
void r0fc_release(r0fc_snapshots *s) {
  if(s->reading<3u)s->state[s->reading]=0u;
  s->reading=3u;
}
static uint8_t inside(uint32_t p,uint16_t n,uint32_t start,uint32_t bytes) {
  return n&&n<=bytes&&p>=start&&p-start<=bytes-n;
}
uint8_t r0fc_range(uint32_t p,uint16_t n,uint8_t write,uint8_t reclaimed) {
  static const uint32_t ranges[][2]={{R0FC_SNAPSHOTS,192u},{R0FC_DISPLAY_META,4000u},
    {R0FC_HUD,2560u},{R0FC_COLOR,2000u},{R0FC_STAGING,8192u},{R0FC_AUDIO,255u},{R0FC_DMA_LIST,17u}};
  uint8_t i;
  if(!n||n>255u)return 0u;
  if(inside(p,n,R0FC_ROM,R0FC_ROM_BYTES))return (uint8_t)(!write||reclaimed);
  if(inside(p,n,R0FC_BACKUP,R0FC_ROM_BYTES))return 1u;
  if(!write&&inside(p,n,R0FC_RESERVE,R0FC_RESERVE_BYTES))return 1u;
  for(i=0u;i<7u;++i)if(inside(p,n,ranges[i][0],ranges[i][1]))return 1u;
  return 0u;
}
uint8_t r0fc_dma_encode(uint8_t *out,uint32_t src,uint32_t dst,uint16_t n,uint8_t reclaimed) {
  uint8_t i;
  if(!n||n>R0FC_MAX_DMA||!inside(src,n,R0FC_STAGING,8192u)||
    !(inside(dst,n,R0FC_STAGING,8192u)||(reclaimed&&inside(dst,n,R0FC_ROM,R0FC_ROM_BYTES)))||
    (src<dst+n&&dst<src+n))return 0u;
  for(i=0u;i<17u;++i)out[i]=0u;
  out[0]=0x0au;out[1]=0x80u;out[3]=0x81u;out[7]=(uint8_t)n;out[8]=(uint8_t)(n>>8u);
  for(i=0u;i<3u;++i){out[9u+i]=(uint8_t)(src>>(i*8u));out[12u+i]=(uint8_t)(dst>>(i*8u));}
  return 1u;
}
