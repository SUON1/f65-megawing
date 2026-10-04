void cfput16(uint16_t at,uint16_t v){cfresult[at]=(uint8_t)v;cfresult[at+1u]=(uint8_t)(v>>8u);}
void cfput32(uint16_t at,uint32_t v){uint8_t i;for(i=0u;i<4u;++i){cfresult[at+i]=(uint8_t)v;v>>=8u;}}
uint32_t cfget32(uint16_t at){uint8_t i=4u;uint32_t v=0u;while(i)v=(v<<8u)|cfresult[at+--i];return v;}
uint8_t cfcopy(uint32_t physical,uint8_t *local,uint8_t n,uint8_t to_chip){uint32_t a,b;uint8_t i;
  if(!r0fc_range(physical,n,to_chip,cfreclaimed)||(to_chip&&physical>=R0FC_BACKUP&&physical<R0FC_BACKUP+R0FC_ROM_BYTES&&backup_valid)) {cffault=21u;return 0u;}
  a=to_chip?(uint32_t)(uintptr_t)local:physical;b=to_chip?physical:(uint32_t)(uintptr_t)local;
  for(i=0u;i<4u;++i){r0f_pf_copy_request[i]=(uint8_t)(a>>(i*8u));r0f_pf_copy_request[4u+i]=(uint8_t)(b>>(i*8u));}
  r0f_pf_copy_request[8]=n;if(!r0f_pf_flat_copy()){cffault=22u;return 0u;}return 1u;
}
uint32_t cfphysical_crc(uint32_t start,uint32_t bytes){uint32_t h=0xfffffffful;
  while(bytes){uint8_t n=bytes>255u?255u:(uint8_t)bytes;
    if(!cfcopy(start,block,n,0u))return 0u;
#ifdef R0FG1_INTEGRATION
    h=r0fs_crc32_update(h,block,n);
#else
    for(uint8_t i=0u;i<n;++i)h=crc_byte(h,block[i]);
#endif
    start+=n;bytes-=n;
  }return ~h;
}
uint8_t cfrom_begin(void){uint32_t off=0u;uint8_t i;
  cfline(6u,"VERIFYING IMMUTABLE ROM BACKUP - DO NOT PRESS RESTORE");
  while(off<R0FC_ROM_BYTES){uint8_t n=R0FC_ROM_BYTES-off>255u?255u:(uint8_t)(R0FC_ROM_BYTES-off);
    if(!cfcopy(R0FC_ROM+off,block,n,0u)||!cfcopy(R0FC_BACKUP+off,block,n,1u)||!cfcopy(R0FC_BACKUP+off,r0fg2_foreground_scratch,n,0u))return 0u;
    for(i=0u;i<n;++i)if(block[i]!=r0fg2_foreground_scratch[i]){cffault=23u;return 0u;}off+=n;
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
    if(!cfcopy(R0FC_BACKUP+off,block,n,0u)||!cfcopy(R0FC_ROM+off,block,n,1u)||!cfcopy(R0FC_ROM+off,r0fg2_foreground_scratch,n,0u))return 0u;
    for(i=0u;i<n;++i)if(block[i]!=r0fg2_foreground_scratch[i]){cffault=25u;return 0u;}off+=n;
  }
  cfput32(R0FC_O_RESTORE_MATCHES,off);cfput32(R0FC_O_RESTORE_CRC,cfphysical_crc(R0FC_ROM,R0FC_ROM_BYTES));
  if(cfphysical_crc(R0FC_BACKUP,R0FC_ROM_BYTES)!=cfget32(R0FC_O_ROM_CRC)||cfget32(R0FC_O_RESTORE_CRC)!=cfget32(R0FC_O_ROM_CRC)){cffault=26u;return 0u;}
  if(r0fc_rom_toggle()!=(uint8_t)(features_open|4u)||!(r0fc_trap_flags&1u)||r0fc_trap_base!=2u){cffault=27u;return 0u;}
  cfreclaimed=0u;cfresult[R0FC_O_ROM_STATE]=2u;return 1u;
}
static uint32_t crc_update(uint32_t crc, const volatile uint8_t *bytes,
                           uint16_t length)
{
    // One ordered volatile read per byte, using the shared private CRC codec.
    return r0fs_crc32_update(crc, bytes, length);
}
static uint8_t fixed_physical_copy(uint32_t source, uint32_t destination,
                                   uint8_t length)
{
    uint8_t index;

    for (index = 0u; index < 4u; index++)
    {
        r0f_pf_copy_request[index] = (uint8_t)(source >> (index * 8u));
        r0f_pf_copy_request[4u + index] =
            (uint8_t)(destination >> (index * 8u));
    }
    r0f_pf_copy_request[8] = length;
    return r0f_pf_flat_copy();
}
static uint8_t dos_copy(uint8_t action)
{
    uint16_t offset = 0u;

    while (offset < R0FS_DOS_CONTEXT_BYTES)
    {
        uint16_t remaining = (uint16_t)(R0FS_DOS_CONTEXT_BYTES - offset);
        uint8_t length = remaining > 255u ? 255u : (uint8_t)remaining;
        uint32_t source;
        uint32_t destination;

        if (action == DOS_TO_KERNAL_BACKUP)
        {
            source = R0FS_DOS_CONTEXT + offset;
            destination = R0FS_DOS_KERNAL_ENTRY_BACKUP + offset;
        }
        else if (action == DOS_TO_APPLICATION_BACKUP)
        {
            source = R0FS_DOS_CONTEXT + offset;
            destination = R0FS_DOS_APPLICATION_BACKUP + offset;
        }
        else if (action == APPLICATION_BACKUP_TO_DOS)
        {
            source = R0FS_DOS_APPLICATION_BACKUP + offset;
            destination = R0FS_DOS_CONTEXT + offset;
        }
        else if (action == KERNAL_BACKUP_TO_DOS)
        {
            source = R0FS_DOS_KERNAL_ENTRY_BACKUP + offset;
            destination = R0FS_DOS_CONTEXT + offset;
        }
        else if (action == DOS_TO_LOCAL)
        {
            source = R0FS_DOS_CONTEXT + offset;
            destination = (uint32_t)(uintptr_t)r0fg2_foreground_scratch;
        }
        else if (action == LOCAL_TO_DOS)
        {
            source = (uint32_t)(uintptr_t)r0fg2_foreground_scratch;
            destination = R0FS_DOS_CONTEXT + offset;
        }
        else
        {
            return 0u;
        }
        if (!fixed_physical_copy(source, destination, length))
        {
            return 0u;
        }
        offset = (uint16_t)(offset + length);
    }
    return 1u;
}
static uint32_t dos_crc(uint8_t write_pattern)
{
    uint16_t offset = 0u;
    uint32_t crc = 0xfffffffful;

    while (offset < R0FS_DOS_CONTEXT_BYTES)
    {
        uint16_t remaining = (uint16_t)(R0FS_DOS_CONTEXT_BYTES - offset);
        uint8_t length = remaining > 255u ? 255u : (uint8_t)remaining;
        uint16_t index;

        if (write_pattern)
        {
            for (index = 0u; index < length; index++)
            {
                uint16_t position = (uint16_t)(offset + index);

                r0fg2_foreground_scratch[index] =
                    (uint8_t)(position ^ (position >> 8u) ^ 0x93u);
            }
            if (!fixed_physical_copy((uint32_t)(uintptr_t)r0fg2_foreground_scratch,
                                     R0FS_DOS_CONTEXT + offset, length))
            {
                return 0u;
            }
        }
        if (!fixed_physical_copy(R0FS_DOS_CONTEXT + offset,
                                 (uint32_t)(uintptr_t)r0fg2_foreground_scratch, length))
        {
            return 0u;
        }
        crc = crc_update(crc, r0fg2_foreground_scratch, length);
        offset = (uint16_t)(offset + length);
    }
    return ~crc;
}
static uint8_t display_seed_staging(void)
{
    for (uint8_t index = 0u; index < sizeof(r0fg2_foreground_scratch); index++)
    {
        r0fg2_foreground_scratch[index] = 1u;
    }
    for (uint16_t offset = 0u; offset < R0FSI_DISPLAY_QUANTUM_BYTES;)
    {
        uint16_t remaining = (uint16_t)(R0FSI_DISPLAY_QUANTUM_BYTES - offset);
        uint8_t length = remaining > sizeof(r0fg2_foreground_scratch)
            ? sizeof(r0fg2_foreground_scratch) : (uint8_t)remaining;
        if (!cfcopy(R0FC_STAGING + offset, r0fg2_foreground_scratch, length, 1u))
        {
            return 0u;
        }
        offset = (uint16_t)(offset + length);
    }
    return 1u;
}
static uint8_t transfer(uint8_t trace, uint32_t offset, uint8_t bytes,
                         uint8_t write)
{
    uint32_t base = trace ? R0FG1X_TRACE_START : R0FG1X_CAPSULE_START;
    uint32_t capacity = trace ? R0FG1X_TRACE_CAPACITY : R0FG1X_CAPSULE_BYTES;
    uint32_t local = (uint32_t)(uintptr_t)r0fg2_foreground_scratch;

    if (bytes == 0u || offset > capacity || bytes > capacity - offset
        || (write && !trace))
    {
        return 0u;
    }
    for (uint8_t index = 0u; index < 4u; index++)
    {
        uint32_t source = write ? local : base + offset;
        uint32_t destination = write ? base + offset : local;

        r0f_pf_copy_request[index] = (uint8_t)(source >> (index * 8u));
        r0f_pf_copy_request[4u + index] = (uint8_t)(destination >> (index * 8u));
    }
    r0f_pf_copy_request[8] = bytes;
    return r0f_pf_flat_copy();
}
static uint8_t validate_capsule(uint8_t initial)
{
    uint32_t crc = 0xfffffffful;

    for (uint8_t guard = 0u; guard < 2u; guard++)
    {
        uint32_t offset = guard ? R0FG1X_GUARD_BYTES + R0FG1X_CONTEXT_BYTES : 0u;

        if (!transfer(0u, offset, R0FG1X_GUARD_BYTES, 0u))
        {
            return 0u;
        }
        for (uint8_t index = 0u; index < R0FG1X_GUARD_BYTES; index++)
        {
            if (r0fg2_foreground_scratch[index] != R0FG1X_GUARD_VALUE)
            {
                return 0u;
            }
        }
    }
    for (uint16_t offset = 0u; offset < R0FG1X_CONTEXT_BYTES;)
    {
        uint16_t remaining = (uint16_t)(R0FG1X_CONTEXT_BYTES - offset);
        uint8_t bytes = remaining > sizeof(r0fg2_foreground_scratch) ? sizeof(r0fg2_foreground_scratch) : (uint8_t)remaining;

        if (!transfer(0u, R0FG1X_GUARD_BYTES + offset, bytes, 0u))
        {
            return 0u;
        }
        crc = r0fs_crc32_update(crc, r0fg2_foreground_scratch, bytes);
        offset = (uint16_t)(offset + bytes);
    }
    if (initial)
    {
        capsule_crc = ~crc;
    }
    return (uint8_t)(capsule_crc == ~crc);
}
uint8_t r0fg1_transport_init(void)
{
    return (uint8_t)(validate_capsule(1u) && r0fg1_export_activate(&export));
}
uint8_t r0fg1_trace_write(uint32_t offset, const uint8_t *data, uint8_t bytes)
{
    if (export.state != R0FG1X_S_ACQUIRING || bytes == 0u)
    {
        return 0u;
    }
    for (uint8_t index = 0u; index < bytes; index++)
    {
        r0fg2_foreground_scratch[index] = data[index];
    }
    return transfer(1u, offset, bytes, 1u);
}
uint8_t r0fg1_trace_read(uint32_t offset, uint8_t *data, uint8_t bytes)
{
    if (!transfer(1u, offset, bytes, 0u))
    {
        return 0u;
    }
    for (uint8_t index = 0u; index < bytes; index++)
    {
        data[index] = r0fg2_foreground_scratch[index];
    }
    return 1u;
}
static void terminal_colors(void)
{
    uint8_t index;
    for (index = 0u; index < sizeof(r0fg2_foreground_scratch); index++)
    {
        r0fg2_foreground_scratch[index] = 1u;
    }
    for (uint16_t offset = 0u; offset < GROUP1_SCREEN_CELLS;)
    {
        uint8_t bytes = GROUP1_SCREEN_CELLS - offset > sizeof(r0fg2_foreground_scratch)
            ? sizeof(r0fg2_foreground_scratch) : (uint8_t)(GROUP1_SCREEN_CELLS - offset);
        if (!cfcopy(R0FC_COLOR + offset, r0fg2_foreground_scratch, bytes, 1u))
        {
            break;
        }
        offset = (uint16_t)(offset + bytes);
    }
}
uint8_t r0fg1_transport_prepare(uint32_t bytes, uint32_t expected_crc)
{
    uint32_t actual_crc = 0xfffffffful;
    if (cffault || cfresult[5] != 127u || cfreclaimed)
    {
        return 0u;
    }
    for (uint32_t offset = 0u; offset < bytes;)
    {
        uint32_t remaining = bytes - offset;
        uint8_t count = remaining > sizeof(r0fg2_foreground_scratch) ? sizeof(r0fg2_foreground_scratch) : (uint8_t)remaining;
        if (!transfer(1u, offset, count, 0u) || !r0fg1_export_append(&export, count))
        {
            return 0u;
        }
        actual_crc = r0fs_crc32_update(actual_crc, r0fg2_foreground_scratch, count);
        offset += count;
    }
    if (~actual_crc != expected_crc || !r0fg1_export_freeze(&export, ~actual_crc))
    {
        return 0u;
    }
    r0fg1_export_readiness readiness = {
        .acquisition_stopped = 1u,
        .dma_empty = 1u, // Inherited application DMA is synchronous; main has stopped.
        .display_stopped = (uint8_t)((CFREG(0xd011u) & 0x10u) == 0u),
        .audio_stopped = (uint8_t)(((CFREG(0xd720u) | CFREG(0xd730u)
            | CFREG(0xd740u) | CFREG(0xd750u)) & AUDIO_CHANNEL_CONTROL_MASK) == 0u),
        .irq_masked = (uint8_t)((r0fsi_irq_cpu_status() & 4u) != 0u),
        .rom_verified = (uint8_t)(!cfreclaimed && cfresult[6] == 0u),
        .capsule_verified = validate_capsule(0u),
        .nmi_seen = r0f_pf_nmi_seen,
    };
    uint8_t rejection = r0fg1_export_begin_diagnostic(&export, &readiness);
    if (rejection != 0u)
    {
        r0fg1_export_status = rejection;
        return 0u;
    }
    r0fg1_export_bytes = export.bytes;
    r0fg1_export_permit = 0xa5u;
    return 1u;
}
