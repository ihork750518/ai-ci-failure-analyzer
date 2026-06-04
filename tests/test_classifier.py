from ci_failure_analyzer.classifier import classify_failure


def test_classify_assertion_error():
    assert classify_failure("AssertionError: assert False") == "Assertion failure"


def test_classify_connection_error():
    assert (
        classify_failure("requests.exceptions.ConnectionError")
        == "API / environment connectivity issue"
    )


def test_classify_unknown_error():
    assert classify_failure("Something strange happened") == "Unknown failure"