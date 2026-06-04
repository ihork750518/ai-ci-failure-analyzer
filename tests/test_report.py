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