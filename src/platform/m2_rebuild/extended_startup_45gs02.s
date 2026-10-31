/* Development-profile-only extension after canonical prefix and software SP.
 * No C call; A/X/Y/P clobbered, B=$02, Z unchanged, IRQ remains masked.
 * Disable external cartridge overlays before accessing extended resident data.
 * $D7FD POWEREN stays set; all other owner allocations remain untouched.
 * Clear actual linked compiler scratch in addition to the SDK's BSS clearing.
 * $0222-$0223 are Platform's existing private physical-copy pointer scratch.
 * An early fault enters the resident stack-free terminal sink, never C.
 */
.section .init.150,"ax",@progbits
.global m2re_startup, m2re_noinit_zero, m2re_noinit_done, m2re_startup_done
m2re_startup:
    lda $d7fb
    and #$fd
    sta $d7fb
    lda #$c1
    sta $d7fd
    lda $d7fb
    and #2
    bne .Linvalid
    lda $d7fd
    and #$c0
    cmp #$c0
    bne .Linvalid
    lda $d030
    and #$b9
    bne .Linvalid
    lda #0
    tab
    lda $00
    cmp #$2f
    bne .Linvalid
    lda $01
    cmp #$35
    bne .Linvalid
    lda #2
    tab
    lda #<__m2re_noinit_start
    sta $22
    lda #>__m2re_noinit_start
    sta $23
    ldy #0
m2re_noinit_zero:
.Lzero:
    lda $23
    cmp #>__m2re_noinit_end
    bne .Lstore
    lda $22
    cmp #<__m2re_noinit_end
    beq .Ldone
.Lstore:
    lda #0
    sta ($22),y
    inc $22
    bne .Lzero
    inc $23
    bra .Lzero
.Linvalid:
    jmp m2rb_early_stop
m2re_noinit_done:
m2re_startup_done:
.Ldone:
