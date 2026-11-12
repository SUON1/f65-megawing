"""In-memory negative probes; stdout only, never edits source or evidence."""
import argparse
import importlib.util
import inspect
import io
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools/flight_demo/m2_rebuild"))
import corrected_clock_preflight as subject


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=("helper", "caller"))
    kind = parser.parse_args().kind
    spec = importlib.util.spec_from_file_location("wait_p2_regressions",
        ROOT / "tests/flight_demo/m2_rebuild/test_corrected_clock_preflight.py")
    tests = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tests)
    cases = ("test_wait_bound_both_edges_miss_and_first_poll",
             "test_first_poll_closing_window_counterexample",
             "test_schedule_wait_result_against_independent_timeline")
    name = "publication_wait_bound" if kind == "helper" else "conditional_schedule"
    original = getattr(subject, name)
    source = inspect.getsource(original)
    before, after = (("2 * poll_gap_cycles", "poll_gap_cycles") if kind == "helper" else
        ('wait = publication_wait_bound(frame_upper, interior, gap, costs["publication"])',
         'wait = frame_upper - interior + gap + costs["publication"]'))
    if source.count(before) != 1:
        raise ValueError("unsupported mutation witness")
    mutated = source.replace(before, after, 1)
    scope = dict(vars(subject))
    exec(compile(mutated, f"<in-memory {kind} mutation>", "exec"), scope)
    stream = io.StringIO()
    try:
        setattr(subject, name, scope[name])
        suite = unittest.TestSuite(tests.ConditionalScheduleTests(case) for case in cases)
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    finally:
        setattr(subject, name, original)
    failures = {test._testMethodName for test, _ in result.failures}
    expected = set(cases) if kind == "helper" else {cases[-1]}
    refused = failures == expected and not result.errors and result.testsRun == len(cases)
    print(json.dumps({"kind": kind, "mutation_refused": refused,
                      "expected_failure_names": sorted(expected),
                      "actual_failure_names": sorted(failures),
                      "tests_run": result.testsRun, "errors": len(result.errors),
                      "mutated_source": mutated, "test_output": stream.getvalue(),
                      "source_files_modified": False, "execution_authorized": False}, indent=2))
    return 0 if refused else 1


if __name__ == "__main__":
    raise SystemExit(main())
