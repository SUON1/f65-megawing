import copy
import json
import unittest

import r0f_group1_contract as generator


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.contract = json.loads(generator.PATH.read_text())
        self.export = json.loads((generator.ROOT / "interfaces/r0f_group1_export_contract.json").read_text())

    def test_valid_shape(self):
        self.assertEqual(generator.validate(self.contract, self.export), (3200, 327172))

    def test_invalid_geometry_and_bounds(self):
        for name, value in (("STAGES", 20), ("PHASES", 0), ("MAX_WORLD_EVENTS", 65536),
                            ("RECORD_BYTES", 256), ("TICKS_PER_PHASE", 33)):
            with self.subTest(name=name):
                mutated = copy.deepcopy(self.contract)
                mutated["constants"][name] = value
                with self.assertRaises(ValueError):
                    generator.validate(mutated, self.export)

    def test_capacity_cannot_borrow_reserve(self):
        self.export["constants"]["TRACE_CAPACITY"] = 327171
        with self.assertRaisesRegex(ValueError, "admitted allocation"):
            generator.validate(self.contract, self.export)

    def test_record_overlap(self):
        self.contract["recordOffsets"]["INPUT_COUNTS"] = 60
        with self.assertRaisesRegex(ValueError, "overlap/bounds"):
            generator.validate(self.contract, self.export)

    def test_header_overlap(self):
        self.contract["headerOffsets"]["WORLD_EVENTS"] = 64
        with self.assertRaisesRegex(ValueError, "overlap/bounds"):
            generator.validate(self.contract, self.export)


if __name__ == "__main__":
    unittest.main()
