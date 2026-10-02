#!/usr/bin/env python3
"""Negative ownership checks, independent of any emulator or removable media."""

import copy
import json
import unittest

import r0f_group1_export_admission as admission


class AdmissionTests(unittest.TestCase):
    def setUp(self):
        self.contract = json.loads(admission.CONTRACT.read_text())
        self.delta = json.loads(admission.LEDGER.read_text())
        self.base = json.loads((admission.ROOT / self.delta["baseLedger"]).read_text())

    def validate(self):
        return admission.validate(self.contract, self.delta, self.base)

    def test_original_lifecycle_unchanged(self):
        original = copy.deepcopy(self.base)
        merged = self.validate()
        self.assertEqual(self.base, original)
        for updated, prior in zip(merged["allocations"], original["allocations"]):
            if prior["id"] != "kernal-dos-entry-backup":
                self.assertEqual(updated, prior)
            else:
                self.assertEqual(updated["lifetimes"], prior["lifetimes"]
                                 + ["SERVICES_RESUMED", "TERMINAL_EXPORT"])

    def test_capsule_cannot_alias_original(self):
        self.contract["constants"]["CAPSULE_START"] = 0x08020000
        self.contract["constants"]["CAPSULE_PAYLOAD"] = 0x08020010
        with self.assertRaisesRegex(ValueError, "undeclared overlap"):
            self.validate()

    def test_trace_cannot_alias_capsule(self):
        self.contract["constants"]["TRACE_START"] = 0x08022000
        with self.assertRaisesRegex(ValueError, "undeclared overlap"):
            self.validate()

    def test_staging_cannot_overlap_live_workload(self):
        self.delta["allocations"][2]["lifetimes"].append("SERVICES_RESUMED")
        with self.assertRaisesRegex(ValueError, "active during workload"):
            self.validate()

    def test_undeclared_overlay_rejected(self):
        self.delta["overlays"] = []
        with self.assertRaisesRegex(ValueError, "undeclared overlap"):
            self.validate()

    def test_reserves_and_authoritative_attic_rejected(self):
        self.delta["measuredReserveBytes"] = 1
        with self.assertRaisesRegex(ValueError, "reserve"):
            self.validate()
        self.delta["measuredReserveBytes"] = 0
        self.delta["allocations"][1]["simulationAuthority"] = True
        with self.assertRaisesRegex(ValueError, "simulation authority"):
            self.validate()

    def test_capsule_shape_rejected(self):
        self.contract["constants"]["CONTEXT_BYTES"] -= 1
        with self.assertRaisesRegex(ValueError, "context shape"):
            self.validate()

    def test_unsupported_copy_geometry(self):
        for name, value in (("TRACE_START", 0x08030001),
                            ("STAGING_BYTES", 16385),
                            ("TRACE_CAPACITY", 327681),
                            ("COPY_CHUNK_BYTES", 256)):
            with self.subTest(name=name):
                original = self.contract["constants"][name]
                self.contract["constants"][name] = value
                with self.assertRaisesRegex(ValueError, "copy geometry"):
                    self.validate()
                self.contract["constants"][name] = original


if __name__ == "__main__":
    unittest.main()
