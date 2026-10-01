import unittest

import r0f_group1_export_probe as probe


class TerminalBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.symbols = "\n".join(f"{address:08x} T {name}" for address, name in (
            (0x2001, "r0fg1_terminal_export"),
            (0x2100, "r0fg1_terminal_export_end"),
            (0x2100, "r0fg1_terminal_file_setup"),
            (0x2120, "r0fg1_terminal_file_setup_end"),
        ))
        calls = (0xff87, 0xff84, 0xff8a, 0xff81, 0xffcc, 0xff90,
                 0x2100, 0xffc0, 0xffc3, 0x2100, 0xffd8)
        lines = [f" {0x2001 + index * 3:04x}: 20 00 00\tjsr\t${call:x}"
                 for index, call in enumerate(calls)]
        lines += [" 2030: 4c 30 20\tjmp\t$2030",
                  "00002100 <r0fg1_terminal_file_setup>:",
                  " 2100: 20 bd ff\tjsr\t$ffbd",
                  " 2103: 20 6b ff\tjsr\t$ff6b",
                  " 2106: 20 ba ff\tjsr\t$ffba",
                  " 2109: 60\trts",
                  " 2120: 60\trts"]
        self.disassembly = "\n".join(lines)

    def test_aliased_labels_use_symbol_instruction_bounds(self):
        probe.validate_terminal(self.disassembly, self.symbols)

    def test_terminal_return_rejected(self):
        with self.assertRaisesRegex(ValueError, "must not return"):
            probe.validate_terminal(self.disassembly.replace("jmp\t$2030", "rts"), self.symbols)

    def test_setup_cannot_call_application(self):
        with self.assertRaisesRegex(ValueError, "ROM call allowlist"):
            probe.validate_terminal(self.disassembly.replace("jsr\t$ffbd", "jsr\t$7000"), self.symbols)

    def test_refresh_after_save_rejected(self):
        with self.assertRaisesRegex(ValueError, "refresh must precede"):
            probe.validate_terminal(self.disassembly.replace("jsr\t$ffc0", "jsr\t$TEMP")
                .replace("jsr\t$ffd8", "jsr\t$ffc0").replace("jsr\t$TEMP", "jsr\t$ffd8"), self.symbols)


if __name__ == "__main__":
    unittest.main()
