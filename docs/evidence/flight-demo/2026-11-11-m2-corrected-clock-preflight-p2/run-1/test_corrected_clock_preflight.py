"""Independent host models and fail-closed CC3 fixtures; no target execution."""
from contextlib import contextmanager
from hashlib import sha256
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/flight_demo/m2_rebuild"))
import corrected_clock_preflight as subject

OLD = Path("/private/tmp/f65-m2-fixed-kernel-cost-correction")
REFS = Path("/private/tmp/f65-m2-service-reference")


def countdown(updates):
    """Event oracle, independent of the converter's modulo-phase formula."""
    a = b = 65535
    remaining = updates * 32
    while remaining >= a:
        remaining -= a
        a = 65535
        b -= 1
        if not b:
            b = 65535
    return a - remaining, b


def raw(a, b):
    return 0xffffffff - int.from_bytes(a.to_bytes(2, "little") + b.to_bytes(2, "little"), "little")


def synthetic_costs():
    """Deliberately small abstract fixtures, NOT estimates of renderer costs."""
    result = {name: 1 for name in subject.UNKNOWNS
              if name not in ("clock_gap", "clock_resident_extra", "stack")}
    result.update(product=100, division=100, frame_rest=10000, atomic=100,
                  tick=1000, fragment=200, poll=100, publication=100,
                  capture_gap=100, input_age=10000)
    return result


def event_completion(work, period, tick, phase, irq_period, irq, irq_phase):
    """One-cycle time oracle. Arrivals queue serial CPU work, never overlap."""
    time = 0
    pending = 0
    while work or pending:
        if time >= phase and (time - phase) % period == 0:
            pending += tick
        if time >= irq_phase and (time - irq_phase) % irq_period == 0:
            pending += irq
        if pending:
            pending -= 1
        else:
            work -= 1
        time += 1
        if time > 10000:
            raise AssertionError("oracle did not terminate")
    return time


def publication_timeline(frame, width, gap, ready, first, publication):
    """Independent polling events; no production bound or response formula."""
    sample = ready + first
    while sample % frame >= width:
        sample += gap
    return sample - ready + publication


class ClockAndPhaseTests(unittest.TestCase):
    def test_independent_countdown_across_A_B_and_public_wrap(self):
        # Samples separated by <half range. Multiple hardware periods and
        # public uint32 rollover are distinct; no arbitrary timer pair injection.
        points = [1, 2047, 2049, 65536, 60000000, 120000000,
                  134213632, 134213633, 180000000, 240000000, 268427265]
        clock = subject.Clock()
        for updates in points:
            state = countdown(updates)
            self.assertEqual(state, subject.state_after_updates(updates))
            value = subject.clock_sample(subject.stable_reads(*state))
            self.assertIsNotNone(value)
            self.assertEqual(clock.sample(value), ((updates - points[0]) * 32) & 0xffffffff)
            self.assertFalse(clock.fault)

    def test_sampler_rejection_and_sticky_fault(self):
        reads = list(subject.stable_reads(1234, 5678))
        clock = subject.Clock()
        clock.sample(subject.clock_sample(reads))
        for index in (2, 5, 6, 7):
            torn = reads[:]
            torn[index] ^= 1
            self.assertIsNone(subject.clock_sample(torn))
        prior = clock.sample(0, fault=True)
        self.assertTrue(clock.fault)
        self.assertEqual(clock.sample(raw(1233, 5678)), prior)
        for a in range(0xfff0, 0x10000):
            self.assertIsNone(subject.clock_sample(subject.stable_reads(a, 1234)))

    def test_zero_counter_and_half_range_fail_closed(self):
        for pair in ((0, 3), (3, 0)):
            clock = subject.Clock()
            clock.sample(raw(*pair))
            self.assertTrue(clock.fault)
        clock = subject.Clock()
        clock.sample(raw(*countdown(1)))
        self.assertEqual(clock.sample(raw(*countdown(67108865))), 0)
        self.assertTrue(clock.fault)

    def test_all_calibration_endpoint_classes_and_rounding(self):
        for mode, (rasters, line, _) in subject.MODES.items():
            actual = []
            for difference in range(-rasters, rasters + 1):
                first, last = max(-difference, 0), max(difference, 0)
                phases = [first] + [rasters // 2] * 15 + [last]
                # Independent 17-event timestamp model and bigint quotient.
                events = [32 * (i * rasters + phases[i]) for i in range(17)]
                elapsed = events[-1] - events[0]
                self.assertEqual(elapsed % 16, 0)  # reachable lattice, no hidden truncation
                expected = (405000 * (elapsed // 16) * 65536) // (rasters * line)
                actual.append(subject.calibrated_period(mode, phases))
                self.assertEqual(actual[-1], expected)
            envelope = subject.phase_envelope(mode)
            self.assertEqual((min(actual), max(actual)),
                             (envelope["period_q16_min"], envelope["period_q16_max"]))
            # Nonideal endpoint sample cannot be silently replaced by k=0.
            self.assertNotEqual(subject.calibrated_period(mode, [0] * 17),
                                subject.calibrated_period(mode, [0] * 16 + [1]))

    def test_calibration_partition_and_sample_units_rejected(self):
        for phases in ([0] * 16, [0] * 18, [0] * 16 + [625], [0] * 16 + [0.5],
                       [-1] + [0] * 16):
            with self.assertRaises(ValueError):
                subject.calibrated_period("PAL", phases)
        with self.assertRaises(ValueError):
            subject.calibrated_period("unknown mode", [0] * 17)
        # Two frame observations can sample the same CIA line. The pinned
        # converter accepts a zero delta, so the finite enclosure must too.
        self.assertGreater(subject.calibrated_period("PAL", [624, 0] + [0] * 15), 0)

    def test_all_fraction_and_lattice_phases_with_wrap(self):
        for mode in subject.MODES:
            p = subject.phase_envelope(mode)["period_q16_min"]
            integer_part = p >> 16
            # Exhaust the Q16 carry classes, then independently exhaust the
            # 32 CIA threshold classes for both possible integer increments.
            increments = set()
            for fraction in range(65536):
                value = subject.release(0xfffffff0, fraction, p, 1)
                expected_fraction = fraction + (p & 65535)
                expected = (0xfffffff0 + integer_part + (expected_fraction >> 16)) & 0xffffffff
                self.assertEqual(value, expected)
                increments.add((value - 0xfffffff0) & 0xffffffff)
            for step in increments:
                for phase in range(32):
                    # Independent event threshold search, no ceil formula.
                    start = (phase + 31) // 32
                    end = start
                    while 32 * end < phase + step:
                        end += 1
                    self.assertGreaterEqual(end - start,
                        subject.phase_envelope(mode)["minimum_due_separation_lines"])

    def test_releases_preserve_fraction_across_generations(self):
        period = subject.calibrated_period("NTSC", [0] * 16 + [1])
        origin, fraction, now = 0xffffff00, 65535, 0xffffff00
        for index in range(1, 1000):
            fraction += period & 65535
            now = (now + (period >> 16) + (fraction >> 16)) & 0xffffffff
            fraction &= 65535
            self.assertEqual(now, subject.release(origin, 65535, period, index))


class ConditionalScheduleTests(unittest.TestCase):
    def test_busy_interval_vs_independent_all_phase_timeline(self):
        for period, tick in ((17, 2), (29, 3)):
            bound = subject.response_bound(100, period, tick, 0, 1, 13, 1000)
            for phase in range(period):
                for irq_phase in range(13):
                    self.assertLessEqual(event_completion(100, period, tick, phase, 13, 1, irq_phase), bound)
            # Pending work at the initial boundary only increases the bound.
            fragment_bound = subject.response_bound(100, period, tick, 2, 1, 13, 1000)
            self.assertGreaterEqual(fragment_bound, bound)

    def test_wait_bound_both_edges_miss_and_first_poll(self):
        # Exhaust every discrete ready phase and first poll delay. Subsequent
        # polls intentionally take the maximum gap, across several frames.
        for frame, width, gap in ((101, 23, 7), (79, 19, 4)):
            bound = subject.publication_wait_bound(frame, width, gap, 3)
            observed = []
            for ready in range(frame):
                for first in range(gap + 1):
                    elapsed = publication_timeline(frame, width, gap, ready, first, 3)
                    observed.append(elapsed)
                    self.assertLessEqual(elapsed, bound)
            # Both full and partial wait overlap with scheduled ticks are
            # elapsed time; do not add their CPU duration a second time.
            self.assertTrue(any(t > frame - width for t in observed))

    def test_first_poll_closing_window_counterexample(self):
        # Ready at 16, first poll at 23 misses [0,23). Further polls every
        # seven cycles first reenter the window at 107; publication ends at110.
        elapsed = publication_timeline(101, 23, 7, 16, 7, 3)
        self.assertEqual(elapsed, 94)
        self.assertGreater(elapsed, 88)  # The one-gap bound is insufficient.
        self.assertLessEqual(elapsed, subject.publication_wait_bound(101, 23, 7, 3))

    def test_schedule_wait_result_against_independent_timeline(self):
        # Exercise the caller too: a separately correct helper cannot mask an
        # undercount in conditional_schedule's returned wait.
        for mode, (rasters, line, top) in subject.MODES.items():
            costs = synthetic_costs()
            result = subject.conditional_schedule(mode, costs)
            frame = rasters * (line + costs["batch_excess"])
            width = (top - 21) * line
            gap = result["poll_response_upper_CPU_cycles"]
            for ready in (0, width - gap, width - gap + 1, width - 1,
                          width, width + 1, frame - 1):
                for first in (0, 1, gap - 1, gap):
                    elapsed = publication_timeline(frame, width, gap, ready, first, costs["publication"])
                    self.assertLessEqual(elapsed, result["publication_wait_elapsed_upper_CPU_cycles"])
            self.assertFalse(result["execution_authorized"])

    def test_publication_wait_unknown_and_invalid_bounds_refused(self):
        for index in range(4):
            for bad in (None, 0, -1, True, 1.5):
                args = [101, 23, 7, 3]
                args[index] = bad
                with self.assertRaises(ValueError):
                    subject.publication_wait_bound(*args)
        for args in ((101, 101, 7, 3), (101, 102, 7, 3), (101, 23, 23, 3), (101, 23, 24, 3)):
            with self.assertRaises(ValueError):
                subject.publication_wait_bound(*args)

    def test_synthetic_profile_keeps_actual_admission_false(self):
        for mode in subject.MODES:
            result = subject.conditional_schedule(mode, synthetic_costs())
            self.assertFalse(result["execution_authorized"])
            self.assertIn("synthetic", result["status"])
            self.assertLessEqual(result["intercommit_upper_CPU_cycles"], 2025000)
            self.assertLessEqual(result["persistent_pose_age_upper_CPU_cycles"], 4050000)

    def test_missing_unknown_zero_units_and_tile_credit_fail(self):
        for name in synthetic_costs():
            for kind in ("missing", "unknown", "zero"):
                costs = synthetic_costs()
                if kind == "missing":
                    del costs[name]
                else:
                    costs[name] = None if kind == "unknown" else 0
                with self.assertRaises(ValueError):
                    subject.conditional_schedule("PAL", costs)
        for kwargs in ({"units": "native counts"}, {"tiles": 550}):
            with self.assertRaises(ValueError):
                subject.conditional_schedule("PAL", synthetic_costs(), **kwargs)

    def test_strict_window_calibration_atomic_and_poll_constraints(self):
        for name, value in (("publication", 1287), ("frame_poll_gap", 676962),
                            ("frame_read_to_sample", 1287), ("atomic", 200),
                            ("poll", 100000), ("tick", 400000),
                            ("frame_rest", 2025000), ("input_age", 4050000)):
            costs = synthetic_costs()
            costs[name] = value
            with self.assertRaises(ValueError, msg=name):
                subject.conditional_schedule("NTSC", costs)

    def test_native_guard_strict_equality_and_wrap(self):
        # Verify the required upper conversion independently by positioning
        # every operation start in a line. No real grants are generated.
        for cycles in (1, 1286, 1287, 1288, 4000):
            upper_counts = 32 * ((cycles + 1286) // 1287 + 1)
            for phase in range(1287):
                updates = (phase + cycles) // 1287
                self.assertLessEqual(updates * 32, upper_counts)
        for now in (100, 0xfffffff0):
            op, overhead = 64, 32
            for delta, allowed in ((96, False), (97, True), (0x80000000, False)):
                release = (now + delta) & 0xffffffff
                remaining = (release - now) & 0xffffffff
                self.assertEqual(remaining < 0x80000000 and remaining > op + overhead, allowed)
        self.assertGreater(32 * ((3000000 + 1286) // 1287 + 1), 65535)


def identities(files):
    return {str(p): (p.stat().st_size, sha256(p.read_bytes()).hexdigest()) for p in files}


class FrozenInputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="f65-cc3-fixtures-")
        cls.old, cls.current, cls.refs = (Path(cls.temp.name).resolve() / n for n in ("old", "current", "refs"))
        sources = json.loads((OLD / subject.TARGET / "result.json").read_text())["inputs"]
        source_paths = {n for n in sources if n.startswith(("src/", "interfaces/generated/"))}
        historical_ids = json.loads((OLD / "docs/evidence/flight-demo/2026-11-11-m2-fixed-kernel-preflight/source-identities.json").read_text())
        old_files = set(source_paths) | (set(historical_ids) - {"WORK_IN_PROGRESS.md"})
        for rel in (subject.TARGET, Path("docs/evidence/flight-demo/2026-11-11-m2-fixed-kernel-preflight")):
            old_files.update(str(p.relative_to(OLD)) for p in (OLD / rel).rglob("*") if p.is_file())
        current_files = source_paths | {"src/platform/m1/clock_private.h"}
        for name in subject.PACKETS:
            current_files.update(str(p.relative_to(ROOT)) for p in (ROOT / "docs/evidence/flight-demo" / name).rglob("*") if p.is_file())
        cls.protected = []
        for source, destination, files in ((OLD, cls.old, old_files), (ROOT, cls.current, current_files),
                                           (REFS, cls.refs, subject.REFERENCES)):
            for name in files:
                path = destination / name
                path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source / name, path)
                cls.protected.append(source / name)
        cls.before = identities(cls.protected)

    @classmethod
    def tearDownClass(cls):
        try:
            if identities(cls.protected) != cls.before:
                raise AssertionError("sealed inputs changed during successful/failing checks")
        finally:
            cls.temp.cleanup()

    @contextmanager
    def changed(self, path, change):
        original = path.read_bytes()
        change(path)
        try:
            yield
        finally:
            if path.is_symlink():
                path.unlink()
            path.write_bytes(original)

    def run_model(self):
        return subject.analyze(self.old, self.current, self.refs)

    def test_valid_inputs_preserve_unknowns_and_stop(self):
        result = self.run_model()
        self.assertEqual(result["old_target_input_count"], 81)
        self.assertEqual(len(result["corrected_source_inputs"]), 82)
        self.assertEqual(result["actual_complete_cost_admission"], "UNPROVEN")
        self.assertEqual(result["actual_phase_schedule"], "NOT REACHED")
        self.assertIsNone(result["remaining_cost_allowance_cycles"])
        self.assertIsNone(result["service_budgets"])
        self.assertFalse(result["execution_authorized"])
        self.assertTrue(all(row["value"] is None for row in result["unknown_costs"].values()))
        self.assertEqual(result["historical_resident"]["deficit"], 755)
        self.assertEqual(result["historical_cold_lower_bound"]["deficit"], 298776)
        self.assertEqual(result["retained_demand"]["tiles"], 640)
        self.assertEqual(result["conditional_replacement_bytes"]["upper_before_other_clock_charges"], 5810)

    def test_wrong_root_and_old_source_as_current_refused(self):
        with self.assertRaisesRegex(ValueError, "distinct"):
            subject.analyze(self.old, self.old, self.refs)
        path = self.current / "src/platform/m1/m1_platform.c"
        with self.changed(path, lambda p: p.write_bytes((OLD / p.relative_to(self.current)).read_bytes())):
            with self.assertRaisesRegex(ValueError, "input identity"):
                self.run_model()

    def test_changed_missing_and_symlink_inputs_refused(self):
        for root, name in ((self.old, "src/core/m1_runtime.c"),
                           (self.current, "src/platform/m1/clock_private.h"),
                           (self.refs, "xemu/cia6526.c")):
            path = root / name
            for change in (lambda p: p.write_bytes(p.read_bytes() + b"\n"),
                           lambda p: p.unlink(),
                           lambda p: (p.unlink(), p.symlink_to(ROOT / "src/platform/m1/clock_private.h"))):
                with self.changed(path, change):
                    with self.assertRaises((OSError, ValueError)):
                        self.run_model()

    def test_sealed_cap_six_and_extra_member_refused(self):
        packet = self.current / "docs/evidence/flight-demo/2026-11-11-m2-platform-clock-p2"
        path = packet / "run-1.stdout"
        with self.changed(path, lambda p: p.write_bytes(p.read_bytes().replace(b'"admitted_feedback_cap": 12', b'"admitted_feedback_cap": 6'))):
            with self.assertRaisesRegex(ValueError, "input identity"):
                self.run_model()
        extra = packet / "extra.txt"
        extra.write_text("not sealed")
        try:
            with self.assertRaisesRegex(ValueError, "inventory"):
                self.run_model()
        finally:
            extra.unlink()

    def test_parent_symlink_and_unsupported_source_shape(self):
        alias = Path(self.temp.name) / "alias"
        alias.symlink_to(self.refs, target_is_directory=True)
        try:
            with self.assertRaisesRegex(ValueError, "symlinked"):
                subject.analyze(self.old, self.current, alias)
        finally:
            alias.unlink()
        refs = {name: (self.refs / name).read_text() for name in subject.REFERENCES}
        refs["targets/mega65/mega65.c"] = "unsupported"
        with self.assertRaisesRegex(ValueError, "source shape"):
            subject.witnesses(self.current, refs)


if __name__ == "__main__":
    unittest.main()
