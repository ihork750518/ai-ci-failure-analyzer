def is_flaky_candidate(category: str, error_line: str) -> bool:
    flaky_categories = {
        "Timeout / wait issue",
        "UI locator issue",
        "API / environment connectivity issue",
    }

    flaky_keywords = [
        "timeout",
        "timed out",
        "connectionerror",
        "connection refused",
        "failed to establish",
        "no such element",
        "stale element",
        "element not interactable",
        "element click intercepted",
    ]

    if category in flaky_categories:
        return True

    normalized_error = error_line.lower()

    return any(
        keyword in normalized_error
        for keyword in flaky_keywords
    )


def get_flaky_reason(category: str, error_line: str) -> str:
    if not is_flaky_candidate(category, error_line):
        return "Not detected as a flaky candidate."

    if category == "Timeout / wait issue":
        return "Timeout-based failure may be caused by slow environment, unstable waits, or performance issues."

    if category == "UI locator issue":
        return "UI-related failure may be caused by unstable selectors, timing issues, or recent UI changes."

    if category == "API / environment connectivity issue":
        return "Connectivity failure may be caused by network instability, unavailable service, or environment configuration issue."

    return "Failure contains patterns commonly associated with flaky or environment-dependent tests."