#!/usr/bin/env python3
"""Test transcript integrity against retained emulator evidence, not hardware."""
from pathlib import Path
import unittest

from r0f_successor_capture import parse_rows

ROOT = Path(__file__).resolve().parents[2]


class CaptureTests(unittest.TestCase):
    def setUp(self):
        self.data = (ROOT / 'docs/evidence/r0f/successor/2026-09-22-workflow/'
                     'R0FIRQ11/ntsc-1/result.bin').read_bytes()
        self.rows = [f'{offset:04X} ' + self.data[offset:offset + 16].hex(' ')
                     for offset in range(0, 512, 16)]

    def test_exact(self):
        self.assertEqual(parse_rows('\n'.join(self.rows)), self.data)

    def test_missing(self):
        with self.assertRaises(ValueError):
            parse_rows('\n'.join(self.rows[:-1]))

    def test_duplicate(self):
        self.rows[1] = self.rows[0]
        with self.assertRaises(ValueError):
            parse_rows('\n'.join(self.rows))

    def test_order(self):
        self.rows.reverse()
        with self.assertRaises(ValueError):
            parse_rows('\n'.join(self.rows))

    def test_corruption(self):
        self.rows[10] = self.rows[10][:-2] + 'FF'
        with self.assertRaises(ValueError):
            parse_rows('\n'.join(self.rows))

    def test_extra_byte(self):
        self.rows[0] += ' 00'
        with self.assertRaises(ValueError):
            parse_rows('\n'.join(self.rows))

    def test_nonhex(self):
        self.rows[0] = self.rows[0][:-2] + '??'
        with self.assertRaises(ValueError):
            parse_rows('\n'.join(self.rows))


if __name__ == '__main__':
    unittest.main()
