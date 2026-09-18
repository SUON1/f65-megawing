        .section .init.011,"ax",@progbits
        .globl f65_basepage_enter
f65_basepage_enter:
        lda #$02
        tab

        .section .fini.989,"ax",@progbits
        .globl f65_basepage_leave
f65_basepage_leave:
        lda #$00
        tab

        .text
        .globl r0a_abi_echo_u8
r0a_abi_echo_u8:
        rts

        .globl r0a_basepage_read
r0a_basepage_read:
        tba
        rts

        .globl r0a_basepage_sentinel_seed
r0a_basepage_sentinel_seed:
        tya
        pha
        ldy #$00
.seed:
        tya
        eor #$a5
        sta mos16($0002),y
        iny
        cpy #$20
        bne .seed
        pla
        tay
        rts

        .globl r0a_basepage_sentinel_unchanged
r0a_basepage_sentinel_unchanged:
        tya
        pha
        ldy #$00
.check:
        tya
        eor #$a5
        cmp mos16($0002),y
        bne .changed
        iny
        cpy #$20
        bne .check
        pla
        tay
        lda #$01
        rts
.changed:
        pla
        tay
        lda #$00
        rts
