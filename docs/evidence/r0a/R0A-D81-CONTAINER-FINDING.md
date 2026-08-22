# R0-A D81 Container Finding

**Status:** Host, Xemu, and physical-MEGA65 proof passing

VICE 3.10 `c1541` is pinned in the local toolchain lock. `make r0a-build` tokenizes `src/r0a/autoboot.bas` as BASIC 65, formats an 80-track D81, writes `autoboot.c65` and `f65-r0a-proof`, reopens the image, and validates its listing and exact 819200-byte size. Lower-byte PETSCII names are required for the owner ROM's exact BASIC-65 filename lookup; the BASIC launcher uses the same byte form.

MEGA65 documentation defines a disk containing `AUTOBOOT.C65` as bootable; when mounted on unit 0, the system loads and runs it. The R0-A program is loaded by the BASIC-65 launcher and then executes the B-register sentinel/nested-C proof.

Xemu runtime execution is verified with the owner-supplied ROM and initialized local SD image. On 2026-08-20, the owner mounted the corrected D81 on physical MEGA65 hardware and captured `R0-A TEST RUN COMPLETE`, `R0A-BP-001 PASS`, and `R0A-PTR-001 PASS`. The program's `HARDWARE PROBES NOT RUN` line refers to additional probes outside this focused base-page test; it is expected output, not a failure. This is the physical R0-A PASS.
