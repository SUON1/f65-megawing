#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
java_home="$root/toolchain/runtime/jdk-full/jdk-21.0.12+8/Contents/Home"
java="$java_home/bin/java"
javac="$java_home/bin/javac"
cc="$root/toolchain/runtime/llvm-mos/bin/mos-mega65-clang"
objdump="$root/toolchain/runtime/llvm-mos/bin/llvm-objdump"
nm="$root/toolchain/runtime/llvm-mos/bin/llvm-nm"
vice="$root/toolchain/vice/VICE.app/Contents/Resources/bin"
c1541="$vice/c1541"
petcat="$vice/petcat"
xemu="$root/toolchain/xemu/xmega65"
out="$root/build/r0b"
classes="$out/host-classes"
need_tools() { test -x "$java" && test -x "$javac" && test -x "$cc" && test -x "$objdump" && test -x "$nm" && test -x "$c1541" && test -x "$petcat"; }
compile_host() { mkdir -p "$classes"; "$javac" -d "$classes" "$root/tools/generators/src/main/java/f65/tools/R0BHostTools.java"; }
generate() { need_tools; compile_host; "$java" -cp "$classes" f65.tools.R0BHostTools generate "$root"; }
host_test() { generate; "$java" -cp "$classes" f65.tools.R0BHostTools host-test "$root"; python3 "$root/tools/diagnostics/r0b_validate.py" "$root"; }
build() {
  host_test
  mkdir -p "$out/reports" "$out/artifacts" "$out/evidence"
  "$cc" -mcpu=mos45gs02 -mlto-zp=0 -Os -Wall -Wextra -Wconversion -Werror -I"$root/interfaces/generated" "$root/src/r0b/main.c" "$root/src/diagnostics/r0b/proof_stage2.c" "$root/src/platform/r0b/vic4_probe.c" "$root/src/platform/r0b/timing.c" "$root/src/input/r0b/input_fixture.c" "$root/src/audio/r0b/audio_fixture.c" "$root/src/platform/r0a_platform_45gs02.s" -Wl,-Map,"$out/reports/F65-R0B-PROOF.map" -o "$out/artifacts/F65-R0B-PROOF.prg"
  "$nm" "$out/artifacts/F65-R0B-PROOF.prg.elf" > "$out/reports/F65-R0B-PROOF.symbols"
  "$objdump" -d --print-imm-hex "$out/artifacts/F65-R0B-PROOF.prg.elf" > "$out/reports/F65-R0B-PROOF.disassembly"
  python3 "$root/tools/diagnostics/r0b_validate_target.py" "$root"
  "$petcat" -w65 -o "$out/artifacts/AUTOBOOT.C65" -- "$root/src/r0b/autoboot.bas"
  "$petcat" -65 "$out/artifacts/AUTOBOOT.C65" > "$out/reports/AUTOBOOT.C65.listing"
  "$c1541" -format 'F65 R0-B,65' d81 "$out/artifacts/F65-R0B-PROOF.d81" -write "$out/artifacts/AUTOBOOT.C65" autoboot.c65 -write "$out/artifacts/F65-R0B-PROOF.prg" f65-r0b-proof -list > "$out/reports/F65-R0B-PROOF.d81-create.txt" 2>&1
  "$c1541" "$out/artifacts/F65-R0B-PROOF.d81" -list > "$out/reports/F65-R0B-PROOF.d81-list.txt" 2>&1
  python3 "$root/tools/diagnostics/r0b_validate_package.py" "$root"
  shasum -a 256 "$out/artifacts/F65-R0B-PROOF.prg" > "$out/artifacts/F65-R0B-PROOF.prg.sha256"
  shasum -a 256 "$out/artifacts/F65-R0B-PROOF.d81" > "$out/artifacts/F65-R0B-PROOF.d81.sha256"
}
build_fcm_safe() {
  host_test
  mkdir -p "$out/reports" "$out/artifacts" "$out/evidence"
  "$cc" -mcpu=mos45gs02 -mlto-zp=0 -Os -Wall -Wextra -Wconversion -Werror -I"$root/interfaces/generated" "$root/src/r0b/fcm_safe_main.c" "$root/src/diagnostics/r0b/fcm_safe.c" "$root/src/platform/r0b/fcm_restore_45gs02.s" "$root/src/platform/r0a_platform_45gs02.s" -Wl,-Map,"$out/reports/F65-R0B-FCM-SAFE.map" -o "$out/artifacts/F65-R0B-FCM-SAFE.prg"
  "$nm" "$out/artifacts/F65-R0B-FCM-SAFE.prg.elf" > "$out/reports/F65-R0B-FCM-SAFE.symbols"
  "$objdump" -d --print-imm-hex "$out/artifacts/F65-R0B-FCM-SAFE.prg.elf" > "$out/reports/F65-R0B-FCM-SAFE.disassembly"
  python3 "$root/tools/diagnostics/r0b_validate_fcm_safe_target.py" "$root"
  "$petcat" -w65 -o "$out/artifacts/AUTOBOOT-FCM.C65" -- "$root/src/r0b/autoboot_fcm_safe.bas"
  "$petcat" -65 "$out/artifacts/AUTOBOOT-FCM.C65" > "$out/reports/AUTOBOOT-FCM.C65.listing"
  "$c1541" -format 'F65 R0-B FCM,65' d81 "$out/artifacts/F65-R0B-FCM-SAFE.d81" -write "$out/artifacts/AUTOBOOT-FCM.C65" autoboot.c65 -write "$out/artifacts/F65-R0B-FCM-SAFE.prg" f65-r0a-proof -list > "$out/reports/F65-R0B-FCM-SAFE.d81-create.txt" 2>&1
  "$c1541" "$out/artifacts/F65-R0B-FCM-SAFE.d81" -list > "$out/reports/F65-R0B-FCM-SAFE.d81-list.txt" 2>&1
  python3 "$root/tools/diagnostics/r0b_validate_fcm_safe_package.py" "$root"
  shasum -a 256 "$out/artifacts/F65-R0B-FCM-SAFE.prg" > "$out/artifacts/F65-R0B-FCM-SAFE.prg.sha256"
  shasum -a 256 "$out/artifacts/F65-R0B-FCM-SAFE.d81" > "$out/artifacts/F65-R0B-FCM-SAFE.d81.sha256"
}
build_fcm_visible() {
  host_test
  mkdir -p "$out/reports" "$out/artifacts" "$out/evidence"
  "$cc" -mcpu=mos45gs02 -mlto-zp=0 -Os -Wall -Wextra -Wconversion -Werror -I"$root/interfaces/generated" "$root/src/r0b/fcm_visible_main.c" "$root/src/diagnostics/r0b/fcm_visible.c" "$root/src/platform/r0b/fcm_visible_45gs02.s" "$root/src/platform/r0a_platform_45gs02.s" -Wl,-Map,"$out/reports/F65-R0B-FCM-VISIBLE.map" -o "$out/artifacts/F65-R0B-FCM-VISIBLE.prg"
  "$nm" "$out/artifacts/F65-R0B-FCM-VISIBLE.prg.elf" > "$out/reports/F65-R0B-FCM-VISIBLE.symbols"
  "$objdump" -d --print-imm-hex "$out/artifacts/F65-R0B-FCM-VISIBLE.prg.elf" > "$out/reports/F65-R0B-FCM-VISIBLE.disassembly"
  python3 "$root/tools/diagnostics/r0b_validate_fcm_visible_target.py" "$root"
  "$petcat" -w65 -o "$out/artifacts/AUTOBOOT-FCM-VISIBLE.C65" -- "$root/src/r0b/autoboot_fcm_safe.bas"
  "$petcat" -65 "$out/artifacts/AUTOBOOT-FCM-VISIBLE.C65" > "$out/reports/AUTOBOOT-FCM-VISIBLE.C65.listing"
  "$c1541" -format 'F65 R0-B FCM VIS,65' d81 "$out/artifacts/F65-R0B-FCM-VISIBLE.d81" -write "$out/artifacts/AUTOBOOT-FCM-VISIBLE.C65" autoboot.c65 -write "$out/artifacts/F65-R0B-FCM-VISIBLE.prg" f65-r0a-proof -list > "$out/reports/F65-R0B-FCM-VISIBLE.d81-create.txt" 2>&1
  "$c1541" "$out/artifacts/F65-R0B-FCM-VISIBLE.d81" -list > "$out/reports/F65-R0B-FCM-VISIBLE.d81-list.txt" 2>&1
  python3 "$root/tools/diagnostics/r0b_validate_fcm_visible_package.py" "$root"
  shasum -a 256 "$out/artifacts/F65-R0B-FCM-VISIBLE.prg" > "$out/artifacts/F65-R0B-FCM-VISIBLE.prg.sha256"
  shasum -a 256 "$out/artifacts/F65-R0B-FCM-VISIBLE.d81" > "$out/artifacts/F65-R0B-FCM-VISIBLE.d81.sha256"
}
xemu_run() {
  test -x "$xemu" || { echo 'R0-B Xemu blocked: no verified xmega65 binary.' >&2; exit 2; }
  test -n "${F65_MEGA65_ROM:-}" && test -f "$F65_MEGA65_ROM" || { echo 'R0-B Xemu blocked: set F65_MEGA65_ROM to the owner ROM outside the repository.' >&2; exit 2; }
  test -f "$out/artifacts/F65-R0B-PROOF.d81" || build
  rom_sha=$(shasum -a 256 "$F65_MEGA65_ROM" | awk '{print $1}')
  test "$rom_sha" = 'af3c447f791a2fdc48cb21e1bd3fab015e32641228d9d30d21259b9e878c6fa0' || { echo "R0-B Xemu blocked: unexpected ROM SHA-256: $rom_sha" >&2; exit 2; }
  "$xemu" -headless -sleepless -fastboot -rom "$F65_MEGA65_ROM" -8 "$out/artifacts/F65-R0B-PROOF.d81" -autoload -dumpscreen "$out/reports/R0B-XEMU.screen.txt" -dumpmem "$out/reports/R0B-XEMU.memory.bin" -screenshot "$out/reports/R0B-XEMU.png" &
  pid=$!; sleep "${F65_XEMU_RUN_SECONDS:-25}"; kill -TERM "$pid" 2>/dev/null || true; wait "$pid" || true
  python3 "$root/tools/diagnostics/r0b_validate_xemu.py" "$root"
}
xemu_fcm_safe_run() {
  test -x "$xemu" || { echo 'R0-B FCM-safe Xemu blocked: no verified xmega65 binary.' >&2; exit 2; }
  test -n "${F65_MEGA65_ROM:-}" && test -f "$F65_MEGA65_ROM" || { echo 'R0-B FCM-safe Xemu blocked: set F65_MEGA65_ROM to the owner ROM outside the repository.' >&2; exit 2; }
  test -f "$out/artifacts/F65-R0B-FCM-SAFE.d81" || build_fcm_safe
  rom_sha=$(shasum -a 256 "$F65_MEGA65_ROM" | awk '{print $1}')
  test "$rom_sha" = 'af3c447f791a2fdc48cb21e1bd3fab015e32641228d9d30d21259b9e878c6fa0' || { echo "R0-B FCM-safe Xemu blocked: unexpected ROM SHA-256: $rom_sha" >&2; exit 2; }
  "$xemu" -headless -sleepless -fastboot -rom "$F65_MEGA65_ROM" -8 "$out/artifacts/F65-R0B-FCM-SAFE.d81" -autoload -dumpscreen "$out/reports/R0B-FCM-SAFE-XEMU.screen.txt" -dumpmem "$out/reports/R0B-FCM-SAFE-XEMU.memory.bin" -screenshot "$out/reports/R0B-FCM-SAFE-XEMU.png" &
  pid=$!; sleep "${F65_XEMU_RUN_SECONDS:-25}"; kill -TERM "$pid" 2>/dev/null || true; wait "$pid" || true
  python3 "$root/tools/diagnostics/r0b_validate_fcm_safe_xemu.py" "$root"
}
xemu_fcm_visible_run() {
  test -x "$xemu" || { echo 'R0-B FCM-visible Xemu blocked: no verified xmega65 binary.' >&2; exit 2; }
  test -n "${F65_MEGA65_ROM:-}" && test -f "$F65_MEGA65_ROM" || { echo 'R0-B FCM-visible Xemu blocked: set F65_MEGA65_ROM to the owner ROM outside the repository.' >&2; exit 2; }
  test -f "$out/artifacts/F65-R0B-FCM-VISIBLE.d81" || build_fcm_visible
  rom_sha=$(shasum -a 256 "$F65_MEGA65_ROM" | awk '{print $1}')
  test "$rom_sha" = 'af3c447f791a2fdc48cb21e1bd3fab015e32641228d9d30d21259b9e878c6fa0' || { echo "R0-B FCM-visible Xemu blocked: unexpected ROM SHA-256: $rom_sha" >&2; exit 2; }
  "$xemu" -headless -sleepless -fastboot -rom "$F65_MEGA65_ROM" -8 "$out/artifacts/F65-R0B-FCM-VISIBLE.d81" -autoload -dumpscreen "$out/reports/R0B-FCM-VISIBLE-XEMU.screen.txt" -dumpmem "$out/reports/R0B-FCM-VISIBLE-XEMU.memory.bin" -screenshot "$out/reports/R0B-FCM-VISIBLE-XEMU.png" &
  pid=$!; sleep "${F65_XEMU_RUN_SECONDS:-25}"; kill -TERM "$pid" 2>/dev/null || true; wait "$pid" || true
  python3 "$root/tools/diagnostics/r0b_validate_fcm_visible_xemu.py" "$root"
}
case ${1:-} in
 bootstrap) need_tools; "$cc" --version; "$java" -version 2>&1 ;;
 generate) generate ;;
 host-test) host_test ;;
 build) build ;;
 xemu) xemu_run ;;
 fcm-safe-build) build_fcm_safe ;;
 fcm-visible-build) build_fcm_visible ;;
 fcm-visible-xemu) xemu_fcm_visible_run ;;
 fcm-safe-xemu) xemu_fcm_safe_run ;;
 evidence) host_test ;;
 verify) host_test; build ;;
 clean) test -d "$out" && rm -rf "$out" || true ;;
 *) echo "usage: $0 {bootstrap|generate|host-test|build|xemu|fcm-safe-build|fcm-safe-xemu|fcm-visible-build|fcm-visible-xemu|evidence|verify|clean}" >&2; exit 64 ;;
esac
