import copy
import json
import unittest

import r0f_group1_pool_contract as contract


class PoolContractTests(unittest.TestCase):
    def setUp(self):
        self.wire = json.loads(contract.PATH.read_text())

    def test_valid_and_generated(self):
        self.assertEqual(len(contract.validate(self.wire)), 8)
        self.assertEqual(contract.HEADER.read_text(), contract.render(self.wire))

    def test_capacity_range_and_integer(self):
        for value in (0, -1, 65536, True, 2.5):
            bad = copy.deepcopy(self.wire)
            bad["pools"]["FACES"]["capacity"] = value
            with self.assertRaises(ValueError):
                contract.validate(bad)
        self.wire["pools"]["FACES"]["capacity"] = 65535
        with self.assertRaises(ValueError):
            contract.validate(self.wire)

    def test_units_and_identity(self):
        self.wire["pools"]["FACES"]["unit"] = " "
        with self.assertRaises(ValueError):
            contract.validate(self.wire)
        del self.wire["pools"]["RED_TRACKS"]
        with self.assertRaises(ValueError):
            contract.validate(self.wire)

    def test_fixed_domains_and_channels(self):
        for name in ("MEGA_TRACKS", "RED_TRACKS", "PCM_CHANNELS"):
            bad = copy.deepcopy(self.wire)
            bad["pools"][name]["capacity"] += 1
            with self.assertRaises(ValueError):
                contract.validate(bad)

    def test_no_production_promotion(self):
        self.wire["status"] = "PRODUCTION"
        with self.assertRaises(ValueError):
            contract.validate(self.wire)


if __name__ == "__main__":
    unittest.main()
