.section .text.r0f_pf,"ax",@progbits
.global r0f_pf_enter, r0f_pf_start_irq, r0f_pf_stop_irq
.global r0f_pf_flat_copy, r0f_pf_register_probe

/* PF-001: one-way reset-only takeover. No ROM or hypervisor call. */
r0f_pf_enter:
    sei
    cld
    lda #0
    tax
    tay
    taz
    map
    /* LLVM-MOS linker relaxes even mos16($0001) to direct page. Clear the
     * inherited MAP first, then select B=0 so this reaches the CPU port. */
    lda #0
    tab
    lda #$35
    sta $01
    lda $01
    sta r0f_pf_cpu_port
    lda #$47
    sta $d02f
    lda #$53
    sta $d02f
    lda $d030
    and #$46
    sta $d030
    eom
    lda #2
    tab
    lda #$7f
    sta $dc0d
    sta $dd0d
    lda $dc0d
    lda $dd0d
    lda #0
    sta $d01a
    sta $d713
    lda #15
    sta $d019
    lda #<r0f_pf_irq
    sta $fffe
    lda #>r0f_pf_irq
    sta $ffff
    lda #<r0f_pf_nmi
    sta $fffa
    lda #>r0f_pf_nmi
    sta $fffb
    tsy
    tya
    sta r0f_pf_stack_high
    tba
    rts

r0f_pf_start_irq:
    lda $d011
    and #$7f
    sta $d011
    lda #0
    sta $d012
    lda #1
    sta $d019
    sta $d01a
    cli
    rts

r0f_pf_stop_irq:
    sei
    lda #0
    sta $d01a
    lda #15
    sta $d019
    rts

/* No C calls, direct-page accesses, MAP, DMA or audio in either handler. */
r0f_pf_irq:
    pha
    phx
    phy
    phz
    tba
    pha
    lda $d019
    and #1
    beq .Lirq_done
    inc r0f_pf_irq_seq
    inc r0f_pf_irq_count
    bne .Lirq_nocarry
    inc r0f_pf_irq_count+1
.Lirq_nocarry:
    lda #$80
    sta r0f_pf_irq_seen
    lda #1
    sta $d019
    inc r0f_pf_irq_seq
.Lirq_done:
    pla
    tab
    plz
    ply
    plx
    pla
    rti

r0f_pf_nmi:
    pha
    lda #1
    sta r0f_pf_nmi_seen
    pla
    rti

/* Request: LE32 source, LE32 destination, length. Both ranges prevalidated. */
r0f_pf_flat_copy:
    php
    phx
    phy
    phz
    tba
    pha
    cmp #2
    bne .Lcopy_bad
    ldx #0
.Lcopy_ptr:
    lda r0f_pf_copy_request,x
    sta $22,x
    inx
    cpx #8
    bne .Lcopy_ptr
    ldx r0f_pf_copy_request+8
    beq .Lcopy_bad
    ldz #0
.Lcopy_loop:
    lda [$22],z
    sta [$26],z
    inz
    dex
    bne .Lcopy_loop
    lda #1
    sta r0f_pf_copy_ok
    bra .Lcopy_exit
.Lcopy_bad:
    lda #0
    sta r0f_pf_copy_ok
.Lcopy_exit:
    pla
    tab
    plz
    ply
    plx
    lda r0f_pf_copy_ok
    plp
    rts

/* Bounded register canary while genuine raster IRQs run. BIT changes NZV
 * only. Carry/decimal remain canaries. Loop timeout uses a private word. */
r0f_pf_register_probe:
    php
    pha
    phx
    phy
    phz
    sei
    lda #0
    sta r0f_pf_irq_seen
    sta r0f_pf_probe_timeout
    sta r0f_pf_probe_timeout+1
    cld
    clc
    lda #$a5
    ldx #$5a
    ldy #$c3
    ldz #$3c
    cli
.Lprobe_wait:
    bit r0f_pf_irq_seen
    bmi .Lprobe_done
    inc r0f_pf_probe_timeout
    bne .Lprobe_wait
    inc r0f_pf_probe_timeout+1
    bne .Lprobe_wait
.Lprobe_done:
    sta r0f_pf_probe_regs
    stx r0f_pf_probe_regs+1
    sty r0f_pf_probe_regs+2
    stz r0f_pf_probe_regs+3
    php
    pla
    sta r0f_pf_probe_regs+5
    tba
    sta r0f_pf_probe_regs+4
    lda r0f_pf_irq_seen
    sta r0f_pf_probe_regs+6
    plz
    ply
    plx
    pla
    plp
    rts
