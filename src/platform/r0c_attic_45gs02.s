; R0-C proof-only Attic staging backend.
;
; The C facade validates the request and owns the request block.  These
; private zero-argument helpers are the only C/assembly boundary.  They use
; 45GS02 flat physical addressing and never alter MAP, IRQ, $01, or ROM.
; Q is untouched (LLVM-MOS has no PHQ/PLQ instruction); A is the result.

        .text

        .globl r0c_attic_fixture_seed_private
r0c_attic_fixture_seed_private:
        php
        phx
        phy
        phz
        tba
        pha
        cmp #$02
        bne r0c_attic_seed_fail
        lda r0c_attic_request+4
        sta $22
        lda r0c_attic_request+5
        sta $23
        lda r0c_attic_request+6
        sta $24
        lda r0c_attic_request+7
        sta $25
        ldz #$00
        lda #$52
        sta [$22],z
        inz
        lda #$30
        sta [$22],z
        inz
        lda #$43
        sta [$22],z
        inz
        lda #$50
        sta [$22],z
        inz
        lda #$01
        sta [$22],z
        inz
        lda #$03
        sta [$22],z
        lda #$01
        bra r0c_attic_seed_done
r0c_attic_seed_fail:
        lda #$00
r0c_attic_seed_done:
        sta r0c_attic_request+18
        sta r0c_attic_request+19
        pla
        tab
        plz
        ply
        plx
        plp
        lda r0c_attic_request+18
        rts

        .globl r0c_attic_stage_cpu_copy_private
r0c_attic_stage_cpu_copy_private:
        php
        phx
        phy
        phz
        tba
        pha
        cmp #$02
        bne r0c_attic_copy_fail
        lda r0c_attic_request+4
        sta $22
        lda r0c_attic_request+5
        sta $23
        lda r0c_attic_request+6
        sta $24
        lda r0c_attic_request+7
        sta $25
        lda r0c_attic_request+8
        sta $26
        lda r0c_attic_request+9
        sta $27
        lda r0c_attic_request+10
        sta $28
        lda r0c_attic_request+11
        sta $29
        ldx r0c_attic_request+12
        ldz #$00
        lda #$00
        sta r0c_attic_request+16
        sta r0c_attic_request+17
r0c_attic_copy_loop:
        cpx #$00
        beq r0c_attic_copy_ok
        lda [$22],z
        sta [$26],z
        clc
        adc r0c_attic_request+16
        sta r0c_attic_request+16
        lda r0c_attic_request+17
        adc #$00
        sta r0c_attic_request+17
        inz
        dex
        bra r0c_attic_copy_loop
r0c_attic_copy_ok:
        lda #$01
        bra r0c_attic_copy_done
r0c_attic_copy_fail:
        lda #$00
r0c_attic_copy_done:
        sta r0c_attic_request+18
        sta r0c_attic_request+19
        pla
        tab
        plz
        ply
        plx
        plp
        lda r0c_attic_request+18
        rts
