"""Capacity/summary failures stop before constructing or testing a carrier."""
import copy
import unittest
from pathlib import Path
from unittest.mock import patch

import r0f_group1_capacity_carrier as subject


class CapacityCarrierAdmissionTests(unittest.TestCase):
    def test_case_admission_fails_closed(self):
        case = {"result": "PASS", "allocationBytes": 327680,
                "realEvidenceBytesIncludingCrc": 310580, "diagnosticTailBytes": 17100,
                "outsideAcquisitionTiming": True}
        values = {
            "capacity.json": {"result": "PASS", "scope": "ACTUAL_EXPORTED_VERSION_7",
                              "capacityRejections": list(range(12)), "capacity": copy.deepcopy(case)},
            "reduction.json": {"capacityCase": copy.deepcopy(case)},
            "operator-summary.json": {"result": "PASS_PROTECTED_TEXT", "status": 4, "error": 0, "files": 20},
        }
        with patch.object(subject, "read", side_effect=lambda path: values[path.name]):
            subject.require_case(Path("unused"))
            for name, field, bad in (("capacity.json", "result", "FAIL"),
                    ("capacity.json", "scope", "SYNTHETIC_CODEC_ONLY"),
                    ("capacity.json", "capacityRejections", list(range(11))),
                    ("operator-summary.json", "result", "FAIL"),
                    ("operator-summary.json", "status", 5),
                    ("operator-summary.json", "error", 1),
                    ("operator-summary.json", "files", 19)):
                original = copy.deepcopy(values[name])
                values[name][field] = bad
                with self.assertRaises(ValueError):
                    subject.require_case(Path("unused"))
                values[name] = original
            values["reduction.json"]["capacityCase"]["outsideAcquisitionTiming"] = False
            with self.assertRaises(ValueError):
                subject.require_case(Path("unused"))

    def test_capacity_admission_precedes_construction(self):
        with patch.object(subject.candidate, "preserve"), \
             patch.object(subject, "require_case", side_effect=ValueError("rejected")), \
             patch.object(subject.previous, "build") as construct:
            with self.assertRaises(ValueError):
                subject.build("R0FG1P04.D81")
            construct.assert_not_called()


if __name__ == "__main__":
    unittest.main()
