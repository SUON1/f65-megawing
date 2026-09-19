; R0-B isolated VIC-IV $D031 80-to-40-column transition/restore probe.
;
; This proof is deliberately narrower than the FCM card proof.  It only
; admits C65 context, saves $D031, clears H640 (bit 7), verifies the latch,
; and restores the exact original byte.  It never accesses $D02F, $D054,
; screen pointers, palette, DMA, MAP, or IRQ state.
;
; Return A bitfield:
;   bit 0: C65 context ($D018 bit 5) observed
;   bit 1: $D031 read back exactly as saved-value with bit 7 clear
;   bit 2: $D031 read back exactly as its original saved value after restore

        .text
        .globl r0b_d031_restore_probe
        .globl r0b_d031_saved
        .globl r0b_d031_target
        .globl r0b_d031_readback

r0b_d031_restore_probe:
        lda #$00
        sta r0b_d031_probe_flags

        lda $d018
        and #$20
        beq r0b_d031_done

        lda #$01
        sta r0b_d031_probe_flags

        lda $d031
        sta r0b_d031_saved
        and #$7f
        sta r0b_d031_target
        sta $d031

        lda $d031
        sta r0b_d031_readback
        cmp r0b_d031_target
        bne r0b_d031_restore
        lda r0b_d031_probe_flags
        ora #$02
        sta r0b_d031_probe_flags

r0b_d031_restore:
        lda r0b_d031_saved
        sta $d031
        cmp $d031
        bne r0b_d031_done
        lda r0b_d031_probe_flags
        ora #$04
        sta r0b_d031_probe_flags

r0b_d031_done:
        lda r0b_d031_probe_flags
        rts

        .bss
r0b_d031_saved:
        .zero 1
r0b_d031_target:
        .zero 1
r0b_d031_readback:
        .zero 1
r0b_d031_probe_flags:
        .zero 1
