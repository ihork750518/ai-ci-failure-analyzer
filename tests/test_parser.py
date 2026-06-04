from ci_failure_analyzer.parser import parse_failed_tests


def test_parse_failed_tests():
    log_text = """
FAILED tests/test_export.py::test_export_image - AssertionError: assert False
FAILED tests/test_api.py::test_get_user - requests.exceptions.ConnectionError
"""

    failed_tests = parse_failed_tests(log_text)

    assert len(failed_tests) == 2
    assert failed_tests[0].test_id == "tests/test_export.py::test_export_image"
    assert failed_tests[0].error_line == "AssertionError: assert False"
    assert failed_tests[1].test_id == "tests/test_api.py::test_get_user"
    assert failed_tests[1].error_line == "requests.exceptions.ConnectionError"