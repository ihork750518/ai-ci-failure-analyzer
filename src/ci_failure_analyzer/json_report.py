import json
from ci_failure_analyzer.classifier import classify_failure
from ci_failure_analyzer.parser import FailedTest
from ci_failure_analyzer.report import suggest_next_step


def generate_json_report(failed_tests: list[FailedTest]) -> str:
    failures = []

    for test in failed_tests:
        category = classify_failure(test.error_line)

        failures.append(
            {
                "test_id": test.test_id,
                "error_line": test.error_line,
                "category": category,
                "suggested_next_step": suggest_next_step(category),
                "failure_block": test.failure_block,
            }
        )

    report = {
        "total_failed_tests": len(failed_tests),
        "failures": failures,
    }

    return json.dumps(report, indent=2, ensure_ascii=False)