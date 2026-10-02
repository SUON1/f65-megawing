.include "interfaces/generated/r0f_successor.inc"
.include "src/platform/r0f/opaque_context_capture.inc"

/* This is a proof-only pre-C capture skeleton. B=0x16 selects scratch at
 * 0x1622-0x162a, outside the opaque 0x0000-0x15ff source. No stack access,
 * callback, MAP change or DMA occurs before every source byte is captured. */
.section .init.005,"ax",@progbits
.global r0fs_pre_c_capture, r0fs_pre_c_capture_end
r0fs_pre_c_capture:
    r0f_capture_opaque_context R0FS_KERNAL_CONTEXT_ALLOCATION, R0FS_KERNAL_CONTEXT_PAYLOAD
r0fs_pre_c_capture_end:

/* Structural admission markers. The full successor workload will replace
 * these with the admitted storage trampoline. Protected transition code must
 * remain below 0x8000 and ordinary C cannot call the Attic copy path. */
.section .text.r0fs_protected,"ax",@progbits
.global r0fs_quiesce_marker
r0fs_quiesce_marker:
    sei
    rts

.global r0fs_context_restore_marker
r0fs_context_restore_marker:
    sei
    rts

.global r0fs_canonical_restore_marker
r0fs_canonical_restore_marker:
    jsr r0f_pf_enter
    rts

.global r0fs_resume_marker
r0fs_resume_marker:
    rts
