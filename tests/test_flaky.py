from ci_failure_analyzer.flaky import get_flaky_reason, is_flaky_candidate


def test_timeout_failure_is_flaky_candidate():
    result = is_flaky_candidate(
        category="Timeout / wait issue",
        error_line="TimeoutError: element was not visible",
    )

    assert result is True


def test_ui_locator_failure_is_flaky_candidate():
    result = is_flaky_candidate(
        category="UI locator issue",
        error_line="NoSuchElementException: unable to locate element",
    )

    assert result is True


def test_api_connectivity_failure_is_flaky_candidate():
    result = is_flaky_candidate(
        category="API / environment connectivity issue",
        error_line="requests.exceptions.ConnectionError",
    )

    assert result is True


def test_assertion_failure_is_not_flaky_candidate():
    result = is_flaky_candidate(
        category="Assertion failure",
        error_line="AssertionError: expected 200, got 500",
    )

    assert result is False


def test_keyword_based_flaky_detection():
    result = is_flaky_candidate(
        category="Unknown failure",
        error_line="Element click intercepted by another element",
    )

    assert result is True


def test_get_flaky_reason_for_non_flaky_failure():
    reason = get_flaky_reason(
        category="Assertion failure",
        error_line="AssertionError: expected 200, got 500",
    )

    assert reason == "Not detected as a flaky candidate."