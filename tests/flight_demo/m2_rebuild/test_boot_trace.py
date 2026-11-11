"""Fail-closed tests for the pre-SYS observer, without an emulator process."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'tools/flight_demo/m2_rebuild'))
from boot_trace import Observer, RAM


class BootTraceEntry(unittest.TestCase):
    def setUp(self):
        self.observer = Observer.__new__(Observer)
        self.observer.config = {'standard': 'PAL'}
        self.prg = bytes([1, 0x20, 0x78])
        self.observer.read = self.read
        self.admission = {'cf001': {'emulator_rom_and_sdl': {'rom': {'sha256': 'pinned'}}},
                          'load': {'origin': 0x2001, 'resident_end': 0x2002}}
        self.row = {'name': 'sys', 'flags': {'I': False}, 'nmi_edge': 0, 'irq_level': 0,
                    'cia2_icr_mask_data': [0, 3], 'privileged': False, 'video_6f': 0,
                    'pc': 0x2017, 'fetch_page_base': 0x20000000,
                    'map_hi_mb_lo_mb_hi_offset_lo_offset_mask': [0, 0, 0x30000, 0, 0x8e]}

    def read(self, at, count):
        self.assertEqual((at, count), (RAM + 0x2001, 1))
        return self.prg[2:]

    def test_identity_map_and_lazy_fetch(self):
        self.observer.check(self.row, self.admission, self.prg)
        self.assertEqual(self.row['derived_sys_physical_fetch'], 0x2017)

    def test_wrong_fetch_or_interference_fails_closed(self):
        for changed in (
            {'map_hi_mb_lo_mb_hi_offset_lo_offset_mask': [0, 0, 0x30000, 0x100, 0x8e]},
            {'fetch_page_base': 0x5000}, {'nmi_edge': 1}, {'irq_level': 1},
            {'cia2_icr_mask_data': [1, 0]}, {'video_6f': 0x80},
        ):
            with self.subTest(changed=changed), self.assertRaises(RuntimeError):
                self.observer.check(self.row | changed, self.admission, self.prg)
