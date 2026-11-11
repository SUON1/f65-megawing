"""A changed generated numeric contract cannot silently retain specialization."""
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]


class Specialization(unittest.TestCase):
    def test_changed_contract_fails_compilation(self):
        original = (ROOT / "interfaces/generated/m2_pr1.h").read_text()
        changes = [("M2_CLIP_SCALE (16777216L)", "M2_CLIP_SCALE (8388608L)"),
                   ("M2_ROTATION_SCALE (70368744177664LL)", "M2_ROTATION_SCALE (35184372088832LL)"),
                   ("M2_VERTICAL_NUM (2L)", "M2_VERTICAL_NUM (3L)"),
                   ("M2_WIDTH (320L)", "M2_WIDTH (640L)"),
                   ("M2_FAR_FT (40000L)", "M2_FAR_FT (50000L)"),
                   ("M2_TILT_LIMIT_DEG (60L)", "M2_TILT_LIMIT_DEG (90L)")]
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            for before, after in [(None, None), *changes]:
                text = original if before is None else original.replace(before, after)
                self.assertTrue(before is None or text != original)
                (temporary / "m2_pr1.h").write_text(text)
                result = subprocess.run(["/usr/bin/clang", "-std=c11", "-fsyntax-only",
                    "-I" + str(temporary), "-I" + str(ROOT / "src/graphics"), "-x", "c", "-"],
                    input='#include "m2_compact.h"\n', text=True, capture_output=True)
                with self.subTest(change=before):
                    if before is None:
                        self.assertEqual(result.returncode, 0, result.stderr)
                    else:
                        self.assertNotEqual(result.returncode, 0)
                        self.assertIn("static assertion failed", result.stderr)


if __name__ == "__main__":
    unittest.main()
