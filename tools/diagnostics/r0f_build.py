#!/usr/bin/env python3
"""Bounded R0-F source build and native functional regression (no media writes)."""
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import os

ROOT = pathlib.Path(__file__).resolve().parents[2]
VARIANT = os.environ.get("F65_R0F_VARIANT", "startup-fix")
if VARIANT not in ("startup-fix", "cia-timing", "capture"):
    raise ValueError("unknown R0-F variant")
CAPTURE = VARIANT == "capture"
TIMING = VARIANT in ("cia-timing", "capture")
OUT = ROOT / "build/r0f" / ("cia-timing-safe" if VARIANT == "cia-timing" else VARIANT)
CARRIER_NAME = "F65R0F5.D81" if CAPTURE else "F65R0F4.D81" if TIMING else "F65R0F2.D81"
CARRIER_LABEL = "F65 R0-F5" if CAPTURE else "F65 R0-F4" if TIMING else "F65 R0-F2"
TOOLS = ROOT / "toolchain/runtime/llvm-mos/bin"
CONTRACT = ROOT / "interfaces/r0f_proof_contract.json"
MEDIA_OPERATION_STARTED = False


def run(args, **kwargs):
    return subprocess.run([str(a) for a in args], cwd=ROOT, check=True, **kwargs)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rom_transfers(disassembly):
    return re.findall(r"^\s*([0-9a-f]+):[^\n]*\b(?:jsr|jmp)\s+\$([ef][0-9a-f]{3})\b", disassembly, re.M)


def generate():
    c = json.loads(CONTRACT.read_text())
    header = "/* Generated from interfaces/r0f_proof_contract.json. */\n"
    header += "#ifndef F65_R0F_INTERFACES_H\n#define F65_R0F_INTERFACES_H\n"
    header += "".join(f"#define R0F_{k} {v}u\n" for k, v in c["constants"].items())
    header += "".join(f"#define R0F_{k} {v}u\n" for k, v in c["cia_timing"]["constants"].items())
    header += "".join(f"#define R0F_{k} {v}u\n" for k, v in c["capture_viewer"]["constants"].items())
    header += "#endif\n"
    (ROOT / "interfaces/generated/r0f_interfaces.h").write_text(header)
    OUT.mkdir(parents=True, exist_ok=True)


def validate_result(b, failed_phase=False):
    if TIMING and len(b) == 256 and b[4] == 2:
        return validate_timing_result(b)
    if len(b) != 256 or b[:7] != b"R0F1\x01\x64\x15":
        raise ValueError("result identity/length")
    if b[7] != 127 or sum(b[:255]) % 256 != b[255]:
        raise ValueError("functional status or result checksum")
    profile = b"".join(n.to_bytes(4, "little") for n in (9, 16, 24, 48, 64))
    if b[8:28] != profile or b[28:33] != bytes([3, 64, 1, 0, 5]):
        raise ValueError("proxy profile/snapshot metadata")
    if any(b[33:40]) or any(b[60:64]):
        raise ValueError("functional reserved encoding")
    # Independent closed-form expected counts, not target-produced expectations.
    checksum = 0x0065e001
    for tick in range(1, 1001):
        checksum = ((checksum << 5) ^ (checksum >> 2) ^ tick) & 0xffffffff
    if checksum != 393387319:
        raise ValueError("oracle golden checksum")
    for case in range(5):
        if int.from_bytes(b[40+case*4:44+case*4], "little") != checksum:
            raise ValueError("case checksum")
        at = 64 + case * 16
        counts = [1000, 202 if case == 1 else 1000, 798 if case == 1 else 0,
                  2000 if case == 4 else 1000, 2000 if case == 4 else 1000]
        expected = bytes([case, 1]) + b"".join(n.to_bytes(2, "little") for n in counts)
        expected += bytes([63 if case == 2 else 0, 1 if case == 3 else 0, 0, 0])
        if b[at:at+16] != expected:
            raise ValueError(f"functional case {case}")
        mask = 0xfff7 if failed_phase else 0xffff
        if int.from_bytes(b[240+case*2:242+case*2], "little") != mask:
            raise ValueError("phase validity")
    if b[151] != (0 if failed_phase else 127):
        raise ValueError("acquisition status")
    if b[144:151] != b"RT\x01\x10\x21\x05\x10" or b[152:160] != bytes([1])+bytes(7) or any(b[250:255]):
        raise ValueError("observation header/reserved encoding")


def validate_timing_result(b):
    if len(b) != 256 or b[:7] != b"R0F1\x02\x64\x15" or sum(b[:255]) % 256 != b[255]:
        raise ValueError("CIA result identity/checksum")
    # Reuse the independently checked inherited functional record, not its old
    # raster observations. No claim is made about this synthetic adapter block.
    old = bytearray(b)
    old[4] = 1
    old[144:160] = b"RT\x01\x10\x21\x05\x10\x7f\x01" + bytes(7)
    old[240:255] = bytes([255])*10 + bytes(5)
    old[255] = sum(old[:255]) % 256
    validate_result(old)
    if b[144:152] != b"CT\x01\x10\x21\x05\x10\x7f" or b[156:158] != b"\x10\0":
        raise ValueError("CIA acquisition incomplete/header")
    if b[244:248] != (10000).to_bytes(4,"little") or b[250:253] != (10880).to_bytes(2,"little") + b"\0" or b[254]:
        raise ValueError("CIA metadata/fault")
    ptr = int.from_bytes(b[248:250],"little")
    if not 0x2001 <= ptr <= 0xd000-10880 or b[253] != 3:
        raise ValueError("CIA raw range/snapshot high-water")
    for at in (152,240):
        if not 128000 <= int.from_bytes(b[at:at+4],"little") <= 960000:
            raise ValueError("CIA frame calibration guard")
    for case in range(5):
        if b[170+case*16:172+case*16] != b"\xff\xff":
            raise ValueError("CIA phase coverage incomplete")


def java_oracle(payload, label):
    home = pathlib.Path(os.environ.get("F65_JAVA_HOME", "/Users/slice/Documents/Codex/f65-megawing/toolchain/runtime/jdk-full/jdk-21.0.12+8/Contents/Home"))
    version = run([home/"bin/java", "-version"], capture_output=True).stderr
    if b"Temurin-21.0.12+8" not in version:
        raise ValueError("pinned full Java runtime unavailable")
    source = ROOT/"tools/generators/src/main/java/f65/tools/R0FTimingOracle.java"
    classes = OUT/"java-classes"
    classes.mkdir(exist_ok=True)
    run([home/"bin/javac", "-d", classes, source,
         ROOT/"tools/generators/src/main/java/f65/tools/R0FCapturePages.java"])
    data = OUT/(label+".capture.bin")
    data.write_bytes(payload)
    answer = run([home/"bin/java", "-cp", classes, "f65.tools.R0FTimingOracle", data], capture_output=True)
    (OUT/(label+".java.txt")).write_bytes(answer.stdout)
    (OUT/"java-identity.json").write_text(json.dumps({"home":str(home),
        "version":version.decode(),"javaSha256":sha(home/"bin/java"),
        "javacSha256":sha(home/"bin/javac"),"releaseSha256":sha(home/"release"),
        "oracleSourceSha256":sha(source)},indent=2)+"\n")
    return answer.stdout.decode().strip()


def capture_verify(payload, label):
    pages = run([OUT/"r0f-capture-host-test"], input=payload, capture_output=True).stdout
    page_file = OUT/(label+".pages.bin")
    page_file.write_bytes(pages)
    raw_file = OUT/(label+".capture.bin")
    raw_file.write_bytes(payload)
    home = pathlib.Path(json.loads((OUT/"java-identity.json").read_text())["home"])
    answer = run([home/"bin/java", "-cp", OUT/"java-classes", "f65.tools.R0FCapturePages",
                  "--self-test", page_file, raw_file], capture_output=True).stdout
    (OUT/(label+".pages.java.txt")).write_bytes(answer)
    return pages


def capture_host_test():
    run(["/usr/bin/clang", "-std=c11", "-Wall", "-Wextra", "-Wconversion", "-Werror",
         "-fsanitize=address,undefined", "-DR0F_CAPTURE_TEST", "-Iinterfaces/generated",
         "src/diagnostics/r0f/capture_view.c", "src/platform/r0f/capture_key.c",
         "tools/diagnostics/r0f_capture_host_test.c", "-o", OUT/"r0f-capture-host-test"])
    payload = (OUT/"host-timing.capture.bin").read_bytes()
    pages = capture_verify(payload, "host-capture")
    (OUT/"capture-host-test.json").write_text(json.dumps({
        "result":"PASS", "tier":"native ASan/UBSan and independent Java, not hardware",
        "pages":22,"bytes":len(payload),"captureSha256":hashlib.sha256(payload).hexdigest(),
        "pagesSha256":hashlib.sha256(pages).hexdigest(),
        "controls":"N/space/P/clamps/S/C/lowercase/unknown; D610 read/ack; source immutable",
        "oracle":(OUT/"host-capture.pages.java.txt").read_text().strip()},indent=2)+"\n")


def timing_host_test():
    clock_test = OUT / "r0f-clock-host-test"
    run(["/usr/bin/clang", "-std=c11", "-Wall", "-Wextra", "-Wconversion", "-Werror",
         "-fsanitize=address,undefined", "-DR0F_CLOCK_TEST", "-Iinterfaces/generated",
         "src/platform/r0f/cia_clock.c", "tools/diagnostics/r0f_clock_host_test.c", "-o", clock_test])
    clock_result = run([clock_test], capture_output=True).stdout.decode().strip()
    binary = OUT / "r0f-timing-host-test"
    run(["/usr/bin/clang", "-std=c11", "-Wall", "-Wextra", "-Wconversion", "-Werror",
         "-fsanitize=address,undefined", "-DR0F_HOST_TEST", "-DR0F_CIA_TIMING", "-Iinterfaces/generated",
         "src/diagnostics/r0f/composite.c", "src/diagnostics/r0f/timing_sweep.c",
         "tools/diagnostics/r0f_timing_host_test.c", "-o", binary])
    payload = run([binary], capture_output=True).stdout
    validate_timing_result(payload[:256])
    oracle = java_oracle(payload, "host-timing")
    overrun = run([binary, "overrun"], capture_output=True).stdout
    validate_timing_result(overrun[:256])
    java_oracle(overrun, "host-overrun")
    if int.from_bytes(overrun[168:170], "little") != 16:
        raise ValueError("injected deadline misses not observed")
    rejected = 0
    for mode in ("begin-fail", "read-fail", "stuck-clock", "stuck-frame", "overflow", "clock-jump"):
        bad = run([binary, mode], capture_output=True).stdout
        try:
            validate_timing_result(bad[:256])
        except ValueError:
            rejected += 1
        else:
            raise ValueError("timer failure incorrectly passed: " + mode)
    report = {"result":"PASS", "samples":2640, "faultCasesRejected":rejected,
              "wrap":"mock starts at FFFF0000; unsigned 32-bit rollover exercised",
              "java":oracle,"wrapper":clock_result,"deadlineInjection":"16 misses per case observed; never relabeled deadline PASS", "units":"mock counts, not target or physical timing"}
    (OUT/"timing-host-test.json").write_text(json.dumps(report,indent=2)+"\n")


def host_test():
    generate()
    if rom_transfers("2035: 20 d2 ff\tjsr\t$ffd2 <unrelated_symbol>") != [("2035", "ffd2")]:
        raise ValueError("static ROM-call rejection regression")
    if rom_transfers("2035: 4c 00 e0\tjmp\t$e000") != [("2035", "e000")]:
        raise ValueError("static ROM-tail-call rejection regression")
    if rom_transfers("2035: 20 00 30\tjsr\t$3000 <function>\n2038: ad 12 d0\tlda\t$d012"):
        raise ValueError("static ROM-call false positive")
    binary = OUT / "r0f-host-test"
    run(["/usr/bin/clang", "-std=c11", "-Wall", "-Wextra", "-Wconversion", "-Werror",
         "-fsanitize=address,undefined", "-DR0F_HOST_TEST", "-Iinterfaces/generated",
         "src/diagnostics/r0f/composite.c", "tools/diagnostics/r0f_host_test.c", "-o", binary])
    rejected = 0
    for failed in (False, True):
        b = run([binary] + (["fail-phase"] if failed else []), capture_output=True).stdout
        validate_result(b, failed)
        if b[160:240] != bytes((index * 17) % 256 for index in range(80)):
            raise ValueError("raw sample order/encoding")
        # Every fixed field must be checked independently of the byte checksum.
        # Raster samples are observations, so no value is a timing threshold.
        mutations = []
        for offset in (*range(160), *range(240, 255)):
            bad = bytearray(b)
            bad[offset] ^= 1
            bad[255] = sum(bad[:255]) % 256
            mutations.append((f"field {offset}", bad))
        bad = bytearray(b)
        bad[7] = 0
        bad[255] = sum(bad[:255]) % 256
        mutations.append(("functional failure with valid checksum", bad))
        bad = bytearray(b)
        bad[255] ^= 1
        mutations.extend([("checksum", bad), ("short", b[:-1]), ("long", b + b"\0")])
        for label, bad in mutations:
            try:
                validate_result(bad, failed)
            except ValueError:
                rejected += 1
            else:
                raise ValueError(f"validator accepted corrupted {label}")
        for value in (0, 255):
            observed = bytearray(b)
            observed[160:240] = bytes([value]) * 80
            observed[255] = sum(observed[:255]) % 256
            validate_result(observed, failed)
    report = {"result":"PASS", "tier":"native C with simulated raster, NOT Xemu",
              "cases":5, "phaseSamples":80, "timeoutInjection":"PASS",
              "failureRejection":"PASS", "sanitizers":"address,undefined",
              "rejectedMutations":rejected,
              "rawSampleEndpoints":"0 and 255 accepted; no timing threshold",
              "romTransferScanner":"PASS: ROM call/tail call rejected; local call/read allowed",
              "javaOracle":"NOT RUN; pinned JDK unavailable"}
    (OUT / "host-test.json").write_text(json.dumps(report, indent=2) + "\n")
    print("R0-F native functional/phase-timeout/negative tests PASS (not Xemu)")
    if TIMING:
        timing_host_test()
    if CAPTURE:
        capture_host_test()


def build():
    host_test()
    cc = TOOLS / "mos-mega65-clang"
    if sha(cc) != "cc557ae99a68ed36e098062b0f5376a878e94ac187b87446c8e603e4fb45a906":
        raise ValueError("pinned compiler hash mismatch")
    if sha(TOOLS / "llvm-objdump") != "5327f031a741bfcd4104317fbad3d1e45275d70b49821f0da52391120848a8e9":
        raise ValueError("pinned disassembler hash mismatch")
    artifact = OUT / "F65-R0F-PROOF.prg"
    mp = OUT / "F65-R0F-PROOF.map"
    extra = ["-DR0F_CIA_TIMING", "src/diagnostics/r0f/timing_sweep.c", "src/platform/r0f/cia_clock.c"] if TIMING else []
    if CAPTURE:
        extra += ["-DR0F_RAW_CAPTURE", "src/diagnostics/r0f/capture_view.c", "src/platform/r0f/capture_key.c"]
    run([cc, *extra, "-mcpu=mos45gs02", "-mlto-zp=0", "-Os", "-Wall", "-Wextra",
         "-Wconversion", "-Werror", "-Iinterfaces/generated", "src/r0f/main.c",
         "src/diagnostics/r0f/composite.c", "src/platform/r0f/raster_observation.c",
         "src/platform/r0a_platform_45gs02.s", "-Wl,-T,src/platform/r0f/startup.ld",
         f"-Wl,-Map,{mp}", "-o", artifact])
    for tool, options, suffix in [("llvm-nm", [], "symbols"),
                                  ("llvm-objdump", ["-d", "--print-imm-hex"], "disassembly")]:
        output = run([TOOLS / tool, *options, str(artifact)+".elf"], capture_output=True).stdout
        (OUT / f"F65-R0F-PROOF.{suffix}").write_bytes(output)
    text = mp.read_text()
    sections = {}
    for name in (".basic_header", ".text", ".rodata", ".data", ".bss", ".noinit", ".zp.data", ".zp.bss"):
        m = re.search(r"^\s*([0-9a-f]+)\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+" + re.escape(name) + r"$", text, re.M)
        if not m:
            raise ValueError(f"missing map section {name}")
        start, size = (int(x, 16) for x in m.groups())
        if size and (start < 0x2001 or start + size > 0xd000):
            raise ValueError(f"section outside admitted linked region: {name}")
        sections[name] = {"address":start, "bytes":size}
    occupied = sorted((s["address"], s["address"] + s["bytes"], name)
                      for name, s in sections.items() if s["bytes"])
    for previous, current in zip(occupied, occupied[1:]):
        if previous[1] > current[0]:
            raise ValueError(f"overlapping linked sections: {previous[2]}, {current[2]}")
    if not re.search(r"__stack = 0xd000", text):
        raise ValueError("unexpected software stack top")
    report = {"identity":json.loads(CONTRACT.read_text())["identity"],
              "sourceCommit":run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
              "sourceState":"working-tree; source hashes identify exact inputs",
              "inputs":{str(p.relative_to(ROOT)):sha(p) for p in [CONTRACT, ROOT/"interfaces/generated/r0f_interfaces.h", ROOT/"memory/r0f-memory-ledger.json", ROOT/"tools/diagnostics/r0f_build.py", ROOT/"tools/diagnostics/r0f_host_test.c", ROOT/"toolchain/f65_toolchain.lock.json", ROOT/"src/r0f/main.c", ROOT/"src/diagnostics/r0f/composite.c", ROOT/"src/platform/r0f/raster_observation.c", ROOT/"src/platform/r0f/startup.ld", ROOT/"src/platform/r0a_platform_45gs02.s"]},
              "compilerSha256":sha(cc), "prgSha256":sha(artifact), "prgBytes":artifact.stat().st_size,
              "sections":sections, "stackTop":53248, "stackHighWater":"NOT MEASURED",
              "linkedResidentBytes":sum(s["bytes"] for s in sections.values()),
              "compilerStaticStackBytes":sections[".noinit"]["bytes"],
              "reserveBytes":0, "dma":"NOT EXECUTED", "irq":"NOT MEASURED",
              "xemu":"NOT VERIFIED", "physical":"NOT VERIFIED", "d81":"NOT CREATED"}
    if TIMING:
        report["identity"] = json.loads(CONTRACT.read_text())["cia_timing"]["identity"]
        report["timing"] = "CIA counts; not calibrated SI or physical timing; reset-only timer ownership"
        for name in ("src/diagnostics/r0f/timing_sweep.c", "src/platform/r0f/cia_clock.c", "tools/diagnostics/r0f_timing_host_test.c", "tools/diagnostics/r0f_clock_host_test.c", "tools/generators/src/main/java/f65/tools/R0FTimingOracle.java", "docs/reports/R0-F_CIA_TIMING_CONTRACT.md"):
            report["inputs"][name] = sha(ROOT/name)
    if CAPTURE:
        report["identity"] = "R0F5-REV2-raw-count-screen-capture"
        for name in ("src/diagnostics/r0f/capture_view.c", "src/platform/r0f/capture_key.c",
                     "tools/diagnostics/r0f_capture_host_test.c",
                     "tools/generators/src/main/java/f65/tools/R0FCapturePages.java",
                     "docs/reports/R0-F_CAPTURE_CONTRACT.md"):
            report["inputs"][name] = sha(ROOT/name)
    (OUT / "build-accounting.json").write_text(json.dumps(report, indent=2)+"\n")
    print("R0-F LLVM-MOS compile/link/map/symbols/disassembly PASS; no D81 release")


def audit():
    """Build and review this standalone proof; never operate on a D81."""
    build()
    accounting = json.loads((OUT / "build-accounting.json").read_text())
    ledger = json.loads((ROOT / "memory/r0f-memory-ledger.json").read_text())
    sections = accounting["sections"]
    contract = json.loads(CONTRACT.read_text())
    allocations = {a["owner"]: a for a in ledger["allocations"]}
    if (allocations["R0-F result"]["bytes"] != contract["constants"]["RESULT_BYTES"]
            or int(allocations["R0-F result"]["range"].split("-")[0], 16)
            != contract["constants"]["RESULT_ADDRESS"]):
        raise ValueError("result contract/ledger disagreement")
    for owner, section in (("R0-F snapshot records", ".bss"),
                           ("R0-F compiler static stack", ".noinit")):
        if not TIMING and allocations[owner]["bytes"] != sections[section]["bytes"]:
            raise ValueError(f"ledger/linked storage disagreement: {owner}")
    if TIMING:
        variant = ledger["capture_variant" if CAPTURE else "cia_timing_variant"]
        if sections[".bss"]["bytes"] < variant["rawCaptureBytes"] + variant["sortingScratchBytes"] + 192:
            raise ValueError("timing storage missing from linked ledger")
        if sections[".bss"]["bytes"] != variant["linkedBssBytes"] or sections[".noinit"]["bytes"] != variant["compilerStaticStackBytes"]:
            raise ValueError("timing linked storage/ledger disagreement")
    if ledger["reserveBytes"] or ledger["dmaBytes"]:
        raise ValueError("unexpected reserve/DMA allocation")
    # Inspect instructions, not symbolic annotations (objdump may label ROM
    # targets relative to an unrelated linker symbol such as __heap_start).
    disassembly = (OUT / "F65-R0F-PROOF.disassembly").read_text()
    startup = disassembly.split("<_start>:", 1)[1].split("<main>:", 1)[0]
    if not re.search(r"lda\s+#\$2\s*\n[^\n]*\btab\b", startup):
        raise ValueError("B=$02 startup sequence missing")
    if TIMING:
        if re.search(r"^\s*[0-9a-f]+:[^\n]*\b(?:map|eom)\s*$", disassembly, re.M):
            raise ValueError("unadmitted mapping instruction")
        symbols = (OUT/"F65-R0F-PROOF.symbols").read_text()
        raw = re.search(r"^([0-9a-f]+) [bB] r0f_capture$", symbols, re.M)
        if not raw or not sections[".bss"]["address"] <= int(raw[1],16) <= sections[".bss"]["address"]+sections[".bss"]["bytes"]-10880:
            raise ValueError("raw capture outside charged BSS")
    rom_calls = rom_transfers(disassembly)
    findings = [{"id":"R0F-STATIC-STARTUP-001", "status":"BLOCKED",
                 "callAddress":"0x" + at, "target":"0x" + target,
                 "reason":"ROM call after B=$02 entry; separate B-save/B=$00/B-restore thunk admission and proof required",
                 "authority":"docs/decisions/R0-A-45GS02-B-REGISTER-INTEGRATION.md"}
                for at, target in rom_calls]
    # Revalidate retained result bytes, without mounting or touching the carrier.
    retained = json.loads((ROOT / "docs/evidence/r0f/xemu/evidence.json").read_text())
    for boot in retained["boots"]:
        validate_result(bytes.fromhex(boot["resultHex"]))
    prior = json.loads((ROOT / "docs/evidence/r0f/host/build-accounting.json").read_text())
    report = {"status":"BLOCKED" if findings else "PASS_BOUNDED_STATIC_ONLY",
              "scope":"bounded proxy static/host review only; not full R0-F acceptance",
              "hostResult":json.loads((OUT / "host-test.json").read_text()),
              "ledgerReconciliation":"PASS",
              "findings":findings,
              "prgMatchesRetainedBuild":accounting["prgSha256"] == prior["prgSha256"],
              "retainedXemuResultRevalidation":"PASS; two stored result blocks, not fresh boots",
              "artifacts":{p.name:sha(p) for p in [OUT/"build-accounting.json", OUT/"host-test.json", OUT/"F65-R0F-PROOF.prg", OUT/"F65-R0F-PROOF.map", OUT/"F65-R0F-PROOF.symbols", OUT/"F65-R0F-PROOF.disassembly"]},
              "limits":["No complete SI-calibrated measurement contract", "Dynamic stack high-water not measured", "Physical platform identity incomplete", "This audit performs no fresh Xemu or physical run", "No D81 operation"]}
    if TIMING:
        report["timingHostResult"] = json.loads((OUT/"timing-host-test.json").read_text())
    else:
        report["limits"].append("Java oracle not implemented/run for legacy REV1")
    if CAPTURE:
        report["captureHostResult"] = json.loads((OUT/"capture-host-test.json").read_text())
    (OUT / "step3-audit.json").write_text(json.dumps(report, indent=2) + "\n")
    if findings:
        raise ValueError(f"Step 3 BLOCKED: startup ROM call conflicts with B-register contract; see {OUT}/step3-audit.json")
    print("R0-F static audit recorded; owner/platform review still required")


def package():
    global MEDIA_OPERATION_STARTED
    # Mandatory root D81 contract controls this operation. Never copy/append.
    image = OUT / CARRIER_NAME
    if image.exists():
        raise ValueError("carrier identity already exists; never overwrite or silently rebuild")
    audit()
    lock = json.loads((ROOT / "toolchain/f65_toolchain.lock.json").read_text())
    petcat = ROOT / "toolchain/vice/VICE.app/Contents/Resources/bin/petcat"
    builder = ROOT / lock["r0d_d81_builder"]["c1541_relative_path"]
    if sha(petcat) != lock["vice"]["petcat_sha256"] or sha(builder) != lock["r0d_d81_builder"]["c1541_sha256"]:
        raise ValueError("pinned media tool identity mismatch")
    boot = OUT / "AUTOBOOT.C65"
    run([petcat, "-w65", "-o", boot, "--", ROOT/"src/r0f/autoboot.bas"], capture_output=True)
    listing = run([petcat, "-65", boot], capture_output=True)
    if listing.stderr or b'load "r0f-proof",8,1' not in listing.stdout.lower():
        raise ValueError("boot tokenizer/listing check")
    (OUT / "AUTOBOOT.listing").write_bytes(listing.stdout)
    evidence = OUT / "R0F-EVID.txt"
    evidence.write_bytes((OUT / "build-accounting.json").read_bytes())
    command = [builder, "-format", CARRIER_LABEL + ",65", "d81", image,
               "-write", boot, "autoboot.c65", "-write", OUT/"F65-R0F-PROOF.prg", "r0f-proof",
               "-write", evidence, "r0f-evid", "-list"]
    MEDIA_OPERATION_STARTED = True
    result = subprocess.run([str(a) for a in command], cwd=ROOT, capture_output=True)
    (OUT / "construction.stdout").write_bytes(result.stdout)
    (OUT / "construction.stderr").write_bytes(result.stderr)
    if result.returncode or result.stderr or re.search(rb"warning|error|failed|fatal|duplicate|truncat|allocation|opencbm", result.stdout, re.I):
        raise ValueError("INVALID carrier: construction diagnostic; preserve identity, do not reuse")
    run([sys.executable, ROOT/"tools/diagnostics/r0f_d81_loadability_gate.py", ROOT, image])


def xemu(prg_only=False):
    global MEDIA_OPERATION_STARTED
    missing = []
    if not (ROOT / "toolchain/xemu/xmega65").is_file():
        missing.append("pinned Xemu binary")
    import os
    if not os.environ.get("F65_MEGA65_ROM"):
        missing.append("owner ROM path F65_MEGA65_ROM")
    release = OUT / "manifests/r0f-d81-release.json"
    if not prg_only and not release.is_file():
        missing.append("host-verified R0-F D81")
    if missing:
        raise ValueError("XEMU NOT VERIFIED: " + "; ".join(missing))
    import shutil
    import tempfile
    import time
    emulator = ROOT / "toolchain/xemu/xmega65"
    rom = pathlib.Path(os.environ["F65_MEGA65_ROM"])
    sd = pathlib.Path(os.environ.get("F65_MEGA65_SD_IMAGE", ""))
    if not sd.is_file():
        raise ValueError("XEMU NOT VERIFIED: set F65_MEGA65_SD_IMAGE to initialized owner Xemu SD image (not physical device)")
    if sha(emulator) != "dd37baf7846b9696adcb662ffe5da040031b07214c66aef9a7f48cc30040b738" or sha(rom) != "af3c447f791a2fdc48cb21e1bd3fab015e32641228d9d30d21259b9e878c6fa0":
        raise ValueError("Xemu/ROM hash does not match pinned identity")
    image = OUT / ("F65-R0F-PROOF.prg" if prg_only else CARRIER_NAME)
    manifest = {"D81_STATE":"HOST_CONTENT_VERIFIED", "D81_SHA256":sha(image)} if prg_only else json.loads(release.read_text())
    if manifest["D81_STATE"] != "HOST_CONTENT_VERIFIED" or sha(image) != manifest["D81_SHA256"]:
        raise ValueError("host gate/immutable D81 identity mismatch")
    boots = []
    runner_hash = sha(pathlib.Path(__file__))
    evidence_name = os.environ.get("F65_XEMU_ATTEMPT", "xemu")
    if not re.fullmatch(r"xemu(?:-[a-z0-9-]+)?", evidence_name):
        raise ValueError("invalid Xemu evidence directory name")
    evidence = OUT / evidence_name
    evidence.mkdir(exist_ok=False)  # Fresh evidence only; never accept stale dumps.
    MEDIA_OPERATION_STARTED = not prg_only
    for label in ("boot1", "boot2"):
        screen, memory, screenshot = [evidence / (label+s) for s in (".screen.txt", ".memory.bin", ".png")]
        # A separate disposable initialized SD copy per process, never user media.
        with tempfile.TemporaryDirectory(prefix="r0f-xemu-") as temp:
            local_sd = pathlib.Path(temp) / "sd.img"
            shutil.copyfile(sd, local_sd)
            media_args = ["-prg", str(image)] if prg_only else ["-8", str(image), "-autoload"]
            args = [str(emulator), "-headless", "-sleepless", "-fastboot", "-rom", str(rom),
                    "-sdimg", str(local_sd), *media_args,
                    "-dumpscreen", str(screen), "-dumpmem", str(memory), "-screenshot", str(screenshot)]
            with (evidence / (label+".log")).open("wb") as log:
                process = subprocess.Popen(args, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
                try:
                    time.sleep(40)
                finally:
                    process.terminate()
                    try:
                        process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()
                        raise ValueError("Xemu did not terminate cleanly")
        block = memory.read_bytes()[0x1900:0x1a00]
        validate_result(block)
        if TIMING:
            raw_at = int.from_bytes(block[248:250], "little")
            raw_bytes = memory.read_bytes()[raw_at:raw_at+10880]
            java_oracle(block + raw_bytes, label+"-timing")
            if CAPTURE:
                pages = capture_verify(block + raw_bytes, label+"-capture")
                if pages[:2000] != memory.read_bytes()[0x800:0xfd0]:
                    raise ValueError("target capture screen differs from validated C formatter")
        displayed = screen.read_text(errors="replace").replace("{", "").replace("}", "")
        banners = ("R0-F CIA COUNT SWEEP - F65R0F4", "ACQUISITION: COMPLETE", "FUNCTIONAL FIXTURE: PASS") if TIMING else ("R0-F COMBINED-LOAD FUNCTIONAL PROXY", "FUNCTIONAL PASS", "F65R0F2 STARTUP FIX")
        if CAPTURE:
            banners = ("R0-F RAW CAPTURE - F65R0F5", "ACQUISITION COMPLETE", "FUNCTIONAL FIXTURE PASS")
        if any(banner not in displayed for banner in banners):
            raise ValueError("Xemu stable identity/pass banner absent")
        if not screenshot.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"):
            raise ValueError("Xemu screenshot missing")
        if re.search(r"(?:I/O|filesystem|disk).*error|failed to (?:mount|load)", (evidence/(label+".log")).read_text(errors="replace"), re.I):
            raise ValueError("Xemu media diagnostic failure")
        if sha(image) != manifest["D81_SHA256"]:
            raise ValueError("Xemu modified exact carrier")
        boots.append({"label":label, "arguments":args, "screenSha256":sha(screen), "memorySha256":sha(memory),
                      "screenshotSha256":sha(screenshot), "resultHex":block.hex()})
    # Functional portions must repeat; raster bytes need not be deterministic.
    if bytes.fromhex(boots[0]["resultHex"])[:144] != bytes.fromhex(boots[1]["resultHex"])[:144]:
        raise ValueError("clean-boot functional results differ")
    record = {"result":"PASS", "runnerSha256":runner_hash, "prgSha256" if prg_only else "d81Sha256":sha(image), "emulatorSha256":sha(emulator),
              "romSha256":sha(rom), "sdInputSha256":sha(sd), "boots":boots,
              "limitations":"No physical chooser, physical timing, IRQ, DMA, latency, or measured-limit evidence"}
    (evidence / "evidence.json").write_text(json.dumps(record, indent=2)+"\n")
    if not prg_only:
        manifest.update(D81_STATE="XEMU_BOOT_VERIFIED", XEMU_RESULT="PASS", XEMU_EVIDENCE=str(evidence/"evidence.json"))
        release.write_text(json.dumps(manifest, indent=2)+"\n")
    print("R0-F two clean Xemu " + ("direct-PRG" if prg_only else "D81") + " boots PASS; physical/SD gates NOT VERIFIED")


def recover_xemu_preflight():
    """Reclassify only the recorded pre-initialization config-permission error.

    This is not recovery from a carrier, mount, payload or runtime failure.
    Preserve the erroneous runner label and all logs for audit.
    """
    release = OUT / "manifests/r0f-d81-release.json"
    manifest = json.loads(release.read_text())
    evidence = OUT / "xemu"
    log = (evidence / "boot1.log").read_text()
    expected = "ERROR: Cannot save config template\nCannot create file: @mega65-template.cfg.TMP\nOperation not permitted\n"
    if (not log.startswith(expected) or "D81:" in log or "SDCARD:" in log
            or "MEM:" in log or "FILE:" in log
            or any(evidence.glob("*.memory.bin")) or any(evidence.glob("*.png"))):
        raise ValueError("not the known pre-initialization environment failure")
    if (manifest["D81_STATE"] != "INVALID — DO NOT USE"
            or manifest.get("operation") != "xemu"
            or manifest.get("error") != f"[Errno 2] No such file or directory: '{evidence}/boot1.memory.bin'"
            or manifest["HOST_STRUCTURAL_RESULT"] != "PASS"
            or manifest["HOST_CONTENT_RESULT"] != "PASS"
            or sha(OUT / CARRIER_NAME) != manifest["D81_SHA256"]):
        raise ValueError("environment recovery identity mismatch")
    record = {"classification":"XEMU_ENVIRONMENT_NOT_VERIFIED_CARRIER_NOT_EXERCISED",
              "reason":"Configuration template write denied before emulator memory/media initialization; absent dump was incorrectly classified as carrier failure by the generic runner handler",
              "previousRelease":manifest.copy(), "logSha256":sha(evidence/"boot1.log"),
              "carrierSha256":sha(OUT/CARRIER_NAME),
              "authorization":"Owner requested continuation and Xemu tests; no failed carrier is repaired or reused"}
    with (OUT / "xemu-environment-review.json").open("x") as stream:
        stream.write(json.dumps(record, indent=2) + "\n")
    manifest.update(D81_STATE="HOST_CONTENT_VERIFIED", XEMU_RESULT="NOT VERIFIED: environment preflight failure",
                    XEMU_ENVIRONMENT_REVIEW=str(OUT/"xemu-environment-review.json"))
    del manifest["error"]
    del manifest["operation"]
    release.write_text(json.dumps(manifest, indent=2) + "\n")
    print("Preserved preflight failure; carrier unchanged and not yet Xemu-tested")


if __name__ == "__main__":
    try:
        action = sys.argv[1] if len(sys.argv) == 2 else ""
        {"generate":generate, "host-test":host_test, "build":build, "audit":audit, "package":package, "xemu":xemu, "xemu-prg":lambda: xemu(prg_only=True), "recover-xemu-preflight":recover_xemu_preflight}[action]()
    except (KeyError, ValueError, OSError, subprocess.CalledProcessError) as e:
        if MEDIA_OPERATION_STARTED:
            # Preserve the failed identity and all output, never automatically retry.
            failure = {"D81_STATE":"INVALID — DO NOT USE", "error":str(e), "operation":action}
            image = OUT / CARRIER_NAME
            if image.is_file():
                failure.update(D81_FILENAME=image.name, D81_SHA256=sha(image))
            (OUT / "carrier-failure.json").write_text(json.dumps(failure, indent=2)+"\n")
            release = OUT / "manifests/r0f-d81-release.json"
            if release.is_file():
                manifest = json.loads(release.read_text())
                manifest.update(failure)
                release.write_text(json.dumps(manifest, indent=2)+"\n")
        print(f"R0-F stopped: {e}", file=sys.stderr)
        sys.exit(2)
