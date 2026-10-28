"""Private design/ownership checks, with temporary generated outputs only."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location("m2rb_generate", ROOT / "tools/flight_demo/m2_rebuild/generate.py")
GENERATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GENERATOR)


class Contract(unittest.TestCase):
    def test_generated_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            data = GENERATOR.generate(destination=destination)
            self.assertEqual(data["identity"], "65AERO-M2-MIN-REBUILD-1")
            for name in ["interfaces/generated/m2_rebuild_profile.h", "memory/m2-rebuild-ledger.json"]:
                self.assertEqual((ROOT / name).read_bytes(), (destination / name).read_bytes())

    def test_unreviewed_profile_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "interfaces").mkdir()
            data = json.loads((ROOT / "interfaces/m2_rebuild.json").read_text())
            data["selection"][-1] = 16
            (root / "interfaces/m2_rebuild.json").write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "Unreviewed"):
                GENERATOR.generate(root=root)
            self.assertFalse((root / "interfaces/generated").exists())

    def test_memory_and_owner_bounds(self):
        data = json.loads((ROOT / "interfaces/m2_rebuild.json").read_text())
        self.assertEqual(data["selection"], [0,1,2,3,4,5,7,11,15])
        self.assertEqual(data["target_budgets"], [0] * 8)
        self.assertFalse(data["runtime_enablement"] or data["banking"] or data["dma"])
        ranges = list(data["memory"].values())[:-1]
        ranges += [[start, start + data["store_bytes"]] for start in data["stores"]]
        ranges += [[data["color_base"], data["color_base"] + data["color_bytes"]]]
        for i, first in enumerate(ranges):
            for last in ranges[i + 1:]:
                self.assertTrue(first[1] <= last[0] or last[1] <= first[0], (first, last))
        self.assertEqual(data["memory"]["resident"][1] - data["memory"]["resident"][0], 24575)
        self.assertEqual(2048 + 960 * 64, data["blank_offset"])
        self.assertEqual(data["blank_offset"] + 64, data["store_bytes"])
        self.assertEqual(data["color_bytes"], 40 * 25 * 2)
        self.assertEqual(data["memory"]["reserve_used"], 0)

    def test_integrated_public_bytes_unchanged(self):
        paths = ["src/core/m1_runtime.c", "src/input/m1_input.c", "src/presentation/m1_snapshot.c",
                 "src/environment/m2_fixture.c", "src/graphics/m2_geometry.c", "src/graphics/m2_q46_private.h",
                 "interfaces/generated/m2_pr1.h", "interfaces/generated/m2_tables.c",
                 "interfaces/m2_pr1.json", "interfaces/m1_development.json", "memory/m1-development-ledger.json",
                 "memory/m2-pr1-ledger.json", "tests/flight_demo/m2/oracle.py",
                 "tests/flight_demo/m2/clip_regressions.py"]
        for name in paths:
            expected = subprocess.check_output(["git", "show", "b044440:" + name], cwd=ROOT)
            self.assertEqual(hashlib.sha256(expected).digest(), hashlib.sha256((ROOT / name).read_bytes()).digest(), name)

    def test_source_ownership_and_denied_dispatch(self):
        for name in ["src/graphics/m2_rebuild.c", "src/graphics/m2_rebuild_text.c",
                     "src/diagnostics/m2_rebuild/camera.c"]:
            text = (ROOT / name).read_text()
            for prohibited in ["CFREG", "volatile uint8_t *", "r0f_", "combined_platform", "cfdma"]:
                self.assertNotIn(prohibited, text)
        main = (ROOT / "src/diagnostics/m2_rebuild/main.c").read_text()
        self.assertIn("volatile uint32_t m2rb_target_budgets[8];", main)
        self.assertIn("volatile uint8_t m2rb_launch_authorized;", main)
        self.assertNotIn("m2rb_launch_authorized =", main)
        self.assertNotIn("m2rb_target_budgets[slot] =", main)
        self.assertIn("m2rb_guard(now, release, budget, m2rb_guard_budget)", main)
        source = (ROOT / "src/graphics/m2_rebuild.c").read_text()
        self.assertEqual(source.count("m2_project_prepared("), 1)
        self.assertEqual(source.count("m2_prepare("), 1)
        self.assertNotIn("m2_pair_eligible(", source)


if __name__ == "__main__":
    unittest.main()
