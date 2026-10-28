"""SDK identity regressions use disposable fixtures, never real SDK/evidence writes."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location(
    "m2rb_toolchain_identity", ROOT / "tools/flight_demo/m2_rebuild/toolchain_identity.py")
IDENTITY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(IDENTITY)


def fixture(root):
    sdk = root / "sdk"
    files = {"bin/clang": b"compiler", "bin/ld.lld": b"linker",
             "bin/llvm-objdump": b"objdump", "bin/llvm-nm": b"nm",
             "bin/mos-mega65.cfg": b"--config=mos-common.cfg\n",
             "bin/mos-common.cfg": b"-isystem ../lib/clang/24/include\n",
             "lib/clang/24/include/stddef.h": b"resource header",
             "mos-platform/mega65/include/mega65.h": b"platform header",
             "mos-platform/mega65/lib/mega65.ld": b"INCLUDE commodore.ld\n",
             "mos-platform/commodore/lib/commodore.ld": b"linker configuration",
             "mos-platform/mega65/lib/runtime.a": b"runtime library"}
    for name, content in files.items():
        path = sdk / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    (sdk / "bin/mos-clang").symlink_to("clang")
    (sdk / "bin/mos-mega65-clang").symlink_to("mos-clang")
    return sdk


class ToolchainIdentity(unittest.TestCase):
    def test_complete_tree_and_deterministic_serialization(self):
        with tempfile.TemporaryDirectory() as directory:
            sdk = fixture(Path(directory))
            inventory = IDENTITY.capture(sdk)
            expected = {path.relative_to(sdk).as_posix() for path in sdk.rglob("*")}
            self.assertEqual(set(inventory["entries"]), expected)
            self.assertEqual(inventory["entries"]["bin/mos-mega65-clang"],
                             {"kind": "symlink", "target": "mos-clang",
                              "resolved": "bin/clang", "resolved_kind": "file"})
            restored = json.loads(json.dumps(inventory))
            self.assertEqual(IDENTITY.capture(sdk), restored)
            self.assertEqual(IDENTITY.digest(restored), IDENTITY.digest(inventory))
            IDENTITY.verify(sdk, restored)

    def test_configuration_resource_runtime_and_tool_changes_are_detected(self):
        names = ["bin/mos-mega65.cfg", "bin/mos-common.cfg",
                 "lib/clang/24/include/stddef.h", "mos-platform/mega65/lib/mega65.ld",
                 "mos-platform/commodore/lib/commodore.ld",
                 "mos-platform/mega65/lib/runtime.a", "bin/clang", "bin/ld.lld",
                 "bin/llvm-objdump", "bin/llvm-nm"]
        for name in names:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                sdk = fixture(Path(directory))
                inventory = IDENTITY.capture(sdk)
                (sdk / name).write_bytes(b"changed input")
                with self.assertRaisesRegex(ValueError, "SDK identity changed"):
                    IDENTITY.verify(sdk, inventory)

    def test_removed_and_added_files_are_detected(self):
        for mutation in ["remove", "add"]:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                sdk = fixture(Path(directory))
                inventory = IDENTITY.capture(sdk)
                if mutation == "remove":
                    (sdk / "bin/mos-common.cfg").unlink()
                else:
                    (sdk / "bin/new-default.cfg").write_bytes(b"new configuration")
                with self.assertRaisesRegex(ValueError, "SDK identity changed"):
                    IDENTITY.verify(sdk, inventory)

    def test_retargeted_or_removed_symlink_is_detected(self):
        for mutation in ["retarget", "remove", "dangling"]:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                sdk = fixture(Path(directory))
                (sdk / "bin/other-clang").write_bytes(b"compiler")
                inventory = IDENTITY.capture(sdk)
                link = sdk / "bin/mos-mega65-clang"
                link.unlink()
                if mutation != "remove":
                    link.symlink_to("other-clang" if mutation == "retarget" else "missing")
                with self.assertRaises(ValueError):
                    IDENTITY.verify(sdk, inventory)

    def test_external_links_fail_closed_at_every_hop(self):
        for target in ["../outside", "../outside/../sdk/bin/clang", "internal-alias/clang"]:
            with self.subTest(target=target), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                sdk = fixture(root)
                (root / "outside").mkdir()
                (root / "outside/clang").write_bytes(b"outside compiler")
                (sdk / "external").symlink_to(target)
                if target.startswith("internal-alias"):
                    (sdk / "internal-alias").symlink_to("../outside")
                with self.assertRaisesRegex(ValueError, "escapes its root"):
                    IDENTITY.capture(sdk)

    def test_confined_directory_link_and_cycle(self):
        with tempfile.TemporaryDirectory() as directory:
            sdk = fixture(Path(directory))
            (sdk / "resource-headers").symlink_to("lib/clang/24/include", target_is_directory=True)
            inventory = IDENTITY.capture(sdk)
            self.assertEqual(inventory["entries"]["resource-headers"]["resolved_kind"], "directory")
            self.assertNotIn("resource-headers/stddef.h", inventory["entries"])
            (sdk / "cycle-a").symlink_to("cycle-b")
            (sdk / "cycle-b").symlink_to("cycle-a")
            with self.assertRaisesRegex(ValueError, "cycle"):
                IDENTITY.capture(sdk)

    def test_reading_does_not_modify_sdk_or_neighbor_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sdk = fixture(root)
            evidence = root / "archived-evidence"
            evidence.write_bytes(b"sealed historical bytes")
            paths = [evidence, sdk, *sdk.rglob("*")]

            def snapshot():
                return {str(path): (path.lstat().st_mtime_ns, path.lstat().st_ctime_ns,
                                    path.lstat().st_mode,
                                    os.readlink(path) if path.is_symlink() else
                                    path.read_bytes() if path.is_file() else None)
                        for path in paths}

            before = snapshot()
            inventory = IDENTITY.capture(sdk)
            IDENTITY.verify(sdk, inventory)
            self.assertEqual(before, snapshot())

    @unittest.skipUnless(hasattr(os, "mkfifo"), "requires a POSIX FIFO fixture")
    def test_special_file_fails_closed_without_reading_it(self):
        with tempfile.TemporaryDirectory() as directory:
            sdk = fixture(Path(directory))
            os.mkfifo(sdk / "unexpected-fifo")
            with self.assertRaisesRegex(ValueError, "unsupported file type"):
                IDENTITY.capture(sdk)


if __name__ == "__main__":
    unittest.main()
