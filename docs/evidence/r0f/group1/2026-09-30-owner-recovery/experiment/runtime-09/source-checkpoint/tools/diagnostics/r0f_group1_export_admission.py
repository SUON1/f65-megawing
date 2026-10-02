#!/usr/bin/env python3
"""Generate private export bindings and validate the delta ownership ledger."""

import copy
import json
from pathlib import Path

import r0f_successor_admission as successor


ROOT = successor.ROOT
CONTRACT = ROOT / "interfaces/r0f_group1_export_contract.json"
LEDGER = ROOT / "memory/r0f-group1-export-memory-ledger.json"


def validate(contract, delta, base):
    constants = contract["constants"]
    if delta["contract"] != str(CONTRACT.relative_to(ROOT)):
        raise ValueError("export contract authority")
    original = json.loads((ROOT / contract["predecessor"]).read_text())
    inherited = original["constants"]
    if (constants["CONTEXT_BYTES"] != inherited["KERNAL_CONTEXT_BYTES"]
            or constants["GUARD_BYTES"] != inherited["KERNAL_CONTEXT_GUARD_BYTES"]
            or constants["GUARD_VALUE"] != inherited["KERNAL_CONTEXT_GUARD"]):
        raise ValueError("opaque context shape differs from predecessor")
    if (constants["CAPSULE_BYTES"] != constants["CONTEXT_BYTES"]
            + 2 * constants["GUARD_BYTES"]
            or constants["CAPSULE_PAYLOAD"] != constants["CAPSULE_START"]
            + constants["GUARD_BYTES"]):
        raise ValueError("capsule guards and payload")
    # These are constraints of the admitted byte-copy and SAVE implementation,
    # not alternative layout authority. Reject unsupported contract edits here.
    if (constants["CONTEXT_BYTES"] % 256
            or not 256 <= constants["CONTEXT_BYTES"] <= 65280
            or constants["CAPSULE_BYTES"] % 256 == 0
            or constants["TRACE_START"] % 256
            or constants["STAGING_START"] % 256
            or constants["STAGING_BYTES"] % 256
            or not 256 <= constants["STAGING_BYTES"] <= 32768
            or constants["TRACE_CAPACITY"] % 65536
            or not 65536 <= constants["TRACE_CAPACITY"] <= 20 * constants["STAGING_BYTES"]
            or not 1 <= constants["COPY_CHUNK_BYTES"] <= 255):
        raise ValueError("unsupported terminal copy geometry")
    if delta["resourceReserveBytes"] or delta["measuredReserveBytes"]:
        raise ValueError("reserve consumption")
    merged = copy.deepcopy(base)
    if "TERMINAL_EXPORT" in merged["lifetimeOrder"]:
        raise ValueError("terminal state already defined")
    merged["lifetimeOrder"].append("TERMINAL_EXPORT")
    # Terminal execution retains only this admitted low resident envelope.
    # The rest of the old resident allocation is dead and may become staging.
    protected_start = inherited["RESIDENT_START"]
    protected_end = constants["STAGING_START"]
    if protected_end <= protected_start:
        raise ValueError("empty protected terminal envelope")
    merged["allocations"].append({
        "id": "group1-terminal-resident",
        "range": f"0x{protected_start:08x}-0x{protected_end - 1:08x}",
        "bytes": protected_end - protected_start,
        "owner": "private terminal exporter code and data",
        "lifetimes": ["TERMINAL_EXPORT"],
        "simulationAuthority": False,
    })
    merged["overlapDeclarations"].append({
        "id": "resident/group1-terminal-resident",
        "relationship": "lifetime_overlay",
        "members": ["resident", "group1-terminal-resident"],
        "range": f"0x{protected_start:08x}-0x{protected_end - 1:08x}",
        "exclusive": True,
    })
    for name, lifetimes in delta.get("extendLifetimes", {}).items():
        if name != "kernal-dos-entry-backup":
            raise ValueError("unadmitted lifetime extension")
        node = next(entry for entry in merged["allocations"] if entry["id"] == name)
        for lifetime in lifetimes:
            if lifetime not in ("SERVICES_RESUMED", "TERMINAL_EXPORT"):
                raise ValueError("unadmitted export lifetime")
            if lifetime not in node["lifetimes"]:
                node["lifetimes"].append(lifetime)
    for allocation in delta["allocations"]:
        node = dict(allocation)
        start = constants[node.pop("startConstant")]
        length = constants[node.pop("bytesConstant")]
        if length <= 0 or start + length > 0x10000000:
            raise ValueError("physical extent")
        node["range"] = f"0x{start:08x}-0x{start + length - 1:08x}"
        node["bytes"] = length
        if node["simulationAuthority"]:
            raise ValueError("export memory cannot be simulation authority")
        if node["id"] != "group1-terminal-staging":
            if start < 0x08000000 or start + length > 0x08800000:
                raise ValueError("diagnostic allocation outside Attic")
        else:
            if start < 0x2001 or start + length > 0x8000:
                raise ValueError("terminal staging must remain KERNAL-visible")
            if node["lifetimes"] != ["TERMINAL_EXPORT"]:
                raise ValueError("terminal overlay active during workload")
        merged["allocations"].append(node)
    nodes = {entry["id"]: entry for entry in merged["allocations"]}
    for overlay in delta["overlays"]:
        first, second = (nodes[overlay[key]] for key in ("first", "second"))
        first_start, first_end = successor.parse_range(first["range"])
        second_start, second_end = successor.parse_range(second["range"])
        start, end = max(first_start, second_start), min(first_end, second_end)
        merged["overlapDeclarations"].append({
            "id": first["id"] + "/" + second["id"],
            "relationship": "lifetime_overlay",
            "members": [first["id"], second["id"]],
            "range": f"0x{start:08x}-0x{end - 1:08x}",
            "exclusive": True,
        })
    successor.validate_overlap_model(merged)
    return merged


def bindings(contract):
    header = ["/* Generated by r0f_group1_export_admission.py. */",
              "#ifndef R0FG1X_GENERATED_H", "#define R0FG1X_GENERATED_H"]
    assembly = ["/* Generated by r0f_group1_export_admission.py. */"]
    for group, prefix in (("constants", ""), ("states", "S_")):
        for name, value in contract[group].items():
            header.append(f"#define R0FG1X_{prefix}{name} {value}ul")
            assembly.append(f".equ R0FG1X_{prefix}{name}, {value}")
    return "\n".join(header + ["#endif", ""]), "\n".join(assembly + [""])


def main():
    contract, delta = json.loads(CONTRACT.read_text()), json.loads(LEDGER.read_text())
    base = json.loads((ROOT / delta["baseLedger"]).read_text())
    merged = validate(contract, delta, base)
    header, assembly = bindings(contract)
    (ROOT / "interfaces/generated/r0f_group1_export.h").write_text(header)
    (ROOT / "interfaces/generated/r0f_group1_export.inc").write_text(assembly)
    out = ROOT / "build/r0f/group1"
    out.mkdir(parents=True, exist_ok=True)
    (out / "export-resolved-memory-ledger.json").write_text(
        json.dumps(merged, indent=2) + "\n")
    print("Group 1 export bindings and lifetime/overlap admission PASS")


if __name__ == "__main__":
    main()
