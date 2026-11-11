"""Independent raw-image startup/load and necessary renderer-service checks.

No emulator is started. A lower bound that already exceeds the frame allowance
is sufficient to reject service; it is never an operation's admitted WCET.
"""
import hashlib
import json
from pathlib import Path
import re
import struct

from stack_admission import BRANCHES, branch_targets, parse


def elf_sections(raw):
    if raw[:7] != b"\x7fELF\x01\x01\x01":
        raise ValueError("expected ELF32 little endian")
    start = struct.unpack_from("<I", raw, 32)[0]
    width, count, strings_index = struct.unpack_from("<HHH", raw, 46)
    if width != 40 or not count or strings_index >= count:
        raise ValueError("unsupported ELF section table")
    rows = [struct.unpack_from("<10I", raw, start + index * width) for index in range(count)]
    strings = rows[strings_index]
    names = raw[strings[4]:strings[4] + strings[5]]
    output = {}
    for row in rows:
        if not (row[2] & 2) or not row[5]:
            continue
        name = names[row[0]:].split(b"\0", 1)[0].decode()
        output[name] = {"type": row[1], "flags": row[2], "address": row[3],
                        "bytes": row[5], "data": raw[row[4]:row[4] + row[5]]}
    return output


def image_bytes(prg, address, count):
    origin = int.from_bytes(prg[:2], "little")
    offset = address - origin + 2
    if offset < 2 or offset + count > len(prg):
        raise ValueError("raw code/data missing from PRG")
    return prg[offset:offset + count]


def check_load(prg, elf, result):
    origin = int.from_bytes(prg[:2], "little")
    if origin != 0x2001:
        raise ValueError("PRG initial load address changed")
    end = origin + len(prg) - 2
    sections = elf_sections(elf)
    copied = []
    for name, section in sections.items():
        address, size = section["address"], section["bytes"]
        if not origin <= address < address + size <= 0x9000:
            raise ValueError("allocation outside private resident contract: " + name)
        if section["type"] == 1:
            if image_bytes(prg, address, size) != section["data"]:
                raise ValueError("PRG payload differs from linked section: " + name)
            copied.append(name)
        elif section["type"] != 8:
            raise ValueError("unknown allocated section load semantics: " + name)
    runtime_end = max(s["address"] + s["bytes"] for s in sections.values())
    if runtime_end != result["resident_end"] or runtime_end - origin != result["resident_bytes"]:
        raise ValueError("complete resident accounting mismatch")
    # ELF .data may be empty and absent from this list; all file-backed bytes
    # through its end are the actual direct-PRG payload, including alignment.
    file_end = max(s["address"] + s["bytes"] for s in sections.values() if s["type"] == 1)
    if end != file_end:
        raise ValueError("PRG truncation or unexpected trailing payload")
    executable_above = sum(max(0, s["address"] + s["bytes"] - max(0x8000, s["address"]))
                           for s in sections.values() if s["flags"] & 4)
    return {"status": "PASS", "scope": "raw PRG/ELF load identity; not observed CPU execution",
            "origin": origin, "payload_end": end, "payload_bytes": len(prg) - 2,
            "payload_bytes_above_8000": max(0, end - 0x8000),
            "file_backed_sections_compared": copied, "resident_end": runtime_end,
            "executable_section_bytes_above_8000": executable_above,
            "loader_rule": "pinned Xemu inject.c copies PRG stream into main_ram + load_addr without an $8000 split",
            "BSS_and_scratch": "NOBITS; initialization separately verified, not loaded payload"}


def simulate_extension(prg, names, io=None):
    """Small independent decoder for the new boot fragment, not full CPU proof."""
    memory = bytearray([0xa5]) * 65536
    origin = int.from_bytes(prg[:2], "little")
    memory[origin:origin + len(prg) - 2] = prg[2:]
    registers = {0xd7fb: 2, 0xd7fd: 1, 0xd030: 0x44, 0: 0x2f, 1: 0x35}
    if io:
        registers.update(io)
    pc, a, y, b, zero = names["m2re_startup"], 0, 0, 2, False
    writes = set()
    for _ in range(200000):
        if pc == names["m2rb_early_stop"]:
            return {"terminal": True, "writes": writes}
        if pc == names["m2re_startup_done"]:
            return {"terminal": False, "writes": writes, "memory": memory, "base_page": b,
                    "registers": registers}
        opcode = image_bytes(prg, pc, 1)[0]
        size = 3 if opcode in {0xad, 0x8d, 0x4c} else 1 if opcode == 0x5b else 2
        raw = image_bytes(prg, pc, size)
        pc += size
        operand = int.from_bytes(raw[1:], "little")
        address = operand + b * 256 if opcode in {0xa5, 0x85, 0xe6} else operand
        if opcode in {0xa9, 0xa5, 0xad}:
            a = operand if opcode == 0xa9 else registers[address] if address in registers else memory[address]
            zero = a == 0
        elif opcode == 0x29:
            a &= operand; zero = a == 0
        elif opcode == 0xc9:
            zero = a == operand
        elif opcode == 0xa0:
            y = operand; zero = y == 0
        elif opcode == 0x5b:
            b = a
        elif opcode in {0x85, 0x8d, 0x91}:
            if opcode == 0x91:
                pointer = b * 256 + operand
                address = (int.from_bytes(memory[pointer:pointer + 2], "little") + y) & 65535
            if address in registers:
                registers[address] = a
            else:
                memory[address] = a; writes.add(address)
        elif opcode == 0xe6:
            memory[address] = (memory[address] + 1) & 255
            zero = memory[address] == 0; writes.add(address)
        elif opcode in {0xd0, 0xf0, 0x80}:
            if opcode == 0x80 or (opcode == 0xf0) == zero:
                pc = (pc + int.from_bytes(raw[1:], "little", signed=True)) & 65535
        elif opcode == 0x4c:
            pc = operand
        else:
            raise ValueError("unsupported startup opcode: " + hex(opcode))
    raise ValueError("startup decoder did not terminate within bound")


def check_initialization(prg, disassembly, symbol_text):
    instructions, names = parse(disassembly, symbol_text)
    branch_targets(instructions)
    start, end = names["__m2re_noinit_start"], names["__m2re_noinit_end"]
    bss, count = names["__bss_start"], names["__bss_size"]
    if not (names["__do_init_stack"] < names["m2re_startup"] < names["m2re_startup_done"]
            == names["__do_zero_bss"] < names["main"]):
        raise ValueError("startup/scratch/BSS order differs")
    if (names["__do_init_stack"] + 8 != names["m2re_startup"]
        or image_bytes(prg, names["__do_init_stack"], 8) != bytes.fromhex("a9 00 85 02 a9 d0 85 03")):
        raise ValueError("software SP initialization does not fall through into extension")
    callsite = bytes([0x20, names["__zero_bss"] & 255, names["__zero_bss"] >> 8,
                      0x20, names["main"] & 255, names["main"] >> 8])
    if image_bytes(prg, names["__do_zero_bss"], 6) != callsite:
        raise ValueError("BSS/main initialization callsite bypassed")
    cases = 0
    for cart in [0, 2, 255]:
        for forced in [0, 1, 0xc0, 0xc1, 255]:
            state = simulate_extension(prg, names, {0xd7fb: cart, 0xd7fd: forced})
            if state["terminal"] or state["base_page"] != 2:
                raise ValueError("canonical extension failed")
            if state["writes"] != set(range(start, end)) | {0x222, 0x223}:
                raise ValueError("scratch initialization wrote an unexpected byte")
            if any(state["memory"][start:end]):
                raise ValueError("compiler scratch not completely zeroed")
            if state["registers"][0xd7fb] & 2 or state["registers"][0xd7fd] != 0xc1:
                raise ValueError("cartridge lines not disabled")
            cases += 1
    for io in [{0xd030: 0x4c}, {0: 0}, {1: 0x37}]:
        state = simulate_extension(prg, names, io)
        if not state["terminal"] or state["writes"]:
            raise ValueError("bad visibility state reached dependent memory")
    # Prove the exact linked SDK zero-BSS arguments and tail helper, including
    # its zero-length check, 16-bit pointer/count and loop termination.
    memset = names["__memset"]
    expected = bytes([0xa2, count & 255, 0xa0, count >> 8, 0xa9, bss & 255,
                      0x85, 4, 0xa9, bss >> 8, 0x85, 5, 0xa9, 0, 0x84, 6,
                      0x4c, memset & 255, memset >> 8])
    if image_bytes(prg, names["__zero_bss"], len(expected)) != expected:
        raise ValueError("BSS clear arguments/helper changed")
    helper = bytes.fromhex("a4 06 d0 04 e0 00 f0 13 92 04 e3 04 ca e0 ff d0 02 c6 06 a4 06 d0 f1 e0 00 d0 ed 60")
    if image_bytes(prg, memset, len(helper)) != helper:
        raise ValueError("BSS zeroing helper changed; independent analysis required")
    # This loop mirrors only the documented machine count/pointer rule; it is
    # independent of C's object layouts and confirms every admitted BSS byte.
    pointer, remaining, written = bss, count, []
    while remaining:
        written.append(pointer); pointer = (pointer + 1) & 65535; remaining -= 1
    if written != list(range(bss, bss + count)) or bss + count != start:
        raise ValueError("BSS/scratch extent or wrap differs")
    return {"status": "PASS", "tier": "raw boot-fragment decoding/static helper proof",
            "scratch": [start, end], "scratch_zeroed": end - start,
            "BSS": [bss, bss + count], "BSS_zeroed": count,
            "cartridge_entry_cases": cases, "bad_port_ROM_cases_fail_closed": 3,
            "code_above_8000": "same canonical near-address policy; actual extent reported from ELF",
            "startup_overall": "UNPROVEN until exact fresh-entry, privileged trap and asynchronous execution qualification"}


def check_application_mapping(disassembly, symbol_text):
    instructions, names = parse(disassembly, symbol_text)
    prefix = names["m2rb_startup"]
    takeover = names["r0f_pf_enter"]
    maps = {at for at, (op, _, _) in instructions.items() if op == "map"}
    if maps != {prefix + 11, prefix + 17, takeover + 7}:
        raise ValueError("application MAP instruction outside canonical normalization")
    expected = [("sei", ""), ("cld", ""), ("lda", "#$0"), ("tax", ""),
                ("tay", ""), ("taz", ""), ("map", "")]
    actual = [i[:2] for at, i in sorted(instructions.items()) if takeover <= at <= takeover + 7]
    if actual != expected:
        raise ValueError("takeover MAP is not canonical zero")
    rom_stores = {at for at, (op, operand, _) in instructions.items()
                  if op in {"sta", "stx", "sty", "stz"} and operand == "$d030"}
    if rom_stores != {prefix + 46, takeover + 35}:
        raise ValueError("unexpected ROM-overlay write")
    # Validate the masking instruction too; clearing only ROM8 is insufficient
    # if another ROM overlay or CRAM2K displaces data/vectors/interrupt I/O.
    if instructions[takeover + 33][:2] != ("and", "#$46"):
        raise ValueError("takeover ROM-overlay mask changed")
    return {"status": "PASS", "tier": "application linked MAP/ROM writer exclusion",
            "canonical_MAP_sites": sorted(maps), "ROM_overlay_writer_sites": sorted(rom_stores),
            "temporary_application_MAP": "none; covering $8000-$9fff and all other windows forbidden",
            "staging": "actual retained physical-copy range validator tested separately; Graphics seam only names display/Color classes",
            "privileged_trap": "UNPROVEN execution: separate Hypervisor suspension/restore; no application window lease or bank-zero overwrite authorized",
            "physical_cartridge": "not qualified by Xemu; pinned primary VHDL contract only"}


def service_lower_bound(prg, disassembly, symbol_text, timings):
    instructions, names = parse(disassembly, symbol_text)
    branch_targets(instructions)
    # Pin the complete equal-byte loop, not source-line counts or assumptions
    # about how the compiler implements memcmp. The skipped DEX is excluded.
    start = names["memcmp"] + 9
    pattern = [0xb2, 0xd2, 0xd0, 0xe3, 0xe3, 0xa0, 0xc6, 0xc4, 0xd0,
               0x8a, 0xd0, 0xa5, 0xd0]
    at = start
    actual = []
    for index in range(len(pattern)):
        if index == 9:
            at += 1  # Count <256 never takes the DEX path.
        op, operand, raw = instructions[at]
        if raw[0] != pattern[index] or image_bytes(prg, at, len(raw)) != raw:
            raise ValueError("memcmp equality loop changed; no bound inferred")
        actual.append({"address": at, "opcode": raw[0], "minimum_cycles": timings[raw[0]]})
        at += len(raw)
    camera = names["m2_camera_same"]
    camera_end = min(a for a in names.values() if a > camera)
    camera_code = [i for a, i in sorted(instructions.items()) if camera <= a < camera_end]
    if sum(op == "jsr" and operand == "$" + format(names["memcmp"], "x")
           for op, operand, _ in camera_code) != 2:
        raise ValueError("camera comparison closure changed")
    if [(op, operand) for op, operand, _ in camera_code].count(("lda", "#$12")) != 1 \
       or [(op, operand) for op, operand, _ in camera_code].count(("lda", "#$4")) != 1:
        raise ValueError("camera comparison lengths changed")
    dispatch = names["m2rb_dispatch"]
    dispatch_end = min(a for a in names.values() if a > dispatch)
    calls = [a for a, (op, operand, _) in instructions.items()
             if dispatch <= a < dispatch_end and op == "jsr"
             and operand == "$" + format(camera, "x")]
    if len(calls) != 1:
        raise ValueError("dispatch camera-check path changed")
    cycles_per_byte = sum(item["minimum_cycles"] for item in actual)
    dispatches = 40 * 16 * 8
    bound = dispatches * 22 * cycles_per_byte
    allowance = 40500000 // 20
    return {"status": "FAIL" if bound > allowance else "UNPROVEN",
            "tier": "necessary lower-bound rejection only; not WCET or observed cadence",
            "operation": "unchanged-camera equality checks on mandatory BACKGROUND dispatches",
            "geometry_world_tiles": 40 * 16, "background_dispatches_per_tile": 8,
            "mandatory_background_dispatches": dispatches, "camera_bytes_per_dispatch": 22,
            "minimum_cycles_per_equal_byte": cycles_per_byte,
            "equality_loop_instructions": actual, "camera_check_call": calls[0],
            "minimum_frame_cycles": bound, "maximum_available_cycles_at_20hz": allowance,
            "minimum_frame_milliseconds": bound * 1000 / 40500000,
            "optimistic_maximum_hz": 40500000 / bound,
            "excluded_positive_costs": ["calls/returns/setup", "taken-branch surcharges", "painting",
                "geometry", "copies", "raster", "text", "clock/guard", "100Hz ticks", "IRQ/NMI"],
            "eight_dispatch_WCETs": ["UNPROVEN"] * 8,
            "launch_and_grants": "remain zero; no timing invented",
            "smallest_correction": "amortize checked camera/generation and dispatch control across bounded batches; preserve cancellation before publication and per-tick yields"}
