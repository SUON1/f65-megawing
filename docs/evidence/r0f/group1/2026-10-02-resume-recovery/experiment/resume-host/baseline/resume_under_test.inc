uint8_t cfclock_begin(void){if(CFREG(0xdc0eu)&0x40u){cffault=2u;return 0u;}
  CFREG(0xdc0eu)=0u;CFREG(0xdc0fu)=0u;CFREG(0xdc04u)=255u;CFREG(0xdc05u)=255u;CFREG(0xdc06u)=255u;CFREG(0xdc07u)=255u;
  CFREG(0xdc0fu)=0x51u;CFREG(0xdc0eu)=0x11u;r0f_pf_start_irq();return 1u;}

uint32_t cfnow(void){uint8_t n;for(n=0u;n<32u;++n){uint8_t bh=CFREG(0xdc07u),bl=CFREG(0xdc06u),bh2=CFREG(0xdc07u);
    uint8_t ah=CFREG(0xdc05u),al=CFREG(0xdc04u),ah2=CFREG(0xdc05u),bl2=CFREG(0xdc06u),bh3=CFREG(0xdc07u);
    if(bh==bh2&&bh==bh3&&bl==bl2&&ah==ah2&&!(ah==255u&&al>=240u))return ~((uint32_t)bh<<24u|(uint32_t)bl<<16u|(uint16_t)ah<<8u|al);
  }cffault=3u;return 0u;}

uint8_t cfdma(uint32_t src,uint32_t dst,uint16_t n){uint32_t a,b;
  if(!r0fc_dma_encode(list,src,dst,n,cfreclaimed)){cffault=30u;return 0u;}
  if(!cfcopy(R0FC_DMA_LIST,list,17u,1u))return 0u;
  a=cfnow();CFREG(0xd702u)=5u;CFREG(0xd704u)=0u;CFREG(0xd701u)=0x60u;CFREG(0xd705u)=0u;b=cfnow();
#ifdef R0FG1_INTEGRATION
  r0fg1_dma(a);
#endif
  {uint16_t jobs=(uint16_t)(cfresult[R0FC_O_DMA_JOBS]|(uint16_t)cfresult[R0FC_O_DMA_JOBS+1u]<<8u);cfput16(R0FC_O_DMA_JOBS,(uint16_t)(jobs+1u));}
  if(b-a>cfget32(R0FC_O_DMA_MAX))cfput32(R0FC_O_DMA_MAX,b-a);
  return (uint8_t)!cffault;
}

static uint8_t application_dma(uint32_t source, uint32_t destination,
                               uint16_t length)
{
    uint8_t ok;

    if (application_dma_outstanding)
    {
        cffault = 89u;
        return 0u;
    }
    application_dma_outstanding = 1u;
    ok = cfdma(source, destination, length);
    application_dma_outstanding = 0u;
    return ok;
}

static uint8_t display_seed_staging(void)
{
    for (uint8_t index = 0u; index < sizeof(transfer); index++)
    {
        transfer[index] = 1u;
    }
    for (uint16_t offset = 0u; offset < R0FSI_DISPLAY_QUANTUM_BYTES;)
    {
        uint16_t remaining = (uint16_t)(R0FSI_DISPLAY_QUANTUM_BYTES - offset);
        uint8_t length = remaining > sizeof(transfer)
            ? sizeof(transfer) : (uint8_t)remaining;
        if (!cfcopy(R0FC_STAGING + offset, transfer, length, 1u))
        {
            return 0u;
        }
        offset = (uint16_t)(offset + length);
    }
    return 1u;
}

static uint8_t display_resume(void)
{
    if (!display_suspended || application_dma_outstanding)
    {
        return 0u;
    }
#ifdef R0FG1_INTEGRATION
    // ROM restoration destroyed both pixel stores. Discard the ready attempt
    // and display an explicit unregistered fallback, never stale registration.
    // Low-application backup is already restored; staging can be seeded again.
    r0fg1_presentation_cancel(&display_presentation);
    display_presentation.displayed_valid = 0u;
    display_ready = 0u;
    if (!display_seed_staging())
    {
        return 0u;
    }
    for (display_clear_at = 0u;
         display_clear_at < R0FSI_DISPLAY_BUFFER_BYTES;
         display_clear_at = (uint16_t)(display_clear_at + R0FSI_DISPLAY_QUANTUM_BYTES))
    {
        if (!application_dma(R0FC_STAGING,
                R0FC_ROM + (uint32_t)display_front * 0x10000ul + display_clear_at,
                R0FSI_DISPLAY_QUANTUM_BYTES))
        {
            return 0u;
        }
    }
#endif
    display_configure();
    CFREG(0xd011u) = display_suspended_d011;
    display_suspended = 0u;
    return 1u;
}

static void lockout(uint8_t fault);

static void result_u16(uint16_t offset, uint16_t value)
{
    cfresult[offset] = (uint8_t)value;
    cfresult[offset + 1u] = (uint8_t)(value >> 8u);
}

static uint8_t transition(uint8_t event)
{
    lifecycle_state = r0fs_transition(lifecycle_state, event);
    if (lifecycle_state == R0FS_S_LOCKOUT)
    {
        lockout(71u);
        return 0u;
    }
    return 1u;
}

static uint8_t resume_boundary(void)
{
    uint16_t tick_before = 1600u;
    uint32_t checksum_before = 0x6b765fdbul;
    uint32_t low_before = 1u, low_after = 1u;
    uint32_t dos_before = 2u, dos_after = 2u;
    r0fs_context_invalidate();
    context_invalidated_record = 1u;
    if (r0f_pf_nmi_seen
        || !r0fs_resume_allowed(lifecycle_state, 1u, 1u, 0u)
        || !transition(R0FS_E_RESUME_SERVICES)
        || !reclaim_after_storage())
    {
        lockout(81u);
        return 0u;
    }
    if (!display_resume())
    {
        lockout(93u);
        return 0u;
    }
    if (!cfclock_begin())
    {
        lockout(82u);
        return 0u;
    }
    r0fsi_irq_select_line();
    // Audio initialization reads the CIA clock; restart it first after KERNAL.
    cfaudio_begin();
    if (r0f_pf_nmi_seen)
    {
        lockout(94u);
        return 0u;
    }
    next_deadline = cfnow() + (cfperiod >> 16u);
    tick_before_record = tick_before;
    checksum_before_record = checksum_before;
    low_before_record = low_before;
    low_after_record = low_after;
    dos_before_record = dos_before;
    dos_after_record = dos_after;
    return 1u;
}
