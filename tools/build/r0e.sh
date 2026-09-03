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

d81_blocked(){ echo 'R0-E D81 creation/testing blocked: R0-E2 and R0-E3 are invalid; capture the failed R0-E3 SD extent map before assigning a new carrier identity.' >&2; exit 2; }

need_host(){ test -x "$java" && test -x "$javac"; }
need_target(){ test -x "$cc" && test -x "$objdump" && test -x "$nm"; }
need_d81(){ test -x "$c1541" && test -x "$petcat"; }
hostc(){ mkdir -p "$classes"; "$javac" -d "$classes" "$root/tools/generators/src/main/java/f65/tools/R0EHostTools.java"; }
host(){ "$java" -Df65.root="$root" -cp "$classes" f65.tools.R0EHostTools "$@"; }
generate(){ need_host; hostc; host generate; }
hosttest(){ generate; host host-test; python3 "$root/tools/diagnostics/r0e_validate_target.py" "$root" --source-only; }
clean_c1541(){ report=$1; shift; stdout="$report.stdout"; stderr="$report.stderr"; rm -f "$stdout" "$stderr"; if ! "$c1541" "$@" >"$stdout" 2>"$stderr"; then cat "$stdout" "$stderr" >&2; return 1; fi; if test -s "$stderr" || rg -n -i 'warning|error|failed|fatal|duplicate|truncat|allocation|opencbm' "$stdout" "$stderr"; then cat "$stdout" "$stderr" >&2; return 1; fi; cat "$stdout" >"$report"; rm -f "$stdout" "$stderr"; }
build(){ d81_blocked; }
xemu_run(){ d81_blocked; }
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
