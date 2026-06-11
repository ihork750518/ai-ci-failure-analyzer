import json

from ci_failure_analyzer.json_report import generate_json_report
from ci_failure_analyzer.parser import FailedTest


def test_generate_json_report_contains_failures():
    failed_tests = [
        FailedTest(
            test_id="test_login",
            error_line="AssertionError: expected 200, got 500",
            failure_block="Full failure details",
        )
    ]

    report = generate_json_report(failed_tests)
    data = json.loads(report)

    assert data["total_failed_tests"] == 1
    assert len(data["failures"]) == 1

    failure = data["failures"][0]

    assert failure["test_id"] == "test_login"
    assert failure["error_line"] == "AssertionError: expected 200, got 500"
    assert failure["category"] == "Assertion failure"
    assert failure["suggested_next_step"] == "Check expected vs actual result and test data."
    assert failure["failure_block"] == "Full failure details"


def test_generate_json_report_contains_failure_categories():
    failed_tests = [
        FailedTest(
            test_id="test_one",
            error_line="AssertionError: expected 200, got 500",
            failure_block="",
        ),
        FailedTest(
            test_id="test_two",
            error_line="AssertionError: expected true",
            failure_block="",
        ),
        FailedTest(
            test_id="test_three",
            error_line="TimeoutError: element was not visible",
            failure_block="",
        ),
    ]

    report = generate_json_report(failed_tests)
    data = json.loads(report)

    assert data["failure_categories"]["Assertion failure"] == 2
    assert data["failure_categories"]["Timeout / wait issue"] == 1


def test_generate_json_report_with_no_failures():
    report = generate_json_report([])
    data = json.loads(report)

    assert data["total_failed_tests"] == 0
    assert data["failure_categories"] == {}
    assert data["failures"] == []