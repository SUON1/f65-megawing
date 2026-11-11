"""Fail closed for dead symbols and incomplete target composition."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location("compact_check", ROOT / "tools/flight_demo/m2_rebuild/compact_check.py")
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class LinkedClosure(unittest.TestCase):
    def fixture(self):
        names = ["main", *CHECKER.REQUIRED]
        symbols = "\n".join(f"{0x2000 + i * 4:08x} 00000004 T {name}" for i, name in enumerate(names))
        assembly = "\n".join(f" {0x2000 + i * 4:x}: 20 00 00 jsr ${0x2000 + (i + 1) * 4:x}\n"
                             f" {0x2003 + i * 4:x}: 60 rts" for i in range(len(names) - 1))
        assembly += f"\n {0x2000 + (len(names)-1)*4:x}: 60 rts\n"
        return assembly, symbols

    def test_complete_without_old_ground_symbol(self):
        assembly, symbols = self.fixture()
        self.assertNotIn("m2_ground_prepared", symbols)
        self.assertEqual(CHECKER.check(assembly, symbols)["required_reachable"], CHECKER.REQUIRED)

    def test_missing_behavior_fails(self):
        assembly, symbols = self.fixture()
        with self.assertRaisesRegex(ValueError, "missing required"):
            CHECKER.check(assembly, symbols.replace("m2l_service", "unrelated"))

    def test_native_batch_retention_fails(self):
        assembly, symbols = self.fixture()
        for name in ["m2_prepare", "m2_ground_prepared", "__muldi3", "__udivdi3"]:
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "batch/native-wide"):
                CHECKER.check(assembly, symbols + f"\n00004000 00000001 T {name}")

    def test_present_but_dead_fails(self):
        assembly, symbols = self.fixture()
        with self.assertRaisesRegex(ValueError, "not reachable"):
            CHECKER.check(assembly.replace("2000: 20 00 00 jsr $2004", "2000: 4c 00 20 jmp $2000"), symbols)

    def test_indirect_transfer_is_not_evidence_of_reachability(self):
        assembly, symbols = self.fixture()
        with self.assertRaisesRegex(ValueError, "not reachable"):
            CHECKER.check(assembly.replace("2000: 20 00 00 jsr $2004", "2000: 6c 04 20 jmp ($2004)"), symbols)


if __name__ == "__main__":
    unittest.main()
