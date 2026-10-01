import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import r0f_group1_carrier as carrier


class CarrierAdmissionTests(unittest.TestCase):
    def test_retired_identity_rejects_before_boot_or_finish(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            (path / "retirement.json").write_text('{}')
            with patch.object(carrier, "location", return_value=path):
                with self.assertRaisesRegex(ValueError, "retired"):
                    carrier.checked_gate("R0FG1P01.D81")

    def test_structural_failure_retires_candidate(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            gate = {"D81_SHA256": "a" * 64}
            with patch.object(carrier, "checked_gate", return_value=(path, None, gate)), \
                    patch.object(carrier, "_boot", side_effect=SystemExit("chain mismatch")):
                with self.assertRaises(SystemExit):
                    carrier.boot("R0FG1P01.D81", "1", 1)
            result = json.loads((path / "retirement.json").read_text())
            self.assertEqual(result["failedRun"], "ntsc-01")
            self.assertFalse(result["testEligible"])

    def test_exact_name_rejects_aliases(self):
        for name in ("group1.d81", "G1 LONG.D81", "GROUP1234.D81", "G1~1.D81"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                carrier.location(name)
        self.assertEqual(carrier.location("R0FG1P01.D81").name, "R0FG1P01")

    def test_timing_failures_precede_any_construction(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            base = {"prgSha256": "a" * 64}
            execution = {"videoArgument": "1", "status": 4, "error": 0}
            report = {"nominalTiming": "WITHIN_OBSERVED_BOUNDS"}
            for name, value in (("build-identity.json", base),
                                ("execution.json", execution), ("reduction.json", report)):
                (path / name).write_text(json.dumps(value))
            for field, value in (("nominalTiming", "FAIL"),
                                 ("nominalTiming", "INCONCLUSIVE")):
                (path / "reduction.json").write_text(json.dumps({**report, field: value}))
                with self.assertRaisesRegex(ValueError, "timing admission"):
                    carrier.checked_timing(path, "1", base, "")
            (path / "reduction.json").write_text(json.dumps(report))
            with self.assertRaisesRegex(ValueError, "timing admission"):
                carrier.checked_timing(path, "0", base, "")
            with self.assertRaisesRegex(ValueError, "timing admission"):
                carrier.checked_timing(path, "1", {"prgSha256": "b" * 64}, "")

    def test_failed_admission_has_no_image_side_effect(self):
        with patch.object(carrier.acquisition, "checked_build", return_value=({}, None, "")), \
                patch.object(carrier, "checked_timing", side_effect=ValueError("blocked")), \
                patch.object(carrier.runtime, "fresh_d81") as construct:
            with self.assertRaisesRegex(ValueError, "blocked"):
                carrier.build("R0FG1P01.D81", Path("ntsc"), Path("pal"))
            construct.assert_not_called()


if __name__ == "__main__":
    unittest.main()
