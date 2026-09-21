.include "interfaces/generated/r0f_successor.inc"

/* This is a proof-only pre-C capture skeleton. B=0x16 selects scratch at
 * 0x1622-0x162a, outside the opaque 0x0000-0x15ff source. No stack access,
 * callback, MAP change or DMA occurs before every source byte is captured. */
.section .init.005,"ax",@progbits
.global r0fs_pre_c_capture, r0fs_pre_c_capture_end
r0fs_pre_c_capture:
    sei
    lda #R0FS_PRE_C_SCRATCH_BASE_PAGE
    tab
    lda #$00
    sta $22
    sta $23
    sta $24
    sta $25
    lda #<R0FS_KERNAL_CONTEXT_ALLOCATION
    sta $26
    lda #>R0FS_KERNAL_CONTEXT_ALLOCATION
    sta $27
    lda #((R0FS_KERNAL_CONTEXT_ALLOCATION >> 16) & $ff)
    sta $28
    lda #((R0FS_KERNAL_CONTEXT_ALLOCATION >> 24) & $ff)
    sta $29
    lda #R0FS_KERNAL_CONTEXT_GUARD
    ldz #$00
    .rept R0FS_KERNAL_CONTEXT_GUARD_BYTES
    sta [$26],z
    inz
    .endr
    lda #<R0FS_KERNAL_CONTEXT_PAYLOAD
    sta $26
    lda #>R0FS_KERNAL_CONTEXT_PAYLOAD
    sta $27
    lda #(R0FS_KERNAL_CONTEXT_BYTES / $100)
    sta $2a
    ldz #$00
.Lcapture_byte:
    lda [$22],z
    sta [$26],z
    inz
    bne .Lcapture_byte
    inc $23
    inc $27
    dec $2a
    bne .Lcapture_byte
    lda #R0FS_KERNAL_CONTEXT_GUARD
    ldz #$00
    .rept R0FS_KERNAL_CONTEXT_GUARD_BYTES
    sta [$26],z
    inz
    .endr
r0fs_pre_c_capture_end:

/* Structural admission markers. The full successor workload will replace
 * these with the admitted storage trampoline. Protected transition code must
 * remain below 0x8000 and ordinary C cannot call the Attic copy path. */
.section .text.r0fs_protected,"ax",@progbits
.global r0fs_quiesce_marker
r0fs_quiesce_marker:
    sei
    rts

.global r0fs_context_restore_marker
r0fs_context_restore_marker:
    sei
    rts

.global r0fs_canonical_restore_marker
r0fs_canonical_restore_marker:
    jsr r0f_pf_enter
    rts

.global r0fs_resume_marker
r0fs_resume_marker:
    rts
