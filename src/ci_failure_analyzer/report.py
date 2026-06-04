from ci_failure_analyzer.classifier import classify_failure
from ci_failure_analyzer.parser import FailedTest


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

    lines.append("## Failed Tests")
    lines.append("")

    for test in failed_tests:
        category = classify_failure(test.error_line)

        lines.append(f"### {test.test_id}")
        lines.append("")
        lines.append(f"- Error: `{test.error_line}`")
        lines.append(f"- Category: **{category}**")
        lines.append(f"- Suggested next step: {suggest_next_step(category)}")
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