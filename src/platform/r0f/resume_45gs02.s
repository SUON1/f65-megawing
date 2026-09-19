.section .init.005,"ax",@progbits
/* Opaque KERNAL context, captured before the C base page is relocated or
 * the proof seeds unused hardware-stack bytes. Never interpret fields. */
.global r0fr_kernel, r0fr_kernel_snapshot
r0fr_kernel_snapshot:
    sei
    lda #0
    tab
    ldx #0
.Lkernel_snapshot:
    .set page,0
    .rept 22
    lda page*$100,x
    sta r0fr_kernel+page*$100,x
    .set page,page+1
    .endr
    inx
    beq .Lsnapshot_done
    jmp .Lkernel_snapshot
.Lsnapshot_done:
.section .text.r0fr,"ax",@progbits
.global r0fr_storage, r0fr_bp
.set r0fr_call_index, 0
.macro kernal address
    pha
    phx
    phy
    phz
    /* IOINIT changes port/banking. Re-establish documented prerequisites
     * at EACH call, never assume one initialization preserves the next. */
    lda #0
    tab
    ldy #0
    ldx #$0f
    ldz #$0f
    map
    ldx #0
    /* E000-FFFF -> physical 03E000-03FFFF. IOINIT changes D030
     * while executing, so D030's ROME overlay alone is insufficient. */
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
    ora #$20                /* Native KERNAL interface ROM at 2.C000. */
    sta $d030
    plz
    ply
    plx
    pla
    .set r0fr_call_index, r0fr_call_index+1
    pha
    lda #r0fr_call_index
    sta $1f10
    pla
    jsr \address
    pha
    lda #r0fr_call_index
    sta $1f11
    pla
.endm
/* Private zero-argument mailbox boundary. Caller has quiesced hardware,
 * backed up 0300-1fff and verified ROM restoration/protection. No C in scope. */
r0fr_storage:
    php
    sei
    phx
    phy
    phz
    tba
    pha
    cmp #2
    beq .Lbp_ok
    jmp .Ldenied
.Lbp_ok:
    lda r0fr_permit
    cmp #$a5
    beq .Lpermit_ok
    jmp .Ldenied
.Lpermit_ok:
    lda #0
    sta r0fr_permit
    ldx #0
.Lsavebp:
    lda $0200,x
    sta r0fr_bp,x
    inx
    bne .Lsavebp
    tsx
    stx r0fr_app_sp
    ldx #0
.Lsave_stack:
    lda $0100,x
    sta r0fr_app_stack,x
    inx
    bne .Lsave_stack
    lda #0
    tab
    ldx #2
.Lrestore_kernel_zp:
    lda r0fr_kernel,x
    sta $00,x
    inx
    bne .Lrestore_kernel_zp
    ldx #0
.Lrestore_kernel:
    .set page,1
    .rept 21
    lda r0fr_kernel+page*$100,x
    sta page*$100,x
    .set page,page+1
    .endr
    inx
    beq .Lkernel_ready
    jmp .Lrestore_kernel
.Lkernel_ready:
    ldx #$ff
    txs                     /* KERNAL calls use a separate stack context. */
    lda #$35
    sta $01
    lda $d030
    and #$46
    ora #$20
    sta $d030
    lda #1
    sta r0fr_phase
    kernal $ff87              /* RAMTAS; no return to previous BASIC. */
    kernal $ff84              /* IOINIT including DOS */
    kernal $ff8a              /* RESTOR, public vector installation */
    kernal $ff81              /* CINT */
    kernal $ffcc              /* CLRCH: establish default I/O channels */
    sei
    lda #0
    tab
    kernal $ff41              /* GETIO: observe, don't poke internal vars */
    stx r0fr_input
    sty r0fr_output
    lda #0
    kernal $ff90              /* SETMSG: suppress file messages */
    lda #2
    sta r0fr_phase
    lda #0
    ldx #0
    kernal $ff6b
    lda #0
    ldx #8
    ldy #0
    kernal $ffba
    lda #5
    ldx #<.Ltoken
    ldy #>.Ltoken
    kernal $ffbd
    lda #0
    ldx #<r0fr_read
    ldy #>r0fr_read
    kernal $ffd5
    bcc .Linput_loaded
    jmp .Lio_error
.Linput_loaded:
    stx r0fr_end
    sty r0fr_end+1
    ldx #31
.Ltoken_copy:
    lda r0fr_read,x
    sta r0fr_token,x
    dex
    bpl .Ltoken_copy
    lda #3
    sta r0fr_phase
    lda #0
    ldx #0
    kernal $ff6b
    lda #0
    ldx #8
    ldy #1
    kernal $ffba
    lda #7
    ldx #<.Lsaved
    ldy #>.Lsaved
    kernal $ffbd
    lda #0
    tab
    lda #<r0fr_payload
    sta $fe
    lda #>r0fr_payload
    sta $ff
    lda #$fe
    ldx #<(r0fr_payload+32)
    ldy #>(r0fr_payload+32)
    kernal $ffd8
    bcc .Lsaved_ok
    jmp .Lio_error
.Lsaved_ok:
    lda #4
    sta r0fr_phase
    ldx #31
    lda #$cc
.Lclear_read:
    sta r0fr_read,x
    dex
    bpl .Lclear_read
    lda #0
    ldx #0
    kernal $ff6b
    lda #0
    ldx #8
    ldy #0
    kernal $ffba
    lda #7
    ldx #<.Lsaved
    ldy #>.Lsaved
    kernal $ffbd
    lda #0
    ldx #<r0fr_read
    ldy #>r0fr_read
    kernal $ffd5
    bcc .Lreadback_ok
    jmp .Lio_error
.Lreadback_ok:
    stx r0fr_end+2
    sty r0fr_end+3
    kernal $ffcc
    kernal $ff41
    stx r0fr_input_end
    sty r0fr_output_end
    lda #5
    sta r0fr_phase
    lda #0
    sta r0fr_error
    bra .Lcanonical
.Lio_error:
    sta r0fr_error
.Lcanonical:
    /* Canonical setup is resident assembly, not C. B temporarily unknown
     * is handled inside it; no compiler scratch can be used until restored. */
    jsr r0f_pf_enter
    ldx #0
.Lrestorebp:
    lda r0fr_bp,x
    sta $0200,x
    inx
    bne .Lrestorebp
    ldx #0
.Lrestore_stack:
    lda r0fr_app_stack,x
    sta $0100,x
    inx
    bne .Lrestore_stack
    ldx r0fr_app_sp
    txs
    lda #1
    sta r0fr_returned
    bra .Lexit
.Ldenied:
    inc r0fr_denied
.Lexit:
    pla
    tab
    plz
    ply
    plx
    lda r0fr_returned
    plp
    rts
.global r0fr_storage_end
r0fr_storage_end:
.Ltoken: .ascii "TOKEN"
.Lsaved: .ascii "RHSTATE"
.section .bss.r0fr_bp,"aw",@nobits
r0fr_bp: .space 256
r0fr_app_stack: .space 256
r0fr_app_sp: .space 1
.section .noinit.r0fr_kernel,"aw",@nobits
r0fr_kernel: .space $1600
