"""Independent linked prefix/terminal-byte checks, not asynchronous/runtime proof."""
import re


def symbols(symbol_text):
    names = {}
    for line in symbol_text.splitlines():
        match = re.match(r"^([0-9a-f]+)\s+(?:[0-9a-f]+\s+)?[A-Za-z]\s+(\S+)$", line)
        if match:
            names[match[2]] = int(match[1], 16)
    return names


def check_normal_prefix(disassembly, symbol_text):
    """Check only the straight-line prefix, including historical unsafe links."""
    names = symbols(symbol_text)
    instructions = {}
    for line in disassembly.splitlines():
        match = re.match(r"^\s*([0-9a-f]+):\s+(?:[0-9a-f]{2} )+\s*(\w+)\s*(.*)$", line)
        if match:
            operand = match[3].split(";")[0].split(" <")[0].strip()
            operand = re.sub(r"\$0+([0-9a-f])", r"$\1", operand)
            instructions[int(match[1], 16)] = (match[2], operand)
    start = names["m2rb_startup"]
    if names["_start"] != start:
        raise ValueError("normal entry bypasses startup prefix")
    normalized = names["m2rb_normalized"]
    actual = [value for address, value in sorted(instructions.items()) if start <= address < normalized]
    # LLVM's disassembler can print EOM's $EA encoding as NOP.
    expected = [("sei", ""), ("cld", ""), ("lda", "#$0"), ("tab", ""),
                ("ldy", "#$0"), ("ldx", "#$f"), ("ldz", "#$f"), ("map", ""),
                ("lda", "#$0"), ("tax", ""), ("tay", ""), ("taz", ""), ("map", "")]
    if len(actual) < 14 or actual[:13] != expected or actual[13][0] not in {"eom", "nop"}:
        raise ValueError("canonical megabyte/MAP prefix differs")
    if actual[14:23] != [("see", ""), ("ldy", "#$1"), ("tys", ""),
                        ("ldx", "#$ff"), ("txs", ""), ("lda", "#$2f"),
                        ("sta", "$0"), ("lda", "#$35"), ("sta", "$1")]:
        raise ValueError("stack/CPU-port normalization differs")
    handler = names["m2rb_early_stop"]
    middle = [("lda", "#$47"), ("sta", "$d02f"),
              ("lda", "#$53"), ("sta", "$d02f"),
              ("lda", "#$44"), ("sta", "$d030"),
              ("lda", "#$7f"), ("sta", "$dc0d"), ("sta", "$dd0d"),
              ("lda", "$dc0d"), ("lda", "$dd0d"),
              ("lda", "#$0"), ("sta", "$d01a"), ("sta", "$d713"),
              ("lda", "#$f"), ("sta", "$d019"),
              ("lda", "#$" + format(handler & 255, "x")),
              ("sta", "$fffa"), ("sta", "$fffe"),
              ("lda", "#$" + format(handler >> 8, "x")),
              ("sta", "$fffb"), ("sta", "$ffff")]
    if len(actual) != 48 or actual[23:45] != middle:
        raise ValueError("I/O, interrupt or vector initialization differs")
    required_stores = {"$d02f", "$d030", "$dc0d", "$dd0d", "$d01a", "$d713",
                       "$d019", "$fffa", "$fffb", "$fffe", "$ffff", "$0", "$1"}
    stores = {operand for op, operand in actual if op == "sta"}
    if stores != required_stores:
        raise ValueError("unexpected dependent store before normalization")
    if any(op in {"jsr", "jmp", "bra", "pha", "php", "phx", "phy", "phz"}
           or op.startswith("b") for op, _ in actual):
        raise ValueError("early prefix contains control flow or stack access")
    if actual[-3:] != [("lda", "#$2"), ("tab", ""), ("ldz", "#$0")]:
        raise ValueError("canonical B/Z not established")
    for name in ["__do_init_stack", "__zero_bss", "main"]:
        if names[name] < normalized:
            raise ValueError(name + " precedes normalization")
    # The C startup call must occur after the prefix; calls into BSS helpers from
    # an earlier PC are rejected even if helper placement itself is later.
    for address, (op, _) in instructions.items():
        if start <= address < normalized and op == "jsr":
            raise ValueError("initialization called before normalization")
    return {"normal_entry_ordering": "PASS", "start": start, "normalized": normalized,
            "pre_normalization_instructions": len(actual),
            "scope": "linked straight-line reset-entry prefix only",
            "runtime_startup_admission": "UNPROVEN; no inherited-entry/async NMI/ROM-trap execution proof"}


def check(disassembly, symbol_text, prg_bytes=None):
    """Require an exact stack-free terminal loop in the raw linked PRG bytes."""
    result = check_normal_prefix(disassembly, symbol_text)
    if prg_bytes is None:
        raise ValueError("raw PRG bytes required for terminal-handler control-flow check")
    if len(prg_bytes) < 2:
        raise ValueError("PRG load address missing")
    handler = symbols(symbol_text)["m2rb_early_stop"]
    load_address = int.from_bytes(prg_bytes[:2], "little")
    offset = handler - load_address + 2
    if not 0 <= handler <= 0xffff or offset < 2 or offset + 4 > len(prg_bytes):
        raise ValueError("linked terminal-handler bytes missing from PRG")
    code = prg_bytes[offset:offset + 4]
    # A closed SEI/JMP loop has no return, fallthrough, dependent data access,
    # or stack operation. Decode its absolute operand directly: disassembler
    # label annotations can conceal a branch into the preceding instruction.
    if code[:2] != b"\x78\x4c":
        raise ValueError("early terminal handler is not SEI + absolute JMP: " + code.hex())
    target = int.from_bytes(code[2:4], "little")
    if target != handler:
        raise ValueError("early terminal JMP target $" + format(target, "04x")
                         + " differs from handler $" + format(handler, "04x"))
    result.update(terminal_handler_control_flow="PASS", terminal_handler=handler,
                  terminal_handler_bytes=code.hex(), terminal_handler_target=target,
                  scope="linked reset-entry prefix and raw terminal-handler closure only")
    return result
