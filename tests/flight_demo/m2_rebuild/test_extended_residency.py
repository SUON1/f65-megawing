"""Profile/lease negatives use temporary outputs; sealed evidence is read-only."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location("extended_profile", ROOT /
    "tools/flight_demo/m2_rebuild/residency.py")
PROFILE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROFILE)


class ExtendedResidency(unittest.TestCase):
    def test_generated_profile_and_production_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            data = PROFILE.generate(destination=target)
            self.assertEqual(data["development_resident"][1] - data["development_resident"][0], 28671)
            self.assertEqual(data["production_resident"], [8193, 32768])
            for name in PROFILE.OUTPUTS:
                self.assertEqual((ROOT / name).read_bytes(), (target / name).read_bytes(), name)

    def test_larger_ceiling_owner_borrowing_or_early_enablement_rejected(self):
        changes = {"development_resident": [8193, 40960],
                   "production_resident": [8193, 36864],
                   "forbidden_covering_map_block": [36864, 40960],
                   "software_stack": [40960, 53248],
                   "protected_reserve": [368640, 393216],
                   "reserve_used": 1, "banking": True, "dma": True,
                   "tick_hz": 99, "stages": 20, "normal_world_minimum_hz": 6,
                   "runtime_enablement": True, "target_budgets": [1] * 8}
        for field, value in changes.items():
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (root / "interfaces").mkdir()
                data = json.loads((ROOT / PROFILE.CONTRACT).read_text())
                data[field] = value
                (root / PROFILE.CONTRACT).write_text(json.dumps(data))
                with self.assertRaises(AssertionError):
                    PROFILE.generate(root=root)
                self.assertFalse((root / "interfaces/generated").exists())

    def test_initial_load_is_distinct_from_later_staging(self):
        data = PROFILE.load()
        self.assertIn("own initial PRG load is permitted", data["staging_policy"])
        self.assertIn("no later loading or staging", data["staging_policy"])
        # A covering 8KiB MAP is forbidden even if its requested subrange starts
        # at the new $9000 ceiling. $9000-$9fff is not independently remappable.
        for start in [0x8000, 0x8fff, 0x9000, 0x9fff]:
            self.assertEqual(start // data["map_block_bytes"] * data["map_block_bytes"], 0x8000)


if __name__ == "__main__":
    unittest.main()
