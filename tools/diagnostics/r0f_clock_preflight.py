#!/usr/bin/env python3
"""Build/run the host-only clock preflight. No target, D81, or SD operations."""
import argparse
import hashlib
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
JAVA_SHA256 = "34b9c157bedcebafc6033b8beaa72c2ff14e2b697e33f45aa959a8373d6581a0"
PROFILE = "b5c770c6-ntsc-526-no-debug"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--java-home", type=pathlib.Path, required=True)
    parser.add_argument("--capture", type=pathlib.Path, required=True)
    parser.add_argument("--sha256", required=True, help="independently retained expected capture hash")
    args = parser.parse_args()
    java = args.java_home / "bin/java"
    javac = args.java_home / "bin/javac"
    if sha(java) != JAVA_SHA256:
        raise ValueError("Java binary differs from the retained F5 validator identity")
    version = subprocess.run([java, "-version"], check=True, capture_output=True, text=True).stderr
    if "Temurin-21.0.12+8" not in version:
        raise ValueError("wrong Java runtime version")
    out = ROOT / "build/r0f/clock-preflight"
    classes = out / "classes"
    classes.mkdir(parents=True, exist_ok=True)
    sources = [ROOT / f"tools/generators/src/main/java/f65/tools/{name}.java"
               for name in ("R0FTimingOracle", "R0FClockPreflight")]
    compile_command = [str(javac), "-Xlint:all", "-Werror", "-d", str(classes), *map(str, sources)]
    subprocess.run(compile_command, check=True, cwd=ROOT)
    base = [str(java), "-cp", str(classes)]
    commands = [
        base + ["f65.tools.R0FTimingOracle", str(args.capture)],
        base + ["f65.tools.R0FClockPreflight", "--self-test", str(args.capture), args.sha256],
        base + ["f65.tools.R0FClockPreflight", "--inspect", str(args.capture), args.sha256, PROFILE],
    ]
    outputs = [subprocess.run(cmd, check=True, cwd=ROOT, capture_output=True, text=True).stdout
               for cmd in commands]
    report = json.loads(outputs[2])
    assert report["calibrationValid"] is False and report["combinedHardwareReady"] is False
    files = {"raw-oracle.txt": outputs[0], "self-test.txt": outputs[1], "preflight.json": outputs[2]}
    for name, content in files.items():
        (out / name).write_text(content)
    manifest = {
        "status": "HOST_PREFLIGHT_BUILT_NOT_COMBINED_TARGET",
        "javaVersion": version.strip(), "javaSha256": sha(java),
        "javacSha256": sha(javac), "javaReleaseSha256": sha(args.java_home / "release"),
        "sourceSha256": {str(p.relative_to(ROOT)): sha(p) for p in [*sources, pathlib.Path(__file__)]},
        "captureSha256": report["captureSha256"],
        "commands": [compile_command, *commands],
        "outputSha256": {name: sha(out / name) for name in files},
        "targetBuild": "NOT_RUN_NO_TARGET_CHANGE",
        "xemu": "NOT_RUN_NO_NEW_TARGET_OR_CARRIER",
        "physical": "EXISTING_F5_CAPTURE_READ_ONLY_NO_NEW_TEST",
        "calibration": "NOT_QUALIFIED",
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(outputs[0].strip())
    print(outputs[1].strip())
    print("HOST PREFLIGHT BUILT; combined target NOT BUILT; calibration NOT QUALIFIED")
    print(out / "preflight.json")


if __name__ == "__main__":
    main()
