#!/usr/bin/env python3
"""R0-F T04 successor emulator and exact-carrier evidence runner.

MANDATORY D81 LOADABILITY GATE

Before creating, modifying, copying, renaming, packaging, mounting, testing, or releasing any D81, read and obey the repository-root file 00_D81_LOADABILITY_GATE.md.

The work must fail closed. A D81 may not be called final, test-ready, loadable, or delivered for physical testing until the exact artifact passes every applicable state in this order:

UNVERIFIED
-> HOST_STRUCTURALLY_VERIFIED
-> HOST_CONTENT_VERIFIED
-> XEMU_BOOT_VERIFIED
-> SD_COPY_VERIFIED
-> SD_CONTIGUITY_VERIFIED
-> PHYSICAL_CHOOSER_VERIFIED
-> TEST_ELIGIBLE

Never build a new test carrier by copying an existing D81 and reopening the copy in a second c1541 session to append files. Fresh-format the image and populate all files in one pinned-tool construction session.

ERROR CODE FF at the MEGA65 chooser is a hard chooser/attach-stage failure. Retire that tested copy and diagnose D81 construction, exact copied bytes, SD physical allocation, safe ejection, and platform identity before assigning a replacement. Do not patch, append to, rename, or re-test the failed copy and do not blame the program inside it.

A matching hash of the SD-card copy is necessary but not sufficient. The MEGA65 Freezer requires a disk-image file to occupy one contiguous FAT32 extent. A fragmented file can hash perfectly and still fail to mount with ERROR CODE FF. Do not submit a copied image to the physical chooser until an independent extent check reports exactly one extent.
"""

import binascii
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys

import r0f_platform_build as platform_build
from d81_foundation_compare import Image


ROOT = platform_build.ROOT
OUT = ROOT / "build/r0f/successor-t04"
T03_OUT = ROOT / "build/r0f/successor-integration"
PRG = T03_OUT / "R0F-SUCCESSOR-INTEGRATION.prg"
SYMBOLS = T03_OUT / "R0F-SUCCESSOR-INTEGRATION.symbols"
ACCOUNTING = T03_OUT / "accounting.json"
SOURCE_BRANCH = "codex/r0f-successor-emulator-exact-carrier"
REVIEWED_T03_PRG_BYTES = 21489
REVIEWED_T03_PRG_SHA256 = (
    "43074a4322b9a2ec35428e966d9f64ab30655c8f0f27516317e7e3f9e417264a"
)
EXPECTED_PRG_BYTES = 21481
EXPECTED_PRG_SHA256 = (
    "d0979c56c373f8885e4741670141ebf22c0a2e9ef8a84f6a931eaef05592d9df"
)
EXPECTED_PAYLOAD_ADDRESS = 0x29C4
CANONICAL_NAME = "R0FSUCC10.D81"
EXPECTED_CANONICAL_BYTES = 819200
EXPECTED_CANONICAL_SHA256 = (
    "3721dff9b84cfb7842cc154f6885861e0c7cbd3c3408c8ecec190bf6b405d461"
)
CANONICAL_LABEL = "R0F SUCC T04"
CANONICAL_ID = "65"
CANONICAL = OUT / "canonical-10" / CANONICAL_NAME
EVIDENCE = ROOT / "docs/evidence/r0f/successor/2026-09-21"
ORACLE_SOURCE = (
    "tools/generators/src/main/java/f65/tools/"
    "R0FSuccessorRuntimeOracle.java"
)
CARRIER_LOADER_SOURCE = (
    ROOT / "tools/diagnostics/r0f_successor_carrier_loader.s"
)
CARRIER_LOADER_LINKER = (
    ROOT / "tools/diagnostics/r0f_successor_carrier_loader.ld"
)
ROM = Path(os.environ.get(
    "F65_MEGA65_ROM",
    "/Users/slice/Documents/Codex/f65-megawing/MEGA65.ROM",
))
XEMU_SD = Path(os.environ.get(
    "F65_XEMU_SD_IMAGE",
    "/Users/slice/Library/Application Support/xemu-lgb/mega65/mega65.img",
))
COMMANDS = []


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(arguments, **kwargs):
    command = list(map(str, arguments))
    COMMANDS.append(command)
    return subprocess.run(command, cwd=ROOT, **kwargs)


def checked_run(arguments, **kwargs):
    kwargs["check"] = True
    return run(arguments, **kwargs)


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def read_json(path):
    return json.loads(path.read_text())


def git_text(*arguments):
    return checked_run(
        ["git", *arguments], capture_output=True, text=True
    ).stdout.strip()


def source_commit():
    return git_text("rev-parse", "HEAD")


def require_clean_source_freeze():
    if git_text("branch", "--show-current") != SOURCE_BRANCH:
        raise ValueError("T04 source branch drift")
    status = git_text("status", "--porcelain", "--untracked-files=all")
    if status:
        raise ValueError("T04 source freeze is not a clean commit")


def pin_runtime_tools():
    platform_build.pin(
        ROOT / "toolchain/xemu/xmega65",
        "dd37baf7846b9696adcb662ffe5da040031b07214c66aef9a7f48cc30040b738",
    )
    platform_build.pin(
        ROM,
        "af3c447f791a2fdc48cb21e1bd3fab015e32641228d9d30d21259b9e878c6fa0",
    )
    if not XEMU_SD.is_file():
        raise ValueError("initialized Xemu SD template is unavailable")


def require_target_identity():
    if not PRG.is_file() or PRG.stat().st_size != EXPECTED_PRG_BYTES:
        raise ValueError("reviewed T03 PRG byte length drift")
    if sha256(PRG) != EXPECTED_PRG_SHA256:
        raise ValueError("reviewed T03 PRG SHA-256 drift")
    accounting = read_json(ACCOUNTING)
    if accounting["prgBytes"] != EXPECTED_PRG_BYTES:
        raise ValueError("T03 accounting byte length drift")
    if accounting["prgSha256"] != EXPECTED_PRG_SHA256:
        raise ValueError("T03 accounting identity drift")
    match = re.search(
        r"^([0-9a-f]+)\s+[A-Za-z]\s+r0fsi_payload$",
        SYMBOLS.read_text(), re.M,
    )
    if not match or int(match.group(1), 16) != EXPECTED_PAYLOAD_ADDRESS:
        raise ValueError("reviewed storage payload address drift")
    return accounting


def build():
    require_clean_source_freeze()
    OUT.mkdir(parents=True, exist_ok=True)
    checked_run([
        sys.executable, "-B",
        "tools/diagnostics/r0f_successor_integration.py", "build",
    ])
    accounting = require_target_identity()
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
    checked_run([
        platform_build.JAVA / "javac", "-Xlint:all", "-Werror",
        "-d", classes, ORACLE_SOURCE,
    ])
    model = checked_run([
        platform_build.JAVA / "java", "-cp", classes,
        "f65.tools.R0FSuccessorRuntimeOracle", "--model",
    ], capture_output=True, text=True).stdout
    (OUT / "oracle-model.txt").write_text(model)
    identity = {
        "identity": "R0F-SUCCESSOR-T04",
        "sourceCommit": source_commit(),
        "sourceBranch": git_text("branch", "--show-current"),
        "sourceState": "clean T04 source-freeze commit",
        "reviewedT03Input": {
            "reproducedBeforeRuntimeWork": True,
            "prgBytes": REVIEWED_T03_PRG_BYTES,
            "prgSha256": REVIEWED_T03_PRG_SHA256,
            "directRuntimeResult": "LOCKOUT fault 84 before canonical construction",
        },
        "t04RuntimeCorrection": {
            "scope": "apply the official single-MAP all-zero clear before CPU-port/I/O access; perform canonical entry before high linked-BSS consumers",
            "architectureChange": False,
            "carrierIdentityInvalidatedAndRebuilt": True,
        },
        "prgPath": str(PRG.relative_to(ROOT)),
        "prgBytes": PRG.stat().st_size,
        "prgSha256": sha256(PRG),
        "residentBytes": accounting["actualResidentBytes"],
        "residentCapacityBytes": accounting["residentCapacityBytes"],
        "residentMarginBytes": accounting["residentMarginBytes"],
        "residentHighWaterExclusive": accounting["residentHighWaterExclusive"],
        "protectedResidentEndExclusive":
            accounting["protectedResidentEndExclusive"],
        "atticTransitionBytes": accounting["atticTransitionBytes"],
        "reserveBytes": accounting["reserveBytes"],
        "lineage": {
            "tick33": "D9EEAB81",
            "tick66": "307A70D6",
        },
        "t03Regression": "PASS",
        "independentOracleModel": "PASS",
        "d81": "NOT YET RUN",
        "xemu": "NOT YET RUN",
        "sd": "NOT RUN",
        "physical": "NOT RUN",
        "fullAcceptance": False,
        "commands": COMMANDS,
    }
    write_json(OUT / "target-identity.json", identity)
    print("T04 corrected target identity and full T03 host/static regression PASS")


def c154(arguments):
    tool = ROOT / "toolchain/vice-clean/bin/c1541"
    platform_build.pin(
        tool,
        "73235289aca30a7e2e8067e521bf604743156cc1d7499c888a3894d6e46fcb3c",
    )
    result = checked_run(
        [tool, *arguments], capture_output=True, text=True, encoding="latin-1"
    )
    diagnostic = result.stdout + result.stderr
    if result.stderr or re.search(
            r"warning|error|failed|fatal|duplicate|truncat|allocation",
            result.stdout, re.I):
        raise ValueError("c1541 diagnostic failure: " + diagnostic)
    return result.stdout


def token_bytes(valid=True):
    payload = bytes(index ^ 0x65 for index in range(32))
    if not valid:
        payload = bytes(32)
    return b"\x00\x20" + payload


def make_boot(directory, stage):
    source = directory / "autoboot.bas"
    payload = stage.read_bytes()[2:]
    lines = [
        "10 bank 0",
        f"20 for i=0 to {len(payload) - 1}:read a:poke 4096+i,a:next",
        "30 sys 4096",
    ]
    for offset in range(0, len(payload), 12):
        values = ",".join(str(value) for value in payload[offset:offset + 12])
        lines.append(f"{100 + offset // 12 * 10} data {values}")
    source.write_text("\n".join(lines) + "\n")
    petcat = ROOT / "toolchain/vice/VICE.app/Contents/Resources/bin/petcat"
    platform_build.pin(
        petcat,
        "a2d0416c3a9f0361792990f0fa2b55cd50e297363148898b9a8b4326597fb433",
    )
    boot = directory / "AUTOBOOT.C65"
    result = checked_run(
        [petcat, "-w65", "-o", boot, "--", source], capture_output=True
    )
    if result.stderr:
        raise ValueError("petcat tokenization diagnostic")
    listing = checked_run(
        [petcat, "-65", boot], capture_output=True, text=True
    )
    if (listing.stderr or "poke 4096+i" not in listing.stdout.lower()
            or "sys 4096" not in listing.stdout.lower()):
        raise ValueError("autoboot detokenization mismatch")
    (directory / "AUTOBOOT.C65.listing").write_text(listing.stdout)
    return boot


def make_carrier_loader(directory):
    tools = ROOT / "toolchain/runtime/llvm-mos/bin"
    compiler = tools / "mos-mega65-clang"
    linker = tools / "ld.lld"
    platform_build.pin(
        compiler,
        "cc557ae99a68ed36e098062b0f5376a878e94ac187b87446c8e603e4fb45a906",
    )
    platform_build.pin(
        linker,
        "0676f6ecbafea9ab5a1fe2bf8dd3cdd67b8ed856ee137d7550b90fe5202e2b58",
    )
    obj = directory / "stage.o"
    stage = directory / "stage"
    checked_run([
        compiler, "-mcpu=mos45gs02", "-c", CARRIER_LOADER_SOURCE,
        "-o", obj,
    ])
    checked_run([
        linker, "-T", CARRIER_LOADER_LINKER, obj, "-o", stage,
    ])
    data = stage.read_bytes()
    if not 2 < len(data) <= 258 or data[:2] != b"\x00\x10":
        raise ValueError("carrier loader layout drift")
    if data.count(b"R0FSUCC") != 1:
        raise ValueError("carrier loader filename drift")
    obj.unlink()
    return stage


def check_disk(image, expected, label, identifier, extracted):
    disk = Image(image)
    header = disk.sector((40, 0))
    if header[2] != 0x44 or (disk.label, disk.identifier) != (
            label, identifier):
        raise ValueError("D81 header/identity mismatch")
    for sector, link in ((1, bytes((40, 2))), (2, bytes((0, 255)))):
        block = disk.sector((40, sector))
        if (block[:2] != link or block[2:4] != bytes((0x44, 0xBB))
                or block[4:6] != header[22:24]):
            raise ValueError("D81 BAM header mismatch")
    for location in disk.directory_sectors:
        block = disk.sector(location)
        if (location[0] != 40 or location in {(40, 0), (40, 1), (40, 2)}
                or (block[0] == 0 and block[1] != 255)):
            raise ValueError("D81 directory metadata mismatch")
    if [entry["name"] for entry in disk.entries] != list(expected):
        raise ValueError("D81 payload list mismatch")
    if extracted.exists():
        raise ValueError("refusing to overwrite extracted D81 contents")
    extracted.mkdir(parents=True)
    extracted_paths = {}
    for entry in disk.entries:
        name = entry["name"]
        path = extracted / name
        c154([image, "-read", name, path])
        wanted = expected[name]
        if (path.read_bytes() != wanted
                or entry["payloadSha256"]
                != hashlib.sha256(wanted).hexdigest()):
            raise ValueError("D81 extracted content mismatch: " + name)
        extracted_paths[name] = str(path)
    listing = c154([image, "-list"])
    reported = re.search(r"(\d+) blocks free", listing, re.I)
    excluded = sum(
        1 for sector in range(40) if (40, sector) not in disk.occupied
    )
    if (not reported
            or int(reported.group(1)) != disk.free_blocks - excluded):
        raise ValueError("D81 free-block accounting mismatch")
    report = disk.describe()
    report["extracted"] = extracted_paths
    report["c1541Listing"] = listing
    report["bamAllocatedSectors"] = len(disk.occupied)
    report["bamFreeSectors"] = disk.free_blocks
    return report


def fresh_d81(directory, image, label, expected):
    if image.exists():
        raise ValueError("refusing to overwrite a D81 candidate")
    arguments = ["-format", label + "," + CANONICAL_ID, "d81", image]
    for name, path in expected.items():
        arguments.extend(["-write", path, name])
    arguments.append("-list")
    construction = c154(arguments)
    (directory / "construction.log").write_text(construction)
    expected_bytes = {name: path.read_bytes() for name, path in expected.items()}
    return check_disk(
        image, expected_bytes, label, CANONICAL_ID,
        directory / "pre-extracted",
    )


def decode_result(result):
    if len(result) != 512:
        raise ValueError("result length")

    def u16(offset):
        return int.from_bytes(result[offset:offset + 2], "little")

    def u32(offset):
        return int.from_bytes(result[offset:offset + 4], "little")

    return {
        "identity": result[:4].decode("ascii", "replace"),
        "version": result[4],
        "stage": result[5],
        "fault": result[6],
        "lifecycle": result[7],
        "tickBefore": u16(8),
        "tickAfter": u16(10),
        "checksumBefore": f"{u32(12):08X}",
        "checksumAfter": f"{u32(16):08X}",
        "contextCrc32": f"{u32(20):08X}",
        "romCrc32": f"{u32(24):08X}",
        "restoredRomCrc32": f"{u32(28):08X}",
        "reserveBeforeCrc32": f"{u32(32):08X}",
        "reserveAfterCrc32": f"{u32(36):08X}",
        "lowBeforeCrc32": f"{u32(40):08X}",
        "lowAfterCrc32": f"{u32(44):08X}",
        "dosBeforeCrc32": f"{u32(48):08X}",
        "dosAfterCrc32": f"{u32(52):08X}",
        "storagePhase": result[56],
        "storageError": result[57],
        "storageReturned": result[58],
        "storageDenied": result[59],
        "irqBefore": u16(60),
        "irqAfter": u16(62),
        "dmaBefore": u16(64),
        "dmaAfter": u16(66),
        "inputBefore": u32(68),
        "inputAfter": u32(72),
        "audioBefore": u32(76),
        "audioAfter": u32(80),
        "snapshotsBefore": u32(84),
        "snapshotsAfter": u32(88),
        "canonicalBasePage": result[92],
        "canonicalCpuPort": result[93],
        "contextInvalidated": result[94],
        "resumedServiceMask": result[95],
        "nmiSticky": result[96],
        "resultCrc32": f"{u32(508):08X}",
        "independentCrc32": f"{binascii.crc32(result[:508]) & 0xffffffff:08X}",
    }


def save_bytes(checksum):
    payload = bytes(
        ((checksum >> ((index & 3) * 8)) & 0xFF) ^ index
        for index in range(32)
    )
    return EXPECTED_PAYLOAD_ADDRESS.to_bytes(2, "little") + payload


def expected_save(result):
    return save_bytes(int.from_bytes(result[12:16], "little"))


def validate_success_result(result):
    decoded = decode_result(result)
    checks = {
        "identity": decoded["identity"] == "RSI1",
        "version": decoded["version"] == 1,
        "completion": decoded["stage"] == 127,
        "fault": decoded["fault"] == 0,
        "lifecycle": decoded["lifecycle"] == 9,
        "ticks": decoded["tickBefore"] == 33 and decoded["tickAfter"] == 66,
        "lineage": decoded["checksumBefore"] == "D9EEAB81"
            and decoded["checksumAfter"] == "307A70D6",
        "context": decoded["contextCrc32"] != "00000000",
        "rom": decoded["romCrc32"] != "00000000"
            and decoded["romCrc32"] == decoded["restoredRomCrc32"],
        "reserve": decoded["reserveBeforeCrc32"]
            == decoded["reserveAfterCrc32"],
        "lowMemory": decoded["lowBeforeCrc32"]
            == decoded["lowAfterCrc32"],
        "dos": decoded["dosBeforeCrc32"] == decoded["dosAfterCrc32"],
        "storage": decoded["storagePhase"] == 5
            and decoded["storageError"] == 0
            and decoded["storageReturned"] == 1
            and decoded["storageDenied"] == 0,
        "canonical": decoded["canonicalBasePage"] == 2
            and decoded["canonicalCpuPort"] == 0x35
            and decoded["contextInvalidated"] == 1,
        "services": decoded["resumedServiceMask"] == 31,
        "nmi": decoded["nmiSticky"] == 0,
        "crc": decoded["resultCrc32"] == decoded["independentCrc32"],
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise ValueError("runtime result rejection: " + ", ".join(failed))
    return decoded


def java_oracle(result_path, saved_path, check=True):
    invocation = [
        platform_build.JAVA / "java", "-cp", OUT / "classes",
        "f65.tools.R0FSuccessorRuntimeOracle", result_path, saved_path,
    ]
    completed = run(
        invocation, capture_output=True, text=True, check=False
    )
    if check and completed.returncode != 0:
        raise ValueError("independent Java oracle rejected valid evidence: "
                         + completed.stdout + completed.stderr)
    return completed


def run_xemu(directory, mode, image, tier, autoload):
    if mode not in ("0", "1"):
        raise ValueError("video standard")
    pin_runtime_tools()
    sd = directory / "disposable-sd.img"
    checked_run(["/bin/cp", "-c", XEMU_SD, sd])
    emulator = ROOT / "toolchain/xemu/xmega65"
    arguments = [
        emulator, "-skipconfigfile", "-headless", "-fastboot",
        "-videostd", mode, "-fastclock", "40.5", "-rom", ROM,
        "-sdimg", sd, "-8", image,
    ]
    if autoload:
        arguments.append("-autoload")
    else:
        arguments.extend(["-prg", PRG])
    arguments.extend([
        "-dumpscreen", directory / "screen.txt",
        "-dumpmem", directory / "memory.bin",
        "-screenshot", directory / "screen.png",
    ])
    command = list(map(str, arguments))
    COMMANDS.append(command)
    started_at = datetime.now(timezone.utc).isoformat()
    with (directory / "xemu.log").open("wb") as output:
        output.write(
            ("T04_SOURCE_BRANCH=" + SOURCE_BRANCH + "\n"
             + "T04_SOURCE_COMMIT=" + source_commit() + "\n"
             + "T04_MOUNTED_D81_FILENAME=" + image.name + "\n")
            .encode("ascii")
        )
        output.flush()
        process = subprocess.Popen(
            command, cwd=ROOT, stdout=output, stderr=subprocess.STDOUT
        )
        print(f"T04 Xemu {tier} mode={mode}: {directory}", flush=True)
        timed_out = False
        timeout_seconds = (
            100 if tier == "EXACT_CANONICAL_CARRIER_COPY" else 80
        )
        try:
            process.wait(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            timed_out = True
            process.send_signal(signal.SIGTERM)
            process.wait(timeout=10)
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()
    memory_path = directory / "memory.bin"
    if not memory_path.is_file() or memory_path.stat().st_size < 0x1B00:
        raise ValueError("Xemu memory capture unavailable")
    result = memory_path.read_bytes()[0x1900:0x1B00]
    result_path = directory / "result.bin"
    result_path.write_bytes(result)
    return result, {
        "tier": tier,
        "startedAtUtc": started_at,
        "finishedAtUtc": datetime.now(timezone.utc).isoformat(),
        "videoMode": "NTSC" if mode == "1" else "PAL",
        "videoArgument": mode,
        "timedTerminationAfterSeconds": timeout_seconds if timed_out else None,
        "processReturnCode": process.returncode,
        "command": command,
        "sourceBranch": SOURCE_BRANCH,
        "sourceCommit": source_commit(),
        "mountedD81Filename": image.name,
        "xemu": {
            "path": str(emulator.relative_to(ROOT)),
            "sha256": sha256(emulator),
            "version": "20260129235930",
            "sourceCommit": "40dfef0d1d5f56be2469492715c12bdb32c75b67",
        },
        "rom": {"path": str(ROM), "sha256": sha256(ROM)},
        "disposableSdSha256": sha256(sd),
    }


def finish_success_run(
        directory, image, result, base_evidence, expected, label):
    decoded = validate_success_result(result)
    screen = (directory / "screen.txt").read_text(errors="replace")
    if ("SUCCESSOR HOST/STATIC IMAGE - RUNTIME UNVERIFIED" not in screen
            or "NO D81 / XEMU / SD / HARDWARE / R0-F ACCEPTANCE" not in screen):
        raise ValueError("stable exact-T03 identity banner missing")
    saved = expected_save(result)
    expected_post = dict(expected)
    expected_post["rsstate"] = saved
    post = check_disk(
        image, expected_post, label, CANONICAL_ID,
        directory / "post-extracted",
    )
    saved_path = Path(post["extracted"]["rsstate"])
    if saved_path.read_bytes() != saved:
        raise ValueError("independent SAVE payload mismatch")
    retained_saved = directory / "saved.prg"
    retained_saved.write_bytes(saved_path.read_bytes())
    oracle = java_oracle(directory / "result.bin", retained_saved)
    (directory / "oracle.txt").write_text(oracle.stdout)
    write_json(directory / "post-structure.json", post)
    evidence = {
        **base_evidence,
        "result": decoded,
        "resultSha256": sha256(directory / "result.bin"),
        "resultReduction": "PASS",
        "javaOracle": "PASS",
        "screenIdentity": "PASS",
        "screenshotSha256": sha256(directory / "screen.png"),
        "postRunD81Sha256": post["sha256"],
        "postRunStructureAndContent": "PASS",
        "extractedSaveSha256": sha256(retained_saved),
        "extractedSaveBytes": retained_saved.stat().st_size,
        "extractedSaveValidation": "PASS",
        "sd": "NOT RUN",
        "physical": "NOT RUN",
        "fullAcceptance": False,
    }
    write_json(directory / "evidence.json", evidence)
    return evidence


def direct_fixture(mode):
    require_target_identity()
    name = "ntsc" if mode == "1" else "pal"
    directory = OUT / "direct" / ("source-freeze-" + name)
    if directory.exists():
        raise ValueError("refusing to overwrite direct-run evidence: " + name)
    directory.mkdir(parents=True)
    token = directory / "TOKEN.prg"
    token.write_bytes(token_bytes())
    image = directory / "run.D81"
    initial = fresh_d81(
        directory, image, "R0F T04 DEV", {"token": token}
    )
    write_json(directory / "host-gate.json", {
        "state": "HOST_CONTENT_VERIFIED",
        "structural": "PASS",
        "content": "PASS",
        "entry": "direct exact successor PRG; D81 supplies TOKEN only",
        "image": initial,
        "canonicalCarrier": False,
        "hardwareRelease": False,
    })
    result, evidence = run_xemu(
        directory, mode, image, "DIRECT_PRG_DEVELOPMENT", False
    )
    expected = {"token": token.read_bytes()}
    base = {
        **evidence,
        "prgSha256": sha256(PRG),
        "expectedCanonicalD81Filename": CANONICAL_NAME,
        "expectedCanonicalD81Sha256": EXPECTED_CANONICAL_SHA256,
        "initialD81Sha256": initial["sha256"],
        "canonicalCarrier": False,
    }
    return finish_success_run(
        directory, image, result, base, expected, "R0F T04 DEV"
    )


def direct_clean():
    if not (OUT / "target-identity.json").is_file():
        raise ValueError("run build before direct diagnostics")
    runs = [direct_fixture("1"), direct_fixture("0")]
    summary = {
        "identity": "R0F-SUCCESSOR-T04-DIRECT-PRG",
        "sourceBranch": SOURCE_BRANCH,
        "sourceCommit": source_commit(),
        "result": "PASS",
        "runs": runs,
        "canonicalCarrier": "NOT YET CONSTRUCTED",
        "nonClaim": "direct PRG development tier is not exact-carrier evidence",
    }
    write_json(OUT / "direct-summary.json", summary)
    print("T04 clean NTSC/PAL direct-PRG diagnostics PASS")


def fault_fixture(name, mode, token_kind, expected_fault):
    directory = OUT / "fault" / name
    if directory.exists():
        raise ValueError("refusing to overwrite fault evidence: " + name)
    directory.mkdir(parents=True)
    expected_paths = {}
    expected_bytes = {}
    if token_kind != "missing":
        token = directory / "TOKEN.prg"
        token.write_bytes(token_bytes(valid=token_kind == "valid"))
        expected_paths["token"] = token
        expected_bytes["token"] = token.read_bytes()
    image = directory / "run.D81"
    initial = fresh_d81(
        directory, image, "R0F T04 FLT", expected_paths
    )
    result, runtime = run_xemu(
        directory, mode, image, "DIRECT_PRG_FAULT", False
    )
    decoded = decode_result(result)
    if (decoded["identity"] != "RSI1" or decoded["stage"] == 127
            or decoded["fault"] != expected_fault
            or decoded["lifecycle"] != 10):
        raise ValueError("fault fixture emitted wrong lockout")
    if token_kind == "invalid":
        expected_bytes["rsstate"] = save_bytes(0xD9EEAB81)
    post = check_disk(
        image, expected_bytes, "R0F T04 FLT", CANONICAL_ID,
        directory / "post-extracted",
    )
    evidence = {
        **runtime,
        "case": name,
        "sourceBranch": SOURCE_BRANCH,
        "sourceCommit": source_commit(),
        "expectedCanonicalD81Filename": CANONICAL_NAME,
        "expectedCanonicalD81Sha256": EXPECTED_CANONICAL_SHA256,
        "input": token_kind + " TOKEN",
        "expectedFault": expected_fault,
        "result": decoded,
        "falsePassPrevented": True,
        "initialD81Sha256": initial["sha256"],
        "postRunD81Sha256": post["sha256"],
        "canonicalCarrier": False,
        "destructiveMediaTest": False,
    }
    write_json(directory / "post-structure.json", post)
    write_json(directory / "evidence.json", evidence)
    return evidence


def fault_tests():
    if not (OUT / "direct-summary.json").is_file():
        raise ValueError("clean direct diagnostics must pass first")
    missing = fault_fixture("source-freeze-missing-token", "1", "missing", 77)
    invalid = fault_fixture("source-freeze-invalid-token", "0", "invalid", 78)
    good_result = OUT / "direct/source-freeze-ntsc/result.bin"
    good_saved = OUT / "direct/source-freeze-ntsc/saved.prg"
    corrupt_dir = OUT / "fault/source-freeze-host-corruption"
    corrupt_dir.mkdir(parents=True)
    corrupt_result = bytearray(good_result.read_bytes())
    corrupt_result[5] ^= 1
    corrupt_result_path = corrupt_dir / "corrupt-result.bin"
    corrupt_result_path.write_bytes(corrupt_result)
    corrupt_saved = bytearray(good_saved.read_bytes())
    corrupt_saved[2] ^= 1
    corrupt_saved_path = corrupt_dir / "corrupt-saved.prg"
    corrupt_saved_path.write_bytes(corrupt_saved)
    rejected = []
    for case, result_path, saved_path in (
            ("corrupt-result", corrupt_result_path, good_saved),
            ("corrupt-save", good_result, corrupt_saved_path)):
        completed = java_oracle(result_path, saved_path, check=False)
        if completed.returncode == 0:
            raise ValueError("independent oracle accepted " + case)
        rejected.append({
            "case": case,
            "returnCode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        })
    try:
        validate_success_result(bytes(corrupt_result))
    except ValueError as error:
        python_rejection = str(error)
    else:
        raise ValueError("Python reducer accepted corrupt result")
    summary = {
        "identity": "R0F-SUCCESSOR-T04-FAULTS",
        "sourceBranch": SOURCE_BRANCH,
        "sourceCommit": source_commit(),
        "canonicalD81Filename": CANONICAL_NAME,
        "canonicalD81Sha256": EXPECTED_CANONICAL_SHA256,
        "result": "PASS",
        "targetLockouts": [missing, invalid],
        "oracleRejections": rejected,
        "pythonReducerRejection": python_rejection,
        "falseSuccessfulResumeOrPass": False,
        "canonicalCarrierModified": False,
        "destructiveMediaTests": False,
    }
    write_json(OUT / "fault-summary.json", summary)
    print("T04 deterministic missing/invalid-token and reducer lockouts PASS")


def package():
    require_target_identity()
    if not (OUT / "direct-summary.json").is_file():
        raise ValueError("direct diagnostics must pass before canonical D81")
    canonical_dir = CANONICAL.parent
    if canonical_dir.exists():
        raise ValueError("refusing to replace canonical carrier directory")
    canonical_dir.mkdir(parents=True)
    stage = make_carrier_loader(canonical_dir)
    boot = make_boot(canonical_dir, stage)
    target = canonical_dir / "r0fsucc"
    shutil.copyfile(PRG, target)
    if target.read_bytes() != PRG.read_bytes():
        raise ValueError("canonical successor identity mismatch")
    token = canonical_dir / "TOKEN.prg"
    token.write_bytes(token_bytes())
    expected_paths = {
        "autoboot.c65": boot,
        "r0fsucc": target,
        "token": token,
    }
    construction = fresh_d81(
        canonical_dir, CANONICAL, CANONICAL_LABEL, expected_paths
    )
    canonical_sha = construction["sha256"]
    if (CANONICAL.stat().st_size != EXPECTED_CANONICAL_BYTES
            or canonical_sha != EXPECTED_CANONICAL_SHA256):
        raise ValueError("canonical D81 identity drift")
    CANONICAL.chmod(0o444)
    lock = read_json(ROOT / "toolchain/f65_toolchain.lock.json")
    builder = ROOT / lock["r0d_d81_builder"]["c1541_relative_path"]
    host_gate = {
        "identity": "R0F-SUCCESSOR-T04-CANONICAL",
        "D81_STATE": "HOST_CONTENT_VERIFIED",
        "D81_FILENAME": CANONICAL.name,
        "D81_SHA256": canonical_sha,
        "D81_BYTES": CANONICAL.stat().st_size,
        "DISK_LABEL": CANONICAL_LABEL,
        "DISK_ID": CANONICAL_ID,
        "ENTRY_FILENAME": "AUTOBOOT.C65 embeds STAGE -> SYS $1000 -> KERNAL LOAD R0FSUCC",
        "SOURCE_BRANCH": SOURCE_BRANCH,
        "SOURCE_COMMIT": source_commit(),
        "PRG_SHA256": sha256(PRG),
        "CARRIER_LOADER_SHA256": sha256(stage),
        "CARRIER_LOADER_SOURCE_SHA256": sha256(CARRIER_LOADER_SOURCE),
        "CARRIER_LOADER_LINKER_SHA256": sha256(CARRIER_LOADER_LINKER),
        "TOKEN_SHA256": sha256(token),
        "BUILDER_IDENTITY": {
            "path": str(builder.relative_to(ROOT)),
            "version": lock["r0d_d81_builder"]["version"],
            "sha256": sha256(builder),
            "realdevice": "disabled",
        },
        "STRUCTURAL_VALIDATOR_IDENTITY": {
            "paths": [
                "tools/diagnostics/d81_foundation_compare.py",
                "tools/diagnostics/r0f_successor_emulator.py",
            ],
            "sha256": {
                "d81_foundation_compare.py": sha256(
                    ROOT / "tools/diagnostics/d81_foundation_compare.py"),
                "r0f_successor_emulator.py": sha256(Path(__file__)),
            },
        },
        "HOST_STRUCTURAL_RESULT": "PASS",
        "HOST_CONTENT_RESULT": "PASS",
        "XEMU_RESULT": "AWAITING_T04_CARRIER_RUNS",
        "XEMU_EVIDENCE": None,
        "SD_COPY_SHA256": None,
        "SD_FILESYSTEM": None,
        "SD_TRANSFER_METHOD": None,
        "SD_CONTIGUITY_RESULT": "NOT RUN",
        "SD_EXTENT_COUNT": None,
        "SD_EXTENT_EVIDENCE": None,
        "SD_SAFE_EJECT_RESULT": "NOT RUN",
        "PHYSICAL_CHOOSER_RESULT": "NOT RUN",
        "PHYSICAL_EVIDENCE": None,
        "construction":
            "fresh format plus all payload writes in one pinned c1541 invocation",
        "immutableAfterAdmission": True,
        "mountedInXemu": False,
        "image": construction,
        "fullAcceptance": False,
    }
    write_json(canonical_dir / "host-gate.json", host_gate)
    print("T04 canonical D81 HOST_STRUCTURALLY_VERIFIED -> HOST_CONTENT_VERIFIED")
    print("canonical sha256=" + canonical_sha)


def carrier_run(mode, number):
    host_gate = read_json(CANONICAL.parent / "host-gate.json")
    canonical_sha = host_gate["D81_SHA256"]
    if sha256(CANONICAL) != canonical_sha:
        raise ValueError("canonical D81 identity changed")
    name = ("ntsc" if mode == "1" else "pal") + f"-{number}"
    directory = OUT / "carrier-source-freeze" / name
    if directory.exists():
        raise ValueError("refusing to overwrite carrier-run evidence: " + name)
    directory.mkdir(parents=True)
    image = directory / CANONICAL.name
    shutil.copyfile(CANONICAL, image)
    image.chmod(0o644)
    pre_sha = sha256(image)
    if pre_sha != canonical_sha:
        raise ValueError("disposable carrier pre-run hash mismatch")
    initial = Image(image).describe()
    result, runtime = run_xemu(
        directory, mode, image, "EXACT_CANONICAL_CARRIER_COPY", True
    )
    canonical_expected = {
        entry["name"]: Path(host_gate["image"]["extracted"][entry["name"]])
            .read_bytes()
        for entry in host_gate["image"]["entries"]
    }
    base = {
        **runtime,
        "run": name,
        "sourceBranch": SOURCE_BRANCH,
        "sourceCommit": source_commit(),
        "prgSha256": EXPECTED_PRG_SHA256,
        "canonicalD81Path": str(CANONICAL.relative_to(ROOT)),
        "canonicalD81Filename": CANONICAL.name,
        "mountedD81Filename": image.name,
        "canonicalD81Sha256": canonical_sha,
        "preRunD81Sha256": pre_sha,
        "preRunByteIdenticalToCanonical": True,
        "preRunStructure": initial,
        "canonicalMountedWritable": False,
        "disposableCopyMountedWritable": True,
    }
    evidence = finish_success_run(
        directory, image, result, base, canonical_expected, CANONICAL_LABEL
    )
    if sha256(CANONICAL) != canonical_sha:
        raise ValueError("canonical D81 changed during carrier run")
    return evidence


def carrier_tests():
    if not CANONICAL.is_file():
        raise ValueError("canonical D81 is missing")
    runs = []
    for mode, number in (("1", 1), ("1", 2), ("0", 1), ("0", 2)):
        runs.append(carrier_run(mode, number))
    host_gate_path = CANONICAL.parent / "host-gate.json"
    host_gate = read_json(host_gate_path)
    if sha256(CANONICAL) != host_gate["D81_SHA256"]:
        raise ValueError("canonical D81 final identity mismatch")
    host_gate["D81_STATE"] = "XEMU_BOOT_VERIFIED"
    host_gate["XEMU_RESULT"] = "PASS"
    host_gate["XEMU_EVIDENCE"] = [
        {
            "run": evidence["run"],
            "videoMode": evidence["videoMode"],
            "sourceBranch": evidence["sourceBranch"],
            "sourceCommit": evidence["sourceCommit"],
            "mountedD81Filename": evidence["mountedD81Filename"],
            "preRunD81Sha256": evidence["preRunD81Sha256"],
            "postRunD81Sha256": evidence["postRunD81Sha256"],
            "resultSha256": evidence["resultSha256"],
            "resultCrc32": evidence["result"]["resultCrc32"],
            "extractedSaveSha256": evidence["extractedSaveSha256"],
        }
        for evidence in runs
    ]
    write_json(host_gate_path, host_gate)
    summary = {
        "identity": "R0F-SUCCESSOR-T04-EXACT-CARRIER",
        "sourceBranch": SOURCE_BRANCH,
        "sourceCommit": source_commit(),
        "result": "PASS",
        "D81_STATE": "XEMU_BOOT_VERIFIED",
        "canonicalD81Sha256": host_gate["D81_SHA256"],
        "canonicalD81Bytes": host_gate["D81_BYTES"],
        "canonicalD81Filename": CANONICAL.name,
        "exactMountedFilenameEveryRun": CANONICAL.name,
        "canonicalFinalIdentityUnchanged": True,
        "runs": runs,
        "ntscRuns": 2,
        "palRuns": 2,
        "freshDisposableCopyPerRun": True,
        "postRunImagesRetainedLocally": True,
        "postRunImagesReused": False,
        "sd": "NOT RUN",
        "physicalChooser": "NOT RUN",
        "fullAcceptance": False,
    }
    write_json(OUT / "carrier-summary.json", summary)
    print("T04 two NTSC plus two PAL exact-carrier Xemu runs PASS")


def retain():
    identity_path = OUT / "target-identity.json"
    identity = read_json(identity_path)
    identity.update({
        "sourceBranch": SOURCE_BRANCH,
        "sourceCommit": source_commit(),
        "sourceState": "clean T04 source-freeze commit",
        "d81": "XEMU_BOOT_VERIFIED",
        "xemu": "PASS",
        "canonicalD81Filename": CANONICAL.name,
        "canonicalD81Sha256": EXPECTED_CANONICAL_SHA256,
    })
    write_json(identity_path, identity)
    for required in (
            OUT / "target-identity.json",
            OUT / "direct-summary.json",
            OUT / "fault-summary.json",
            OUT / "carrier-summary.json",
            CANONICAL.parent / "host-gate.json"):
        if not required.is_file():
            raise ValueError("missing required T04 evidence: " + str(required))
    if EVIDENCE.exists():
        raise ValueError("refusing to overwrite retained T04 evidence")
    EVIDENCE.mkdir(parents=True)
    top_level = {
        OUT / "target-identity.json": EVIDENCE / "target-identity.json",
        OUT / "oracle-model.txt": EVIDENCE / "oracle-model.txt",
        OUT / "direct-summary.json": EVIDENCE / "direct-summary.json",
        OUT / "fault-summary.json": EVIDENCE / "fault-summary.json",
        OUT / "carrier-summary.json": EVIDENCE / "carrier-summary.json",
        CANONICAL.parent / "host-gate.json": EVIDENCE / "canonical-host-gate.json",
        CANONICAL.parent / "construction.log": EVIDENCE / "canonical-construction.log",
        CANONICAL.parent / "AUTOBOOT.C65": EVIDENCE / "AUTOBOOT.C65",
        CANONICAL.parent / "AUTOBOOT.C65.listing": EVIDENCE / "AUTOBOOT.C65.listing",
        CANONICAL.parent / "stage": EVIDENCE / "stage",
        CANONICAL.parent / "r0fsucc": EVIDENCE / "r0fsucc",
        CANONICAL.parent / "TOKEN.prg": EVIDENCE / "TOKEN.prg",
    }
    for source, destination in top_level.items():
        shutil.copy2(source, destination)
    run_files = (
        "construction.log", "host-gate.json", "post-structure.json",
        "evidence.json", "result.bin", "saved.prg", "oracle.txt",
        "screen.txt", "screen.png", "xemu.log",
    )
    for group, names in (
            ("direct", ("source-freeze-ntsc", "source-freeze-pal")),
            ("carrier-source-freeze",
             ("ntsc-1", "ntsc-2", "pal-1", "pal-2")),
            ("fault", ("source-freeze-missing-token",
                       "source-freeze-invalid-token"))):
        for name in names:
            source_dir = OUT / group / name
            destination_dir = EVIDENCE / group / name
            destination_dir.mkdir(parents=True)
            for filename in run_files:
                source = source_dir / filename
                if source.is_file():
                    shutil.copy2(source, destination_dir / filename)
    corruption = EVIDENCE / "fault/source-freeze-host-corruption"
    corruption.mkdir(parents=True)
    for source in (OUT / "fault/source-freeze-host-corruption").iterdir():
        if source.is_file():
            shutil.copy2(source, corruption / source.name)
    print("T04 non-D81 evidence retained at " + str(EVIDENCE))


def all_steps():
    build()
    direct_clean()
    fault_tests()
    package()
    carrier_tests()
    retain()


def main():
    commands = {
        "build": build,
        "direct-clean": direct_clean,
        "fault-tests": fault_tests,
        "package": package,
        "carrier-tests": carrier_tests,
        "retain": retain,
        "all": all_steps,
    }
    if len(sys.argv) != 2 or sys.argv[1] not in commands:
        raise SystemExit(
            "usage: r0f_successor_emulator.py "
            "build|direct-clean|fault-tests|package|carrier-tests|retain|all"
        )
    commands[sys.argv[1]]()


if __name__ == "__main__":
    main()
