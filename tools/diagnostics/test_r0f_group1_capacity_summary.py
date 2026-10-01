"""Protected PETSCII summary must match the actual export outcome, not imply timing."""
import unittest
from pathlib import Path
from unittest.mock import patch

import r0f_group1_capacity_summary as subject


class OperatorSummaryTests(unittest.TestCase):
    def check(self, status, error, files, expected_failure=False, corrupt=False):
        text = (b"\x93" + f"G1 EXPORT S:{status} E:{error:02X} F:{files:02X}\r".encode("ascii")
                + b"4=OK 5=FAIL / E,F HEX\rREDUCE FOR TIMING\rNOT ACCEPTANCE\rRESET\r\0")
        memory = bytearray(512)
        memory[:len(text)] = text
        memory[256:259] = bytes((status, error, files))
        if corrupt:
            memory[1] ^= 1
        addresses = {"r0fg1_operator_text": 0, "r0fg1_operator_text_end": len(text),
                     "r0fg1_export_status": 256, "r0fg1_export_error": 257, "r0fg1_export_files": 258}
        with patch.object(subject, "read", return_value={"build_label": "runtime"}), \
             patch.object(Path, "read_text", return_value="symbols"), \
             patch.object(Path, "read_bytes", return_value=bytes(memory)), \
             patch.object(subject.prior.previous.probe.integration, "symbol",
                          side_effect=lambda _, name: addresses[name]), \
             patch.object(subject, "write") as write:
            subject.operator_check(Path("unused"), expected_failure=expected_failure)
            report = write.call_args.args[1]
            self.assertEqual(report["status"], status)
            self.assertIn("NOT ACCEPTANCE", report["text"])

    def test_success_and_failure_control_prefix(self):
        self.check(4, 0, 20)
        self.check(5, 3, 0, True)
        self.check(5, 255, 0, True)

    def test_wrong_outcome_or_text_rejects(self):
        for values in ((5, 3, 0, False, False), (5, 0, 0, True, False),
                       (5, 3, 1, True, False), (4, 0, 19, False, False),
                       (4, 0, 20, False, True)):
            with self.subTest(values=values), self.assertRaises(ValueError):
                self.check(*values)


if __name__ == "__main__":
    unittest.main()
