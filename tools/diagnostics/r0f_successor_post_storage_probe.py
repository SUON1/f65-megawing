#!/usr/bin/env python3
"""Run the current successor PRG in Xemu without making a release carrier.

MANDATORY D81 LOADABILITY GATE: read 00_D81_LOADABILITY_GATE.md before use.
The token-only D81s here are fresh disposable development fixtures, not SD or
physical candidates. Never substitute their result for exact-carrier proof.
"""

import json
from pathlib import Path

import r0f_successor_emulator as runtime


ROOT = runtime.ROOT
OUT = ROOT / "build/r0f/successor-post-storage-first-fault-probe"
LABEL = "R0F DEV T07"
NAME = "R0FDEV07.D81"


def main():
    if OUT.exists():
        raise ValueError("refusing to overwrite first-fault probe evidence")
    accounting = json.loads(runtime.ACCOUNTING.read_text())
    prg_bytes = runtime.PRG.stat().st_size
    prg_sha = runtime.sha256(runtime.PRG)
    if (accounting["prgBytes"] != prg_bytes
            or accounting["prgSha256"] != prg_sha):
        raise ValueError("target PRG/accounting identity mismatch")

    runtime.OUT = OUT
    runtime.EXPECTED_PRG_BYTES = prg_bytes
    runtime.EXPECTED_PRG_SHA256 = prg_sha
    runtime.SOURCE_BRANCH = runtime.git_text("branch", "--show-current")
    runtime.EXPECTED_SCREEN_LINES = (
        "DEVELOPMENT EVIDENCE - NOT R0-F ACCEPTANCE",
        "SUCCESSOR HOST/STATIC IMAGE - RUNTIME UNVERIFIED",
        "FAULT   STATE   TICK    MASK  NMI",
        "RESERVE BEFORE   RESERVE AFTER",
        "RESULT CRC32",
    )
    runtime.require_target_identity()
    OUT.mkdir(parents=True)
    classes = OUT / "classes"
    classes.mkdir()
    runtime.checked_run([
        runtime.platform_build.JAVA / "javac", "-Xlint:all", "-Werror",
        "-d", classes, ROOT / runtime.ORACLE_SOURCE,
    ])

    runs = []
    for mode, name in (("1", "ntsc"), ("0", "pal")):
        directory = OUT / name
        directory.mkdir()
        token = directory / "TOKEN.prg"
        token.write_bytes(runtime.token_bytes())
        image = directory / NAME
        initial = runtime.fresh_d81(
            directory, image, LABEL, {"token": token}
        )
        result, environment = runtime.run_xemu(
            directory, mode, image, "DIRECT_PRG_DEVELOPMENT", False
        )
        evidence = runtime.finish_success_run(
            directory, image, result,
            {
                **environment,
                "sourceBranch": runtime.SOURCE_BRANCH,
                "sourceCommit": runtime.source_commit(),
                "prgSha256": prg_sha,
                "initialD81Sha256": initial["sha256"],
                "canonicalCarrier": False,
            },
            {"token": token.read_bytes()}, LABEL,
        )
        runs.append({
            "mode": name,
            "result": "PASS",
            "fault": evidence["result"]["fault"],
            "prgSha256": prg_sha,
            "fixtureSha256": initial["sha256"],
            "evidence": str((directory / "evidence.json").relative_to(ROOT)),
        })
    runtime.write_json(OUT / "summary.json", {
        "result": "PASS",
        "tier": "DIRECT_PRG_DEVELOPMENT_NOT_CARRIER",
        "prgBytes": prg_bytes,
        "prgSha256": prg_sha,
        "runs": runs,
        "sd": "NOT RUN",
        "physical": "NOT RUN",
        "fullAcceptance": False,
    })
    print("R0-F first-fault direct-PRG NTSC/PAL Xemu probe PASS")
    print("prg_sha256=" + prg_sha)
    print("D81 SD / physical NOT RUN")


if __name__ == "__main__":
    main()
