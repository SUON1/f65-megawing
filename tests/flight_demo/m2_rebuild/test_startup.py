"""Replay the pinned link and mutate only memory; never write sealed artifacts."""
import hashlib
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
PACKET = ROOT / "docs/evidence/flight-demo/2026-10-27-m2-min-rebuild/target-1793158803095519000"
SPEC = importlib.util.spec_from_file_location("m2rb_startup", ROOT / "tools/flight_demo/m2_rebuild/startup_check.py")
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class Startup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.disassembly = (PACKET / "UNADMITTED.disassembly").read_text()
        cls.symbols = (PACKET / "UNADMITTED.symbols").read_text()
        cls.prg = (PACKET / "UNADMITTED.prg").read_bytes()
        cls.handler = 0x227e
        cls.handler_offset = cls.handler - int.from_bytes(cls.prg[:2], "little") + 2
        cls.inventory = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in PACKET.iterdir() if p.is_file()}

    def test_normalized_boundary_is_first_stack_instruction(self):
        result = CHECKER.check_normal_prefix(self.disassembly, self.symbols)
        self.assertEqual(result["normal_entry_ordering"], "PASS")
        self.assertEqual(result["runtime_startup_admission"].split(";")[0], "UNPROVEN")

    def test_earlier_stack_initialization_rejected(self):
        modified = self.symbols.replace("00002078 00000000 T __do_init_stack", "00002076 00000000 T __do_init_stack")
        with self.assertRaisesRegex(ValueError, "precedes"):
            CHECKER.check_normal_prefix(self.disassembly, modified)

    def test_bypassed_entry_rejected(self):
        modified = self.symbols.replace("00002017 00000000 T _start", "00002078 00000000 T _start")
        with self.assertRaisesRegex(ValueError, "bypasses"):
            CHECKER.check_normal_prefix(self.disassembly, modified)

    def test_wrong_cpu_port_rejected(self):
        modified = self.disassembly.replace("lda\t#$35", "lda\t#$34", 1)
        with self.assertRaisesRegex(ValueError, "CPU-port"):
            CHECKER.check_normal_prefix(modified, self.symbols)

    def test_wrong_io_map_rejected(self):
        modified = self.disassembly.replace("lda\t#$44", "lda\t#$64", 1)
        with self.assertRaisesRegex(ValueError, "initialization differs"):
            CHECKER.check_normal_prefix(modified, self.symbols)

    def test_missing_map_rejected(self):
        modified = self.disassembly.replace("map\n", "clc\n", 1)
        with self.assertRaisesRegex(ValueError, "prefix differs"):
            CHECKER.check_normal_prefix(modified, self.symbols)

    def handler_prg(self, code):
        """Patch only an in-memory copy of the pinned four-byte handler."""
        modified = bytearray(self.prg)
        modified[self.handler_offset:self.handler_offset + 4] = code
        return bytes(modified)

    def test_absolute_terminal_loop_raw_bytes_accepted(self):
        # This is a synthetic byte mutation, not a relink or target proof.
        prg = self.handler_prg(b"\x78\x4c" + self.handler.to_bytes(2, "little"))
        result = CHECKER.check(self.disassembly, self.symbols, prg)
        self.assertEqual(result["terminal_handler_control_flow"], "PASS")
        self.assertEqual(result["terminal_handler_target"], self.handler)
        self.assertEqual(result["terminal_handler_bytes"], "784c7e22")
        self.assertTrue(result["runtime_startup_admission"].startswith("UNPROVEN"))

    def test_historical_unsafe_handler_rejected(self):
        # Its disassembler annotation names the handler despite targeting the
        # preceding RTS. Prefix ordering alone remains independently testable.
        self.assertEqual(self.prg[self.handler_offset:self.handler_offset + 4], b"\x78\x83\xfc\xff")
        with self.assertRaisesRegex(ValueError, "terminal handler"):
            CHECKER.check(self.disassembly, self.symbols, self.prg)

    def test_full_check_requires_raw_prg(self):
        with self.assertRaisesRegex(ValueError, "raw PRG bytes required"):
            CHECKER.check(self.disassembly, self.symbols)

    def test_off_by_one_terminal_targets_rejected(self):
        for delta in [-1, 1]:
            with self.subTest(delta=delta):
                prg = self.handler_prg(b"\x78\x4c" + (self.handler + delta).to_bytes(2, "little"))
                with self.assertRaisesRegex(ValueError, "JMP target"):
                    CHECKER.check(self.disassembly, self.symbols, prg)

    def test_return_or_fallthrough_rejected(self):
        for code in [b"\x78\x60\xea\xea", b"\x78\xea\xea\xea"]:
            with self.subTest(code=code.hex()):
                with self.assertRaisesRegex(ValueError, "terminal handler"):
                    CHECKER.check(self.disassembly, self.symbols, self.handler_prg(code))

    def test_changed_branch_rejected(self):
        for opcode in [0x80, 0x83, 0x6c]:
            with self.subTest(opcode=opcode):
                prg = self.handler_prg(bytes([0x78, opcode, 0x7e, 0x22]))
                with self.assertRaisesRegex(ValueError, "terminal handler"):
                    CHECKER.check(self.disassembly, self.symbols, prg)

    def test_missing_branch_bytes_rejected(self):
        prg = self.prg[:self.handler_offset + 1]
        with self.assertRaisesRegex(ValueError, "terminal-handler bytes missing"):
            CHECKER.check(self.disassembly, self.symbols, prg)

    def test_zz_sealed_packet_preserved(self):
        current = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in PACKET.iterdir() if p.is_file()}
        self.assertEqual(current, self.inventory)


if __name__ == "__main__":
    unittest.main()
