"""Fail-closed linked whole-program stack analysis; no target execution.

Unlike the historical PR1 probe, use the complete nm alias table, distinguish
nonreturning paths, and analyze both interrupt handlers. Every direct branch
successor is checked. Software SP writes require an exact constant-adjustment
idiom; unknown transfers/instructions/stack writes never become zero cost.
"""
import re

BRANCHES = set("bcc bcs beq bne bmi bpl bvc bvs".split())
PUSHES = set("pha phx phy phz php".split())
PULLS = set("pla plx ply plz plp".split())
ORDINARY = set("""adc and asl bit clc cld cli clv cmp cpx cpy dec dew dex dey
    eor inc inw inx iny inz lda ldx ldy ldz lsr nop ora rol ror sbc sec sei
    sta stx sty stz tab tax tay taz tba tsx tsy txa tya map""".split())
WRITES = set("sta stx sty stz inc dec inw dew asl lsr rol ror".split())


def parse(disassembly, symbols):
    instructions = {}
    for line in disassembly.splitlines():
        match = re.match(r"^\s*([0-9a-f]+):\s+((?:[0-9a-f]{2} )+)\s*(\w+)\s*(.*)$", line)
        if match:
            address = int(match[1], 16)
            raw = bytes.fromhex(match[2])
            operand = match[4].split(";")[0].split(" <")[0].strip()
            operand = re.sub(r"\$0+([0-9a-f])", r"$\1", operand)
            if address in instructions:
                raise ValueError("duplicate instruction address")
            instructions[address] = (match[3], operand, raw)
    names = {}
    for line in symbols.splitlines():
        match = re.match(r"^([0-9a-f]+)\s+(?:[0-9a-f]+\s+)?[A-Za-z]\s+(\S+)$", line)
        if match:
            names[match[2]] = int(match[1], 16)
    return instructions, names


def branch_targets(instructions):
    """Decode raw 45GS02 offsets, never trust a symbolic label annotation."""
    for at, (op, operand, raw) in instructions.items():
        if op not in BRANCHES | {"bra", "jmp", "jsr"}:
            continue
        match = re.fullmatch(r"\$([0-9a-f]+)", operand)
        if not match:
            raise ValueError("indirect/unknown transfer at " + hex(at))
        displayed = int(match[1], 16)
        if op in {"jmp", "jsr"}:
            if raw[0] != (0x4c if op == "jmp" else 0x20) or len(raw) != 3:
                raise ValueError("unsupported transfer encoding")
            actual = int.from_bytes(raw[1:], "little")
        elif len(raw) in {2, 3}:
            # Both forms use opcode-address+2; long branches do NOT use PC+3.
            actual = (at + 2 + int.from_bytes(raw[1:], "little", signed=True)) & 0xffff
        else:
            raise ValueError("unsupported relative-branch encoding")
        if actual != displayed:
            raise ValueError("raw branch/disassembly disagreement at " + hex(at))
        if actual not in instructions:
            raise ValueError("branch is not an instruction boundary: " + hex(actual))


def stack_effects(instructions, names):
    ordered = sorted(instructions)
    effect = {}
    admitted = set()
    protected_interiors = set()
    for index, address in enumerate(ordered):
        window = ordered[index:index + 7]
        if len(window) != 7:
            continue
        if any(a + len(instructions[a][2]) != b for a, b in zip(window, window[1:])):
            continue
        ops = [instructions[a][:2] for a in window]
        if (ops[0] == ("clc", "") and ops[1] == ("lda", "$2")
            and ops[3] == ("sta", "$2") and ops[4] == ("lda", "$3")
            and ops[6] == ("sta", "$3") and ops[2][0] == ops[5][0] == "adc"):
            lo = re.fullmatch(r"#\$([0-9a-f]{1,2})", ops[2][1])
            hi = re.fullmatch(r"#\$([0-9a-f]{1,2})", ops[5][1])
            if lo and hi:
                delta = int(lo[1], 16) + 256 * int(hi[1], 16)
                if delta >= 32768:
                    delta -= 65536
                effect[window[-1]] = -delta
                admitted.update((window[3], window[-1]))
                protected_interiors.update(window[1:])
    init = names.get("__do_init_stack")
    if init is not None:
        addresses = []
        at = init
        for _ in range(4):
            addresses.append(at)
            at += len(instructions[at][2])
        if [instructions[a][:2] for a in addresses] != [
                ("lda", "#$0"), ("sta", "$2"), ("lda", "#$d0"), ("sta", "$3")]:
            raise ValueError("software SP initialization changed")
        admitted.update((addresses[1], addresses[3]))
        protected_interiors.update(addresses[1:])
    for at, (op, operand, _) in instructions.items():
        if op in BRANCHES | {"jmp", "bra", "jsr"}:
            target = re.fullmatch(r"\$([0-9a-f]+)", operand)
            if target and int(target[1], 16) in protected_interiors:
                raise ValueError("control flow enters a partial software SP adjustment at " + hex(at))
    writes = {a for a, (op, operand, _) in instructions.items()
              if op in WRITES and re.match(r"^\$[23](?:$|,)", operand)}
    if writes != admitted:
        raise ValueError("unaccounted software SP writes: " + ",".join(hex(a) for a in sorted(writes ^ admitted)))
    return effect


def handler_effects(instructions, reachable):
    for at in reachable:
        op, operand, _ = instructions[at]
        if op == "map":
            raise ValueError("interrupt MAP is forbidden")
        absolute = re.match(r"^\$([0-9a-f]{3,4})(?:$|,)", operand)
        if op in WRITES and absolute and 0xd640 <= int(absolute[1], 16) <= 0xd67f:
            raise ValueError("interrupt trap is forbidden")
        if not operand.startswith("#") and re.search(r"\$[0-9a-f]{1,2}(?![0-9a-f])", operand):
            raise ValueError("interrupt accesses compiler direct page")


class Graph:
    def __init__(self, instructions, effects=None):
        self.instructions = instructions
        self.effects = effects or {}
        self.cache = {}
        self.reachable = set()
        self.call_edges = set()

    def walk(self, entry, mode="call", ancestors=frozenset()):
        key = (entry, mode)
        if key in self.cache:
            return self.cache[key]
        if key in ancestors:
            raise ValueError("recursive call graph at " + hex(entry))
        pending = [(entry, 0, 0)]
        depths = {}
        peak_hardware = peak_software = 0
        returns = False
        while pending:
            at, hardware, software = pending.pop()
            if at in depths:
                if depths[at] != (hardware, software):
                    raise ValueError("unequal stack join at " + hex(at))
                continue
            if at not in self.instructions:
                raise ValueError("transfer/fallthrough outside decoded code: " + hex(at))
            depths[at] = (hardware, software)
            self.reachable.add(at)
            op, operand, raw = self.instructions[at]
            allowed = ORDINARY | BRANCHES | PUSHES | PULLS | {"rts", "rti", "jmp", "bra", "jsr"}
            if op not in allowed:
                raise ValueError("unsupported instruction at " + hex(at) + ": " + op)
            software += self.effects.get(at, 0)
            hardware += (1 if op in PUSHES else -1 if op in PULLS else 0)
            if min(hardware, software) < 0:
                raise ValueError("stack underflow at " + hex(at))
            peak_hardware = max(peak_hardware, hardware)
            peak_software = max(peak_software, software)
            if op in {"rts", "rti"}:
                if (op == "rti") != (mode == "interrupt"):
                    raise ValueError("incorrect return domain at " + hex(at))
                if hardware or software:
                    raise ValueError("unbalanced return at " + hex(at))
                returns = True
                continue
            if op in BRANCHES | {"jmp", "bra", "jsr"}:
                match = re.fullmatch(r"\$([0-9a-f]+)", operand)
                if not match:
                    raise ValueError("indirect/unknown transfer at " + hex(at))
                destination = int(match[1], 16)
                if op == "jsr":
                    self.call_edges.add((at, destination))
                    callee = self.walk(destination, ancestors=ancestors | {key})
                    peak_hardware = max(peak_hardware, hardware + 2 + callee[0])
                    peak_software = max(peak_software, software + callee[1])
                    if not callee[2]:
                        continue
                else:
                    pending.append((destination, hardware, software))
                    if op in {"jmp", "bra"}:
                        continue
            pending.append((at + len(raw), hardware, software))
        result = (peak_hardware, peak_software, returns)
        self.cache[key] = result
        return result


def check(disassembly, symbols):
    instructions, names = parse(disassembly, symbols)
    branch_targets(instructions)
    effects = stack_effects(instructions, names)
    graph = Graph(instructions, effects)
    # Prefix stack reset/MAP state is checked independently before this root.
    main = graph.walk(names["__do_init_stack"])
    irq = graph.walk(names["r0f_pf_irq"], mode="interrupt")
    nmi = graph.walk(names["r0f_pf_nmi"], mode="interrupt")
    # 45GS02 hardware interrupt frame is PC16 + P8. A single edge-triggered NMI
    # may preempt the IRQ; external repeated nested NMI is not an admitted input.
    interrupt_hardware = 3 + irq[0] + 3 + nmi[0]
    hardware = main[0] + interrupt_hardware
    software = main[1] + max(irq[1], nmi[1])
    if hardware >= 256 or software > 4096:
        raise ValueError("whole-program stack envelope exceeded")
    # Handlers may not share compiler BP/scratch or perform calls, MAP or traps.
    handlers = Graph(instructions)
    handlers.walk(names["r0f_pf_irq"], mode="interrupt")
    handlers.walk(names["r0f_pf_nmi"], mode="interrupt")
    if handlers.call_edges:
        raise ValueError("interrupt C/helper calls require independent scratch accounting")
    handler_effects(instructions, handlers.reachable)
    return {"status": "PASS", "tier": "static application stack proof",
            "root": "__do_init_stack (including BSS/startup, application and all reachable compiler helpers)",
            "main_hardware_peak": main[0], "irq_frame_and_saves": 3 + irq[0],
            "nmi_frame_and_saves": 3 + nmi[0], "hardware_bound": hardware,
            "software_bound": software, "hardware_capacity": 256, "software_capacity": 4096,
            "constant_software_adjustments": len(effects), "call_entries": len(graph.cache),
            "reachable_instructions": len(graph.reachable),
            "software_initialization_alias": names["__do_init_stack"],
            "interrupt_compiler_scratch": "none; no direct-page accesses or calls",
            "privileged_trap_sites": [at for at in sorted(graph.reachable)
                if instructions[at][:2] == ("sta", "$d640")],
            "whole_program_status": "UNPROVEN: exact Hypervisor internal stack/restoration and entry/NMI conditions require separate closure",
            "conditions": ["canonical prefix establishes E=1/page1 hardware stack before root",
                "one nonrecursive external NMI edge may preempt IRQ; repeated nested external NMI is excluded",
                "CF001 Hypervisor trap uses its separate protected stack; exact trap restoration required"],
            "limitations": "No exercised high-water or arbitrary physical NMI-rate claim; Hypervisor internal stack is a separate gate"}
