; R0-B isolated visible-FCM card and exact-restore control wrapper.
;
; This wrapper is intentionally narrower than a presentation/swap service.
; It has no D02F write, MAP, DMA, IRQ, raster, palette, or display-pointer
; write.  The caller is allowed to touch only the already-visible default C65
; text matrix at $0800 after this wrapper admits that exact configuration.
;
; Preconditions checked without mutation.  The live values are retained for
; the fixed $1800 result block so a failed admission identifies the actual
; context instead of implying that the default C65 values were observed.
;   D018 bit 5 = C65 context;
;   D031 bit 7 = 0 (40 logical 16-bit characters per 80-byte line);
;   D060..D063 = $00000800 (the default matrix the caller owns temporarily).
;
; r0b_fcm_visible_begin return A bits:
;   bit 0 C65 context; bit 1 40-column-pair precondition;
;   bit 2 default $0800 screen pointer; bit 3 D054 accepted $07.
; r0b_fcm_visible_restore return A bit 0 when the exact saved D054 byte read
; back after restoration.

        .text
        .globl r0b_fcm_visible_begin
        .globl r0b_fcm_visible_restore
        .globl r0b_fcm_visible_hold
        .globl r0b_fcm_visible_observed_d018
        .globl r0b_fcm_visible_observed_d031
        .globl r0b_fcm_visible_observed_d054
        .globl r0b_fcm_visible_observed_d060
        .globl r0b_fcm_visible_observed_d061
        .globl r0b_fcm_visible_observed_d062
        .globl r0b_fcm_visible_observed_d063

r0b_fcm_visible_begin:
        lda #$00
        sta r0b_fcm_visible_flags

        lda $d018
        sta r0b_fcm_visible_observed_d018
        lda $d031
        sta r0b_fcm_visible_observed_d031
        lda $d054
        sta r0b_fcm_visible_observed_d054
        lda $d060
        sta r0b_fcm_visible_observed_d060
        lda $d061
        sta r0b_fcm_visible_observed_d061
        lda $d062
        sta r0b_fcm_visible_observed_d062
        lda $d063
        sta r0b_fcm_visible_observed_d063

        lda r0b_fcm_visible_observed_d018
        and #$20
        beq r0b_fcm_visible_check_d031
        lda #$01
        sta r0b_fcm_visible_flags

r0b_fcm_visible_check_d031:
        lda r0b_fcm_visible_observed_d031
        and #$80
        bne r0b_fcm_visible_check_screen
        lda r0b_fcm_visible_flags
        ora #$02
        sta r0b_fcm_visible_flags

r0b_fcm_visible_check_screen:
        lda r0b_fcm_visible_observed_d060
        cmp #$00
        bne r0b_fcm_visible_check_d054
        lda r0b_fcm_visible_observed_d061
        cmp #$08
        bne r0b_fcm_visible_check_d054
        lda r0b_fcm_visible_observed_d062
        bne r0b_fcm_visible_check_d054
        lda r0b_fcm_visible_observed_d063
        bne r0b_fcm_visible_check_d054
        lda r0b_fcm_visible_flags
        ora #$04
        sta r0b_fcm_visible_flags

r0b_fcm_visible_check_d054:
        lda r0b_fcm_visible_flags
        and #$07
        cmp #$07
        bne r0b_fcm_visible_done
        lda r0b_fcm_visible_observed_d054
        sta r0b_fcm_visible_saved_d054
        ora #$07
        sta $d054
        lda $d054
        and #$07
        cmp #$07
        bne r0b_fcm_visible_done
        lda r0b_fcm_visible_flags
        ora #$08
        sta r0b_fcm_visible_flags

r0b_fcm_visible_done:
        lda r0b_fcm_visible_flags
        rts

r0b_fcm_visible_restore:
        lda r0b_fcm_visible_flags
        and #$08
        beq r0b_fcm_visible_restore_fail
        lda r0b_fcm_visible_saved_d054
        sta $d054
        cmp $d054
        bne r0b_fcm_visible_restore_fail
        lda #$01
        rts
r0b_fcm_visible_restore_fail:
        lda #$00
        rts

; Nominal visible dwell.  This does not measure or claim a duration; it merely
; leaves the card present long enough for an owner-operated observation.
; A, X, and Y are preserved.  No interrupt state changes.
r0b_fcm_visible_hold:
        pha
        lda #$b0
        sta r0b_fcm_visible_delay_high
        lda #$ff
        sta r0b_fcm_visible_delay_mid
        sta r0b_fcm_visible_delay_low
r0b_fcm_visible_hold_outer:
        dec r0b_fcm_visible_delay_low
        bne r0b_fcm_visible_hold_outer
        dec r0b_fcm_visible_delay_mid
        bne r0b_fcm_visible_hold_outer
        dec r0b_fcm_visible_delay_high
        bne r0b_fcm_visible_hold_outer
        pla
        rts

        .bss
r0b_fcm_visible_saved_d054:
        .zero 1
r0b_fcm_visible_flags:
        .zero 1
r0b_fcm_visible_delay_low:
        .zero 1
r0b_fcm_visible_delay_mid:
        .zero 1
r0b_fcm_visible_delay_high:
        .zero 1
r0b_fcm_visible_observed_d018:
        .zero 1
r0b_fcm_visible_observed_d031:
        .zero 1
r0b_fcm_visible_observed_d054:
        .zero 1
r0b_fcm_visible_observed_d060:
        .zero 1
r0b_fcm_visible_observed_d061:
        .zero 1
r0b_fcm_visible_observed_d062:
        .zero 1
r0b_fcm_visible_observed_d063:
        .zero 1
