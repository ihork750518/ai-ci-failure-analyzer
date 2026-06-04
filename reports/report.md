# CI Failure Report

## Summary

Total failed tests: 2

## Failed Tests

### tests/test_export.py::test_export_image

- Error: `AssertionError: assert False`
- Category: **Assertion failure**
- Suggested next step: Check expected vs actual result and test data.

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

<details>
<summary>Failure details</summary>

```text
def test_get_user():
>       response = requests.get("https://api.example.com/users/1")
E       requests.exceptions.ConnectionError: Failed to establish a new connection

tests/test_api.py:8: ConnectionError
```

</details>
