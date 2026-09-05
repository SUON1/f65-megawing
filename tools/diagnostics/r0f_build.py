#!/usr/bin/env python3
"""Bounded R0-F source build and native functional regression (no media writes)."""
import hashlib
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "build/r0f"
TOOLS = ROOT / "toolchain/runtime/llvm-mos/bin"
CONTRACT = ROOT / "interfaces/r0f_proof_contract.json"
MEDIA_OPERATION_STARTED = False


def run(args, **kwargs):
    return subprocess.run([str(a) for a in args], cwd=ROOT, check=True, **kwargs)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generate():
    c = json.loads(CONTRACT.read_text())
    header = "/* Generated from interfaces/r0f_proof_contract.json. */\n"
    header += "#ifndef F65_R0F_INTERFACES_H\n#define F65_R0F_INTERFACES_H\n"
    header += "".join(f"#define R0F_{k} {v}u\n" for k, v in c["constants"].items())
    header += "#endif\n"
    (ROOT / "interfaces/generated/r0f_interfaces.h").write_text(header)
    OUT.mkdir(parents=True, exist_ok=True)


def validate_result(b, failed_phase=False):
    if len(b) != 256 or b[:7] != b"R0F1\x01\x64\x15":
        raise ValueError("result identity/length")
    if b[7] != 127 or sum(b[:255]) % 256 != b[255]:
        raise ValueError("functional status or result checksum")
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


def host_test():
    generate()
    binary = OUT / "r0f-host-test"
    run(["/usr/bin/clang", "-std=c11", "-Wall", "-Wextra", "-Wconversion", "-Werror",
         "-fsanitize=address,undefined", "-DR0F_HOST_TEST", "-Iinterfaces/generated",
         "src/diagnostics/r0f/composite.c", "tools/diagnostics/r0f_host_test.c", "-o", binary])
    for failed in (False, True):
        b = run([binary] + (["fail-phase"] if failed else []), capture_output=True).stdout
        validate_result(b, failed)
        if b[160:240] != bytes((index * 17) % 256 for index in range(80)):
            raise ValueError("raw sample order/encoding")
        bad = bytearray(b)
        bad[7] = 0
        bad[255] = sum(bad[:255]) % 256
        try:
            validate_result(bad, failed)
        except ValueError:
            pass
        else:
            raise ValueError("validator accepted functional failure")
    report = {"result":"PASS", "tier":"native C with simulated raster, NOT Xemu",
              "cases":5, "phaseSamples":80, "timeoutInjection":"PASS",
              "failureRejection":"PASS", "sanitizers":"address,undefined",
              "javaOracle":"NOT RUN; pinned JDK unavailable"}
    (OUT / "host-test.json").write_text(json.dumps(report, indent=2) + "\n")
    print("R0-F native functional/phase-timeout/negative tests PASS (not Xemu)")


def build():
    host_test()
    cc = TOOLS / "mos-mega65-clang"
    if sha(cc) != "cc557ae99a68ed36e098062b0f5376a878e94ac187b87446c8e603e4fb45a906":
        raise ValueError("pinned compiler hash mismatch")
    if sha(TOOLS / "llvm-objdump") != "5327f031a741bfcd4104317fbad3d1e45275d70b49821f0da52391120848a8e9":
        raise ValueError("pinned disassembler hash mismatch")
    artifact = OUT / "F65-R0F-PROOF.prg"
    mp = OUT / "F65-R0F-PROOF.map"
    run([cc, "-mcpu=mos45gs02", "-mlto-zp=0", "-Os", "-Wall", "-Wextra",
         "-Wconversion", "-Werror", "-Iinterfaces/generated", "src/r0f/main.c",
         "src/diagnostics/r0f/composite.c", "src/platform/r0f/raster_observation.c",
         "src/platform/r0a_platform_45gs02.s", f"-Wl,-Map,{mp}", "-o", artifact])
    for tool, options, suffix in [("llvm-nm", [], "symbols"),
                                  ("llvm-objdump", ["-d", "--print-imm-hex"], "disassembly")]:
        output = run([TOOLS / tool, *options, str(artifact)+".elf"], capture_output=True).stdout
        (OUT / f"F65-R0F-PROOF.{suffix}").write_bytes(output)
    text = mp.read_text()
    sections = {}
    for name in (".text", ".rodata", ".data", ".bss"):
        m = re.search(r"^\s*([0-9a-f]+)\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+" + re.escape(name) + r"$", text, re.M)
        if not m:
            raise ValueError(f"missing map section {name}")
        start, size = (int(x, 16) for x in m.groups())
        if size and (start < 0x2001 or start + size > 0xd000):
            raise ValueError(f"section outside admitted linked region: {name}")
        sections[name] = {"address":start, "bytes":size}
    if not re.search(r"__stack = 0xd000", text):
        raise ValueError("unexpected software stack top")
    report = {"identity":json.loads(CONTRACT.read_text())["identity"],
              "sourceCommit":run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
              "sourceState":"working-tree; source hashes identify exact inputs",
              "inputs":{str(p.relative_to(ROOT)):sha(p) for p in [CONTRACT, ROOT/"interfaces/generated/r0f_interfaces.h", ROOT/"src/r0f/main.c", ROOT/"src/diagnostics/r0f/composite.c", ROOT/"src/platform/r0f/raster_observation.c", ROOT/"src/platform/r0a_platform_45gs02.s"]},
              "compilerSha256":sha(cc), "prgSha256":sha(artifact), "prgBytes":artifact.stat().st_size,
              "sections":sections, "stackTop":53248, "stackHighWater":"NOT MEASURED",
              "reserveBytes":0, "dma":"NOT EXECUTED", "irq":"NOT MEASURED",
              "xemu":"NOT VERIFIED", "physical":"NOT VERIFIED", "d81":"NOT CREATED"}
    (OUT / "build-accounting.json").write_text(json.dumps(report, indent=2)+"\n")
    print("R0-F LLVM-MOS compile/link/map/symbols/disassembly PASS; no D81 release")


def package():
    global MEDIA_OPERATION_STARTED
    # Mandatory root D81 contract controls this operation. Never copy/append.
    image = OUT / "F65R0F1.D81"
    if image.exists():
        raise ValueError("carrier identity already exists; never overwrite or silently rebuild")
    build()
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
    command = [builder, "-format", "F65 R0-F1,65", "d81", image,
               "-write", boot, "autoboot.c65", "-write", OUT/"F65-R0F-PROOF.prg", "r0f-proof",
               "-write", evidence, "r0f-evid", "-list"]
    MEDIA_OPERATION_STARTED = True
    result = subprocess.run([str(a) for a in command], cwd=ROOT, capture_output=True)
    (OUT / "construction.stdout").write_bytes(result.stdout)
    (OUT / "construction.stderr").write_bytes(result.stderr)
    if result.returncode or result.stderr or re.search(rb"warning|error|failed|fatal|duplicate|truncat|allocation|opencbm", result.stdout, re.I):
        raise ValueError("INVALID carrier: construction diagnostic; preserve identity, do not reuse")
    run([sys.executable, ROOT/"tools/diagnostics/r0f_d81_loadability_gate.py", ROOT, image])


def xemu():
    global MEDIA_OPERATION_STARTED
    missing = []
    if not (ROOT / "toolchain/xemu/xmega65").is_file():
        missing.append("pinned Xemu binary")
    import os
    if not os.environ.get("F65_MEGA65_ROM"):
        missing.append("owner ROM path F65_MEGA65_ROM")
    release = OUT / "manifests/r0f-d81-release.json"
    if not release.is_file():
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
    manifest = json.loads(release.read_text())
    image = OUT / "F65R0F1.D81"
    if manifest["D81_STATE"] != "HOST_CONTENT_VERIFIED" or sha(image) != manifest["D81_SHA256"]:
        raise ValueError("host gate/immutable D81 identity mismatch")
    boots = []
    evidence = OUT / "xemu"
    evidence.mkdir(exist_ok=False)  # Fresh evidence only; never accept stale dumps.
    MEDIA_OPERATION_STARTED = True
    for label in ("boot1", "boot2"):
        screen, memory, screenshot = [evidence / (label+s) for s in (".screen.txt", ".memory.bin", ".png")]
        # A separate disposable initialized SD copy per process, never user media.
        with tempfile.TemporaryDirectory(prefix="r0f-xemu-") as temp:
            local_sd = pathlib.Path(temp) / "sd.img"
            shutil.copyfile(sd, local_sd)
            args = [str(emulator), "-headless", "-sleepless", "-fastboot", "-rom", str(rom),
                    "-sdimg", str(local_sd), "-8", str(image), "-autoload",
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
        displayed = screen.read_text(errors="replace").replace("{", "").replace("}", "")
        if "R0-F COMBINED-LOAD FUNCTIONAL PROXY" not in displayed or "FUNCTIONAL PASS" not in displayed:
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
    record = {"result":"PASS", "d81Sha256":sha(image), "emulatorSha256":sha(emulator),
              "romSha256":sha(rom), "sdInputSha256":sha(sd), "boots":boots,
              "limitations":"No physical chooser, physical timing, IRQ, DMA, latency, or measured-limit evidence"}
    (evidence / "evidence.json").write_text(json.dumps(record, indent=2)+"\n")
    manifest.update(D81_STATE="XEMU_BOOT_VERIFIED", XEMU_RESULT="PASS", XEMU_EVIDENCE=str(evidence/"evidence.json"))
    release.write_text(json.dumps(manifest, indent=2)+"\n")
    print("R0-F two clean Xemu boots PASS; physical/SD gates NOT VERIFIED")


if __name__ == "__main__":
    try:
        action = sys.argv[1] if len(sys.argv) == 2 else ""
        {"generate":generate, "host-test":host_test, "build":build, "package":package, "xemu":xemu}[action]()
    except (KeyError, ValueError, OSError, subprocess.CalledProcessError) as e:
        if MEDIA_OPERATION_STARTED:
            # Preserve the failed identity and all output, never automatically retry.
            failure = {"D81_STATE":"INVALID — DO NOT USE", "error":str(e), "operation":action}
            image = OUT / "F65R0F1.D81"
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
