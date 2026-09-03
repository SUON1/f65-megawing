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

need_host(){ test -x "$java" && test -x "$javac"; }
need_target(){ test -x "$cc" && test -x "$objdump" && test -x "$nm"; }
need_d81(){ test -x "$c1541" && test -x "$petcat"; }
hostc(){ mkdir -p "$classes"; "$javac" -d "$classes" "$root/tools/generators/src/main/java/f65/tools/R0EHostTools.java"; }
host(){ "$java" -Df65.root="$root" -cp "$classes" f65.tools.R0EHostTools "$@"; }
generate(){ need_host; hostc; host generate; }
hosttest(){ generate; host host-test; python3 "$root/tools/diagnostics/r0e_validate_target.py" "$root" --source-only; }
clean_c1541(){ report=$1; shift; stdout="$report.stdout"; stderr="$report.stderr"; rm -f "$stdout" "$stderr"; if ! "$c1541" "$@" >"$stdout" 2>"$stderr"; then cat "$stdout" "$stderr" >&2; return 1; fi; if test -s "$stderr" || rg -n -i 'warning|error|failed|fatal|duplicate|truncat|allocation|opencbm' "$stdout" "$stderr"; then cat "$stdout" "$stderr" >&2; return 1; fi; cat "$stdout" >"$report"; rm -f "$stdout" "$stderr"; }
build(){ hosttest; need_target; mkdir -p "$out/artifacts" "$out/reports"; "$cc" -mcpu=mos45gs02 -mlto-zp=0 -Os -Wall -Wextra -Wconversion -Werror -I"$root/interfaces/generated" "$root/src/r0e/main.c" "$root/src/diagnostics/r0e/composite.c" "$root/src/platform/r0e/raster_observation.c" "$root/src/platform/r0a_platform_45gs02.s" -Wl,-Map,"$out/reports/F65-R0E-PROOF.map" -o "$out/artifacts/F65-R0E-PROOF.prg"; "$nm" "$out/artifacts/F65-R0E-PROOF.prg.elf" > "$out/reports/F65-R0E-PROOF.symbols"; "$objdump" -d --print-imm-hex "$out/artifacts/F65-R0E-PROOF.prg.elf" > "$out/reports/F65-R0E-PROOF.disassembly"; python3 "$root/tools/diagnostics/r0e_validate_target.py" "$root"; need_d81; "$petcat" -w65 -o "$out/artifacts/AUTOBOOT.C65" -- "$root/src/r0e/autoboot.bas"; "$petcat" -65 "$out/artifacts/AUTOBOOT.C65" > "$out/reports/AUTOBOOT.C65.listing"; candidate="$out/artifacts/F65R0E4.D81"; rm -f "$candidate" "$candidate.sha256"; clean_c1541 "$out/reports/F65R0E4.D81-create.txt" -format 'F65 R0-E4,65' d81 "$candidate" -write "$out/artifacts/AUTOBOOT.C65" autoboot.c65 -write "$out/artifacts/F65-R0E-PROOF.prg" r0e-proof -write "$out/artifacts/R0E-EVID.txt" r0e-evid -list; clean_c1541 "$out/reports/F65R0E4.D81-list.txt" "$candidate" -list; python3 "$root/tools/diagnostics/r0e_d81_loadability_gate.py" "$root" "$candidate"; shasum -a 256 "$out/artifacts/F65-R0E-PROOF.prg" > "$out/artifacts/F65-R0E-PROOF.prg.sha256"; shasum -a 256 "$candidate" > "$candidate.sha256"; }
xemu_boot(){ label=$1; rm -f "$out/reports/R0E-XEMU-$label.screen.txt" "$out/reports/R0E-XEMU-$label.memory.bin" "$out/reports/R0E-XEMU-$label.png"; "$xemu" -headless -sleepless -fastboot -rom "$F65_MEGA65_ROM" -8 "$out/artifacts/F65R0E4.D81" -autoload -dumpscreen "$out/reports/R0E-XEMU-$label.screen.txt" -dumpmem "$out/reports/R0E-XEMU-$label.memory.bin" -screenshot "$out/reports/R0E-XEMU-$label.png" & xemu_pid=$!; sleep "${F65_XEMU_RUN_SECONDS:-20}"; kill -TERM "$xemu_pid" 2>/dev/null || true; if wait "$xemu_pid"; then :; else :; fi; }
xemu_run(){ test -x "$xemu" || { echo 'R0-E Xemu blocked: no pinned xmega65 binary.' >&2; exit 2; }; test -n "${F65_MEGA65_ROM:-}" && test -f "$F65_MEGA65_ROM" || { echo 'R0-E Xemu blocked: set F65_MEGA65_ROM to the owner ROM outside the repository.' >&2; exit 2; }; test -f "$out/artifacts/F65R0E4.D81" || { echo 'R0-E Xemu blocked: build the exact host-gated D81 first.' >&2; exit 2; }; rom_sha=$(shasum -a 256 "$F65_MEGA65_ROM" | awk '{print $1}'); test "$rom_sha" = 'af3c447f791a2fdc48cb21e1bd3fab015e32641228d9d30d21259b9e878c6fa0' || { echo "R0-E Xemu blocked: unexpected ROM SHA-256: $rom_sha" >&2; exit 2; }; mkdir -p "$out/reports"; printf '%s\n' "xmega65=$xemu" "rom_sha256=$rom_sha" "d81_sha256=$(shasum -a 256 "$out/artifacts/F65R0E4.D81" | awk '{print $1}')" 'arguments=-headless -sleepless -fastboot -rom <owner ROM> -8 F65R0E4.D81 -autoload' > "$out/reports/R0E-XEMU-INVOCATION.txt"; xemu_boot boot1; xemu_boot boot2; python3 "$root/tools/diagnostics/r0e_validate_xemu.py" "$root"; }
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
