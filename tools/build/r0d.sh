#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
java_home="$root/toolchain/runtime/jdk-full/jdk-21.0.12+8/Contents/Home"
java="$java_home/bin/java"; javac="$java_home/bin/javac"
cc="$root/toolchain/runtime/llvm-mos/bin/mos-mega65-clang"; objdump="$root/toolchain/runtime/llvm-mos/bin/llvm-objdump"; nm="$root/toolchain/runtime/llvm-mos/bin/llvm-nm"
vice="$root/toolchain/vice/VICE.app/Contents/Resources/bin"; c1541="$root/toolchain/vice-clean/bin/c1541"; petcat="$vice/petcat"
out="$root/build/r0d"; classes="$out/host-classes"
need_tools() { test -x "$java" && test -x "$javac" && test -x "$cc" && test -x "$objdump" && test -x "$nm" && test -x "$c1541" && test -x "$petcat"; }
compile_host() { mkdir -p "$classes"; "$javac" -d "$classes" "$root/tools/generators/src/main/java/f65/tools/R0DHostTools.java"; }
host() { "$java" -Df65.root="$root" -cp "$classes" f65.tools.R0DHostTools "$@"; }
generate() { need_tools; compile_host; host generate; }
host_test() { generate; host host-test; python3 "$root/tools/diagnostics/r0d_validate_target.py" "$root"; }
build() {
  host_test; mkdir -p "$out/artifacts" "$out/reports"
  "$cc" -mcpu=mos45gs02 -mlto-zp=0 -Os -Wall -Wextra -Wconversion -Werror -I"$root/interfaces/generated" "$root/src/r0d/main.c" "$root/src/diagnostics/r0d/composite.c" "$root/src/platform/r0a_platform_45gs02.s" -Wl,-Map,"$out/reports/F65-R0D-CALIBRATION.map" -o "$out/artifacts/F65-R0D-CALIBRATION.prg"
  "$nm" "$out/artifacts/F65-R0D-CALIBRATION.prg.elf" > "$out/reports/F65-R0D-CALIBRATION.symbols"
  "$objdump" -d --print-imm-hex "$out/artifacts/F65-R0D-CALIBRATION.prg.elf" > "$out/reports/F65-R0D-CALIBRATION.disassembly"
  python3 "$root/tools/diagnostics/r0d_validate_build.py" "$root"
  "$petcat" -w65 -o "$out/artifacts/AUTOBOOT.C65" -- "$root/src/r0d/autoboot.bas"
  "$petcat" -65 "$out/artifacts/AUTOBOOT.C65" > "$out/reports/AUTOBOOT.C65.listing"
  candidate="$out/artifacts/F65R0D3.D81"
  rm -f "$candidate" "$candidate.sha256"
  run_c1541_clean "$out/reports/F65R0D3.D81-create.txt" -format 'F65 R0-D3,65' d81 "$candidate" -write "$out/artifacts/AUTOBOOT.C65" autoboot.c65 -write "$out/artifacts/F65-R0D-CALIBRATION.prg" r0d-calib -list
  run_c1541_clean "$out/reports/F65R0D3.D81-list.txt" "$candidate" -list
  python3 "$root/tools/diagnostics/r0d_d81_loadability_gate.py" "$root" "$candidate"
  shasum -a 256 "$out/artifacts/F65-R0D-CALIBRATION.prg" > "$out/artifacts/F65-R0D-CALIBRATION.prg.sha256"
  shasum -a 256 "$candidate" > "$candidate.sha256"
}
run_c1541_clean() {
  report=$1
  shift
  stdout="${report}.stdout"
  stderr="${report}.stderr"
  rm -f "$stdout" "$stderr"
  if ! "$c1541" "$@" >"$stdout" 2>"$stderr"; then
    cat "$stdout" "$stderr" >&2
    return 1
  fi
  if test -s "$stderr" || rg -n -i 'warning|error|failed|fatal|duplicate|truncat|allocation' "$stdout" "$stderr"; then
    cat "$stdout" "$stderr" >&2
    return 1
  fi
  cat "$stdout" "$stderr" > "$report"
  rm -f "$stdout" "$stderr"
}
case ${1:-} in
  bootstrap) need_tools; "$cc" --version; "$java" -version 2>&1 ;;
  generate) generate ;;
  host-test) host_test ;;
  build) build ;;
  verify) generate; host verify; python3 "$root/tools/diagnostics/r0d_validate_target.py" "$root" ;;
  clean) rm -rf "$out" ;;
  *) echo 'usage: r0d.sh {bootstrap|generate|host-test|build|verify|clean}' >&2; exit 2 ;;
esac
