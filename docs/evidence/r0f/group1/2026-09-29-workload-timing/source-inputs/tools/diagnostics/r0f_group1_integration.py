#!/usr/bin/env python3
"""Build the Group 1 acquisition variant using the admitted successor pipeline."""
import r0f_group1_contract as contract
import r0f_group1_export_probe as probe


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
                out=output, prg_name="GROUP1.prg", extra_sources=sources)


if __name__ == "__main__":
    build()
