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


def test_parse_failure_block():
    log_text = """
================================== FAILURES ===================================

____________________________ test_export_image _____________________________

    def test_export_image():
>       assert output_file.exists()
E       AssertionError: assert False

tests/test_export.py:12: AssertionError

=========================== short test summary info ============================
FAILED tests/test_export.py::test_export_image - AssertionError: assert False
"""

    failed_tests = parse_failed_tests(log_text)

    assert len(failed_tests) == 1
    assert failed_tests[0].test_id == "tests/test_export.py::test_export_image"
    assert "assert output_file.exists()" in failed_tests[0].failure_block
    assert "AssertionError" in failed_tests[0].failure_block