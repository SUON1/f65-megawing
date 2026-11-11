"""Host-only static regressions; no target or compiled host program is executed."""
from hashlib import sha256
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/flight_demo/m2_rebuild'))
import clock_gap_v2 as subject

BASELINE = Path('/private/tmp/f65-m2-fixed-kernel-cost-correction')
OLD = ROOT / 'docs/evidence/flight-demo/2026-11-11-m2-platform-clock'


def identities():
    files = list(OLD.rglob('*')) + [ROOT / name for name in
        json.loads((OLD / 'host-result.json').read_text())['sources']]
    return {str(p): (p.stat().st_size, sha256(p.read_bytes()).hexdigest())
            for p in files if p.is_file()}


class NormalizationBounds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before = identities()
        subject.check_identity(BASELINE)
        target = BASELINE / 'docs/evidence/flight-demo/2026-11-09-m2-exact-wide/target'
        cls.args = [(target / 'UNADMITTED.prg').read_bytes(),
                    (target / 'UNADMITTED.disassembly').read_text(),
                    (target / 'UNADMITTED.symbols').read_text(),
                    Path('/private/tmp/f65-m2-service-reference/xemu/cpu65_mega65_timings.h').read_bytes(),
                    subject.PRG_SHA]

    @classmethod
    def tearDownClass(cls):
        if identities() != cls.before:
            raise AssertionError('Success/failure fixtures changed sealed evidence or clock source')

    def setUp(self):
        self.model = subject.Gap(*self.args)
        self.model.results = {}

    def test_divisor_and_product_visits_from_independent_index_sequence(self):
        # Source consumes the last byte once, then visits every remaining byte
        # in reverse order. This index sequence is independent of CAPS/SCC code.
        for width in (1, 2, 3, 4, 5, 6, 13):
            with self.subTest(width=width):
                remaining_indices = list(reversed(range(width - 1)))
                body_visits = len(remaining_indices)
                guard_visits = len([True for _ in remaining_indices] + [False])
                self.assertEqual(body_visits, {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 13: 12}[width])
                self.assertEqual(guard_visits, width)
                proof = self.model.normalization
                self.assertIn(width, proof['source_widths'])
                self.assertGreaterEqual(proof['admitted_feedback_cap'], body_visits)
                self.assertGreaterEqual(proof['admitted_feedback_cap'] + 1, guard_visits)

    def test_old_six_iteration_cap_fails_before_any_cost_analysis(self):
        with patch.dict(subject.CAPS, normalize=6):
            with self.assertRaisesRegex(ValueError, '13-byte product'):
                subject.Gap(*self.args)

    def test_missing_cap_and_off_by_one_fail(self):
        with patch.dict(subject.CAPS):
            subject.CAPS.pop('normalize')
            with self.assertRaisesRegex(ValueError, '13-byte product'):
                subject.Gap(*self.args)
        with patch.dict(subject.CAPS, normalize=11):
            with self.assertRaisesRegex(ValueError, '13-byte product'):
                subject.Gap(*self.args)

    def test_product_operand_change_fails(self):
        op, _, raw = self.model.instructions[0x29ab]
        self.model.instructions[0x29ab] = (op, '#$6', raw)
        with self.assertRaisesRegex(ValueError, 'operand or countdown'):
            subject.check_normalization(self.model)

    def test_countdown_changes_fail(self):
        for address in (0x2a44, 0x2a45, 0x2a62, 0x2a85, 0x2a93, 0x2a95):
            with self.subTest(address=hex(address)):
                original = self.model.instructions[address]
                self.model.instructions[address] = ('nop', '', b'\xea')
                with self.assertRaisesRegex(ValueError, 'operand or countdown'):
                    subject.check_normalization(self.model)
                self.model.instructions[address] = original

    def test_missing_or_extra_caller_fails(self):
        for address in (0x298f, 0x29b3):
            with self.subTest(missing=hex(address)):
                original = self.model.instructions.pop(address)
                with self.assertRaisesRegex(ValueError, 'caller closure'):
                    subject.check_normalization(self.model)
                self.model.instructions[address] = original
        self.model.instructions[0x9000] = ('jsr', '$2a0c', b'\x20\x0c\x2a')
        with self.assertRaisesRegex(ValueError, 'caller closure'):
            subject.check_normalization(self.model)

    def test_shifted_entry_fails(self):
        self.model.names['normalize'] += 1
        with self.assertRaisesRegex(ValueError, 'caller closure'):
            subject.check_normalization(self.model)

    def test_corrected_cost_charges_the_six_previously_missing_visits(self):
        # Independent linear sum of the actual linked loop (including its shift
        # callee), without using the verifier's SCC partition or visit multiplier.
        cycle_cost = 0
        for address in self.model.instructions:
            if 0x2a64 <= address <= 0x2a95:
                cycle_cost += self.model.cycles(address)
                cycle_cost += max((extra for _, extra in self.model.edges(address)), default=0)
                callee = self.model.callee(address)
                if callee is not None:
                    self.assertEqual(callee, self.model.names['__ashlhi3'])
                    cycle_cost += self.model.upper(callee)
        old = json.loads((OLD / 'preflight.json').read_text())['bounds']['normalize']['cpu_cycles']
        new = self.model.upper(self.model.names['normalize'])
        self.assertGreater(cycle_cost, 0)
        self.assertEqual(new - old, 6 * cycle_cost)


if __name__ == '__main__':
    unittest.main(verbosity=2, failfast=True)
