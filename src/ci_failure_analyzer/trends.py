from collections import Counter
from typing import Any


def build_failure_trends(failures: list[dict[str, Any]]) -> dict[str, int]:
    """
    Builds a summary of failure categories.

    Example:
    {
        "Assertion failure": 2,
        "Timeout / wait issue": 1
    }
    """
    categories = [
        failure.get("category", "Unknown failure")
        for failure in failures
    ]

    return dict(Counter(categories))