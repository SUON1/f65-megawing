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
out="$root/build/r0a"
classes="$out/host-classes"

need_tools() { test -x "$java" && test -x "$javac" && test -x "$cc" && test -x "$objdump" && test -x "$nm" && test -x "$c1541" && test -x "$petcat"; }
compile_host() { mkdir -p "$classes"; "$javac" -d "$classes" "$root/tools/generators/src/main/java/f65/tools/R0AHostTools.java"; }
generate() { need_tools; compile_host; "$java" -cp "$classes" f65.tools.R0AHostTools generate "$root"; }
host_test() { generate; "$java" -cp "$classes" f65.tools.R0AHostTools host-test "$root"; python3 "$root/tools/diagnostics/r0a_validate.py" "$root"; }
build() {
  host_test
  mkdir -p "$out/reports" "$out/artifacts"
  "$cc" -mcpu=mos45gs02 -mlto-zp=0 -Os -Wall -Wextra -Wconversion -Werror -I"$root/interfaces/generated" "$root/src/r0a/main.c" "$root/src/platform/r0a_platform_45gs02.s" -Wl,-Map,"$out/reports/F65-R0A-PROOF.map" -o "$out/artifacts/F65-R0A-PROOF.prg"
  "$nm" "$out/artifacts/F65-R0A-PROOF.prg.elf" > "$out/reports/F65-R0A-PROOF.symbols"
  "$objdump" -d --print-imm-hex "$out/artifacts/F65-R0A-PROOF.prg.elf" > "$out/reports/F65-R0A-PROOF.disassembly"
  python3 "$root/tools/diagnostics/r0a_validate_target.py" "$root"
  "$petcat" -w65 -o "$out/artifacts/AUTOBOOT.C65" -- "$root/src/r0a/autoboot.bas"
  "$petcat" -65 "$out/artifacts/AUTOBOOT.C65" > "$out/reports/AUTOBOOT.C65.listing"
  "$c1541" -format 'F65 R0-A,65' d81 "$out/artifacts/F65-R0A-PROOF.d81" -write "$out/artifacts/AUTOBOOT.C65" AUTOBOOT.C65 -write "$out/artifacts/F65-R0A-PROOF.prg" F65-R0A-PROOF -list > "$out/reports/F65-R0A-PROOF.d81-create.txt" 2>&1
  "$c1541" "$out/artifacts/F65-R0A-PROOF.d81" -list > "$out/reports/F65-R0A-PROOF.d81-list.txt" 2>&1
  python3 "$root/tools/diagnostics/r0a_validate_package.py" "$root"
  shasum -a 256 "$out/artifacts/F65-R0A-PROOF.prg" > "$out/artifacts/F65-R0A-PROOF.prg.sha256"
  shasum -a 256 "$out/artifacts/F65-R0A-PROOF.d81" > "$out/artifacts/F65-R0A-PROOF.d81.sha256"
  printf '%s\n' 'Xemu/hardware execution is BLOCKED: a verified xmega65 binary, owner-provided ROM, and system-file configuration are not available locally.' > "$out/reports/R0A_BUILD_BLOCKER.txt"
  return 2
}
case ${1:-} in
  bootstrap) need_tools; "$cc" --version; "$java" -version 2>&1 ;;
  generate) generate ;;
  host-test) host_test ;;
  build) build ;;
  xemu) test -x "$root/toolchain/xemu/xmega65" || { echo 'R0-A Xemu blocked: no verified xmega65 binary is installed.' >&2; exit 2; }; test -n "${F65_MEGA65_ROM:-}" || { echo 'R0-A Xemu blocked: set F65_MEGA65_ROM to the owner ROM; do not copy it into this repository.' >&2; exit 2; }; test -f "$out/artifacts/F65-R0A-PROOF.d81" || { echo 'R0-A Xemu blocked: exact proof D81 has not been produced.' >&2; exit 2; }; echo 'R0-A Xemu blocked: the candidate binary/ROM invocation and captured result protocol require an approved runtime configuration.' >&2; exit 2 ;;
  evidence) host_test ;;
  verify) host_test; build ;;
  clean) test -d "$out" && rm -rf "$out" || true ;;
  *) echo "usage: $0 {bootstrap|generate|host-test|build|xemu|evidence|verify|clean}" >&2; exit 64 ;;
esac
