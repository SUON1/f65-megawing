; R0-B isolated VIC-IV FCM control/restore probe.
;
; Preconditions:
;   - The normal MEGA65 C65 text context is active ($D018 bit 5 set).
;   - VIC-IV I/O has already been made visible by the platform.  This probe
;     deliberately NEVER writes the $D02F key register: the official chipset
;     reference warns that doing so is unsafe from C65 mode.
;
; Effects:
;   - Reads $D018 and $D054.
;   - If the C65 context is present, snapshots $D054, writes only its CHR16
;     and FCLRHI bits ($05), reads the latch, then restores the exact snapshot.
;   - Does not change $D031, screen/colour/character pointers, palette, MAP,
;     B, $01, DMA, IRQ masks, stack, X, Y, Z, or Q.
;
; Return A bitfield:
;   bit 0: C65 context observed
;   bit 1: $D054 read-back contained both requested bits
;   bit 2: $D054 read-back equalled the original snapshot after restoration

        .text
        .globl r0b_fcm_restore_probe

r0b_fcm_restore_probe:
        lda #$00
        sta r0b_fcm_probe_flags

        lda $d018
        and #$20
        beq r0b_fcm_probe_done

        lda #$01
        sta r0b_fcm_probe_flags

        lda $d054
        sta r0b_fcm_saved_d054
        ora #$05
        sta $d054

        lda $d054
        and #$05
        cmp #$05
        bne r0b_fcm_probe_restore
        lda r0b_fcm_probe_flags
        ora #$02
        sta r0b_fcm_probe_flags

r0b_fcm_probe_restore:
        lda r0b_fcm_saved_d054
        sta $d054
        cmp $d054
        bne r0b_fcm_probe_done
        lda r0b_fcm_probe_flags
        ora #$04
        sta r0b_fcm_probe_flags

r0b_fcm_probe_done:
        lda r0b_fcm_probe_flags
        rts

        .bss
r0b_fcm_saved_d054:
        .zero 1
r0b_fcm_probe_flags:
        .zero 1
