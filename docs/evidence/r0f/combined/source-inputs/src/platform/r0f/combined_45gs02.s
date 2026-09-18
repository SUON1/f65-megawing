.section .text.r0fc_platform,"ax",@progbits
.global r0fc_rom_toggle, r0fc_stack_seed, r0fc_stack_measure
/* CF001 private zero-argument trap boundary. No guessed C argument ABI. */
r0fc_rom_toggle:
    php
    sei
    phx
    phy
    phz
    tba
    pha
    lda #$70
    sta $d640
    nop
    sta r0fc_features
    php
    pla
    sta r0fc_trap_flags
    tba
    sta r0fc_trap_base
    pla
    tab
    plz
    ply
    plx
    lda r0fc_features
    plp
    rts

/* Stack canaries are seeded below live frames, never over return addresses.
 * C software SP is rc0/1, whose pinned definition is checked by the builder. */
r0fc_stack_seed:
    php
    sei
    phx
    phy
    tsx
    stx r0fc_hardware_seed
    ldy #0
    lda #$a5
.Lhwseed:
    cpy r0fc_hardware_seed
    beq .Lswseedstart
    sta $0100,y
    iny
    bra .Lhwseed
.Lswseedstart:
    lda $02
    sta r0fc_software_seed
    lda $03
    sta r0fc_software_seed+1
    lda #0
    sta $22
    lda #$c0
    sta $23
    ldy #0
.Lswseed:
    lda $23
    cmp $03
    bne .Lswstore
    lda $22
    cmp $02
    beq .Lseedend
.Lswstore:
    lda #$a5
    sta ($22),y
    inc $22
    bne .Lswseed
    inc $23
    bra .Lswseed
.Lseedend:
    ply
    plx
    plp
    rts

r0fc_stack_measure:
    php
    sei
    phx
    phy
    ldy #0
.Lhwscan:
    lda $0100,y
    cmp #$a5
    bne .Lhwfound
    iny
    cpy r0fc_hardware_seed
    bne .Lhwscan
.Lhwfound:
    sty r0fc_hardware_low
    lda #0
    sta $22
    lda #$c0
    sta $23
    ldy #0
.Lswscan:
    lda $23
    cmp r0fc_software_seed+1
    bne .Lswread
    lda $22
    cmp r0fc_software_seed
    beq .Lswfound
.Lswread:
    lda ($22),y
    cmp #$a5
    bne .Lswfound
    inc $22
    bne .Lswscan
    inc $23
    bra .Lswscan
.Lswfound:
    lda $22
    sta r0fc_software_low
    lda $23
    sta r0fc_software_low+1
    ply
    plx
    plp
    rts
