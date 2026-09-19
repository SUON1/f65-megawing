; R0-B composite FCM / presentation transaction.
;
; This is a bounded, reversible proof transaction, not a production display
; driver.  It never writes D02F, MAP, DMA, IRQ, or colour-RAM pointers.
; It captures the live C65 text context, establishes a temporary 40-pair FCM
; context, presents a complete $1000 matrix, exercises one currently-mapped
; palette entry, and restores every register it owns exactly.

        .text
        .globl r0b_final_begin
        .globl r0b_final_swap_to_b
        .globl r0b_final_palette_probe
        .globl r0b_final_restore
        .globl r0b_final_hold
        .globl r0b_final_observed_d018
        .globl r0b_final_observed_d031
        .globl r0b_final_observed_d054
        .globl r0b_final_observed_d060
        .globl r0b_final_observed_d061
        .globl r0b_final_observed_d062
        .globl r0b_final_observed_d063
        .globl r0b_final_observed_d070

; begin return bits: C65 context, D031 target readback, D054 target readback.
r0b_final_begin:
        lda #$00
        sta r0b_final_flags
        lda $d018
        sta r0b_final_observed_d018
        lda $d031
        sta r0b_final_observed_d031
        lda $d054
        sta r0b_final_observed_d054
        lda $d060
        sta r0b_final_observed_d060
        lda $d061
        sta r0b_final_observed_d061
        lda $d062
        sta r0b_final_observed_d062
        lda $d063
        sta r0b_final_observed_d063
        lda $d070
        sta r0b_final_observed_d070

        lda r0b_final_observed_d018
        and #$20
        beq r0b_final_begin_done
        lda #$01
        sta r0b_final_flags

        lda r0b_final_observed_d031
        sta r0b_final_saved_d031
        and #$7f
        sta r0b_final_target_d031
        sta $d031
        lda $d031
        cmp r0b_final_target_d031
        bne r0b_final_begin_restore_d031
        lda r0b_final_flags
        ora #$02
        sta r0b_final_flags

        lda r0b_final_observed_d054
        sta r0b_final_saved_d054
        ora #$07
        sta r0b_final_target_d054
        sta $d054
        lda $d054
        and #$07
        cmp #$07
        bne r0b_final_begin_restore_d054
        lda r0b_final_flags
        ora #$04
        sta r0b_final_flags
        bra r0b_final_begin_done

r0b_final_begin_restore_d054:
        lda r0b_final_saved_d054
        sta $d054
r0b_final_begin_restore_d031:
        lda r0b_final_saved_d031
        sta $d031
r0b_final_begin_done:
        lda r0b_final_flags
        rts

; Swaps the precise screen pointer to the fully composed $00001000 matrix.
; Return bit 0 confirms all four pointer bytes read back as the intended value.
r0b_final_swap_to_b:
        lda r0b_final_flags
        and #$07
        cmp #$07
        bne r0b_final_swap_fail
        lda #$00
        sta $d060
        lda #$10
        sta $d061
        lda #$00
        sta $d062
        lda r0b_final_observed_d063
        and #$f0
        sta r0b_final_target_d063
        sta $d063
        lda $d060
        bne r0b_final_swap_fail
        lda $d061
        cmp #$10
        bne r0b_final_swap_fail
        lda $d062
        bne r0b_final_swap_fail
        lda $d063
        cmp r0b_final_target_d063
        bne r0b_final_swap_fail
        lda #$01
        sta r0b_final_swap_flags
        rts
r0b_final_swap_fail:
        lda #$00
        sta r0b_final_swap_flags
        rts

; A minimal active-palette proof.  The mapped bank selector is observed but is
; never changed.  One RGB entry is saved, changed, read back, restored, and
; read back exactly.  Return bits: write/readback, exact restore.
r0b_final_palette_probe:
        lda r0b_final_swap_flags
        beq r0b_final_palette_fail
        lda $d070
        cmp r0b_final_observed_d070
        bne r0b_final_palette_fail
        lda $d110
        sta r0b_final_saved_red
        eor #$0f
        sta r0b_final_target_red
        sta $d110
        lda $d110
        cmp r0b_final_target_red
        bne r0b_final_palette_restore
        lda #$01
        sta r0b_final_palette_flags
r0b_final_palette_restore:
        lda r0b_final_saved_red
        sta $d110
        lda $d110
        cmp r0b_final_saved_red
        bne r0b_final_palette_done
        lda r0b_final_palette_flags
        ora #$02
        sta r0b_final_palette_flags
r0b_final_palette_done:
        lda r0b_final_palette_flags
        rts
r0b_final_palette_fail:
        lda #$00
        sta r0b_final_palette_flags
        rts

; Restore order deliberately returns the screen pointer before returning to
; normal character/display settings.  Return bits: pointer, D054, D031 exact.
r0b_final_restore:
        lda #$00
        sta r0b_final_restore_flags
        lda r0b_final_observed_d060
        sta $d060
        lda r0b_final_observed_d061
        sta $d061
        lda r0b_final_observed_d062
        sta $d062
        lda r0b_final_observed_d063
        sta $d063
        lda $d060
        cmp r0b_final_observed_d060
        bne r0b_final_restore_d054
        lda $d061
        cmp r0b_final_observed_d061
        bne r0b_final_restore_d054
        lda $d062
        cmp r0b_final_observed_d062
        bne r0b_final_restore_d054
        lda $d063
        cmp r0b_final_observed_d063
        bne r0b_final_restore_d054
        lda #$01
        sta r0b_final_restore_flags
r0b_final_restore_d054:
        lda r0b_final_saved_d054
        sta $d054
        cmp $d054
        bne r0b_final_restore_d031
        lda r0b_final_restore_flags
        ora #$02
        sta r0b_final_restore_flags
r0b_final_restore_d031:
        lda r0b_final_saved_d031
        sta $d031
        cmp $d031
        bne r0b_final_restore_done
        lda r0b_final_restore_flags
        ora #$04
        sta r0b_final_restore_flags
r0b_final_restore_done:
        lda r0b_final_restore_flags
        rts

; Deliberate non-raster-synchronised visible dwell. It counts $D012 changes,
; making the complete matrix observable for roughly a couple of PAL seconds.
; It makes no atomicity or raster-IRQ claim.
r0b_final_hold:
        pha
        lda $d012
        sta r0b_final_hold_previous
        lda #$80
        sta r0b_final_hold_high
        lda #$00
        sta r0b_final_hold_low
r0b_final_hold_wait:
        lda $d012
        cmp r0b_final_hold_previous
        beq r0b_final_hold_wait
        sta r0b_final_hold_previous
        dec r0b_final_hold_low
        bne r0b_final_hold_wait
        dec r0b_final_hold_high
        bne r0b_final_hold_wait
        pla
        rts

        .bss
r0b_final_flags: .zero 1
r0b_final_swap_flags: .zero 1
r0b_final_palette_flags: .zero 1
r0b_final_restore_flags: .zero 1
r0b_final_saved_d031: .zero 1
r0b_final_target_d031: .zero 1
r0b_final_saved_d054: .zero 1
r0b_final_target_d054: .zero 1
r0b_final_target_d063: .zero 1
r0b_final_saved_red: .zero 1
r0b_final_target_red: .zero 1
r0b_final_observed_d018: .zero 1
r0b_final_observed_d031: .zero 1
r0b_final_observed_d054: .zero 1
r0b_final_observed_d060: .zero 1
r0b_final_observed_d061: .zero 1
r0b_final_observed_d062: .zero 1
r0b_final_observed_d063: .zero 1
r0b_final_observed_d070: .zero 1
r0b_final_hold_previous: .zero 1
r0b_final_hold_low: .zero 1
r0b_final_hold_high: .zero 1
