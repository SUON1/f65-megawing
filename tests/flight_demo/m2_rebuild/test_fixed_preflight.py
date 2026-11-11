"""Host-only fail-closed regressions; no writes to retained evidence."""
from graphlib import CycleError
from hashlib import sha256
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/flight_demo/m2_rebuild"))
from fixed_preflight import TickBounds, TARGET, check_identity, design_budget
from service_costs import InstructionTiming
from wide_static import PRG_SHA

REFERENCES = Path("/private/tmp/f65-m2-service-reference")


def model():
    target = ROOT / TARGET
    return TickBounds((target / "UNADMITTED.prg").read_bytes(),
                      (target / "UNADMITTED.disassembly").read_text(),
                      (target / "UNADMITTED.symbols").read_text(),
                      (REFERENCES / "xemu/cpu65_mega65_timings.h").read_bytes(), PRG_SHA)


class FixedPreflightTests(unittest.TestCase):
    def test_current_tick_has_positive_slack(self):
        result = model().tick_iteration()
        self.assertGreater(result["iteration_cpu_cycles_upper"], 0)
        self.assertLess(result["iteration_cpu_cycles_upper"], result["interval_cpu_cycles"])
        self.assertEqual(result["own_instructions"] + sum(result["calls"].values())
                         + 2 * result["irq_including_entry"] + result["nmi_including_entry"],
                         result["iteration_cpu_cycles_upper"])

    def test_uncovered_cycle_fails(self):
        with self.assertRaises(CycleError):
            TickBounds.check_cycles({1: ((2, 0),), 2: ((1, 0),)}, set())

    def test_missing_feedback_witness_fails(self):
        with self.assertRaisesRegex(ValueError, "missing feedback"):
            TickBounds.check_cycles({1: ()}, {(1, 2)})

    def test_unknown_dependency_fails(self):
        with self.assertRaisesRegex(ValueError, "unreviewed tick dependency"):
            model().bound("m2rb_dispatch")

    def test_missing_and_oversized_sdk_limits_fail(self):
        for limit in (None, -1, 23):
            with self.subTest(limit=limit), self.assertRaisesRegex(ValueError, "SDK limit"):
                model().bound("memcpy", limit)

    def test_second_command_producer_fails(self):
        subject = model()
        subject.instructions[0x7c8c] = ("jsr", "$474c", bytes.fromhex("20 4c 47"))
        with self.assertRaisesRegex(ValueError, "call graph changed"):
            subject.check_producers()

    def test_changed_image_fails(self):
        target = ROOT / TARGET
        raw = bytearray((target / "UNADMITTED.prg").read_bytes())
        raw[-1] ^= 1
        with self.assertRaisesRegex(ValueError, "sealed image"):
            InstructionTiming(raw, "", "", b"", PRG_SHA)

    def test_changed_seal_fails_without_evidence_write(self):
        original = ROOT / TARGET / "seal.json"
        before = sha256(original.read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / TARGET
            target.mkdir(parents=True)
            (target / "seal.json").write_text("{}\n")
            with self.assertRaisesRegex(ValueError, "seal identity"):
                check_identity(root)
        self.assertEqual(before, sha256(original.read_bytes()).hexdigest())

    def test_all_target_sources_match_original_link(self):
        self.assertGreaterEqual(len(check_identity(ROOT)), 81)

    def test_partial_budget_cannot_be_mistaken_for_admission(self):
        subject = model()
        budget = design_budget(subject, REFERENCES, subject.tick_iteration())
        self.assertEqual(budget["partial_budget_cycles"], sum(budget["rows"].values()))
        self.assertGreater(budget["partial_budget_excess"], 0)
        self.assertTrue(budget["unknown_additional_costs"])
        self.assertEqual(budget["resident"]["actual_successor_fit"], "NOT BUILT / UNPROVEN")

    def test_cli_fails_closed(self):
        result = subprocess.run([sys.executable, "-B", str(ROOT / "tools/flight_demo/m2_rebuild/fixed_preflight.py"),
                                 "--references", str(REFERENCES)], capture_output=True)
        self.assertEqual(result.returncode, 2, result.stderr.decode())
        self.assertIn(b'FAIL TO ESTABLISH ADMISSION', result.stdout)


if __name__ == "__main__":
    unittest.main()
