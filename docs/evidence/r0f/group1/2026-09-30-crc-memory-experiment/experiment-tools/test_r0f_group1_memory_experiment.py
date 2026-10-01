import copy
import unittest

import r0f_group1_memory_experiment as experiment


class FocusedNtscGateTests(unittest.TestCase):
    def setUp(self):
        self.reduction = {"acquisition": "PASS", "records": 3200,
                          "nominalTiming": "WITHIN_OBSERVED_BOUNDS"}
        self.execution = {"videoArgument": "1", "videoMode": "NTSC",
                          "status": 4, "error": 0}

    def test_complete_ntsc_pass(self):
        experiment.require_ntsc_gate(self.reduction, self.execution)

    def test_pal_cannot_satisfy_ntsc_gate(self):
        for argument, label in (("0", "PAL"), ("0", "NTSC"), ("1", "PAL")):
            with self.subTest(argument=argument, label=label):
                execution = {**self.execution, "videoArgument": argument,
                             "videoMode": label}
                with self.assertRaises(ValueError):
                    experiment.require_ntsc_gate(self.reduction, execution)

    def test_incomplete_export_rejects(self):
        for key, value in (("status", 3), ("status", 5), ("error", 1)):
            with self.subTest(key=key, value=value):
                execution = {**self.execution, key: value}
                with self.assertRaises(ValueError):
                    experiment.require_ntsc_gate(self.reduction, execution)

    def test_nominal_failure_or_uncertainty_rejects(self):
        for timing in ("FAIL", "INCONCLUSIVE"):
            with self.subTest(timing=timing):
                reduction = {**self.reduction, "nominalTiming": timing}
                with self.assertRaises(ValueError):
                    experiment.require_ntsc_gate(reduction, self.execution)

    def test_partial_or_invalid_acquisition_rejects(self):
        for key, value in (("records", 3199), ("acquisition", "FAIL")):
            with self.subTest(key=key, value=value):
                reduction = {**self.reduction, key: value}
                with self.assertRaises(ValueError):
                    experiment.require_ntsc_gate(reduction, self.execution)

    def test_missing_evidence_rejects(self):
        for source in ("reduction", "execution"):
            record = getattr(self, source)
            for key in record:
                with self.subTest(source=source, key=key):
                    reduction, execution = copy.deepcopy(self.reduction), copy.deepcopy(self.execution)
                    del (reduction if source == "reduction" else execution)[key]
                    with self.assertRaises(ValueError):
                        experiment.require_ntsc_gate(reduction, execution)


if __name__ == "__main__":
    unittest.main()
