# R0-A D81 Container Finding

**Status:** Container proof passing; Xemu boot and hardware execution pending

VICE 3.10 `c1541` is pinned in the local toolchain lock. `make r0a-build` tokenizes `src/r0a/autoboot.bas` as BASIC 65, formats an 80-track D81, writes `AUTOBOOT.C65` and `F65-R0A-PROOF`, reopens the image, and validates its listing and exact 819200-byte size.

MEGA65 documentation defines a disk containing `AUTOBOOT.C65` as bootable; when mounted on unit 0, the system loads and runs it. The R0-A program is loaded by the BASIC-65 launcher and then executes the B-register sentinel/nested-C proof.

The only unproven portion is runtime execution: a candidate `xmega65` binary is version-pinned, but the protected owner-provided ROM, system-file configuration, headless invocation, result capture, and runtime behavior are not validated. This evidence must not be interpreted as an Xemu or hardware PASS.
