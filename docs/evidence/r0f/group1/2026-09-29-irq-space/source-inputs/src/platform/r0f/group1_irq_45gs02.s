/* Build-local instrumentation selection; the shared PF handler stays the
 * sole owner of acknowledgment, count/seqlock and register restoration. */
.set R0FG1_IRQ_TIMING, 1
.include "src/platform/r0f/qualification_45gs02.s"
.include "interfaces/generated/r0f_group1_trace.inc"

.section .text.r0fg1_irq,"ax",@progbits
/* Entry after A/X/Y/Z/B pushes; exit before their pops. No C, direct page,
 * MAP, DMA or CIA writes. Hardware-saved P restores interrupted D on RTI.
 * Only CIA read-pair interval is measured, not entry latency or whole ISR.
 * The ordinary IRQ count includes every serviced raster interrupt. These
 * private metrics include only declared acquisition cohorts. */
r0fg1_irq_begin:
    cld
    lda r0fg1_irq_epoch
    sta r0fg1_irq_entered
    beq .Lbegin_done
    jsr r0fg1_irq_read
    ldx #3
.Lsave_start:
    lda r0fg1_irq_now,x
    sta r0fg1_irq_start,x
    dex
    bpl .Lsave_start
.Lbegin_done:
    rts

r0fg1_irq_end:
    lda r0fg1_irq_entered
    beq .Lend_done
    jsr r0fg1_irq_read
    sec
    .irp byte,0,1,2,3
    lda r0fg1_irq_start+\byte
    sbc r0fg1_irq_now+\byte
    sta r0fg1_irq_now+\byte
    .endr
    /* Reject a duration that cannot be represented, never truncate it. */
    lda r0fg1_irq_now+2
    ora r0fg1_irq_now+3
    bne .Lirq_bad
    ldx #0
    lda r0fg1_irq_entered
    cmp #1
    beq .Lsummary
    ldx #R0FG1_IRQ_SUMMARY_BYTES
.Lsummary:
    inc r0fg1_irq_summary+R0FG1_I_COUNT,x
    bne .Ltotal
    inc r0fg1_irq_summary+R0FG1_I_COUNT+1,x
    beq .Lirq_bad
.Ltotal:
    clc
    .irp byte,0,1,2,3
    lda r0fg1_irq_summary+R0FG1_I_TOTAL+\byte,x
    adc r0fg1_irq_now+\byte
    sta r0fg1_irq_summary+R0FG1_I_TOTAL+\byte,x
    .endr
    bcs .Lirq_bad
    lda r0fg1_irq_now
    cmp r0fg1_irq_summary+R0FG1_I_MAX,x
    lda r0fg1_irq_now+1
    sbc r0fg1_irq_summary+R0FG1_I_MAX+1,x
    bcc .Lend_done
    lda r0fg1_irq_now
    sta r0fg1_irq_summary+R0FG1_I_MAX,x
    lda r0fg1_irq_now+1
    sta r0fg1_irq_summary+R0FG1_I_MAX+1,x
.Lend_done:
    rts
.Lirq_bad:
    lda #1
    sta r0fg1_irq_error
    rts

/* Same coherent chained-counter protocol as cfnow, with independent private
 * scratch so an IRQ never damages the foreground reader. Bounded 32 tries. */
r0fg1_irq_read:
    ldx #32
.Lread_retry:
    lda $dc07
    sta r0fg1_irq_now+3
    lda $dc06
    sta r0fg1_irq_now+2
    lda $dc07
    cmp r0fg1_irq_now+3
    bne .Lread_again
    lda $dc05
    sta r0fg1_irq_now+1
    lda $dc04
    sta r0fg1_irq_now
    lda $dc05
    cmp r0fg1_irq_now+1
    bne .Lread_again
    lda $dc06
    cmp r0fg1_irq_now+2
    bne .Lread_again
    lda $dc07
    cmp r0fg1_irq_now+3
    bne .Lread_again
    lda r0fg1_irq_now+1
    cmp #$ff
    bne .Lread_done
    lda r0fg1_irq_now
    cmp #$f0
    bcc .Lread_done
.Lread_again:
    dex
    bne .Lread_retry
    jmp .Lirq_bad
.Lread_done:
    rts
.global r0fg1_irq_timing_end
r0fg1_irq_timing_end:

.section .bss.r0fg1_irq,"aw",@nobits
.global r0fg1_irq_epoch, r0fg1_irq_error, r0fg1_irq_summary
r0fg1_irq_epoch: .space 1
r0fg1_irq_error: .space 1
r0fg1_irq_summary: .space R0FG1_EPOCHS * R0FG1_IRQ_SUMMARY_BYTES
r0fg1_irq_entered: .space 1
r0fg1_irq_start: .space 4
r0fg1_irq_now: .space 4
