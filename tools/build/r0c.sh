#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
java_home="$root/toolchain/runtime/jdk-full/jdk-21.0.12+8/Contents/Home"
java="$java_home/bin/java"; javac="$java_home/bin/javac"
cc="$root/toolchain/runtime/llvm-mos/bin/mos-mega65-clang"; objdump="$root/toolchain/runtime/llvm-mos/bin/llvm-objdump"; nm="$root/toolchain/runtime/llvm-mos/bin/llvm-nm"
vice="$root/toolchain/vice/VICE.app/Contents/Resources/bin"; c1541="$vice/c1541"; petcat="$vice/petcat"; xemu="$root/toolchain/xemu/xmega65"
out="$root/build/r0c"; classes="$out/host-classes"
need_tools() { test -x "$java" && test -x "$javac" && test -x "$cc" && test -x "$objdump" && test -x "$nm" && test -x "$c1541" && test -x "$petcat"; }
compile_host() { mkdir -p "$classes"; "$javac" -d "$classes" "$root/tools/generators/src/main/java/f65/tools/R0CHostTools.java"; }
host() { "$java" -Df65.root="$root" -cp "$classes" f65.tools.R0CHostTools "$@"; }
generate() { need_tools; compile_host; host generate; }
host_test() { generate; host host-test; python3 "$root/tools/diagnostics/r0c_validate_target.py" "$root"; }
build() {
  host_test; mkdir -p "$out/artifacts" "$out/reports" "$out/evidence"
  "$cc" -mcpu=mos45gs02 -mlto-zp=0 -Os -Wall -Wextra -Wconversion -Werror -I"$root/interfaces/generated" "$root/src/r0c/main.c" "$root/src/diagnostics/r0c/composite.c" "$root/src/platform/r0a_platform_45gs02.s" "$root/src/platform/r0c_attic_45gs02.s" -Wl,-Map,"$out/reports/F65-R0C-PROOF.map" -o "$out/artifacts/F65-R0C-PROOF.prg"
  "$nm" "$out/artifacts/F65-R0C-PROOF.prg.elf" > "$out/reports/F65-R0C-PROOF.symbols"
  "$objdump" -d --print-imm-hex "$out/artifacts/F65-R0C-PROOF.prg.elf" > "$out/reports/F65-R0C-PROOF.disassembly"
  "$petcat" -w65 -o "$out/artifacts/AUTOBOOT.C65" -- "$root/src/r0c/autoboot.bas"
  "$petcat" -w65 -o "$out/artifacts/R0C-MEDIA.C65" -- "$root/src/r0c/media_fixture.bas"
  "$petcat" -w65 -o "$out/artifacts/R0C-MEDIA-BOOT.C65" -- "$root/src/r0c/media_boot.bas"
  "$c1541" -format 'F65 R0-C MEDIA,65' d81 "$out/artifacts/R0CMEDIA.D81" -write "$out/artifacts/AUTOBOOT.C65" autoboot.c65 -write "$out/artifacts/F65-R0C-PROOF.prg" r0c-final -write "$out/artifacts/R0C-MEDIA.C65" r0c-media -write "$out/R0CPROOF.PKG" r0cproof -list > "$out/reports/R0CMEDIA.D81-create.txt" 2>&1
  "$c1541" "$out/artifacts/R0CMEDIA.D81" -list > "$out/reports/R0CMEDIA.D81-list.txt" 2>&1
  python3 "$root/tools/diagnostics/r0c_validate_media_fixture.py" "$root"
  host d81-manifest "$out/artifacts/R0CMEDIA.D81"
  shasum -a 256 "$out/artifacts/F65-R0C-PROOF.prg" > "$out/artifacts/F65-R0C-PROOF.prg.sha256"
  shasum -a 256 "$out/artifacts/R0CMEDIA.D81" > "$out/artifacts/R0CMEDIA.D81.sha256"
}
xemu_run() {
  test -x "$xemu" || { echo 'R0-C Xemu blocked: verified xmega65 is unavailable.' >&2; exit 2; }
  test -n "${F65_MEGA65_ROM:-}" && test -f "$F65_MEGA65_ROM" || { echo 'R0-C Xemu blocked: set F65_MEGA65_ROM to the owner ROM.' >&2; exit 2; }
  test -f "$out/artifacts/R0CMEDIA.D81" || build
  "$xemu" -headless -sleepless -fastboot -rom "$F65_MEGA65_ROM" -8 "$out/artifacts/R0CMEDIA.D81" -9 "$out/artifacts/R0CMEDIA.D81" -autoload -dumpscreen "$out/reports/R0C-XEMU.screen.txt" -dumpmem "$out/reports/R0C-XEMU.memory.bin" -screenshot "$out/reports/R0C-XEMU.png" &
  pid=$!; sleep "${F65_XEMU_RUN_SECONDS:-20}"; kill -TERM "$pid" 2>/dev/null || true; wait "$pid" || true
  "$xemu" -headless -sleepless -fastboot -rom "$F65_MEGA65_ROM" -9 "$out/artifacts/R0CMEDIA.D81" -prg "$out/artifacts/R0C-MEDIA-BOOT.C65" -prgmode 65 -dumpscreen "$out/reports/R0C-MEDIA-XEMU.screen.txt" -screenshot "$out/reports/R0C-MEDIA-XEMU.png" &
  pid=$!; sleep "${F65_XEMU_RUN_SECONDS:-20}"; kill -TERM "$pid" 2>/dev/null || true; wait "$pid" || true
  python3 "$root/tools/diagnostics/r0c_validate_xemu.py" "$root"
}
case ${1:-} in
 bootstrap) need_tools; "$cc" --version; "$java" -version 2>&1 ;;
 generate) generate ;;
 host-test) host_test ;;
 build) build ;;
 verify) generate; host verify; python3 "$root/tools/diagnostics/r0c_validate_target.py" "$root" ;;
 xemu) xemu_run ;;
 evidence) host_test; test -f "$out/artifacts/R0CMEDIA.D81" && host d81-manifest "$out/artifacts/R0CMEDIA.D81" || true ;;
 clean) rm -rf "$out" ;;
 *) echo 'usage: r0c.sh {bootstrap|generate|host-test|build|verify|xemu|evidence|clean}' >&2; exit 2 ;;
esac
