import copy
import json
import unittest

import r0f_group1_presentation_contract as contract


class PresentationContractTests(unittest.TestCase):
    def setUp(self):
        self.wire = json.loads(contract.PATH.read_text())

    def test_valid_private_fixture(self):
        self.assertEqual(contract.validate(self.wire)["ANCHORS"], 4)

    def test_invalid_capacities_and_lod(self):
        for name, value in (("VIEWS", 3), ("BUFFERS", 1), ("TIERS", 3),
                            ("ANCHORS", 0), ("ANCHORS", 256),
                            ("ANCHOR_PRIORITIES", 5), ("OCCLUSION_COLUMNS", 0),
                            ("OCCLUSION_COLUMNS", 9), ("LOD_EXIT_PIXELS", 12),
                            ("LOD_EXIT_PIXELS", -1), ("LOD_ENTER_PIXELS", 65536)):
            with self.subTest(name=name, value=value):
                mutated = copy.deepcopy(self.wire)
                mutated["constants"][name] = value
                with self.assertRaises(ValueError):
                    contract.validate(mutated)

    def test_no_production_promotion(self):
        self.wire["status"] = "PRODUCTION"
        with self.assertRaises(ValueError):
            contract.validate(self.wire)

    def test_exact_integer_fields(self):
        for value in (True, 4.0, "4"):
            with self.subTest(value=value):
                mutated = copy.deepcopy(self.wire)
                mutated["constants"]["ANCHORS"] = value
                with self.assertRaises(ValueError):
                    contract.validate(mutated)
        del self.wire["constants"]["ANCHORS"]
        with self.assertRaises(ValueError):
            contract.validate(self.wire)


if __name__ == "__main__":
    unittest.main()
