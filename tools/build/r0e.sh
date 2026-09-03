#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
java="$root/toolchain/runtime/jdk-full/jdk-21.0.12+8/Contents/Home/bin/java"
javac="$root/toolchain/runtime/jdk-full/jdk-21.0.12+8/Contents/Home/bin/javac"
cc="$root/toolchain/runtime/llvm-mos/bin/mos-mega65-clang"
objdump="$root/toolchain/runtime/llvm-mos/bin/llvm-objdump"
nm="$root/toolchain/runtime/llvm-mos/bin/llvm-nm"
c1541="$root/toolchain/vice-clean/bin/c1541"
petcat="$root/toolchain/vice/VICE.app/Contents/Resources/bin/petcat"
xemu="$root/toolchain/xemu/xmega65"
out="$root/build/r0e"
classes="$out/host-classes"

foundation_blocked(){ echo 'R0-E D81 creation/testing blocked: F65R0E2.D81, F65R0E3.D81, and F65R0E4.D81 are retired after physical chooser ERROR CODE FF. Complete D81 foundation qualification before assigning another carrier.' >&2; exit 2; }

need_host(){ test -x "$java" && test -x "$javac" || { echo 'R0-E build blocked: pinned Java runtime/compiler are absent from toolchain/runtime.' >&2; exit 2; }; }
need_target(){ test -x "$cc" && test -x "$objdump" && test -x "$nm" || { echo 'R0-E build blocked: pinned LLVM-MOS target tools are absent from toolchain/runtime.' >&2; exit 2; }; }
need_d81(){ test -x "$c1541" && test -x "$petcat" || { echo 'R0-E build blocked: pinned VICE c1541/petcat tools are absent.' >&2; exit 2; }; }
hostc(){ mkdir -p "$classes"; "$javac" -d "$classes" "$root/tools/generators/src/main/java/f65/tools/R0EHostTools.java"; }
host(){ "$java" -Df65.root="$root" -cp "$classes" f65.tools.R0EHostTools "$@"; }
generate(){ need_host; hostc; host generate; }
hosttest(){ generate; host host-test; python3 "$root/tools/diagnostics/r0e_validate_target.py" "$root" --source-only; }
clean_c1541(){ report=$1; shift; stdout="$report.stdout"; stderr="$report.stderr"; rm -f "$stdout" "$stderr"; if ! "$c1541" "$@" >"$stdout" 2>"$stderr"; then cat "$stdout" "$stderr" >&2; return 1; fi; if test -s "$stderr" || rg -n -i 'warning|error|failed|fatal|duplicate|truncat|allocation|opencbm' "$stdout" "$stderr"; then cat "$stdout" "$stderr" >&2; return 1; fi; cat "$stdout" >"$report"; rm -f "$stdout" "$stderr"; }
build(){ foundation_blocked; }
xemu_boot(){ label=$1; rm -f "$out/reports/R0E-XEMU-$label.screen.txt" "$out/reports/R0E-XEMU-$label.memory.bin" "$out/reports/R0E-XEMU-$label.png"; "$xemu" -headless -sleepless -fastboot -rom "$F65_MEGA65_ROM" -8 "$out/artifacts/F65R0E4.D81" -autoload -dumpscreen "$out/reports/R0E-XEMU-$label.screen.txt" -dumpmem "$out/reports/R0E-XEMU-$label.memory.bin" -screenshot "$out/reports/R0E-XEMU-$label.png" & xemu_pid=$!; sleep "${F65_XEMU_RUN_SECONDS:-20}"; kill -TERM "$xemu_pid" 2>/dev/null || true; if wait "$xemu_pid"; then :; else :; fi; }
xemu_run(){ foundation_blocked; }
case ${1:-} in
  bootstrap) need_host; need_target; "$cc" --version; "$java" -version 2>&1 ;;
  generate) generate ;;
  host-test) hosttest ;;
  build) build ;;
  xemu) xemu_run ;;
  verify) generate; host verify; python3 "$root/tools/diagnostics/r0e_validate_target.py" "$root" --source-only ;;
  clean) rm -rf "$out" ;;
  *) echo 'usage: r0e.sh {bootstrap|generate|host-test|build|xemu|verify|clean}' >&2; exit 2 ;;
esac
