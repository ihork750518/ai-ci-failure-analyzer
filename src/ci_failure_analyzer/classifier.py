def classify_failure(error_line: str) -> str:
    error = error_line.lower()

    if "assertionerror" in error:
        return "Assertion failure"

    if "timeouterror" in error or "timeout" in error:
        return "Timeout / wait issue"

    if "nosuchelementexception" in error:
        return "UI locator issue"

    if "connectionerror" in error or "failed to establish" in error:
        return "API / environment connectivity issue"

    if "modulenotfounderror" in error:
        return "Dependency / environment setup issue"

    return "Unknown failure"