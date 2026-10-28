"""Host-only validator path regression: all commands and target results are mocked.

Disposable output and SDK fixtures never touch sealed packets or the real SDK.
"""
from contextlib import redirect_stdout
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, call, patch

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location(
    "m2rb_validate_sdk_path", ROOT / "tools/flight_demo/m2_rebuild/validate.py")
VALIDATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATE)
IDENTITY = VALIDATE.module(ROOT / "tools/flight_demo/m2_rebuild/toolchain_identity.py",
                           "m2rb_test_sdk_identity")


class ValidateSdkPath(unittest.TestCase):
    def check_sdk_path(self, spelling, compile_exit=0):
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory).resolve()
            caller, repository = temporary / "caller", temporary / "repository"
            caller.mkdir()
            repository.mkdir()
            # Read-only source links support the real generator and input hashes.
            for name in ["interfaces", "memory", "src", "tools", "tests"]:
                (repository / name).symlink_to(ROOT / name, target_is_directory=True)
            sdk = caller / "sdk"
            shadow = repository / "sdk"
            for tree, content in [(sdk, b"selected SDK"), (shadow, b"wrong SDK")]:
                (tree / "bin").mkdir(parents=True)
                for tool in ["mos-mega65-clang", "llvm-objdump", "llvm-nm"]:
                    (tree / "bin" / tool).write_bytes(content + tool.encode())
            (caller / "sdk-alias").symlink_to(sdk, target_is_directory=True)
            lock = {"llvm_mos": {
                "compiler_sha256": VALIDATE.sha(sdk / "bin/mos-mega65-clang"),
                "objdump_sha256": VALIDATE.sha(sdk / "bin/llvm-objdump")}}
            (repository / "toolchain").mkdir()
            (repository / "toolchain/f65_toolchain.lock.json").write_text(json.dumps(lock))
            output = repository / "disposable-output/run"
            sdk_argument = {"relative": Path("sdk"), "absolute": sdk,
                            "symlink": Path("sdk-alias")}[spelling]
            identity = Mock(capture=Mock(wraps=IDENTITY.capture),
                            verify=Mock(wraps=IDENTITY.verify), digest=IDENTITY.digest)
            original_module = VALIDATE.module

            def load_module(path, name):
                if name == "m2rb_sdk_identity":
                    return identity
                if name in ["m2rb_startup_check", "m2rb_stack"]:
                    return Mock(check=Mock(return_value={"status": "MOCK ONLY"}))
                return original_module(path, name)

            def run_mock(command, **kwargs):
                self.assertEqual(kwargs["cwd"], repository)
                tool = Path(command[0]).name
                stdout = ""
                status = 0
                if command[0] == "git":
                    self.assertEqual(command[1:3], ["merge-base", "--is-ancestor"])
                elif tool == "mos-mega65-clang":
                    # Synthetic bytes only; no compiler or linker is invoked.
                    status = compile_exit
                    if status == 0:
                        (output / "UNADMITTED.prg").write_bytes(b"mock PRG")
                        (output / "UNADMITTED.map").write_text("2001 2001 10 1 .text\n")
                elif tool == "llvm-nm":
                    stdout = "\n".join([
                        "m2rb_dispatch", "m2rb_camera_edges", "m2rb_platform_init", "m2rb_glyph",
                        "m2_prepare", "m2_project_prepared", "m2_ground_prepared", "m2rb_io_commit",
                        "m1_tick", "m1_input_sample", "m1_acquire", "r0f_pf_flat_copy"])
                else:
                    self.assertEqual(tool, "llvm-objdump")
                return subprocess.CompletedProcess(command, status, stdout, "")

            previous_cwd = Path.cwd()
            try:
                os.chdir(caller)
                with patch.object(VALIDATE, "ROOT", repository), \
                     patch.object(VALIDATE, "module", side_effect=load_module), \
                     patch.object(VALIDATE, "sha", wraps=VALIDATE.sha) as hashes, \
                     patch.object(VALIDATE.subprocess, "check_output", return_value=VALIDATE.BASE), \
                     patch.object(VALIDATE.subprocess, "run", side_effect=run_mock) as commands, \
                     patch.object(VALIDATE.subprocess, "Popen", side_effect=AssertionError("real subprocess forbidden")), \
                     redirect_stdout(io.StringIO()):
                    result = VALIDATE.execute("target", sdk_argument, output)
            finally:
                os.chdir(previous_cwd)

            self.assertEqual(result, 0 if compile_exit == 0 else 1)
            identity.capture.assert_called_once_with(sdk)
            inventory = json.loads((output / "sdk-inputs-before.json").read_text())
            identity.verify.assert_called_once_with(sdk, inventory)
            for tool in ["mos-mega65-clang", "llvm-objdump"]:
                self.assertIn(call(sdk / "bin" / tool), hashes.call_args_list)
            report = json.loads((output / "result.json").read_text())
            self.assertEqual(report["toolchain"]["sdk"], str(sdk))
            self.assertEqual(inventory["sdk_root"], str(sdk))
            self.assertTrue(report["toolchain"]["sdk_unchanged_after_link"])
            expected_tools = ["mos-mega65-clang"]
            if compile_exit == 0:
                expected_tools += ["llvm-objdump", "llvm-nm"]
            expected_paths = [str(sdk / "bin" / tool) for tool in expected_tools]
            self.assertEqual([entry["argv"][0] for entry in report["commands"]], expected_paths)
            self.assertEqual([call.args[0][0] for call in commands.call_args_list
                              if call.args[0][0] != "git"], expected_paths)
            self.assertEqual(report["compile_link"], "PASS" if compile_exit == 0 else "FAIL")
            # Both successful and failing mocked attempts retain their own seal.
            seal = json.loads((output / "seal.json").read_text())
            for name, expected in seal.items():
                self.assertEqual(VALIDATE.sha(output / name), expected["sha256"])

    def test_relative_sdk_uses_caller_identity_for_every_tool(self):
        self.check_sdk_path("relative")

    def test_absolute_sdk_is_preserved(self):
        self.check_sdk_path("absolute")

    def test_relative_sdk_alias_is_normalized(self):
        self.check_sdk_path("symlink")

    def test_compile_failure_verifies_same_absolute_sdk(self):
        self.check_sdk_path("relative", compile_exit=1)


if __name__ == "__main__":
    unittest.main()
