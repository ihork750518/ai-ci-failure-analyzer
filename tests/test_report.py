from ci_failure_analyzer.parser import FailedTest
from ci_failure_analyzer.report import generate_markdown_report


def test_generate_markdown_report():
    failed_tests = [
        FailedTest(
            test_id="tests/test_export.py::test_export_image",
            error_line="AssertionError: assert False",
        )
    ]

    report = generate_markdown_report(failed_tests)

    assert "# CI Failure Report" in report
    assert "Total failed tests: 1" in report
    assert "Assertion failure" in report
    assert "Check expected vs actual result and test data." in report


def test_generate_report_without_failures():
    report = generate_markdown_report([])

    assert "Total failed tests: 0" in report
    assert "No failed tests detected." in report


def test_generate_report_with_failure_block():
    failed_tests = [
        FailedTest(
            test_id="tests/test_export.py::test_export_image",
            error_line="AssertionError: assert False",
            failure_block="E       AssertionError: assert False",
        )
    ]

    report = generate_markdown_report(failed_tests)

    assert "<details>" in report
    assert "Failure details" in report
    assert "E       AssertionError: assert False" in report


def test_markdown_report_contains_flaky_candidate_info():
    failed_tests = [
        FailedTest(
            test_id="tests/test_api.py::test_get_user",
            error_line="requests.exceptions.ConnectionError",
            failure_block="ConnectionError details",
        )
    ]

    report = generate_markdown_report(failed_tests)

    assert "- Flaky candidate: **Yes**" in report
    assert "- Flaky reason: Connectivity failure may be caused by network instability, unavailable service, or environment configuration issue." in report


def test_markdown_report_contains_severity_info():
    failed_tests = [
        FailedTest(
            test_id="tests/test_api.py::test_get_user",
            error_line="requests.exceptions.ConnectionError",
            failure_block="ConnectionError details",
        )
    ]

    report = generate_markdown_report(failed_tests)

    assert "## Severity Counts" in report
    assert "| Severity | Count |" in report
    assert "| high | 1 |" in report
    assert "- Severity: **high**" in report
    assert (
        "- Severity reason: High severity failure may block CI execution "
        "or indicate environment, dependency, or service availability problems."
    ) in report