.section .text.r0fs_loader,"ax",@progbits
.global _start

/* T04 carrier-only bootstrap. BASIC 65 V920413 LOADs this below $2000,
 * where it remains executable while MAP is normalized. The KERNAL LOAD
 * then places the exact reviewed successor PRG in physical bank 0. */
_start:
    jsr map_kernal
    lda #0
    ldx #0
    jsr $ff6b

    jsr map_kernal
    lda #8
    ldx #8
    ldy #1
    jsr $ffba

    jsr map_kernal
    lda #7
    ldx #<filename
    ldy #>filename
    jsr $ffbd

    jsr map_kernal
    lda #0
    ldx #0
    ldy #0
    jsr $ffd5
    bcs load_failed

    lda #0
    tax
    tay
    taz
    map
    eom
    jmp $2b07

load_failed:
    sta $0ff0
    stx $0ff1
    sty $0ff2
    php
    pla
    sta $0ff3
    lda #2
    sta $d020
    bra load_failed

map_kernal:
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
    rts

filename:
    .ascii "R0FSUCC"
