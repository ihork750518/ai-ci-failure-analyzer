from ci_failure_analyzer.severity import get_failure_severity, get_severity_reason


def test_api_connectivity_issue_has_high_severity():
    severity = get_failure_severity(
        category="API / environment connectivity issue",
    )

    assert severity == "high"


def test_dependency_issue_has_high_severity():
    severity = get_failure_severity(
        category="Dependency / environment setup issue",
    )

    assert severity == "high"


def test_assertion_failure_has_medium_severity():
    severity = get_failure_severity(
        category="Assertion failure",
    )

    assert severity == "medium"


def test_timeout_flaky_candidate_has_low_severity():
    severity = get_failure_severity(
        category="Timeout / wait issue",
        is_flaky_candidate=True,
    )

    assert severity == "low"


def test_timeout_non_flaky_failure_has_medium_severity():
    severity = get_failure_severity(
        category="Timeout / wait issue",
        is_flaky_candidate=False,
    )

    assert severity == "medium"


def test_ui_locator_flaky_candidate_has_low_severity():
    severity = get_failure_severity(
        category="UI locator issue",
        is_flaky_candidate=True,
    )

    assert severity == "low"


def test_unknown_failure_has_medium_severity():
    severity = get_failure_severity(
        category="Unknown failure",
    )

    assert severity == "medium"


def test_unknown_category_defaults_to_medium_severity():
    severity = get_failure_severity(
        category="Something unexpected",
    )

    assert severity == "medium"


def test_get_severity_reason_for_high_severity():
    reason = get_severity_reason("high")

    assert reason == (
        "High severity failure may block CI execution or indicate environment, "
        "dependency, or service availability problems."
    )


def test_get_severity_reason_for_unknown_severity():
    reason = get_severity_reason("critical")

    assert reason == "Severity could not be determined, manual review is recommended."