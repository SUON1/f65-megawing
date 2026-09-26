#!/usr/bin/env python3
"""Build and statically validate the T03 successor combined target image."""

import hashlib
import json
import pathlib
import re
import subprocess
import sys

import r0f_platform_build as platform_build
import r0f_successor_admission as admission


ROOT = platform_build.ROOT
OUT = ROOT / "build/r0f/successor-integration"
CONTRACT_PATH = ROOT / "interfaces/r0f_successor_integration_contract.json"
ADMISSION_PATH = ROOT / "interfaces/r0f_successor_contract.json"
LEDGER_PATH = ROOT / "memory/r0f-successor-integration-memory-ledger.json"
HEADER_PATH = ROOT / "interfaces/generated/r0f_successor_integration.h"
INCLUDE_PATH = ROOT / "interfaces/generated/r0f_successor_integration.inc"
PRG_PATH = OUT / "R0F-SUCCESSOR-INTEGRATION.prg"
COMMANDS = []


def run(arguments, **kwargs):
    command = list(map(str, arguments))
    COMMANDS.append(command)
    return subprocess.run(command, cwd=ROOT, check=True, **kwargs)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generated_files(contract):
    header = [
        "/* Generated from r0f_successor_integration_contract.json. */",
        "#ifndef R0FSI_GENERATED_H",
        "#define R0FSI_GENERATED_H",
        "",
    ]
    assembly = [
        "/* Generated from r0f_successor_integration_contract.json. */",
        "",
    ]
    for name, value in contract["constants"].items():
        header.append(f"#define R0FSI_{name} {value}u")
        assembly.append(f".equ R0FSI_{name}, {value}")
    for name, value in contract["resultOffsets"].items():
        header.append(f"#define R0FSI_O_{name} {value}u")
    for name, value in contract["serviceMask"].items():
        header.append(f"#define R0FSI_SERVICE_{name} {value}u")
    for name, value in contract["diagnosticFaults"].items():
        header.append(f"#define R0FSI_FAULT_{name} {value}u")
    header.extend(("", "#endif", ""))
    assembly.append("")
    return "\n".join(header), "\n".join(assembly)


def symbol(symbols, name):
    match = re.search(
        r"^([0-9a-f]+)\s+[A-Za-z]\s+" + re.escape(name) + r"$",
        symbols,
        re.M,
    )
    if not match:
        raise ValueError("missing symbol: " + name)
    return int(match.group(1), 16)


def section_inventory(map_text):
    sections = {}
    pattern = re.compile(
        r"^\s*([0-9a-f]+)\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+"
        r"(\.[A-Za-z0-9_.]+)$",
        re.M,
    )
    for start_text, bytes_text, name in pattern.findall(map_text):
        sections[name] = {
            "start": int(start_text, 16),
            "bytes": int(bytes_text, 16),
        }
    return sections


def validate_contract(contract, admitted, ledger):
    if contract["admissionContract"] != "interfaces/r0f_successor_contract.json":
        raise ValueError("T02 admission reference")
    if ledger["admissionLedger"] != "memory/r0f-successor-memory-ledger.json":
        raise ValueError("T02 ledger reference")
    if ledger["newPhysicalAllocations"]:
        raise ValueError("T03 added a physical allocation")
    if ledger["measuredReserve"]["successorBytes"] != 0:
        raise ValueError("measured reserve consumed")
    if ledger["resourceReserve"]["successorBytes"] != 0:
        raise ValueError("resource reserve consumed")
    constants = admitted["constants"]
    frozen = {
        "KERNAL_CONTEXT_ALLOCATION": 0x08020000,
        "KERNAL_CONTEXT_PAYLOAD": 0x08020010,
        "KERNAL_CONTEXT_ALLOCATION_BYTES": 5664,
        "RESIDENT_START": 0x2001,
        "RESIDENT_END_EXCLUSIVE": 0xC000,
        "SOFTWARE_STACK_START": 0xC000,
        "SOFTWARE_STACK_END_EXCLUSIVE": 0xD000,
        "MEASURED_RESERVE": 0x58000,
        "MEASURED_RESERVE_BYTES": 0x8000,
    }
    for name, value in frozen.items():
        if constants[name] != value:
            raise ValueError("frozen T02 constant: " + name)
    if contract["constants"]["PRE_STORAGE_TICKS"] != 33:
        raise ValueError("CF001 boundary tick")
    if contract["constants"]["POST_STORAGE_TICKS"] == 0:
        raise ValueError("missing post-storage continuation")
    expected_services = {"DISPLAY", "AUDIO", "INPUT", "IRQ", "DMA"}
    if set(contract["serviceMask"]) != expected_services:
        raise ValueError("resumed service inventory")
    if contract["resultOffsets"].get("NMI_STICKY") != 96:
        raise ValueError("sticky NMI result field")
    expected_faults = {
        "POST_STORAGE_TICK": 87,
        "FINAL_RESERVE": 95, "FINAL_LIFECYCLE": 96, "FINAL_NMI": 97,
        "FINAL_DISPLAY": 98, "FINAL_AUDIO": 99, "FINAL_INPUT": 100,
        "FINAL_IRQ": 101, "FINAL_DMA": 102, "FINAL_SERVICE_MASK": 103,
        "FINAL_TICK": 104,
    }
    if contract.get("diagnosticFaults") != expected_faults:
        raise ValueError("physical final-fault classification")
    admission.validate_contract(
        admitted,
        json.loads((ROOT / "memory/r0f-successor-memory-ledger.json").read_text()),
    )


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    contract = json.loads(CONTRACT_PATH.read_text())
    admitted = json.loads(ADMISSION_PATH.read_text())
    ledger = json.loads(LEDGER_PATH.read_text())
    validate_contract(contract, admitted, ledger)
    header, assembly = generated_files(contract)
    HEADER_PATH.write_text(header)
    INCLUDE_PATH.write_text(assembly)

    run([
        "/usr/bin/clang", "-std=c11", "-Wall", "-Wextra", "-Wconversion",
        "-Werror", "-fsanitize=address,undefined", "-Iinterfaces/generated",
        "-Isrc/diagnostics/r0f", "src/diagnostics/r0f/combined_model.c",
        "src/diagnostics/r0f/successor_lifecycle.c",
        "tools/diagnostics/r0f_successor_integration_host_test.c",
        "-o", OUT / "host-test",
    ])
    host_output = run([OUT / "host-test"], capture_output=True,
                      text=True).stdout
    (OUT / "host-test.txt").write_text(host_output)
    print(host_output, end="", flush=True)

    platform_build.pin(
        platform_build.JAVA / "java",
        "34b9c157bedcebafc6033b8beaa72c2ff14e2b697e33f45aa959a8373d6581a0",
    )
    platform_build.pin(
        platform_build.JAVA / "javac",
        "ee7be919e8bc4f364a1de24c245eea5ff8bb8f5560c8eb182ad3e89007adb152",
    )
    classes = OUT / "classes"
    classes.mkdir(exist_ok=True)
    oracle = "tools/generators/src/main/java/f65/tools/R0FSuccessorOracle.java"
    run([
        platform_build.JAVA / "javac", "-Xlint:all", "-Werror",
        "-d", classes, oracle,
    ])
    oracle_output = run([
        platform_build.JAVA / "java", "-cp", classes,
        "f65.tools.R0FSuccessorOracle", "--model",
    ], capture_output=True, text=True).stdout
    (OUT / "oracle.txt").write_text(oracle_output)
    print(oracle_output, end="", flush=True)

    # Rebuild both predecessors from current sources. These are regressions,
    # not promotions of their evidence tiers.
    run([sys.executable, "tools/diagnostics/r0f_combined_build.py", "build"])
    run([sys.executable, "tools/diagnostics/r0f_resume_build.py", "build"])

    platform_build.pin(
        platform_build.TOOLS / "mos-mega65-clang",
        "cc557ae99a68ed36e098062b0f5376a878e94ac187b87446c8e603e4fb45a906",
    )
    platform_build.pin(
        platform_build.TOOLS / "llvm-objdump",
        "5327f031a741bfcd4104317fbad3d1e45275d70b49821f0da52391120848a8e9",
    )
    sources = [
        "src/diagnostics/r0f/successor_integration.c",
        "src/diagnostics/r0f/successor_lifecycle.c",
        "src/diagnostics/r0f/combined_model.c",
        "src/diagnostics/r0f/combined_platform.c",
        "src/platform/r0f/successor_admission_45gs02.s",
        "src/platform/r0f/successor_integration_45gs02.s",
        "src/platform/r0f/combined_45gs02.s",
        "src/platform/r0f/qualification_45gs02.s",
        "src/platform/r0a_platform_45gs02.s",
    ]
    map_path = OUT / "R0F-SUCCESSOR-INTEGRATION.map"
    run([
        platform_build.TOOLS / "mos-mega65-clang", "-mcpu=mos45gs02",
        "-mlto-zp=0", "-Oz", "-fno-inline-functions", "-DR0FS_INTEGRATION",
        "-Wall", "-Wextra", "-Wconversion", "-Werror",
        "-Iinterfaces/generated", "-Isrc/diagnostics/r0f", *sources,
        "-Wl,-T,src/platform/r0f/startup.ld",
        "-Wl,-T,src/platform/r0f/successor_integration.ld",
        f"-Wl,-Map,{map_path}", "-o", PRG_PATH,
    ])
    elf_path = pathlib.Path(str(PRG_PATH) + ".elf")
    symbols_path = OUT / "R0F-SUCCESSOR-INTEGRATION.symbols"
    disassembly_path = OUT / "R0F-SUCCESSOR-INTEGRATION.disassembly"
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
    sections = section_inventory(mapping)
    resident_names = {
        ".basic_header", ".r0fs_protected", ".text", ".rodata",
        ".data", ".bss", ".noinit",
    }
    for name in resident_names:
        if name not in sections:
            raise ValueError("missing resident section: " + name)
        section = sections[name]
        if section["bytes"] and (
            section["start"] < admitted["constants"]["RESIDENT_START"]
            or section["start"] + section["bytes"]
            > admitted["constants"]["RESIDENT_END_EXCLUSIVE"]
        ):
            raise ValueError("resident envelope: " + name)
    intervals = sorted(
        (sections[name]["start"],
         sections[name]["start"] + sections[name]["bytes"], name)
        for name in resident_names if sections[name]["bytes"]
    )
    for (_, end, name), (next_start, _, next_name) in zip(intervals,
                                                          intervals[1:]):
        if end > next_start:
            raise ValueError(f"resident section overlap: {name}/{next_name}")
    resident_bytes = sum(end - start for start, end, _ in intervals)
    resident_capacity = (admitted["constants"]["RESIDENT_END_EXCLUSIVE"]
                         - admitted["constants"]["RESIDENT_START"])
    resident_end = max(end for _, end, _ in intervals)
    protected = sections[".r0fs_protected"]
    if protected["start"] + protected["bytes"] > 0x8000:
        raise ValueError("protected code/data hidden by MAP window")
    if "__stack = 0xd000" not in mapping:
        raise ValueError("software stack top")

    if not (symbol(symbols, "r0fs_pre_c_capture")
            < symbol(symbols, "f65_basepage_enter")
            < symbol(symbols, "__do_zero_bss")):
        raise ValueError("pre-C capture ordering")
    for name in (
        "r0fs_storage", "r0fs_storage_end", "r0fs_context_read",
        "r0fs_context_invalidate", "r0f_pf_enter", "r0fsi_context_buffer",
        "r0fsi_payload", "r0fsi_read", "r0fsi_token",
    ):
        address = symbol(symbols, name)
        if not (protected["start"] <= address
                < protected["start"] + protected["bytes"]):
            raise ValueError("transition symbol outside protected section: "
                             + name)
    capture = disassembly.split("<r0fs_pre_c_capture>:", 1)[1]
    capture = capture.split("<r0fs_pre_c_capture_end>:", 1)[0]
    if re.search(r"\b(?:jsr|map|eom)\b", capture):
        raise ValueError("pre-C capture callback/MAP use")
    storage = disassembly.split("<r0fs_storage>:", 1)[1]
    storage = storage.split("<r0fs_storage_end>:", 1)[0]
    assembly_source = (
        ROOT / "src/platform/r0f/successor_integration_45gs02.s"
    ).read_text()
    for required_token in (
        "R0FS_KERNAL_CONTEXT_PAYLOAD",
        "R0FS_APPLICATION_STACK_BACKUP",
        "R0FS_APPLICATION_BASE_PAGE_BACKUP",
        "r0f_pf_enter",
        "r0fsi_app_sp",
    ):
        if required_token not in assembly_source:
            raise ValueError("storage restoration source token: "
                             + required_token)
    context_source = assembly_source.split("r0fs_context_read:", 1)[1]
    context_source = context_source.split("r0fs_context_invalidate:", 1)[0]
    if not re.search(
            r"lda r0fsi_context_offset\+1\s+adc #0\s+"
            r"bcs \.Lcontext_read_exit\s+"
            r"cmp #>\(R0FS_KERNAL_CONTEXT_BYTES\)", context_source):
        raise ValueError("context mailbox high-byte carry rejection")
    allowed_rom = {
        0xFF87, 0xFF84, 0xFF8A, 0xFF81, 0xFFCC, 0xFF41,
        0xFF90, 0xFF6B, 0xFFBA, 0xFFBD, 0xFFD5, 0xFFD8,
    }
    seen_rom = set()
    for line in disassembly.splitlines():
        match = re.search(r"\b(?:jsr|jmp)\s+\$([ef][0-9a-f]{3})\b", line)
        if not match:
            continue
        address = int(match.group(1), 16)
        if line not in storage or address not in allowed_rom:
            raise ValueError("unadmitted ROM call: " + line)
        seen_rom.add(address)
    if seen_rom != allowed_rom:
        raise ValueError("missing checked storage operation")
    storage_start = symbol(symbols, "r0fs_storage")
    storage_end = symbol(symbols, "r0fs_storage_end")
    for pc_text, opcode in re.findall(
            r"^\s*([0-9a-f]+): ([0-9a-f]{2}) ", disassembly, re.M):
        pc = int(pc_text, 16)
        if (storage_start <= pc < storage_end
                and int(opcode, 16)
                in {0x13, 0x33, 0x53, 0x73, 0x83, 0x93, 0xB3, 0xD3, 0xF3}):
            raise ValueError("unadmitted long branch in storage wrapper")
    for address_text in re.findall(r"\$([89ab][0-9a-f]{3})\b", storage):
        raise ValueError("storage references MAP-hidden resident address: $"
                         + address_text)
    entry = disassembly.split("<r0f_pf_enter>:", 1)[1]
    entry = entry.split("<r0f_pf_start_irq>:", 1)[0]
    if not re.search(
            r"lda\s+#\$0\s*\n[^\n]*\btab\b\s*\n"
            r"[^\n]*lda\s+#\$35\s*\n[^\n]*sta\s+\$1\b", entry):
        raise ValueError("canonical B=0/CPU-port restoration")
    if not re.search(r"lda\s+#\$2\s*\n[^\n]*\btab\b", entry):
        raise ValueError("canonical B=2 restoration")
    irq_handler = disassembly.split("<r0f_pf_irq>:", 1)[1]
    irq_handler = irq_handler.split("<r0f_pf_nmi>:", 1)[0]
    if re.search(r"\b(?:jsr|map|eom)\b|\$d70[05]", irq_handler):
        raise ValueError("IRQ forbidden operation")
    for operation in (
            "pha", "phx", "phy", "phz", "pla", "plx", "ply", "plz",
            "tab", "rti"):
        if not re.search(r"\b" + operation + r"\b", irq_handler):
            raise ValueError("IRQ preservation sequence: " + operation)
    for register in range(32):
        if not re.search(rf"^000000{register + 2:02x} A __rc{register}$",
                         symbols, re.M):
            raise ValueError("compiler base-page ABI")
    target_source = (ROOT / sources[0]).read_text()
    if re.search(r"(?:cfcopy|fixed_physical_copy)\s*\([^\n]*"
                 r"R0FS_MEASURED_RESERVE[^\n]*,\s*1u\s*\)", target_source):
        raise ValueError("measured reserve write")
    if "r0fs_context_invalidate();" not in target_source:
        raise ValueError("missing Attic context invalidation")
    storage_source = target_source.split(
        "static uint8_t storage_transition(void)", 1)[1]
    storage_source = storage_source.split("int main(void)", 1)[0]
    ordered_boundary = [
        "display_drain()", "display_suspend()",
        "restore_rom_after_display_suspend()", "low_application_copy(1u)",
        "r0f_pf_enter()", "display_resume()", "if (!cfclock_begin())",
        "cfaudio_begin()", "next_deadline = cfnow()",
    ]
    positions = [storage_source.find(token) for token in ordered_boundary]
    if -1 in positions or positions != sorted(positions):
        raise ValueError("display/clock/audio resume ordering")
    if target_source.count("cfrom_restore()") != 1:
        raise ValueError("ROM restoration bypasses display-suspend gate")
    if ("application_dma_outstanding" not in target_source
            or "display_suspended_d011 & 0xefu" not in target_source):
        raise ValueError("display fetch/DMA suspension state")
    tick_source = target_source.split(
        "static uint8_t run_authoritative_tick(void)", 1)[1]
    tick_source = tick_source.split("static uint8_t run_ticks", 1)[0]
    if tick_source.count("r0f_pf_nmi_seen") < 3:
        raise ValueError("resumed authoritative-tick NMI lockout")
    if ("R0FSI_O_NMI_STICKY" not in target_source
            or "r0fs_completion_allowed(" not in target_source):
        raise ValueError("final sticky-NMI completion lockout")

    inputs = sources + [
        "interfaces/r0f_successor_contract.json",
        "interfaces/r0f_successor_integration_contract.json",
        "interfaces/generated/r0f_successor.h",
        "interfaces/generated/r0f_successor.inc",
        "interfaces/generated/r0f_successor_integration.h",
        "interfaces/generated/r0f_successor_integration.inc",
        "memory/r0f-successor-memory-ledger.json",
        "memory/r0f-successor-integration-memory-ledger.json",
        "src/diagnostics/r0f/combined_model.h",
        "src/diagnostics/r0f/combined_platform.h",
        "src/diagnostics/r0f/successor_lifecycle.h",
        "src/diagnostics/r0f/successor_lifecycle.c",
        "src/platform/r0f/startup.ld",
        "src/platform/r0f/successor_integration.ld",
        "tools/diagnostics/r0f_successor_integration.py",
        "tools/diagnostics/r0f_successor_integration_host_test.c",
        oracle,
    ]
    accounting = {
        "identity": contract["id"],
        "status": contract["status"],
        "sourceCommit": run(["git", "rev-parse", "HEAD"],
                            capture_output=True, text=True).stdout.strip(),
        "sourceState": "dirty review tree; per-input hashes authoritative",
        "inputs": {path: sha256(ROOT / path) for path in inputs},
        "prgSha256": sha256(PRG_PATH),
        "prgBytes": PRG_PATH.stat().st_size,
        "sections": sections,
        "actualResidentBytes": resident_bytes,
        "residentHighWaterExclusive": resident_end,
        "residentCapacityBytes": resident_capacity,
        "residentMarginBytes": resident_capacity - resident_bytes,
        "addressSpaceTailMarginBytes":
            admitted["constants"]["RESIDENT_END_EXCLUSIVE"] - resident_end,
        "protectedResidentBytes": protected["bytes"],
        "protectedResidentEndExclusive":
            protected["start"] + protected["bytes"],
        "atticTransitionBytes":
            admitted["constants"]["KERNAL_CONTEXT_ALLOCATION_BYTES"],
        "newPhysicalAllocations": [],
        "reserveBytes": 0,
        "predecessorRegression": {
            "cf001": "PASS",
            "rh001": "PASS",
            "cf001AccountingSha256": sha256(
                ROOT / "build/r0f/combined/accounting.json"),
            "rh001AccountingSha256": sha256(
                ROOT / "build/r0f/resume/accounting.json"),
        },
        "hostSanitizer": "PASS",
        "independentOracle": "PASS",
        "targetStatic": "PASS",
        "d81": "NOT RUN",
        "xemu": "NOT RUN",
        "sd": "NOT RUN",
        "physical": "NOT RUN",
        "fullAcceptance": False,
        "commands": COMMANDS,
    }
    (OUT / "accounting.json").write_text(
        json.dumps(accounting, indent=2) + "\n")
    print(json.dumps({
        "actualResidentBytes": resident_bytes,
        "residentCapacityBytes": resident_capacity,
        "residentMarginBytes": resident_capacity - resident_bytes,
        "residentHighWaterExclusive": f"0x{resident_end:04x}",
        "protectedResidentEndExclusive":
            f"0x{protected['start'] + protected['bytes']:04x}",
        "atticTransitionBytes":
            admitted["constants"]["KERNAL_CONTEXT_ALLOCATION_BYTES"],
        "reserveBytes": 0,
    }, indent=2), flush=True)
    print("R0-F successor T03 host/static integration PASS", flush=True)


if __name__ == "__main__":
    if sys.argv[1:] != ["build"]:
        raise SystemExit("usage: r0f_successor_integration.py build")
    build()
