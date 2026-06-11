import json
from typing import Any

from ci_failure_analyzer.classifier import classify_failure
from ci_failure_analyzer.flaky import get_flaky_reason, is_flaky_candidate
from ci_failure_analyzer.parser import FailedTest


def generate_json_report(failed_tests: list[FailedTest]) -> str:
    failures: list[dict[str, Any]] = []

    for test in failed_tests:
        category = classify_failure(test.error_line)

        failures.append(
            {
                "test_id": test.test_id,
                "error_line": test.error_line,
                "category": category,
                "suggested_next_step": suggest_next_step(category),
                "is_flaky_candidate": is_flaky_candidate(
                    category=category,
                    error_line=test.error_line,
                ),
                "flaky_reason": get_flaky_reason(
                    category=category,
                    error_line=test.error_line,
                ),
                "failure_block": test.failure_block,
            }
        )

    report_data = {
        "total_failed_tests": len(failed_tests),
        "failure_categories": build_failure_categories(failures),
        "flaky_candidates_count": count_flaky_candidates(failures),
        "failures": failures,
    }

    return json.dumps(report_data, indent=2)


def build_failure_categories(failures: list[dict[str, Any]]) -> dict[str, int]:
    categories: dict[str, int] = {}

    for failure in failures:
        category = failure["category"]
        categories[category] = categories.get(category, 0) + 1

    return categories


def count_flaky_candidates(failures: list[dict[str, Any]]) -> int:
    return sum(
        1
        for failure in failures
        if failure["is_flaky_candidate"]
    )


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