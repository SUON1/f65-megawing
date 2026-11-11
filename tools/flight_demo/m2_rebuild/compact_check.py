"""Required linked behavior closure, not obsolete implementation-name retention."""
import re

REQUIRED = ["m2rb_dispatch", "m2rb_camera_edges", "m2rb_platform_init", "m2rb_glyph",
            "m2c_prepare_service", "m2c_project_service", "m2c_horizon_service",
            "m2l_service", "m2rb_io_commit", "m1_tick", "m1_input_sample",
            "m1_acquire", "r0f_pf_flat_copy"]


def check(disassembly, symbols):
    addresses = {}
    for line in symbols.splitlines():
        match = re.match(r"^([0-9a-f]+)\s+(?:[0-9a-f]+\s+)?[a-zA-Z]\s+(\S+)$", line)
        if match:
            addresses[match[2]] = int(match[1], 16)
    missing = [name for name in ["main", *REQUIRED] if name not in addresses]
    if missing:
        raise ValueError("missing required implementation: " + ",".join(missing))
    forbidden = {"m2_prepare", "m2_transform", "m2_project_segment",
                 "m2_project_prepared", "m2_ground_prepared", "m2_ground_sample",
                 "m2_pair_eligible", "__muldi3", "__udivdi3"}
    if forbidden.intersection(addresses):
        raise ValueError("batch/native-wide implementation retained: "
                         + ",".join(sorted(forbidden.intersection(addresses))))
    # Use instruction addresses: assembler aliases need not be the displayed label.
    instructions = []
    for line in disassembly.splitlines():
        match = re.match(r"^\s*([0-9a-f]+):\s+((?:[0-9a-f]{2}\s+)+)\s*(\w+)(.*)$", line)
        if match:
            instructions.append((int(match[1], 16), len(match[2].split()), match[3], match[4]))
    by_address = {item[0]: item for item in instructions}
    pending = [addresses["main"]]
    visited = set()
    while pending:
        address = pending.pop()
        if address in visited or address not in by_address:
            continue
        visited.add(address)
        _, size, operation, operand = by_address[address]
        target = re.search(r"\$([0-9a-f]+)", operand)
        if operation in {"jsr", "jmp", "bra", "lbra"} or operation.startswith("b"):
            if target and not operand.lstrip().startswith("("):
                pending.append(int(target[1], 16))
        if operation not in {"rts", "rti", "jmp", "bra", "lbra"}:
            pending.append(address + size)
    unreachable = [name for name in REQUIRED if addresses[name] not in visited]
    if unreachable:
        raise ValueError("required implementation not reachable from main: " + ",".join(unreachable))
    return {"required_reachable": REQUIRED, "instruction_addresses": len(visited),
            "meaning": "static closure only; behavior by host/oracle; no timing/stack admission"}
