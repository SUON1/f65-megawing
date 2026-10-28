/* One-way reset entry. No resident data, direct-page access, push or call
 * precedes canonicalization. Clobbers A/X/Y/Z/B/P/SP; no ABI caller returns.
 * MAP/megabyte selectors become zero; B=$02; hardware stack page 1.
 * IRQ stays masked. Early NMI/IRQ terminate without C, stack or BSS access.
 * PF001 installs its sticky resident handlers only after C initialization.
 */
.section .init.008,"ax",@progbits
.global m2rb_startup, m2rb_normalized
m2rb_startup:
    sei
    cld
    lda #0
    tab
    ldy #0
    ldx #$0f
    ldz #$0f
    map
    lda #0
    tax
    tay
    taz
    map
    eom
    see
    ldy #1
    tys
    ldx #$ff
    txs
    lda #$2f
    sta $00
    lda #$35
    sta $01
    lda #$47
    sta $d02f
    lda #$53
    sta $d02f
    lda #$44
    sta $d030
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
    lda #<m2rb_early_stop
    sta $fffa
    sta $fffe
    lda #>m2rb_early_stop
    sta $fffb
    sta $ffff
    lda #2
    tab
    ldz #0
m2rb_normalized:

.section .text.m2rb_early_stop,"ax",@progbits
.global m2rb_early_stop
m2rb_early_stop:
    sei
    jmp m2rb_early_stop
