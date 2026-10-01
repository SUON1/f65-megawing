/* Shared pre-C capture primitive. No stack, callback, MAP or DMA.
 * Each translation unit expands this once. Source shape/guard are T02-owned. */
.macro r0f_capture_opaque_context allocation, payload
    sei
    lda #R0FS_PRE_C_SCRATCH_BASE_PAGE
    tab
    lda #$00
    sta $22
    sta $23
    sta $24
    sta $25
    lda #<\allocation
    sta $26
    lda #>\allocation
    sta $27
    lda #((\allocation >> 16) & $ff)
    sta $28
    lda #((\allocation >> 24) & $ff)
    sta $29
    lda #R0FS_KERNAL_CONTEXT_GUARD
    ldz #$00
    .rept R0FS_KERNAL_CONTEXT_GUARD_BYTES
    sta [$26],z
    inz
    .endr
    lda #<\payload
    sta $26
    lda #>\payload
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
.endm
