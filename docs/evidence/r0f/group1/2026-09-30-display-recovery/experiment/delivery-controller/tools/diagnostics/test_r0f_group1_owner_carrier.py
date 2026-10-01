"""Version-6 carrier context admission failures cannot construct an image."""
import copy
import unittest
from pathlib import Path
from unittest.mock import patch

import r0f_group1_owner_carrier as subject


class OwnerCarrierAdmissionTests(unittest.TestCase):
    def test_timing_identity_fails_closed(self):
        metadata = {"prgSha256": "exact", "inputs": {"source": "hash"}}
        report = {"acquisition": "PASS", "nominalTiming": "WITHIN_OBSERVED_BOUNDS",
                  "nominalDeadlineMisses": 0, "boundaryUncertain": 0, "cohortsBelow20Hz": 0}
        values = {"build-identity.json": copy.deepcopy(metadata),
                  "execution.json": {"videoArgument": "1", "status": 4, "error": 0},
                  "reduction.json": report, "negatives.json": {"result": "PASS"}}
        with patch.object(subject.candidate, "read", side_effect=lambda path: values[path.name]):
            self.assertEqual(subject.timing_identity(Path("unused"), "1", metadata), report)
            for name, field, bad in (("build-identity.json", "prgSha256", "other"),
                                     ("execution.json", "videoArgument", "0"),
                                     ("execution.json", "status", 3),
                                     ("execution.json", "error", 1),
                                     ("reduction.json", "acquisition", "FAIL"),
                                     ("reduction.json", "nominalTiming", "FAIL"),
                                     ("reduction.json", "nominalDeadlineMisses", 1),
                                     ("reduction.json", "boundaryUncertain", 1),
                                     ("reduction.json", "cohortsBelow20Hz", 1),
                                     ("negatives.json", "result", "FAIL")):
                prior = copy.deepcopy(values[name])
                values[name][field] = bad
                with self.assertRaises(ValueError):
                    subject.timing_identity(Path("unused"), "1", metadata)
                values[name] = prior

    def test_admission_precedes_construction(self):
        with patch.object(subject, "context", return_value=(Path("source"), {}, Path("prg"), "symbols")), \
             patch.object(subject, "timing_identity", side_effect=ValueError("rejected")), \
             patch.object(subject.carrier, "location") as location, \
             patch.object(subject.runtime, "fresh_d81") as create:
            with self.assertRaises(ValueError):
                subject.build("R0FG1P03.D81", Path("experiment"))
            location.assert_not_called()
            create.assert_not_called()


if __name__ == "__main__":
    unittest.main()
