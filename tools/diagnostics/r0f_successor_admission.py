#!/usr/bin/env python3
"""Build and validate the T02 successor memory/lifecycle static admission."""

import copy
import hashlib
import json
import pathlib
import re
import subprocess
import sys

import r0f_platform_build as platform_build


ROOT = platform_build.ROOT
OUT = ROOT / "build/r0f/successor-admission"
CONTRACT_PATH = ROOT / "interfaces/r0f_successor_contract.json"
LEDGER_PATH = ROOT / "memory/r0f-successor-memory-ledger.json"
HEADER_PATH = ROOT / "interfaces/generated/r0f_successor.h"
INCLUDE_PATH = ROOT / "interfaces/generated/r0f_successor.inc"
PRG_PATH = OUT / "R0F-SUCCESSOR-ADMISSION.prg"
COMMANDS = []


def run(arguments, **kwargs):
    command = list(map(str, arguments))
    COMMANDS.append(command)
    return subprocess.run(command, cwd=ROOT, check=True, **kwargs)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generated_files(contract):
    header = [
        "/* Generated from r0f_successor_contract.json. */",
        "#ifndef R0FS_GENERATED_H",
        "#define R0FS_GENERATED_H",
        "",
    ]
    assembly = [
        "/* Generated from r0f_successor_contract.json. */",
        "",
    ]
    for group, prefix in (("constants", ""), ("states", "S_"),
                          ("events", "E_")):
        for name, value in contract[group].items():
            header.append(f"#define R0FS_{prefix}{name} {value}ul")
            assembly.append(f".equ R0FS_{prefix}{name}, {value}")
    header.extend(("", "#endif", ""))
    assembly.append("")
    return "\n".join(header), "\n".join(assembly)


def parse_range(text):
    match = re.fullmatch(r"0x([0-9a-f]+)-0x([0-9a-f]+)", text)
    if not match:
        raise ValueError("invalid ledger range: " + text)
    start, end = (int(value, 16) for value in match.groups())
    if end < start:
        raise ValueError("reversed ledger range: " + text)
    return start, end + 1


def ranges_overlap(first, second):
    first_start, first_end = parse_range(first["range"])
    second_start, second_end = parse_range(second["range"])
    return max(first_start, second_start) < min(first_end, second_end)


def declaration_members(declaration):
    if declaration["relationship"] == "parent_subrange":
        return frozenset((declaration["parent"], declaration["child"]))
    if declaration["relationship"] == "lifetime_overlay":
        return frozenset(declaration["members"])
    raise ValueError("unknown overlap relationship: "
                     + declaration["relationship"])


def validate_overlap_model(ledger):
    nodes = ledger["envelopes"] + ledger["allocations"]
    by_id = {entry["id"]: entry for entry in nodes}
    if len(by_id) != len(nodes):
        raise ValueError("duplicate physical range id")

    declarations = {}
    for declaration in ledger["overlapDeclarations"]:
        members = declaration_members(declaration)
        if len(members) != 2 or not members.issubset(by_id):
            raise ValueError("overlap declaration members: "
                             + declaration["id"])
        if members in declarations:
            raise ValueError("duplicate overlap declaration: "
                             + declaration["id"])
        declarations[members] = declaration

    overlaps = set()
    for index, first in enumerate(nodes):
        for second in nodes[index + 1:]:
            if not ranges_overlap(first, second):
                continue
            members = frozenset((first["id"], second["id"]))
            overlaps.add(members)
            if members not in declarations:
                raise ValueError("undeclared overlap: "
                                 + "/".join(sorted(members)))

    for members, declaration in declarations.items():
        if members not in overlaps:
            raise ValueError("declared ranges do not overlap: "
                             + declaration["id"])
        if declaration["relationship"] == "parent_subrange":
            parent = by_id[declaration["parent"]]
            child = by_id[declaration["child"]]
            parent_start, parent_end = parse_range(parent["range"])
            child_start, child_end = parse_range(child["range"])
            if (parent not in ledger["envelopes"]
                    or child not in ledger["allocations"]
                    or child_start < parent_start or child_end > parent_end):
                raise ValueError("invalid parent/subrange: "
                                 + declaration["id"])
            continue

        first, second = (by_id[member] for member in declaration["members"])
        first_states = set(first["lifetimes"])
        second_states = set(second["lifetimes"])
        if first_states & second_states:
            raise ValueError("overlapping incompatible lifetimes: "
                             + declaration["id"])
        first_start, first_end = parse_range(first["range"])
        second_start, second_end = parse_range(second["range"])
        overlap_start = max(first_start, second_start)
        overlap_end = min(first_end, second_end)
        if (parse_range(declaration["range"])
                != (overlap_start, overlap_end)):
            raise ValueError("declared overlap range: " + declaration["id"])
        if declaration.get("exclusive") is not True:
            raise ValueError("lifetime overlay not exclusive: "
                             + declaration["id"])

    overlay = next((item for item in ledger["overlapDeclarations"]
                    if item["id"] == "dos-application-kernal-overlay"), None)
    if overlay is None:
        raise ValueError("required DOS/application lifetime overlay missing")
    application = by_id["active-simulation-dos-application"]
    kernal = by_id["dos-context"]
    if set(application["lifetimes"]) != set(overlay["applicationOwnerStates"]):
        raise ValueError("DOS overlay application lifetime declaration")
    if set(kernal["lifetimes"]) != set(overlay["kernalOwnerStates"]):
        raise ValueError("DOS overlay KERNAL lifetime declaration")
    required_kernal_states = {
        "KERNAL_ACTIVE", "STORAGE_COMPLETE", "KERNAL_CONTEXT_RESTORED",
    }
    if set(kernal["lifetimes"]) != required_kernal_states:
        raise ValueError("DOS overlay KERNAL owner states")
    state_index = {state: index
                   for index, state in enumerate(ledger["lifetimeOrder"])}
    if not (state_index[overlay["backupCompleteState"]]
            < min(state_index[state] for state in kernal["lifetimes"])
            <= max(state_index[state] for state in kernal["lifetimes"])
            < state_index[overlay["applicationRestoredState"]]
            < state_index[overlay["nextAuthoritativeState"]]):
        raise ValueError("DOS overlay lifecycle ordering")
    if (overlay["simulationAdvancesDuringKernalOwnership"] is not False
            or set(ledger["authoritativeSimulationAdvancesOnlyIn"])
            & set(kernal["lifetimes"])):
        raise ValueError("simulation advances during KERNAL ownership")
    if not {"WORKLOAD_ACTIVE", "SERVICES_RESUMED"}.issubset(
            application["lifetimes"]):
        raise ValueError("application missing active/resumed DOS ownership")


def validate_overlap_negative_cases(ledger):
    validate_overlap_model(ledger)
    cases = 0

    undeclared = copy.deepcopy(ledger)
    undeclared["allocations"].append({
        "id": "negative-undeclared",
        "range": "0x012000-0x012000",
        "bytes": 1,
        "owner": "negative fixture",
        "lifetimes": ["WORKLOAD_ACTIVE"],
    })
    try:
        validate_overlap_model(undeclared)
    except ValueError as error:
        if "undeclared overlap" not in str(error):
            raise
        cases += 1
    else:
        raise ValueError("negative undeclared overlap accepted")

    incompatible = copy.deepcopy(ledger)
    dos = next(entry for entry in incompatible["allocations"]
               if entry["id"] == "dos-context")
    dos["lifetimes"].append("WORKLOAD_ACTIVE")
    try:
        validate_overlap_model(incompatible)
    except ValueError as error:
        if "overlapping incompatible lifetimes" not in str(error):
            raise
        cases += 1
    else:
        raise ValueError("negative incompatible lifetime accepted")

    missing_exclusion = copy.deepcopy(ledger)
    missing_exclusion["overlapDeclarations"] = [
        declaration
        for declaration in missing_exclusion["overlapDeclarations"]
        if declaration["id"] != "dos-application-kernal-overlay"
    ]
    try:
        validate_overlap_model(missing_exclusion)
    except ValueError as error:
        if "undeclared overlap" not in str(error):
            raise
        cases += 1
    else:
        raise ValueError("negative missing DOS overlay exclusion accepted")

    return cases


def validate_contract(contract, ledger):
    constants = contract["constants"]
    context_start = constants["KERNAL_CONTEXT_ALLOCATION"]
    payload_start = constants["KERNAL_CONTEXT_PAYLOAD"]
    guard_bytes = constants["KERNAL_CONTEXT_GUARD_BYTES"]
    context_bytes = constants["KERNAL_CONTEXT_BYTES"]
    allocation_bytes = constants["KERNAL_CONTEXT_ALLOCATION_BYTES"]
    if payload_start != context_start + guard_bytes:
        raise ValueError("leading guard arithmetic")
    if allocation_bytes != context_bytes + 2 * guard_bytes:
        raise ValueError("guarded allocation arithmetic")
    if context_start < constants["ROM_BACKUP"] + constants["ROM_BACKUP_BYTES"]:
        raise ValueError("KERNAL context overlaps ROM backup")
    if constants["RESIDENT_END_EXCLUSIVE"] != constants["SOFTWARE_STACK_START"]:
        raise ValueError("resident/software-stack boundary")
    if constants["MEASURED_RESERVE"] != 0x58000:
        raise ValueError("measured reserve start")
    if constants["MEASURED_RESERVE_BYTES"] != 0x8000:
        raise ValueError("measured reserve bytes")
    if ledger["reserveBytes"] != 0 or ledger["newPublicOwnership"] != "none":
        raise ValueError("reserve or public ownership changed")
    protected = contract["protectedResidentRule"]
    if (protected["residentEnvelope"] != "0x002001-0x00bfff"
            or protected["temporaryMapWindow"] != "0x008000-0x00bfff"
            or protected["requiredWhileMapActiveMustRemainAccessible"]
            is not True
            or protected["ordinaryWorkloadMayUseFullResidentEnvelope"]
            is not True):
        raise ValueError("protected resident rule")

    allocations = {entry["id"]: entry for entry in ledger["allocations"]}
    required = {
        "resident", "hardware-stack", "software-stack", "base-page",
        "low-application", "active-simulation-dos-application",
        "active-simulation-remainder", "dos-context",
        "dos-application-backup",
        "rom-display-stores", "hud-assets", "low-application-backup",
        "application-stack-backup", "application-base-page-backup",
        "resource-staging-remainder", "pcm-cache",
        "kernal-dos-entry-backup", "dma-list", "resource-reserve",
        "measured-limits-reserve", "rom-backup",
        "kernal-context-guarded", "color-attributes",
    }
    if set(allocations) != required:
        raise ValueError("ledger allocation inventory")
    expected_order = [
        name for name, value in sorted(contract["states"].items(),
                                       key=lambda item: item[1])
    ]
    if ledger["lifetimeOrder"] != expected_order:
        raise ValueError("ledger lifecycle order")
    for entry in allocations.values():
        start, end = parse_range(entry["range"])
        if end - start != entry["bytes"]:
            raise ValueError("ledger byte count: " + entry["id"])
        if not set(entry["lifetimes"]).issubset(expected_order):
            raise ValueError("unknown allocation lifecycle state: "
                             + entry["id"])
    if ({entry["id"] for entry in ledger["envelopes"]}
            != {"active-simulation-envelope"}):
        raise ValueError("ledger envelope inventory")
    envelope = ledger["envelopes"][0]
    if parse_range(envelope["range"]) != (0x10000, 0x18000):
        raise ValueError("active-simulation envelope")
    if (parse_range(allocations["active-simulation-dos-application"]["range"])
            != (0x10000, 0x12000)
            or parse_range(
                allocations["active-simulation-remainder"]["range"])
            != (0x12000, 0x18000)):
        raise ValueError("active-simulation envelope partition")
    if (allocations["resident"]["temporaryMapWindow"]
            != "0x008000-0x00bfff"
            or allocations["resident"][
                "requiredWhileMapActiveMustRemainAccessible"] is not True
            or allocations["resident"][
                "ordinaryWorkloadMayUseFullResidentEnvelope"] is not True):
        raise ValueError("resident MAP accessibility rule")

    transition_ids = (
        "low-application-backup", "application-stack-backup",
        "application-base-page-backup", "kernal-dos-entry-backup",
    )
    transition_ranges = []
    for allocation_id in transition_ids:
        start, end = parse_range(allocations[allocation_id]["range"])
        if start < 0x50000 or end > 0x56000:
            raise ValueError("transition allocation outside staging/audio band")
        transition_ranges.append((start, end, allocation_id))
    for index, (start, end, allocation_id) in enumerate(transition_ranges):
        for other_start, other_end, other_id in transition_ranges[index + 1:]:
            if max(start, other_start) < min(end, other_end):
                raise ValueError(f"hidden overlap: {allocation_id}/{other_id}")

    reserve_start, reserve_end = parse_range(
        allocations["measured-limits-reserve"]["range"])
    for allocation_id, entry in allocations.items():
        if allocation_id == "measured-limits-reserve":
            continue
        start, end = parse_range(entry["range"])
        if max(start, reserve_start) < min(end, reserve_end):
            raise ValueError("measured reserve overlap: " + allocation_id)
    validate_overlap_model(ledger)
    if len(ledger["resourceLifetimeExclusions"]) != 3:
        raise ValueError("resource lifetime exclusion inventory")
    if contract["atticSnapshot"]["simulationAuthority"]:
        raise ValueError("Attic snapshot became simulation authority")


def map_sections(map_text):
    sections = {}
    pattern = re.compile(
        r"^\s*([0-9a-f]+)\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+"
        r"(\.[A-Za-z0-9_.]+)$", re.M)
    for start_text, bytes_text, name in pattern.findall(map_text):
        sections[name] = {
            "start": int(start_text, 16),
            "bytes": int(bytes_text, 16),
        }
    return sections


def symbol(symbols, name):
    match = re.search(r"^([0-9a-f]+)\s+[A-Za-z]\s+" + re.escape(name)
                      + r"$", symbols, re.M)
    if not match:
        raise ValueError("missing symbol: " + name)
    return int(match.group(1), 16)


def predecessor_accounting():
    run([sys.executable, "tools/diagnostics/r0f_combined_build.py", "build"])
    run([sys.executable, "tools/diagnostics/r0f_resume_build.py", "build"])
    combined = json.loads(
        (ROOT / "build/r0f/combined/accounting.json").read_text())
    resume = json.loads(
        (ROOT / "build/r0f/resume/accounting.json").read_text())
    resident_start = json.loads(CONTRACT_PATH.read_text())["constants"][
        "RESIDENT_START"]
    combined_bytes = sum(
        section["bytes"] for section in combined["sections"].values()
        if section["start"] >= resident_start)
    resume_bytes = sum(
        section["bytes"] for section in resume["sections"].values()
        if section["start"] >= resident_start)
    resume_without_resident_context = (
        resume_bytes
        - json.loads(CONTRACT_PATH.read_text())["constants"]
        ["KERNAL_CONTEXT_BYTES"])
    return {
        "cf001ResidentBytes": combined_bytes,
        "rh001ResidentBytesIncludingContext": resume_bytes,
        "rh001ConservativeResidentChargeWithoutContext":
            resume_without_resident_context,
        "method": (
            "CF001 complete resident linked charge plus RH001 complete resident "
            "linked charge minus only the 5632-byte context moved to Attic. "
            "This deliberately double-counts shared runtime/model/platform "
            "content."
        ),
        "combinedAccountingSha256": sha256(
            ROOT / "build/r0f/combined/accounting.json"),
        "resumeAccountingSha256": sha256(
            ROOT / "build/r0f/resume/accounting.json"),
    }


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    contract = json.loads(CONTRACT_PATH.read_text())
    ledger = json.loads(LEDGER_PATH.read_text())
    validate_contract(contract, ledger)
    overlap_negative_cases = validate_overlap_negative_cases(ledger)
    print("R0-F exhaustive overlap model PASS; "
          f"{overlap_negative_cases} negative cases rejected", flush=True)
    header, assembly_include = generated_files(contract)
    HEADER_PATH.write_text(header)
    INCLUDE_PATH.write_text(assembly_include)

    run([
        "/usr/bin/clang", "-std=c11", "-Wall", "-Wextra", "-Wconversion",
        "-Werror", "-fsanitize=address,undefined", "-Iinterfaces/generated",
        "-Isrc/diagnostics/r0f",
        "src/diagnostics/r0f/successor_lifecycle.c",
        "tools/diagnostics/r0f_successor_host_test.c", "-o",
        OUT / "host-test",
    ])
    host_result = run([OUT / "host-test"], capture_output=True,
                      text=True).stdout
    (OUT / "host-test.txt").write_text(host_result)
    print(host_result, end="", flush=True)

    platform_build.pin(
        platform_build.TOOLS / "mos-mega65-clang",
        "cc557ae99a68ed36e098062b0f5376a878e94ac187b87446c8e603e4fb45a906")
    platform_build.pin(
        platform_build.TOOLS / "llvm-objdump",
        "5327f031a741bfcd4104317fbad3d1e45275d70b49821f0da52391120848a8e9")
    sources = [
        "src/diagnostics/r0f/successor_admission.c",
        "src/diagnostics/r0f/successor_lifecycle.c",
        "src/platform/r0f/successor_admission_45gs02.s",
        "src/platform/r0f/qualification_45gs02.s",
        "src/platform/r0a_platform_45gs02.s",
    ]
    map_path = OUT / "R0F-SUCCESSOR-ADMISSION.map"
    run([
        platform_build.TOOLS / "mos-mega65-clang", "-mcpu=mos45gs02",
        "-mlto-zp=0", "-Oz", "-fno-inline-functions", "-Wall", "-Wextra",
        "-Wconversion", "-Werror", "-Iinterfaces/generated",
        "-Isrc/diagnostics/r0f", *sources,
        "-Wl,-T,src/platform/r0f/startup.ld",
        "-Wl,-T,src/platform/r0f/successor_admission.ld",
        f"-Wl,-Map,{map_path}", "-o", PRG_PATH,
    ])
    elf_path = pathlib.Path(str(PRG_PATH) + ".elf")
    symbols_path = OUT / "R0F-SUCCESSOR-ADMISSION.symbols"
    disassembly_path = OUT / "R0F-SUCCESSOR-ADMISSION.disassembly"
    symbols_path.write_bytes(run([
        platform_build.TOOLS / "llvm-nm", elf_path,
    ], capture_output=True).stdout)
    disassembly_path.write_bytes(run([
        platform_build.TOOLS / "llvm-objdump", "-d", "--print-imm-hex",
        elf_path,
    ], capture_output=True).stdout)

    mapping = map_path.read_text()
    symbols = symbols_path.read_text()
    disassembly = disassembly_path.read_text()
    sections = map_sections(mapping)
    linker = (ROOT / "src/platform/r0f/successor_admission.ld").read_text()
    for protected_input in (".text.r0fs_protected",
                            ".rodata.r0fs_protected",
                            ".data.r0fs_protected"):
        if protected_input not in linker:
            raise ValueError("protected linker input: " + protected_input)
    for section_name in (".basic_header", ".r0fs_protected", ".text",
                         ".data", ".bss", ".noinit"):
        if section_name not in sections:
            raise ValueError("missing linked section: " + section_name)
        section = sections[section_name]
        if section["bytes"] and (
                section["start"] < contract["constants"]["RESIDENT_START"]
                or section["start"] + section["bytes"]
                > contract["constants"]["RESIDENT_END_EXCLUSIVE"]):
            raise ValueError("resident range: " + section_name)
    protected = sections[".r0fs_protected"]
    if protected["start"] + protected["bytes"] > 0x8000:
        raise ValueError("protected code covered by MAP window")
    if "__stack = 0xd000" not in mapping:
        raise ValueError("software stack top")
    if not (symbol(symbols, "r0fs_pre_c_capture")
            < symbol(symbols, "f65_basepage_enter")
            < symbol(symbols, "__do_zero_bss")):
        raise ValueError("pre-C capture ordering")
    capture_start = symbol(symbols, "r0fs_pre_c_capture")
    capture_end = symbol(symbols, "r0fs_pre_c_capture_end")
    if capture_end <= capture_start:
        raise ValueError("empty capture wrapper")
    capture_disassembly = disassembly.split("<r0fs_pre_c_capture>:", 1)[1]
    capture_disassembly = capture_disassembly.split(
        "<r0fs_pre_c_capture_end>:", 1)[0]
    if "jsr" in capture_disassembly or "map" in capture_disassembly:
        raise ValueError("pre-C capture callback/MAP use")
    for operation in ("tab", "lda\t[$22],z", "sta\t[$26],z"):
        if operation not in capture_disassembly:
            raise ValueError("pre-C copy operation: " + operation)
    if ("lda\t#$a5" not in capture_disassembly
            or capture_disassembly.count("sta\t[$26],z") < 33):
        raise ValueError("pre-C guard initialization")
    canonical = disassembly.split("<r0fs_canonical_restore_marker>:", 1)[1]
    canonical = canonical.split("<r0fs_resume_marker>:", 1)[0]
    if "jsr" not in canonical or "<r0f_pf_enter>" not in canonical:
        raise ValueError("canonical restoration path")
    if re.search(r"\b(?:jsr|jmp)\s+\$[ef][0-9a-f]{3}\b", disassembly):
        raise ValueError("unadmitted ROM call")
    for register in range(32):
        if not re.search(rf"^000000{register + 2:02x} A __rc{register}$",
                         symbols, re.M):
            raise ValueError("compiler base-page ABI")

    predecessor = predecessor_accounting()
    wrapper_bytes = capture_end - capture_start + protected["bytes"]
    skeleton_bytes = sum(
        section["bytes"] for name, section in sections.items()
        if name in {".basic_header", ".r0fs_protected", ".text", ".rodata",
                    ".data", ".bss", ".noinit"})
    resident_capacity = (contract["constants"]["RESIDENT_END_EXCLUSIVE"]
                         - contract["constants"]["RESIDENT_START"])
    admitted_bytes = (predecessor["cf001ResidentBytes"]
                      + predecessor[
                          "rh001ConservativeResidentChargeWithoutContext"]
                      + skeleton_bytes)
    if admitted_bytes > resident_capacity:
        raise ValueError("conservative successor resident fit")

    inputs = [
        "interfaces/r0f_successor_contract.json",
        "interfaces/generated/r0f_successor.h",
        "interfaces/generated/r0f_successor.inc",
        "memory/r0f-successor-memory-ledger.json",
        "src/diagnostics/r0f/successor_admission.c",
        "src/diagnostics/r0f/successor_lifecycle.c",
        "src/diagnostics/r0f/successor_lifecycle.h",
        "src/platform/r0f/successor_admission_45gs02.s",
        "src/platform/r0f/successor_admission.ld",
        "src/platform/r0f/startup.ld",
        "tools/diagnostics/r0f_successor_admission.py",
        "tools/diagnostics/r0f_successor_host_test.c",
    ]
    accounting = {
        "identity": contract["id"],
        "status": contract["status"],
        "sourceCommit": run(["git", "rev-parse", "HEAD"],
                            capture_output=True, text=True).stdout.strip(),
        "sourceState": "dirty review tree; per-input hashes authoritative",
        "inputs": {path: sha256(ROOT / path) for path in inputs},
        "prgSha256": sha256(PRG_PATH),
        "sections": sections,
        "predecessorAccounting": predecessor,
        "atticWrapperBytes": wrapper_bytes,
        "admissionSkeletonResidentBytes": skeleton_bytes,
        "residentCapacityBytes": resident_capacity,
        "conservativeAdmittedResidentBytes": admitted_bytes,
        "residentMarginBytes": resident_capacity - admitted_bytes,
        "atticTransitionBytes":
            contract["constants"]["KERNAL_CONTEXT_ALLOCATION_BYTES"],
        "overlapNegativeCasesRejected": overlap_negative_cases,
        "reserveBytes": 0,
        "highLevelMemoryMapChange": False,
        "publicAbiChange": False,
        "timingOrStageOrderChange": False,
        "fullSuccessorWorkload": False,
        "xemu": "NOT RUN",
        "physical": "NOT RUN",
        "commands": COMMANDS,
    }
    (OUT / "accounting.json").write_text(
        json.dumps(accounting, indent=2) + "\n")
    print(json.dumps({
        "residentCapacityBytes": resident_capacity,
        "conservativeAdmittedResidentBytes": admitted_bytes,
        "residentMarginBytes": resident_capacity - admitted_bytes,
        "atticTransitionBytes":
            contract["constants"]["KERNAL_CONTEXT_ALLOCATION_BYTES"],
        "reserveBytes": 0,
    }, indent=2), flush=True)
    print("R0-F successor static admission PASS", flush=True)


if __name__ == "__main__":
    if sys.argv[1:] != ["build"]:
        raise SystemExit("usage: r0f_successor_admission.py build")
    build()
