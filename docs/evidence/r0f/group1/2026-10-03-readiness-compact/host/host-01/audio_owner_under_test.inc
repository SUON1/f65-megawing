void cfaudio_stop(void)
{
    CFREG(0xd720u) = 0u;
    CFREG(0xd730u) = 0u;
    CFREG(0xd740u) = 0u;
    CFREG(0xd750u) = 0u;
    CFREG(0xd711u) = 0u;
    CFREG(0xd404u) = 0u;
    CFREG(0xd418u) = 0u;
    pcm_on = 0u;
#ifdef R0FG1_INTEGRATION
    r0fg1_owner_sample(R0FG1_POOL_PCM_CHANNELS, pcm_on);
#endif
}

void cfaudio_begin(void)
{
    cfaudio_stop();
#ifdef R0FG1_INTEGRATION
    // Invalidate before rewriting; only a successful copy publishes bytes.
    audio_cache_valid = 0u;
    r0fg1_owner_sample(R0FG1_POOL_AUDIO_CACHE, audio_cache_valid);
#endif
    for (uint8_t index = 0u; index < 255u; index++)
    {
        block[index] = (uint8_t)(112u + (index & 31u));
    }
    if (!cfcopy(R0FC_AUDIO, block, 255u, 1u))
    {
        return;
    }
#ifdef R0FG1_INTEGRATION
    audio_cache_valid = 255u;
    r0fg1_owner_sample(R0FG1_POOL_AUDIO_CACHE, audio_cache_valid);
#endif
  CFREG(0xd711u)=0x80u;CFREG(0xd721u)=0u;CFREG(0xd722u)=0x30u;CFREG(0xd723u)=5u;
  CFREG(0xd72au)=0u;CFREG(0xd72bu)=0x30u;CFREG(0xd72cu)=5u;
  CFREG(0xd727u)=255u;CFREG(0xd728u)=0x30u;CFREG(0xd729u)=16u;CFREG(0xd71cu)=16u;
  CFREG(0xd724u)=0u;CFREG(0xd725u)=16u;CFREG(0xd726u)=0u;
  CFREG(0xd72du)=0u;CFREG(0xd72eu)=0u;CFREG(0xd72fu)=0u;CFREG(0xd720u)=0xe2u;
  pcm_on=1u;pcm_last=CFREG(0xd72au);service_last=cfnow();
#ifdef R0FG1_INTEGRATION
    r0fg1_owner_sample(R0FG1_POOL_PCM_CHANNELS, pcm_on);
#endif
  CFREG(0xd400u)=0x40u;CFREG(0xd401u)=0x12u;CFREG(0xd405u)=0x11u;CFREG(0xd406u)=0xf1u;CFREG(0xd404u)=0x21u;CFREG(0xd418u)=2u;
}
void cfaudio_service(uint8_t warning){uint32_t now;uint8_t p,f=CFREG(0xd7fau);
  if(f==audio_frame&&warning==(uint8_t)!pcm_on)return;
  audio_frame=f;now=cfnow();p=CFREG(0xd72au);
  if(pcm_on&&p!=pcm_last)cfadd(R0FC_O_PCM_PROGRESS,1u);pcm_last=p;
  if(now-service_last>cfget32(R0FC_O_SERVICE_GAP))cfput32(R0FC_O_SERVICE_GAP,now-service_last);service_last=now;
  if(warning&&pcm_on){CFREG(0xd720u)=0u;pcm_on=0u;cfadd(R0FC_O_PREEMPTIONS,1u);CFREG(0xd401u)=0x24u;
#ifdef R0FG1_INTEGRATION
    r0fg1_owner_sample(R0FG1_POOL_PCM_CHANNELS, pcm_on);
#endif
  }
  else if(!warning&&!pcm_on){CFREG(0xd720u)=0xe2u;pcm_on=1u;CFREG(0xd401u)=0x12u;
#ifdef R0FG1_INTEGRATION
    r0fg1_owner_sample(R0FG1_POOL_PCM_CHANNELS, pcm_on);
#endif
  }
  cfadd(R0FC_O_AUDIO_SERVICES,1u);
}
