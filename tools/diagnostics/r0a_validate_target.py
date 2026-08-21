#!/usr/bin/env python3
"""Static evidence gate for the approved 45GS02 B-register R0-A integration."""
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
reports = root / "build" / "r0a" / "reports"
symbols = (reports / "F65-R0A-PROOF.symbols").read_text()
mapping = (reports / "F65-R0A-PROOF.map").read_text()
disassembly = (reports / "F65-R0A-PROOF.disassembly").read_text()

def symbol_value(name):
    match = re.search(r"^([0-9a-fA-F]+)\s+\w\s+" + re.escape(name) + r"$", symbols, re.MULTILINE)
    if not match:
        raise SystemExit(f"R0A-BP-001 FAIL: missing symbol {name}")
    return int(match.group(1), 16)

for index in range(32):
    expected = 0x02 + index
    actual = symbol_value(f"__rc{index}")
    if actual != expected:
        raise SystemExit(f"R0A-BP-001 FAIL: __rc{index} is ${actual:04x}, expected ${expected:04x}")

for name in ("__zp_data_size", "__zp_bss_size"):
    if symbol_value(name) != 0:
        raise SystemExit(f"R0A-BP-001 FAIL: {name} is nonzero with -mlto-zp=0")

def section_address(section):
    match = re.search(r"^\s*([0-9a-fA-F]+)\s+[0-9a-fA-F]+.*\(" + re.escape(section) + r"\)", mapping, re.MULTILINE)
    if not match:
        raise SystemExit(f"R0A-BP-001 FAIL: map lacks section {section}")
    return int(match.group(1), 16)

def address_after(left, right):
    left_match = section_address(left)
    right_match = section_address(right)
    return left_match < right_match

if not address_after(".init.010", ".init.011"):
    raise SystemExit("R0A-BP-001 FAIL: .init.011 does not follow stock .init.010")
if not address_after(".fini.989", ".fini.990"):
    raise SystemExit("R0A-BP-001 FAIL: .fini.989 does not precede stock .fini.990")

def function_block(name):
    match = re.search(r"<[\w.]*" + re.escape(name) + r">:(.*?)(?=\n[0-9a-f]+ <|\Z)", disassembly, re.DOTALL)
    if not match:
        raise SystemExit(f"R0A-BP-001 FAIL: disassembly lacks {name}")
    return match.group(1)

entry = function_block("f65_basepage_enter")
leave = function_block("f65_basepage_leave")
if not re.search(r"lda\s+#\$2\s*\n.*\btab\b", entry):
    raise SystemExit("R0A-BP-001 FAIL: entry does not establish B=$02")
if not re.search(r"lda\s+#\$0\s*\n.*\btab\b", leave):
    raise SystemExit("R0A-BP-001 FAIL: leave does not restore B=$00")
if not re.search(r"99\s+02 00\s+\s*sta\s+\$2,y", disassembly):
    raise SystemExit("R0A-BP-001 FAIL: sentinel seed is not an absolute physical $0002,Y store")
if not re.search(r"d9\s+02 00\s+\s*cmp\s+\$2,y", disassembly):
    raise SystemExit("R0A-BP-001 FAIL: sentinel check is not an absolute physical $0002,Y compare")
if not re.search(r"r0a_abi_heavy", disassembly) or not re.search(r"\$(?:0[2-9a-f]|1[0-9a-f]|2[0-1])\b", function_block("r0a_abi_heavy")):
    raise SystemExit("R0A-BP-001 FAIL: nested C probe did not retain observable direct-page ABI access")
print("R0A-BP-001 PASS: logical ABI registers, B transitions, and no LTO direct-page allocation verified")
