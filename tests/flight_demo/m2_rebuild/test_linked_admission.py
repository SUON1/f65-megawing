"""Raw image/branch regressions preserve the original failed link packet."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/flight_demo/m2_rebuild"))
from linked_admission import check_initialization, check_load, elf_sections
from stack_admission import parse

PACKET = ROOT / "docs/evidence/flight-demo/2026-10-30-m2-extended-resident/target-1793404701167257000"


class LinkedAdmission(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in PACKET.iterdir() if p.is_file()}
        cls.prg = (PACKET / "UNADMITTED.prg").read_bytes()
        cls.elf = (PACKET / "UNADMITTED.prg.elf").read_bytes()
        cls.result = json.loads((PACKET / "result.json").read_text())

    def test_actual_load_extends_past_8000_with_unloaded_bss_and_scratch(self):
        report = check_load(self.prg, self.elf, self.result)
        self.assertGreater(report["payload_end"], 0x8000)
        self.assertEqual(report["executable_section_bytes_above_8000"], 0)
        sections = elf_sections(self.elf)
        self.assertEqual(sections[".bss"]["type"], 8)
        self.assertEqual(sections[".noinit"]["type"], 8)

    def test_missing_changed_extended_payload_and_accounting_rejected(self):
        changed = bytearray(self.prg)
        changed[0x8000 - 0x2001 + 2] ^= 1
        for prg in [self.prg[:-1], bytes(changed), b"\x00\x20" + self.prg[2:]]:
            with self.subTest(size=len(prg)), self.assertRaises(ValueError):
                check_load(prg, self.elf, self.result)
        incorrect = dict(self.result, resident_bytes=self.result["resident_bytes"] - 1)
        with self.assertRaisesRegex(ValueError, "accounting"):
            check_load(self.prg, self.elf, incorrect)

    def test_original_global_relative_startup_branch_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "instruction boundary"):
            check_initialization(self.prg, (PACKET / "UNADMITTED.disassembly").read_text(),
                                 (PACKET / "UNADMITTED.symbols").read_text())

    def test_corrected_initialization_and_bypassed_callsite(self):
        correct = PACKET.parent / "target-1793405200824046000"
        prg = (correct / "UNADMITTED.prg").read_bytes()
        disassembly = (correct / "UNADMITTED.disassembly").read_text()
        symbols = (correct / "UNADMITTED.symbols").read_text()
        self.assertEqual(check_initialization(prg, disassembly, symbols)["status"], "PASS")
        _, names = parse(disassembly, symbols)
        origin = int.from_bytes(prg[:2], "little")
        for site in ["__do_zero_bss", "__do_init_stack"]:
            with self.subTest(site=site):
                changed = bytearray(prg)
                changed[names[site] - origin + 2] = 0xea
                with self.assertRaisesRegex(ValueError, "callsite bypassed|fall through"):
                    check_initialization(bytes(changed), disassembly, symbols)

    def test_zz_failed_packet_remains_sealed(self):
        self.assertEqual(self.before, {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                     for p in PACKET.iterdir() if p.is_file()})


if __name__ == "__main__":
    unittest.main()
