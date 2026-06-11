def get_failure_severity(category: str, is_flaky_candidate: bool = False) -> str:
    """
    Returns severity level for a failure category.

    Severity levels:
    - high: failures that may block CI or indicate environment/service problems
    - medium: product or test assertion failures that need investigation
    - low: likely unstable/flaky issues that may need stabilization
    """

    if category == "API / environment connectivity issue":
        return "high"

    if category == "Dependency / environment setup issue":
        return "high"

    if category == "Assertion failure":
        return "medium"

    if category == "Timeout / wait issue":
        if is_flaky_candidate:
            return "low"

        return "medium"

    if category == "UI locator issue":
        if is_flaky_candidate:
            return "low"

        return "medium"

    if category == "Unknown failure":
        return "medium"

    return "medium"


def get_severity_reason(severity: str) -> str:
    reasons = {
        "high": "High severity failure may block CI execution or indicate environment, dependency, or service availability problems.",
        "medium": "Medium severity failure requires investigation because it may indicate a product issue, test issue, or unclear failure reason.",
        "low": "Low severity failure looks like a possible flaky or stability-related issue, but still needs monitoring.",
    }

    return reasons.get(
        severity,
        "Severity could not be determined, manual review is recommended.",
    )