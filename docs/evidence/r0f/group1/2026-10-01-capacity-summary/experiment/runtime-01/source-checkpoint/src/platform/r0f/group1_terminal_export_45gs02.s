.include "interfaces/generated/r0f_successor.inc"
.include "interfaces/generated/r0f_group1_export.inc"
.include "src/platform/r0f/kernal_call.inc"

/* Irreversible terminal owner. Caller has frozen/verified trace and capsule,
 * restored ROM and DOS, stopped display/audio/IRQ/DMA, and rejected NMI.
 * All CPU registers/flags, page 1, page 2, 0x0000-0x15ff and ordinary resident
 * staging are clobbered. No C return, workload restart or application DMA.
 * Only this protected unit executes after staging overwrites application code.
 * Generated bounds and the linker require this unit/data entirely <0x4000. */
.section .text.r0fs_protected,"ax",@progbits
.global r0fg1_terminal_export, r0fg1_terminal_export_end
r0fg1_terminal_export:
    sei
    cld
    tba
    cmp #2
    beq .Lterminal_base_ok
    jmp .Lterminal_denied
.Lterminal_base_ok:
    lda r0fg1_export_permit
    cmp #$a5
    beq .Lterminal_permit_ok
    jmp .Lterminal_denied
.Lterminal_permit_ok:
    lda #0
    sta r0fg1_export_permit
    lda r0f_pf_nmi_seen
    beq .Lterminal_nmi_ok
    jmp .Lterminal_denied
.Lterminal_nmi_ok:
    lda r0fg1_export_bytes+3
    beq .Lterminal_size_high_ok
    jmp .Lterminal_denied
.Lterminal_size_high_ok:
    lda r0fg1_export_bytes+2
    cmp #((R0FG1X_TRACE_CAPACITY >> 16) & $ff)
    bcc .Lterminal_size_ok
    bne .Lterminal_bad_size
    lda r0fg1_export_bytes
    ora r0fg1_export_bytes+1
    beq .Lterminal_size_ok
.Lterminal_bad_size:
    jmp .Lterminal_denied
.Lterminal_size_ok:
    lda r0fg1_export_bytes
    ora r0fg1_export_bytes+1
    ora r0fg1_export_bytes+2
    bne .Lterminal_nonempty
    jmp .Lterminal_denied
.Lterminal_nonempty:
    lda #R0FG1X_S_EXPORTING
    sta r0fg1_export_status
    lda #R0FS_PRE_C_SCRATCH_BASE_PAGE
    tab
    lda #<R0FG1X_CAPSULE_PAYLOAD
    sta $22
    lda #>R0FG1X_CAPSULE_PAYLOAD
    sta $23
    lda #((R0FG1X_CAPSULE_PAYLOAD >> 16) & $ff)
    sta $24
    lda #((R0FG1X_CAPSULE_PAYLOAD >> 24) & $ff)
    sta $25
    lda #0
    sta $26
    sta $27
    sta $28
    sta $29
    lda #(R0FG1X_CONTEXT_BYTES / $100)
    sta $2a
    ldz #0
.Lterminal_restore:
    lda [$22],z
    sta [$26],z
    inz
    bne .Lterminal_restore
    inc $23
    inc $27
    dec $2a
    bne .Lterminal_restore
    // Consume capsule after copying, before any ROM call or file write.
    lda #<R0FG1X_CAPSULE_START
    sta $26
    lda #>R0FG1X_CAPSULE_START
    sta $27
    lda #((R0FG1X_CAPSULE_START >> 16) & $ff)
    sta $28
    lda #((R0FG1X_CAPSULE_START >> 24) & $ff)
    sta $29
    lda #(R0FG1X_CAPSULE_BYTES / $100)
    sta $2a
    lda #0
    ldz #0
.Lterminal_invalidate:
    sta [$26],z
    inz
    bne .Lterminal_invalidate
    inc $27
    dec $2a
    bne .Lterminal_invalidate
    ldx #(R0FG1X_CAPSULE_BYTES & $ff)
.Lterminal_invalidate_tail:
    sta [$26],z
    inz
    dex
    bne .Lterminal_invalidate_tail
    ldx #$ff
    txs
    lda #0
    tab
    kernal $ff87
    kernal $ff84
    kernal $ff8a
    kernal $ff81
    kernal $ffcc
    lda #0
    kernal $ff90
    // The restored entry-time DOS image can contain a valid but stale BAM:
    // returning storage has since allocated RSSTATE. Refresh through the
    // public command channel before any terminal SAVE, never patch DOS state.
    // OPEN 0,8,15,"I0"; special CLOSE preserves any other command-channel files.
    lda #2
    ldx #<r0fg1_export_initialize
    ldy #>r0fg1_export_initialize
    jsr r0fg1_terminal_file_setup
    kernal $ffc0
    bcc .Lterminal_initialized
    jmp .Lterminal_error
.Lterminal_initialized:
    lda #0
    sec
    kernal $ffc3
    bcc .Lterminal_command_closed
    jmp .Lterminal_error
.Lterminal_command_closed:
    lda #1
    sta r0fg1_export_secondary
    lda #<R0FG1X_TRACE_START
    sta r0fg1_export_source
    lda #>R0FG1X_TRACE_START
    sta r0fg1_export_source+1
    lda #((R0FG1X_TRACE_START >> 16) & $ff)
    sta r0fg1_export_source+2
    lda #((R0FG1X_TRACE_START >> 24) & $ff)
    sta r0fg1_export_source+3
    ldx #3
.Lterminal_remaining:
    lda r0fg1_export_bytes,x
    sta r0fg1_export_remaining,x
    dex
    bpl .Lterminal_remaining
.Lterminal_chunk:
    sei
    lda #<R0FG1X_STAGING_BYTES
    sta r0fg1_export_chunk
    lda #>R0FG1X_STAGING_BYTES
    sta r0fg1_export_chunk+1
    lda r0fg1_export_remaining+2
    bne .Lterminal_chunk_ready
    lda r0fg1_export_remaining+1
    cmp #>R0FG1X_STAGING_BYTES
    bcs .Lterminal_chunk_ready
    sta r0fg1_export_chunk+1
    lda r0fg1_export_remaining
    sta r0fg1_export_chunk
.Lterminal_chunk_ready:
    lda #R0FS_PRE_C_SCRATCH_BASE_PAGE
    tab
    ldx #3
.Lterminal_source:
    lda r0fg1_export_source,x
    sta $22,x
    dex
    bpl .Lterminal_source
    lda #<R0FG1X_STAGING_START
    sta $26
    lda #>R0FG1X_STAGING_START
    sta $27
    lda #0
    sta $28
    sta $29
    lda r0fg1_export_chunk
    sta r0fg1_export_copy_left
    lda r0fg1_export_chunk+1
    sta r0fg1_export_copy_left+1
    ldz #0
.Lterminal_stage_byte:
    lda [$22],z
    sta [$26],z
    inz
    bne .Lterminal_stage_count
    inc $23
    bne .Lterminal_stage_destination
    inc $24
.Lterminal_stage_destination:
    inc $27
.Lterminal_stage_count:
    lda r0fg1_export_copy_left
    bne .Lterminal_stage_low
    dec r0fg1_export_copy_left+1
.Lterminal_stage_low:
    dec r0fg1_export_copy_left
    lda r0fg1_export_copy_left
    ora r0fg1_export_copy_left+1
    bne .Lterminal_stage_byte
    // Source pointers are page-aligned except the final partial chunk.
    ldx #3
.Lterminal_source_update:
    lda $22,x
    sta r0fg1_export_source,x
    dex
    bpl .Lterminal_source_update
    lda #0
    tab
    lda #5
    ldx #<r0fg1_export_filename
    ldy #>r0fg1_export_filename
    jsr r0fg1_terminal_file_setup
    lda #0
    tab
    lda #<R0FG1X_STAGING_START
    sta $fe
    lda #>R0FG1X_STAGING_START
    sta $ff
    clc
    lda #<R0FG1X_STAGING_START
    adc r0fg1_export_chunk
    tax
    lda #>R0FG1X_STAGING_START
    adc r0fg1_export_chunk+1
    tay
    lda #$fe
    kernal $ffd8
    bcc .Lterminal_saved
    jmp .Lterminal_error
.Lterminal_saved:
    inc r0fg1_export_files
    sec
    lda r0fg1_export_remaining
    sbc r0fg1_export_chunk
    sta r0fg1_export_remaining
    lda r0fg1_export_remaining+1
    sbc r0fg1_export_chunk+1
    sta r0fg1_export_remaining+1
    lda r0fg1_export_remaining+2
    sbc #0
    sta r0fg1_export_remaining+2
    ora r0fg1_export_remaining
    ora r0fg1_export_remaining+1
    beq .Lterminal_done
    inc r0fg1_export_filename+4
    lda r0fg1_export_filename+4
    cmp #$3a
    bne .Lterminal_next
    lda #$30
    sta r0fg1_export_filename+4
    inc r0fg1_export_filename+3
.Lterminal_next:
    jmp .Lterminal_chunk
.Lterminal_done:
    kernal $ffcc
    lda #R0FG1X_S_EXPORTED
    sta r0fg1_export_status
    lda #5
    sta $d020
    jmp r0fg1_terminal_summary
.Lterminal_error:
    sta r0fg1_export_error
    kernal $ffcc
    lda #R0FG1X_S_FAILED
    sta r0fg1_export_status
    lda #2
    sta $d020
    jmp r0fg1_terminal_summary
.Lterminal_denied:
    lda #R0FG1X_S_FAILED
    sta r0fg1_export_status
    lda #2
    sta $d020
.Lterminal_halt:
    sei
    jmp .Lterminal_halt
r0fg1_terminal_export_end:

/* Protected shared file-parameter setup, not a return from terminal ownership.
 * Inputs A=length, X/Y=bank-0 command/filename; secondary is protected state.
 * KERNAL mapping/base-page/CPU clobbers remain the shared macro contract.
 * SETNAM may precede SETBNK/SETLFS, as in the public OPEN I0 example. */
.global r0fg1_terminal_file_setup, r0fg1_terminal_file_setup_end
r0fg1_terminal_file_setup:
    kernal $ffbd
    lda #0
    ldx #0
    kernal $ff6b
    lda #0
    ldx #8
    ldy r0fg1_export_secondary
    kernal $ffba
    rts
r0fg1_terminal_file_setup_end:

/* Terminal-only operator output after mapped KERNAL entry and final close.
 * Never reached by an early denied entry. All code/text/state stay protected.
 * CHROUT owns screen output; the macro re-establishes its mapping/base page.
 * Registers/flags and stack are terminal clobbers. X is saved per character.
 * S=4 is export completion, not timing acceptance; E and F are hexadecimal.
 * No C calls, storage retry or return to measured work. */
.global r0fg1_terminal_summary, r0fg1_terminal_summary_end
.global r0fg1_terminal_summary_hex, r0fg1_terminal_summary_hex_end
r0fg1_terminal_summary:
    lda r0fg1_export_status
    ora #$30
    sta r0fg1_operator_status
    lda r0fg1_export_error
    ldy #r0fg1_operator_error-r0fg1_operator_text
    jsr r0fg1_terminal_summary_hex
    lda r0fg1_export_files
    ldy #r0fg1_operator_files-r0fg1_operator_text
    jsr r0fg1_terminal_summary_hex
    ldx #0
.Lsummary_character:
    lda r0fg1_operator_text,x
    beq .Lsummary_halt
    phx
    kernal $ffd2
    plx
    inx
    bra .Lsummary_character
.Lsummary_halt:
    sei
    jmp .Lsummary_halt
r0fg1_terminal_summary_end:

/* A=byte, Y=protected text offset. Writes exactly two hex characters.
 * Clobbers A/X/Y/flags; bounded stack use, no mapped/application references. */
r0fg1_terminal_summary_hex:
    pha
    lsr
    lsr
    lsr
    lsr
    tax
    lda r0fg1_operator_hex,x
    sta r0fg1_operator_text,y
    iny
    pla
    and #$0f
    tax
    lda r0fg1_operator_hex,x
    sta r0fg1_operator_text,y
    rts
r0fg1_terminal_summary_hex_end:

.section .r0fs_protected_data,"aw",@progbits
.global r0fg1_export_permit, r0fg1_export_bytes, r0fg1_export_status
.global r0fg1_export_error, r0fg1_export_files
r0fg1_export_permit: .byte 0
r0fg1_export_status: .byte 0
r0fg1_export_error: .byte 0
r0fg1_export_files: .byte 0
r0fg1_export_bytes: .long 0
r0fg1_export_remaining: .long 0
r0fg1_export_source: .long 0
r0fg1_export_chunk: .word 0
r0fg1_export_copy_left: .word 0
r0fg1_export_filename: .ascii "G1T00"
r0fg1_export_initialize: .ascii "I0"
r0fg1_export_secondary: .byte 15
.global r0fg1_operator_text, r0fg1_operator_text_end
r0fg1_operator_hex: .ascii "0123456789ABCDEF"
r0fg1_operator_text:
    .byte $93
    .ascii "G1 EXPORT S:"
r0fg1_operator_status: .ascii "0"
    .ascii " E:"
r0fg1_operator_error: .ascii "00"
    .ascii " F:"
r0fg1_operator_files: .ascii "00"
    .byte 13
    .ascii "4=OK 5=FAIL / E,F HEX"
    .byte 13
    .ascii "REDUCE FOR TIMING"
    .byte 13
    .ascii "NOT ACCEPTANCE"
    .byte 13
    .ascii "RESET"
    .byte 13,0
r0fg1_operator_text_end:
