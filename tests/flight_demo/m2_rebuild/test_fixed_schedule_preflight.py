"""Independent host regressions for the first FC clock gate; never target execution."""
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/flight_demo/m2_rebuild"))
import fixed_schedule_preflight as subject
from fixed_preflight import TARGET

REFERENCES = Path("/private/tmp/f65-m2-service-reference")
SCRIPT = ROOT / "tools/flight_demo/m2_rebuild/fixed_schedule_preflight.py"


def event_oracle(updates):
    """Independent countdown model: advance to each A expiry, not divmod."""
    remaining = updates * 32
    a = b = 0xffff
    while remaining >= a:
        remaining -= a
        a = 0xffff
        b -= 1
        if b == 0:
            b = 0xffff
    return a - remaining, b


def source_step(a, b):
    """One literal CIA update, used independently of the closed-form proof."""
    a -= 32
    if a <= 0:
        a += 0xffff
        b -= 1
        if b <= 0:
            b += 0xffff
    return a, b


def binary_timestamp(a, b):
    raw = int.from_bytes(a.to_bytes(2, "little") + b.to_bytes(2, "little"), "little")
    return 0xffffffff - raw


def identities(paths):
    return {str(p): (p.stat().st_size, sha256(p.read_bytes()).hexdigest()) for p in paths}


class ClockArithmeticTests(unittest.TestCase):
    def test_force_loaded_state(self):
        self.assertEqual(subject.state_after_updates(0), (65535, 65535))

    def test_first_three_a_reloads_against_update_oracle(self):
        state = (65535, 65535)
        for updates in range(1, 7000):
            state = source_step(*state)
            self.assertEqual(subject.state_after_updates(updates), state)

    def test_upper_reload_reachability_against_event_oracle(self):
        # 65535**2 = 32*134213632 + 1. This is reached from reset; it is
        # not an arbitrary impossible A/B combination injected into the model.
        for updates in (134213630, 134213631, 134213632, 134213633, 134213634):
            self.assertEqual(subject.state_after_updates(updates), event_oracle(updates))
        self.assertEqual(subject.state_after_updates(134213632), (1, 1))
        self.assertEqual(subject.state_after_updates(134213633), (65504, 65535))

    def test_ordinary_update_is_32_counts(self):
        a, b = (4096, 32000)
        after = source_step(a, b)
        self.assertEqual((binary_timestamp(*after) - binary_timestamp(a, b)) & 0xffffffff, 32)

    def test_a_reload_has_one_extra_encoded_count(self):
        before = (31, 2)
        after = source_step(*before)
        self.assertEqual(after, (65534, 1))
        self.assertEqual((binary_timestamp(*after) - binary_timestamp(*before)) & 0xffffffff, 33)

    def test_b_reload_discontinuity_survives_unsigned_subtraction(self):
        before = event_oracle(134213632)
        after = source_step(*before)
        self.assertEqual(binary_timestamp(*before), 0xfffefffe)
        self.assertEqual(binary_timestamp(*after), 0x0000001f)
        self.assertEqual((binary_timestamp(*after) - binary_timestamp(*before)) & 0xffffffff, 65569)
        # Control: ordinary modulo-2**32 wrap itself is not a discontinuity.
        self.assertEqual((0x10 - 0xfffffff0) & 0xffffffff, 32)

    def test_both_witness_samples_are_accepted(self):
        for state in ((1, 1), (65504, 65535)):
            self.assertEqual(subject.clock_sample(subject.stable_reads(*state)), binary_timestamp(*state))

    def test_each_coherence_comparison_rejects_inconsistency(self):
        for index in (2, 5, 6, 7):
            reads = list(subject.stable_reads(1234, 5678))
            reads[index] ^= 1
            self.assertIsNone(subject.clock_sample(reads))

    def test_existing_top_sixteen_reload_exclusion(self):
        for a in range(0xfff0, 0x10000):
            self.assertIsNone(subject.clock_sample(subject.stable_reads(a, 42)))
        self.assertIsNotNone(subject.clock_sample(subject.stable_reads(0xffef, 42)))

    def test_malformed_samples_and_updates_fail(self):
        for value in (-1, 1 << 32, 1.5, True, None):
            with self.assertRaises(ValueError):
                subject.state_after_updates(value)
        for value in (-1, 256, 1.5, True, None):
            with self.assertRaises(ValueError):
                subject.clock_sample([value] + [0] * 7)
        for reads in ([], [0] * 7, [0] * 9):
            with self.assertRaises(ValueError):
                subject.clock_sample(reads)

    def test_first_gate_has_no_frame_or_runtime_success(self):
        result = subject.native_clock_gate()
        self.assertTrue(result["status"].startswith("FAIL"))
        self.assertEqual(result["uint32_timestamp_delta"], 65569)
        self.assertEqual(result["excess_encoded_counts"], 65537)
        self.assertEqual(result["modes"], ["PAL", "NTSC"])


class FrozenInputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        old = ROOT / subject.OLD
        target = ROOT / TARGET
        target_ids = json.loads((target / "result.json").read_text())["inputs"]
        source_ids = json.loads((old / "source-identities.json").read_text())
        cls.root_files = {p.relative_to(ROOT) for directory in (old, target)
                          for p in directory.rglob("*") if p.is_file()}
        cls.root_files.update(p for p in target_ids if p.startswith(("src/", "interfaces/generated/")))
        cls.root_files.update(p for p in source_ids if p != "WORK_IN_PROGRESS.md")
        cls.protected = [ROOT / p for p in cls.root_files]
        cls.protected += [REFERENCES / p for p in subject.REFERENCES]
        cls.before = identities(cls.protected)

    @classmethod
    def tearDownClass(cls):
        if identities(cls.protected) != cls.before:
            raise AssertionError("sealed inputs changed during success/failure regressions")

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="f65-fc-regression-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "root"
        self.refs = Path(self.temp.name) / "references"
        for p in self.root_files:
            destination = self.root / p
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / p, destination)
        for p in subject.REFERENCES:
            destination = self.refs / p
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REFERENCES / p, destination)

    def test_valid_inputs_stop_before_schedule(self):
        result = subject.analyze(self.root, self.refs)
        self.assertEqual(result["status"], "BLOCKED AT FIRST MANDATORY GATE")
        self.assertEqual(result["publication_window_proof"], "NOT REACHED")
        self.assertTrue(result["phase_schedule"].startswith("NOT REACHED"))
        self.assertIsNone(result["remaining_cost_allowance_cycles"])
        self.assertEqual(result["complete_cost_admission"], "UNPROVEN")
        self.assertTrue(result["unknown_costs"])
        self.assertFalse(result["execution_authorized"])
        self.assertEqual(result["resident"]["old_deficit"], 755)
        self.assertEqual(result["retained_demand"]["unconditional_tile_slots"], 640)
        self.assertEqual(result["target_links"], 0)
        self.assertEqual(result["runtime_executions"], 0)

    def test_modified_image_fails(self):
        path = self.root / TARGET / "UNADMITTED.prg"
        raw = bytearray(path.read_bytes()); raw[-1] ^= 1
        path.write_bytes(raw)
        with self.assertRaisesRegex(ValueError, "sealed target member"):
            subject.analyze(self.root, self.refs)

    def test_modified_target_source_fails(self):
        path = self.root / "src/diagnostics/r0f/combined_platform.c"
        path.write_text(path.read_text() + "\n")
        with self.assertRaisesRegex(ValueError, "source invariant identity"):
            subject.analyze(self.root, self.refs)

    def test_each_changed_reference_fails(self):
        for name in subject.REFERENCES:
            path = self.refs / name
            raw = path.read_bytes(); path.write_bytes(raw + b"\n")
            with self.assertRaisesRegex(ValueError, "input identity"):
                subject.analyze(self.root, self.refs)
            path.write_bytes(raw)

    def test_missing_reference_fails(self):
        (self.refs / "xemu/cia6526.c").unlink()
        with self.assertRaisesRegex(ValueError, "missing or non-regular"):
            subject.analyze(self.root, self.refs)

    def test_symlink_reference_fails_even_with_same_bytes(self):
        path = self.refs / "xemu/cia6526.c"
        path.unlink(); path.symlink_to(REFERENCES / "xemu/cia6526.c")
        with self.assertRaisesRegex(ValueError, "missing or non-regular"):
            subject.analyze(self.root, self.refs)

    def test_old_result_cannot_be_regraded_to_allow_unknown_costs(self):
        path = self.root / subject.OLD / "preflight-final.json"
        data = json.loads(path.read_text())
        data["cost_gate"]["unknown_additional_costs"] = []
        data["cost_gate"]["partial_budget_excess"] = -100000
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "input identity"):
            subject.analyze(self.root, self.refs)

    def test_truncated_changed_and_extra_packet_inputs_fail(self):
        path = self.root / subject.OLD / "source-identities.json"
        raw = path.read_bytes()
        path.write_bytes(raw[:20])
        with self.assertRaisesRegex(ValueError, "input identity"):
            subject.analyze(self.root, self.refs)
        path.write_bytes(raw)
        (self.root / subject.OLD / "extra.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "inventory"):
            subject.analyze(self.root, self.refs)

    def test_missing_source_witness_fails(self):
        refs = {name: (self.refs / name).read_text() for name in subject.REFERENCES}
        refs["xemu/cia6526.c"] = refs["xemu/cia6526.c"].replace("cia->TCB <= 0", "cia->TCB < 0")
        with self.assertRaisesRegex(ValueError, "source witness"):
            subject.source_witnesses(self.root, refs)

    def test_cli_exits_nonzero_without_touching_inputs(self):
        before = identities(self.protected)
        command = [sys.executable, "-B", str(SCRIPT), "--root", str(self.root),
                   "--references", str(self.refs)]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "BLOCKED AT FIRST MANDATORY GATE")
        (self.refs / "xemu/cia6526.c").write_text("invalid")
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "INPUT REFUSED")
        self.assertEqual(identities(self.protected), before)


if __name__ == "__main__":
    unittest.main()
