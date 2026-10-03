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