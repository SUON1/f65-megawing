#!/usr/bin/env python3
"""Build the Group 1 acquisition variant using the admitted successor pipeline."""
import re

import r0f_group1_contract as contract
import r0f_group1_export_probe as probe


def validate_irq(disassembly):
    handler = disassembly.split("<r0f_pf_irq>:", 1)[1].split("<r0f_pf_nmi>:", 1)[0]
    instructions = re.findall(r"\t([a-z]+)(?:\t[^\n]*)?\s*$", handler, re.M)
    if instructions[:6] != ["pha", "phx", "phy", "phz", "tba", "pha"] or instructions[-7:] != ["pla", "tab", "plz", "ply", "plx", "pla", "rti"]:
        raise ValueError("IRQ register preservation changed")
    calls = re.findall(r"\bjsr\s+\$[0-9a-f]+ <([^>]+)>", handler)
    if calls != ["r0fg1_irq_begin", "r0fg1_irq_end"]:
        raise ValueError("unexpected IRQ body calls")
    probes = disassembly.split("<r0fg1_irq_begin>:", 1)[1].split("<r0fg1_irq_timing_end>:", 1)[0]
    if re.search(r"\b(?:map|tab|cli|rti)\b", probes) or re.search(r"\b(?:sta|stx|sty|stz|inc|dec)\s+\$d[0-9a-f]{3}\b", probes):
        raise ValueError("IRQ probe changes hardware ownership")
    if set(re.findall(r"\bjsr\s+\$[0-9a-f]+ <([^>]+)>", probes)) != {"r0fg1_irq_read"}:
        raise ValueError("IRQ probe calls outside private reader")


def build():
    contract.generate()
    output = probe.ROOT / "build/r0f/group1/integration"
    sources = [name for name in probe.EXTRA_SOURCES
                           if not name.endswith("group1_export_probe.c")]
    sources += [
        "src/diagnostics/r0f/group1_capture.c",
        "src/diagnostics/r0f/group1_timing.c",
        "src/diagnostics/r0f/group1_workload.c",
    ]
    probe.build(["-DR0FG1_INTEGRATION"],
                "Group 1 phase/timing acquisition; physical and full coverage unverified",
                out=output, prg_name="GROUP1.prg", extra_sources=sources,
                source_replacements={"src/platform/r0f/qualification_45gs02.s":
                                     "src/platform/r0f/group1_irq_45gs02.s"})
    validate_irq((output / "disassembly.txt").read_text())
    report = probe.emulator.read_json(output / "build.json")
    for name in ("tools/diagnostics/r0f_group1_integration.py",
                 "tools/diagnostics/r0f_group1_contract.py"):
        report["inputs"][name] = probe.emulator.sha256(probe.ROOT / name)
    report["irqProbeStatic"] = "PASS"
    probe.emulator.write_json(output / "build.json", report)
    print("IRQ assembly boundaries and no-C/no-hardware-write checks PASS")


if __name__ == "__main__":
    build()
