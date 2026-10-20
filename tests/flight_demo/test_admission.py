"""Reject configuration drift before generating misleading M1 contracts."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/flight_demo'))
from admission import validate


class AdmissionTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'interfaces/m1_development.json').read_text())

    def test_admitted_profile(self):
        validate(self.data)

    def test_unsupported_runtime_configuration(self):
        for key in ('tick_hz', 'stages', 'queue_capacity', 'snapshot_slots',
                    'columns', 'rows', 'render_rows_per_service'):
            with self.subTest(key=key):
                changed = copy.deepcopy(self.data)
                changed[key] += 1
                with self.assertRaises(ValueError):
                    validate(changed)

    def test_each_allocation_is_bound_to_platform(self):
        for key in self.data['memory']:
            with self.subTest(key=key):
                changed = copy.deepcopy(self.data)
                changed['memory'][key] += 1
                with self.assertRaises(ValueError):
                    validate(changed)

    def test_startup_write_cannot_escape_ledger(self):
        for key in ('start', 'end_exclusive'):
            changed = copy.deepcopy(self.data)
            changed['inherited_initialization'][key] += 1
            with self.assertRaises(ValueError):
                validate(changed)

    def test_uninspected_retained_implementation_is_rejected(self):
        self.data['inherited_initialization']['source_sha256'] = '0' * 64
        with self.assertRaises(ValueError):
            validate(self.data)


if __name__ == '__main__':
    unittest.main()
