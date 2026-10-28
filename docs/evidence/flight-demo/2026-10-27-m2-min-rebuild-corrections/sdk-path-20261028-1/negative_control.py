"""Host-only negative control against the preserved pre-fix validator in memory."""
import importlib.util
import sys
import unittest
from pathlib import Path
root=Path('/Users/slice/Developer/f65-megawing-m2-source-baseline')
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path)
 module=importlib.util.module_from_spec(spec)
 spec.loader.exec_module(module)
 return module
test=load(root/'tests/flight_demo/m2_rebuild/test_validate_sdk_path.py','path_tests_negative_control')
test.VALIDATE=load(Path('/private/tmp/f65-sdk-path-6qe2lrcp/before/tools/flight_demo/m2_rebuild/validate.py'),'pre_fix_validator')
suite=unittest.TestSuite([test.ValidateSdkPath('test_relative_sdk_uses_caller_identity_for_every_tool')])
result=unittest.TextTestRunner(verbosity=2).run(suite)
expected=(result.testsRun==1 and len(result.failures)==1 and not result.errors
          and 'Expected: capture(PosixPath(' in result.failures[0][1]
          and "Actual: capture(PosixPath('sdk'))" in result.failures[0][1])
print('Negative control: '+('PASS; prior relative-path defect detected' if expected else 'FAIL; unexpected outcome'))
sys.exit(0 if expected else 1)
