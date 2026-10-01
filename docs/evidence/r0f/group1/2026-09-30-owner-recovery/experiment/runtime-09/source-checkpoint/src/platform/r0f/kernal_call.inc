/* Shared admitted ROM-call mapping. Caller owns lifecycle and call allowlist. */
.set r0fsi_call_index, 0
.macro kernal address
    pha
    phx
    phy
    phz
    lda #0
    tab
    ldy #0
    ldx #$0f
    ldz #$0f
    map
    ldx #0
    ldz #$83
    map
    eom
    lda #$35
    sta $01
    lda #$47
    sta $d02f
    lda #$53
    sta $d02f
    lda $d030
    and #$46
    ora #$20
    sta $d030
    plz
    ply
    plx
    pla
    .set r0fsi_call_index, r0fsi_call_index+1
    pha
    lda #r0fsi_call_index
    sta $1f10
    pla
    jsr \address
    pha
    lda #r0fsi_call_index
    sta $1f11
    pla
.endm
