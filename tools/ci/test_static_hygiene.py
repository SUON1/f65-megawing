"""Fail-closed fixture tests; no target, emulator or SD access."""

import copy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import static_hygiene as hygiene


TEXT_PATH = "docs/evidence/r0f/group1/fixture/original.log"
D81_PATH = "docs/evidence/r0f/group1/fixture/ORIGINAL.D81"
TEXT = b"retained log with original whitespace \n"
MEDIA = b"immutable fixture, not a real carrier"


def fixture_manifest():
    return {
        "schema": 1,
        "authority": "Isolated unit-test fixture",
        "reviewed_commit": "a" * 40,
        "whitespace": {TEXT_PATH: hashlib.sha256(TEXT).hexdigest()},
        "d81": {D81_PATH: hashlib.sha256(MEDIA).hexdigest()},
    }


class PolicyTests(unittest.TestCase):
    def test_valid_manifest(self):
        self.assertEqual(hygiene.load_manifest(json.dumps(fixture_manifest())), fixture_manifest())

    def test_invalid_paths_and_hashes(self):
        for path in ("/tmp/a", "src/new.py", "docs/evidence/r0f/group1/../bad.log", "docs/evidence/r0f/group1//bad.log"):
            with self.subTest(path=path):
                manifest = fixture_manifest()
                manifest["whitespace"] = {path: "a" * 64}
                with self.assertRaises(ValueError):
                    hygiene.load_manifest(json.dumps(manifest))
        manifest = fixture_manifest()
        manifest["d81"][D81_PATH] = "not a hash"
        with self.assertRaises(ValueError):
            hygiene.load_manifest(json.dumps(manifest))

    def test_rom_and_emulator_state_cannot_be_exempted(self):
        for category in ("whitespace", "d81"):
            for suffix in (".ROM", ".rom", ".xemu-state", ".d81"):
                with self.subTest(category=category, suffix=suffix):
                    manifest = fixture_manifest()
                    manifest[category] = {"docs/evidence/r0f/group1/MEGA65" + suffix: "a" * 64}
                    with self.assertRaises(ValueError):
                        hygiene.load_manifest(json.dumps(manifest))

    def test_duplicate_keys_and_unknown_schema(self):
        with self.assertRaises(ValueError):
            hygiene.load_manifest('{"schema":1,"schema":1}')
        for schema in (True, 2):
            manifest = fixture_manifest()
            manifest["schema"] = schema
            with self.assertRaises(ValueError):
                hygiene.load_manifest(json.dumps(manifest))

    def test_guard_allows_only_exact_media(self):
        hygiene.guard_artifacts([D81_PATH, "src/normal.c"], {D81_PATH})
        for path in ("docs/evidence/r0f/group1/NEW.D81", "NEW.D81", "MEGA65.ROM", "save.xemu-state"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                hygiene.guard_artifacts([path], {D81_PATH})

    def test_toolchain_prefixes_remain_blocked_even_if_listed(self):
        for prefix in hygiene.BLOCKED_PREFIXES:
            path = prefix + "ORIGINAL.D81"
            with self.subTest(path=path), self.assertRaises(ValueError):
                hygiene.guard_artifacts([path], {path})


class GitFixtureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="f65-ci-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.run_git("init", "-q")
        self.run_git("config", "user.name", "Fixture")
        self.run_git("config", "user.email", "fixture@example.invalid")
        self.write("live.txt", b"clean\n")
        self.base = self.commit()
        self.write(TEXT_PATH, TEXT)
        self.write(D81_PATH, MEDIA)
        self.write(hygiene.MANIFEST, json.dumps(fixture_manifest()).encode())
        self.head = self.commit()

    def run_git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args], stderr=subprocess.STDOUT)

    def write(self, path, data):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    def commit(self):
        self.run_git("add", "--all")
        self.run_git("commit", "-qm", "fixture")
        return self.run_git("rev-parse", "HEAD").decode().strip()

    def test_exact_pins_pass_pr_push_and_initial_push(self):
        self.assertEqual(hygiene.check(self.root, self.base, self.head)["d81_pins"], 1)
        hygiene.check(self.root, self.base, self.head, merge_base=True)
        empty = self.run_git("hash-object", "-t", "tree", "/dev/null").decode().strip()
        hygiene.check(self.root, empty, self.head)

    def test_group2_exact_pin_passes_but_changed_bytes_fail(self):
        path = "docs/evidence/r0f/group2/fixture/original.log"
        manifest = fixture_manifest()
        manifest["whitespace"][path] = hashlib.sha256(TEXT).hexdigest()
        self.write(path, TEXT)
        self.write(hygiene.MANIFEST, json.dumps(manifest).encode())
        hygiene.check(self.root, self.base, self.commit(), merge_base=True)
        self.write(path, b"normalized\n")
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            hygiene.check(self.root, self.base, self.commit())

    def test_changed_pinned_text_or_media_fails(self):
        for path, data in ((TEXT_PATH, b"normalized\n"), (D81_PATH, MEDIA + b"changed")):
            with self.subTest(path=path):
                self.write(TEXT_PATH, TEXT)
                self.write(D81_PATH, MEDIA)
                self.write(path, data)
                with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                    hygiene.check(self.root, self.base, self.commit())

    def test_missing_renamed_or_symlink_pin_fails(self):
        (self.root / D81_PATH).rename(self.root / (D81_PATH + ".renamed"))
        with self.assertRaisesRegex(ValueError, "missing or not a regular file"):
            hygiene.check(self.root, self.base, self.commit())
        (self.root / D81_PATH).symlink_to("ORIGINAL.D81.renamed")
        with self.assertRaisesRegex(ValueError, "not a regular file"):
            hygiene.check(self.root, self.base, self.commit())

    def test_unlisted_live_and_evidence_whitespace_fails(self):
        paths = (
            "live.txt",
            "docs/evidence/r0f/group1/fixture/new.log",
            "docs/evidence/r0f/group2/fixture/new.log",
        )
        for path in paths:
            with self.subTest(path=path):
                for clean_path in paths:
                    self.write(clean_path, b"clean\n")
                self.write(path, b"new trailing whitespace \n")
                with self.assertRaisesRegex(ValueError, "Changed-range whitespace"):
                    hygiene.check(self.root, self.base, self.commit())

    def test_unlisted_media_fails(self):
        self.write("docs/evidence/r0f/group1/fixture/NEW.D81", MEDIA)
        with self.assertRaisesRegex(ValueError, "Forbidden tracked artifacts"):
            hygiene.check(self.root, self.base, self.commit())

    def test_committed_head_not_mutable_checkout_is_checked(self):
        self.write(D81_PATH, b"uncommitted change")
        self.write(hygiene.MANIFEST, b"uncommitted invalid manifest")
        hygiene.check(self.root, self.base, self.head)

    def test_conflicting_category_hashes_fail(self):
        manifest = copy.deepcopy(fixture_manifest())
        manifest["whitespace"][D81_PATH] = "0" * 64
        self.write(hygiene.MANIFEST, json.dumps(manifest).encode())
        with self.assertRaises(ValueError):
            hygiene.check(self.root, self.base, self.commit())


if __name__ == "__main__":
    unittest.main()
