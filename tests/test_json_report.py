import json

from ci_failure_analyzer.json_report import generate_json_report
from ci_failure_analyzer.parser import FailedTest


def test_generate_json_report():
    failed_tests = [
        FailedTest(
            test_id="tests/test_export.py::test_export_image",
            error_line="AssertionError: assert False",
            failure_block="E       AssertionError: assert False",
        )
    ]

    report_text = generate_json_report(failed_tests)
    report = json.loads(report_text)

    assert report["total_failed_tests"] == 1
    assert len(report["failures"]) == 1

    failure = report["failures"][0]

    assert failure["test_id"] == "tests/test_export.py::test_export_image"
    assert failure["error_line"] == "AssertionError: assert False"
    assert failure["category"] == "Assertion failure"
    assert failure["suggested_next_step"] == "Check expected vs actual result and test data."
    assert failure["failure_block"] == "E       AssertionError: assert False"


def test_generate_json_report_without_failures():
    report_text = generate_json_report([])
    report = json.loads(report_text)

    assert report["total_failed_tests"] == 0
    assert report["failures"] == []