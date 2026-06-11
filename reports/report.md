# CI Failure Report

## Summary

Total failed tests: 2

## Failure Categories

| Category | Count |
|---|---:|
| Assertion failure | 1 |
| API / environment connectivity issue | 1 |

## Failed Tests

### tests/test_export.py::test_export_image

- Error: `AssertionError: assert False`
- Category: **Assertion failure**
- Suggested next step: Check expected vs actual result and test data.
- Flaky candidate: **No**
- Flaky reason: Not detected as a flaky candidate.

<details>
<summary>Failure details</summary>

```text
def test_export_image():
>       assert output_file.exists()
E       AssertionError: assert False

tests/test_export.py:12: AssertionError
```

</details>

### tests/test_api.py::test_get_user

- Error: `requests.exceptions.ConnectionError`
- Category: **API / environment connectivity issue**
- Suggested next step: Check service availability, network, environment config, and credentials.
- Flaky candidate: **Yes**
- Flaky reason: Connectivity failure may be caused by network instability, unavailable service, or environment configuration issue.

<details>
<summary>Failure details</summary>

```text
def test_get_user():
>       response = requests.get("https://api.example.com/users/1")
E       requests.exceptions.ConnectionError: Failed to establish a new connection

tests/test_api.py:8: ConnectionError
```

</details>
