.include "interfaces/generated/r0f_successor.inc"
.include "interfaces/generated/r0f_group1_export.inc"
.include "src/platform/r0f/opaque_context_capture.inc"

/* Second, explicitly admitted capsule. Original .init.005 capture touches
 * only scratch outside 0x0000-0x15ff, so the source is still the pre-C context.
 * This unit is linked only into the Group 1 variant. */
.section .init.006,"ax",@progbits
.global r0fg1_export_capture, r0fg1_export_capture_end
r0fg1_export_capture:
    r0f_capture_opaque_context R0FG1X_CAPSULE_START, R0FG1X_CAPSULE_PAYLOAD
r0fg1_export_capture_end:
