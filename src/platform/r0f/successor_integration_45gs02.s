.include "interfaces/generated/r0f_successor.inc"
.include "interfaces/generated/r0f_successor_integration.inc"

/* Fixed-range bridge for C-side CRC reduction. C supplies only a bounded
 * region/offset/length mailbox; the Attic address remains generated here. */
.section .text.r0fs_protected,"ax",@progbits
.global r0fs_context_read, r0fs_context_invalidate, r0fs_storage
r0fs_context_read:
    php
    sei
    phx
    phy
    phz
    tba
    pha
    lda #0
    sta r0fsi_context_copy_ok
    lda r0fsi_context_length
    beq .Lcontext_read_exit
    cmp #$ff
    beq .Lcontext_length_ok
    bcc .Lcontext_length_ok
    bra .Lcontext_read_exit
.Lcontext_length_ok:
    lda r0fsi_context_region
    cmp #3
    bcs .Lcontext_read_exit
    cmp #1
    beq .Lcontext_check_payload
    lda r0fsi_context_offset
    ora r0fsi_context_offset+1
    bne .Lcontext_read_exit
    lda r0fsi_context_length
    cmp #(R0FS_KERNAL_CONTEXT_GUARD_BYTES+1)
    bcs .Lcontext_read_exit
    bra .Lcontext_bounds_ok
.Lcontext_check_payload:
    clc
    lda r0fsi_context_offset
    adc r0fsi_context_length
    tax
    lda r0fsi_context_offset+1
    adc #0
    bcs .Lcontext_read_exit
    cmp #>(R0FS_KERNAL_CONTEXT_BYTES)
    bcc .Lcontext_bounds_ok
    bne .Lcontext_read_exit
    cpx #<(R0FS_KERNAL_CONTEXT_BYTES)
    bne .Lcontext_read_exit
.Lcontext_bounds_ok:
    lda #R0FS_PRE_C_SCRATCH_BASE_PAGE
    tab
    lda #<R0FS_KERNAL_CONTEXT_PAYLOAD
    sta $22
    lda #>R0FS_KERNAL_CONTEXT_PAYLOAD
    sta $23
    lda #((R0FS_KERNAL_CONTEXT_PAYLOAD >> 16) & $ff)
    sta $24
    lda #((R0FS_KERNAL_CONTEXT_PAYLOAD >> 24) & $ff)
    sta $25
    lda r0fsi_context_region
    cmp #1
    beq .Lcontext_payload
    cmp #2
    beq .Lcontext_trailing
    lda #<R0FS_KERNAL_CONTEXT_ALLOCATION
    sta $22
    lda #>R0FS_KERNAL_CONTEXT_ALLOCATION
    sta $23
    bra .Lcontext_source_ready
.Lcontext_trailing:
    lda #<(R0FS_KERNAL_CONTEXT_PAYLOAD + R0FS_KERNAL_CONTEXT_BYTES)
    sta $22
    lda #>(R0FS_KERNAL_CONTEXT_PAYLOAD + R0FS_KERNAL_CONTEXT_BYTES)
    sta $23
    bra .Lcontext_source_ready
.Lcontext_payload:
    clc
    lda $22
    adc r0fsi_context_offset
    sta $22
    lda $23
    adc r0fsi_context_offset+1
    sta $23
.Lcontext_source_ready:
    lda #<r0fsi_context_buffer
    sta $26
    lda #>r0fsi_context_buffer
    sta $27
    lda #0
    sta $28
    sta $29
    ldx r0fsi_context_length
    ldz #0
.Lcontext_read_loop:
    lda [$22],z
    sta [$26],z
    inz
    dex
    bne .Lcontext_read_loop
    lda #1
    sta r0fsi_context_copy_ok
.Lcontext_read_exit:
    pla
    tab
    plz
    ply
    plx
    lda r0fsi_context_copy_ok
    plp
    rts

/* Invalidation is a fixed zero fill of the entire admitted guarded range. */
r0fs_context_invalidate:
    php
    sei
    phx
    phz
    tba
    pha
    lda #R0FS_PRE_C_SCRATCH_BASE_PAGE
    tab
    lda #<R0FS_KERNAL_CONTEXT_ALLOCATION
    sta $26
    lda #>R0FS_KERNAL_CONTEXT_ALLOCATION
    sta $27
    lda #((R0FS_KERNAL_CONTEXT_ALLOCATION >> 16) & $ff)
    sta $28
    lda #((R0FS_KERNAL_CONTEXT_ALLOCATION >> 24) & $ff)
    sta $29
    lda #(R0FS_KERNAL_CONTEXT_ALLOCATION_BYTES / $100)
    sta $2a
    lda #0
    ldz #0
.Linvalidate_pages:
    sta [$26],z
    inz
    bne .Linvalidate_pages
    inc $27
    dec $2a
    bne .Linvalidate_pages
    ldx #(R0FS_KERNAL_CONTEXT_ALLOCATION_BYTES & $ff)
.Linvalidate_tail:
    sta [$26],z
    inz
    dex
    bne .Linvalidate_tail
    pla
    tab
    plz
    plx
    plp
    rts

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

/* Returning private storage boundary. The application has already saved
 * 0x0300-0x1fff and both DOS overlays. This wrapper owns page 1/page 2 while
 * KERNAL is active and restores them from the frozen physical backups before
 * returning to the same C call chain. */
r0fs_storage:
    php
    sei
    phx
    phy
    phz
    tba
    pha
    cmp #2
    beq .Lstorage_bp_ok
    jmp .Lstorage_denied
.Lstorage_bp_ok:
    lda r0fsi_permit
    cmp #$a5
    beq .Lstorage_permit_ok
    jmp .Lstorage_denied
.Lstorage_permit_ok:
    lda #0
    sta r0fsi_permit
    tsx
    stx r0fsi_app_sp

    /* Save page 1 to physical 0x051d00. */
    lda #R0FS_PRE_C_SCRATCH_BASE_PAGE
    tab
    lda #0
    sta $22
    lda #1
    sta $23
    lda #0
    sta $24
    sta $25
    lda #<R0FS_APPLICATION_STACK_BACKUP
    sta $26
    lda #>R0FS_APPLICATION_STACK_BACKUP
    sta $27
    lda #((R0FS_APPLICATION_STACK_BACKUP >> 16) & $ff)
    sta $28
    lda #((R0FS_APPLICATION_STACK_BACKUP >> 24) & $ff)
    sta $29
    ldz #0
.Lsave_stack:
    lda [$22],z
    sta [$26],z
    inz
    bne .Lsave_stack

    /* Save physical page 2 without using it as scratch. */
    lda #2
    sta $23
    lda #<R0FS_APPLICATION_BASE_PAGE_BACKUP
    sta $26
    lda #>R0FS_APPLICATION_BASE_PAGE_BACKUP
    sta $27
    lda #((R0FS_APPLICATION_BASE_PAGE_BACKUP >> 16) & $ff)
    sta $28
    ldz #0
.Lsave_base_page:
    lda [$22],z
    sta [$26],z
    inz
    bne .Lsave_base_page

    /* Restore the opaque pre-C KERNAL context from guarded Attic payload. */
    lda #<R0FS_KERNAL_CONTEXT_PAYLOAD
    sta $22
    lda #>R0FS_KERNAL_CONTEXT_PAYLOAD
    sta $23
    lda #((R0FS_KERNAL_CONTEXT_PAYLOAD >> 16) & $ff)
    sta $24
    lda #((R0FS_KERNAL_CONTEXT_PAYLOAD >> 24) & $ff)
    sta $25
    lda #0
    sta $26
    sta $27
    sta $28
    sta $29
    lda #(R0FS_KERNAL_CONTEXT_BYTES / $100)
    sta $2a
    ldz #0
.Lrestore_kernal_context:
    lda [$22],z
    sta [$26],z
    inz
    bne .Lrestore_kernal_context
    inc $23
    inc $27
    dec $2a
    bne .Lrestore_kernal_context

    ldx #$ff
    txs
    lda #$35
    sta $01
    lda $d030
    and #$46
    ora #$20
    sta $d030
    lda #1
    sta r0fsi_storage_phase
    kernal $ff87
    kernal $ff84
    kernal $ff8a
    kernal $ff81
    kernal $ffcc
    sei
    lda #0
    tab
    kernal $ff41
    stx r0fsi_input
    sty r0fsi_output
    lda #0
    kernal $ff90

    lda #2
    sta r0fsi_storage_phase
    lda #0
    ldx #0
    kernal $ff6b
    lda #0
    ldx #8
    ldy #0
    kernal $ffba
    lda #5
    ldx #<.Ltoken_name
    ldy #>.Ltoken_name
    kernal $ffbd
    lda #0
    ldx #<r0fsi_read
    ldy #>r0fsi_read
    kernal $ffd5
    bcc .Ltoken_loaded
    jmp .Lstorage_error
.Ltoken_loaded:
    stx r0fsi_end
    sty r0fsi_end+1
    ldx #(R0FSI_STORAGE_FILE_BYTES-1)
.Ltoken_copy:
    lda r0fsi_read,x
    sta r0fsi_token,x
    dex
    bpl .Ltoken_copy

    lda #3
    sta r0fsi_storage_phase
    lda #0
    ldx #0
    kernal $ff6b
    lda #0
    ldx #8
    ldy #1
    kernal $ffba
    lda #7
    ldx #<.Lstate_name
    ldy #>.Lstate_name
    kernal $ffbd
    lda #0
    tab
    lda #<r0fsi_payload
    sta $fe
    lda #>r0fsi_payload
    sta $ff
    lda #$fe
    ldx #<(r0fsi_payload+R0FSI_STORAGE_FILE_BYTES)
    ldy #>(r0fsi_payload+R0FSI_STORAGE_FILE_BYTES)
    kernal $ffd8
    bcc .Lstate_saved
    jmp .Lstorage_error
.Lstate_saved:
    lda #4
    sta r0fsi_storage_phase
    ldx #(R0FSI_STORAGE_FILE_BYTES-1)
    lda #$cc
.Lclear_read:
    sta r0fsi_read,x
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
    ldx #<.Lstate_name
    ldy #>.Lstate_name
    kernal $ffbd
    lda #0
    ldx #<r0fsi_read
    ldy #>r0fsi_read
    kernal $ffd5
    bcc .Lstate_reloaded
    jmp .Lstorage_error
.Lstate_reloaded:
    stx r0fsi_end+2
    sty r0fsi_end+3
    kernal $ffcc
    kernal $ff41
    stx r0fsi_input_end
    sty r0fsi_output_end
    lda #5
    sta r0fsi_storage_phase
    lda #0
    sta r0fsi_storage_error
    bra .Lstorage_canonical
.Lstorage_error:
    sta r0fsi_storage_error
.Lstorage_canonical:
    jsr r0f_pf_enter

    /* Restore application page 1 and base page from fixed physical backups. */
    lda #R0FS_PRE_C_SCRATCH_BASE_PAGE
    tab
    lda #<R0FS_APPLICATION_STACK_BACKUP
    sta $22
    lda #>R0FS_APPLICATION_STACK_BACKUP
    sta $23
    lda #((R0FS_APPLICATION_STACK_BACKUP >> 16) & $ff)
    sta $24
    lda #0
    sta $25
    sta $26
    lda #1
    sta $27
    lda #0
    sta $28
    sta $29
    ldz #0
.Lrestore_stack:
    lda [$22],z
    sta [$26],z
    inz
    bne .Lrestore_stack
    lda #<R0FS_APPLICATION_BASE_PAGE_BACKUP
    sta $22
    lda #>R0FS_APPLICATION_BASE_PAGE_BACKUP
    sta $23
    lda #((R0FS_APPLICATION_BASE_PAGE_BACKUP >> 16) & $ff)
    sta $24
    lda #2
    sta $27
    ldz #0
.Lrestore_base_page:
    lda [$22],z
    sta [$26],z
    inz
    bne .Lrestore_base_page
    lda #2
    tab
    ldx r0fsi_app_sp
    txs
    lda #1
    sta r0fsi_storage_returned
    bra .Lstorage_exit
.Lstorage_denied:
    inc r0fsi_storage_denied
.Lstorage_exit:
    pla
    tab
    plz
    ply
    plx
    lda r0fsi_storage_returned
    plp
    rts
.global r0fs_storage_end
r0fs_storage_end:
.Ltoken_name: .ascii "TOKEN"
.Lstate_name: .ascii "RSSTATE"
