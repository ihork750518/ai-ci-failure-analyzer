from collections import Counter

from ci_failure_analyzer.classifier import classify_failure
from ci_failure_analyzer.flaky import get_flaky_reason, is_flaky_candidate
from ci_failure_analyzer.parser import FailedTest
from ci_failure_analyzer.severity import get_failure_severity, get_severity_reason


def generate_markdown_report(failed_tests: list[FailedTest]) -> str:
    lines: list[str] = []

    lines.append("# CI Failure Report")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"Total failed tests: {len(failed_tests)}")
    lines.append("")

    if not failed_tests:
        lines.append("No failed tests detected.")
        lines.append("")
        return "\n".join(lines)

    categories = [
        classify_failure(test.error_line)
        for test in failed_tests
    ]

    failure_trends = Counter(categories)

    lines.append("## Failure Categories")
    lines.append("")
    lines.append("| Category | Count |")
    lines.append("|---|---:|")

    for category, count in failure_trends.items():
        lines.append(f"| {category} | {count} |")

    lines.append("")

    severity_counts = build_severity_counts(failed_tests)

    lines.append("## Severity Counts")
    lines.append("")
    lines.append("| Severity | Count |")
    lines.append("|---|---:|")

    for severity, count in severity_counts.items():
        lines.append(f"| {severity} | {count} |")

    lines.append("")
    lines.append("## Failed Tests")
    lines.append("")

    for test in failed_tests:
        category = classify_failure(test.error_line)
        flaky_candidate = is_flaky_candidate(
            category=category,
            error_line=test.error_line,
        )
        severity = get_failure_severity(
            category=category,
            is_flaky_candidate=flaky_candidate,
        )

        lines.append(f"### {test.test_id}")
        lines.append("")
        lines.append(f"- Error: `{test.error_line}`")
        lines.append(f"- Category: **{category}**")
        lines.append(f"- Severity: **{severity}**")
        lines.append(f"- Severity reason: {get_severity_reason(severity)}")
        lines.append(f"- Suggested next step: {suggest_next_step(category)}")
        lines.append(f"- Flaky candidate: **{format_bool(flaky_candidate)}**")
        lines.append(
            f"- Flaky reason: {get_flaky_reason(category=category, error_line=test.error_line)}"
        )
        lines.append("")

        if test.failure_block:
            lines.append("<details>")
            lines.append("<summary>Failure details</summary>")
            lines.append("")
            lines.append("```text")
            lines.append(test.failure_block)
            lines.append("```")
            lines.append("")
            lines.append("</details>")
            lines.append("")

    return "\n".join(lines)


def build_severity_counts(failed_tests: list[FailedTest]) -> dict[str, int]:
    severity_counts: dict[str, int] = {}

    for test in failed_tests:
        category = classify_failure(test.error_line)
        flaky_candidate = is_flaky_candidate(
            category=category,
            error_line=test.error_line,
        )
        severity = get_failure_severity(
            category=category,
            is_flaky_candidate=flaky_candidate,
        )

        severity_counts[severity] = severity_counts.get(severity, 0) + 1

    return severity_counts


def format_bool(value: bool) -> str:
    if value:
        return "Yes"

    return "No"


def suggest_next_step(category: str) -> str:
    suggestions = {
        "Assertion failure": "Check expected vs actual result and test data.",
        "Timeout / wait issue": "Check waits, performance, and environment stability.",
        "UI locator issue": "Verify selector stability and recent UI changes.",
        "API / environment connectivity issue": "Check service availability, network, environment config, and credentials.",
        "Dependency / environment setup issue": "Check installed dependencies and CI environment setup.",
        "Unknown failure": "Review full stack trace and logs manually.",
    }

    return suggestions.get(category, "Review logs manually.")