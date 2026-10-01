#ifdef R0FG1_INTEGRATION
static void display_quantum_work(void)
#else
static void display_quantum(void)
#endif
{
#ifndef R0FG1_INTEGRATION
    uint8_t index;
#endif
    uint8_t frame = CFREG(0xd7fau);
    uint32_t destination = display_front ? R0FC_ROM : R0FC_ROM + 0x10000ul;

#ifdef R0FG1_INTEGRATION
    uint8_t view = (uint8_t)((model.tick >> R0FG1P_VIEW_TICK_SHIFT) & 1u);
    if (view != display_presentation.requested_view)
    {
        if (!r0fg1_view_request(&display_presentation, view)
            || display_requests == UINT16_MAX)
        {
            cffault = 113u;
            return;
        }
        display_request_tick = model.tick;
        display_requests++;
        if (display_presentation.busy)
        {
            if (display_cancels == UINT16_MAX)
            {
                cffault = 113u;
                return;
            }
            r0fg1_presentation_cancel(&display_presentation);
            if (display_slot < R0FC_SNAPSHOT_COUNT)
            {
                r0fc_release(&snapshots);
                display_slot = R0FC_SNAPSHOT_COUNT;
            }
            display_ready = 0u;
            display_cancels++;
        }
    }
#endif
    if (frame != display_frame)
    {
        display_frame = frame;
        if (display_ready)
        {
            uint32_t screen = display_front ? R0FC_ROM : R0FC_ROM + 0x10000ul;

#ifdef R0FG1_INTEGRATION
            if (!r0fg1_presentation_swap(&display_presentation))
            {
                cffault = 113u;
                return;
            }
#endif
            // The two stores share pointer low/mid bytes: only $D062 changes.
            // No IRQ reads the foreground registration/composition state.
            CFREG(0xd060u) = (uint8_t)screen;
            CFREG(0xd061u) = (uint8_t)(screen >> 8u);
            CFREG(0xd062u) = (uint8_t)(screen >> 16u);
#ifdef R0FG1_INTEGRATION
            const r0fg1_presentation_key *key = &display_presentation.displayed.key;
            uint8_t anchor_mask = 0u;
            for (uint8_t anchor = 0u;
                 anchor < display_presentation.displayed.anchor_count; anchor++)
            {
                uint16_t handle = display_presentation.displayed.anchors[anchor].handle;
                if (handle >= R0FG1P_SCENE_CANDIDATES)
                {
                    cffault = 113u;
                    return;
                }
                anchor_mask |= (uint8_t)(1u << handle);
            }
            display_views |= (uint8_t)(1u << key->view);
            display_tiers |= (uint8_t)(1u << key->tier);
            r0fg1_world(key->source_tick, display_request_tick,
                (uint8_t)(key->view | (uint8_t)(key->tier << 1u)
                    | (uint8_t)(key->buffer << 2u)), anchor_mask,
                display_registration_crc);
#endif
            display_front ^= 1u;
            display_ready = 0u;
        }
    }
    if (display_ready)
    {
        return;
    }
    if (display_slot == R0FC_SNAPSHOT_COUNT)
    {
        display_slot = r0fc_acquire(&snapshots);
        if (display_slot == R0FC_SNAPSHOT_COUNT)
        {
            return;
        }
#ifdef R0FG1_INTEGRATION
        display_source_tick = (uint16_t)(snapshots.data[display_slot][0]
            | (uint16_t)snapshots.data[display_slot][1] << 8u);
        if (!r0fg1_scene_bind(&display_presentation, display_source_tick,
                             (uint8_t)(display_front ^ 1u)))
        {
            cffault = 113u;
            return;
        }
#endif
        display_snapshot_crc =
            cfcrc(snapshots.data[display_slot], R0FC_SNAPSHOT_BYTES);
        display_clear_at = 0u;
    }
    if (display_clear_at < R0FSI_DISPLAY_BUFFER_BYTES)
    {
        if (!application_dma(R0FC_STAGING, destination + display_clear_at,
                             R0FSI_DISPLAY_QUANTUM_BYTES))
        {
            return;
        }
        display_clear_at =
            (uint16_t)(display_clear_at + R0FSI_DISPLAY_QUANTUM_BYTES);
        return;
    }
#ifdef R0FG1_INTEGRATION
    if (display_clear_at == R0FSI_DISPLAY_BUFFER_BYTES)
    {
        if (!r0fg1_scene_encode(&display_presentation, display_pixels))
        {
            cffault = 113u;
            return;
        }
        display_registration_crc = cfcrc(display_pixels, sizeof(display_pixels));
        display_clear_at++;
        return;
    }
    if (display_clear_at < GROUP1_DISPLAY_COMPLETE)
    {
        // Nine 65-byte fixture copies: the maximum offset is only 520 bytes.
        uint16_t offset = (uint16_t)((display_clear_at - GROUP1_DISPLAY_COPY_BEGIN)
            * sizeof(display_pixels));
        if (cfcopy(destination + offset, display_pixels, sizeof(display_pixels), 1u))
        {
            display_clear_at++;
        }
        return;
    }
#else
    for (index = 0u; index < sizeof(display_pixels); index++)
    {
        display_pixels[index] =
            snapshots.data[display_slot][index] == 0u ? 1u : 5u;
    }
    for (index = 0u; index < 9u; index++)
    {
        uint32_t offset = (uint32_t)index * sizeof(display_pixels);

        if (!cfcopy(destination + offset, display_pixels,
                    sizeof(display_pixels), 1u))
        {
            return;
        }
    }
#endif
    if (cfcrc(snapshots.data[display_slot], R0FC_SNAPSHOT_BYTES)
        != display_snapshot_crc)
    {
        cffault = 70u;
        return;
    }
    r0fc_release(&snapshots);
    display_slot = R0FC_SNAPSHOT_COUNT;
#ifdef R0FG1_INTEGRATION
    if (!r0fg1_presentation_complete(&display_presentation,
                                     &display_presentation.building.key, 1u))
    {
        cffault = 113u;
        return;
    }
#endif
    display_ready = 1u;
    display_services++;
}
