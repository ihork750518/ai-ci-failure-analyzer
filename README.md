# AI CI Failure Analyzer

A small Python tool for analyzing CI/test failure logs and generating readable Markdown reports.

The current version is rule-based and focuses on pytest-style failure logs.
Future versions may include AI-assisted summaries, root cause suggestions, flaky test detection, and Jira bug report drafts.

## Why this project exists

CI failures are often noisy and time-consuming to investigate.
This tool helps quickly extract failed tests from logs, classify common failure types, and generate a short human-readable report with suggested next steps.

## Features

* Parse pytest-style failure logs
* Detect failed tests from short summary output
* Classify common failure types
* Generate Markdown reports
* Suggest basic next steps for investigation
* Covered with pytest tests
* Can be used as a CLI tool
* Aggregates failed tests by category to highlight the most common CI failure reasons.
* Detects potential flaky failures based on error category and failure patterns.
* Assigns severity levels to failures to help prioritize CI investigation.

## Supported failure categories

* Assertion failure
* Timeout / wait issue
* UI locator issue
* API / environment connectivity issue
* Dependency / environment setup issue
* Unknown failure

## Project structure

```text
ai-ci-failure-analyzer/
  README.md
  pyproject.toml
  src/
    ci_failure_analyzer/
      __init__.py
      parser.py
      classifier.py
      report.py
      cli.py
  tests/
    test_parser.py
    test_classifier.py
    test_report.py
  samples/
    pytest_failure.log
  reports/
    report.md
```

## Installation

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project in editable mode with development dependencies:

```bash
./.venv/bin/python -m pip install -e ".[dev]"
```

## Usage

Analyze a sample pytest failure log:

```bash
./.venv/bin/python -m ci_failure_analyzer.cli samples/pytest_failure.log --output reports/report.md
```

Example result:

```text
Report generated: reports/report.md
```

Open generated report:

```bash
cat reports/report.md
```

## Example output

```markdown
# CI Failure Report

## Summary

Total failed tests: 2

## Failed Tests

### tests/test_export.py::test_export_image

- Error: `AssertionError: assert False`
- Category: **Assertion failure**
- Suggested next step: Check expected vs actual result and test data.

### tests/test_api.py::test_get_user

- Error: `requests.exceptions.ConnectionError`
- Category: **API / environment connectivity issue**
- Suggested next step: Check service availability, network, environment config, and credentials.
```

## Running tests

Run all tests:

```bash
./.venv/bin/python -m pytest -v
```

Expected result:

```text
6 passed
```

## Current implementation

The MVP contains three main parts:

### Parser

Reads log text and extracts failed tests from pytest short summary lines.

Example line:

```text
FAILED tests/test_api.py::test_get_user - requests.exceptions.ConnectionError
```

### Classifier

Classifies failures using simple rule-based matching.

For example:

```text
AssertionError -> Assertion failure
ConnectionError -> API / environment connectivity issue
TimeoutError -> Timeout / wait issue
```

### Report generator

Creates a Markdown report with:

* total number of failed tests
* failed test names
* detected error lines
* failure categories
* suggested next steps

## Roadmap

Planned improvements:

* Parse full stack traces
* Support JUnit XML reports
* Add flaky test detection
* Add failure grouping by category
* Add GitHub Actions workflow
* Add AI-generated summaries
* Generate Jira bug report drafts
* Export reports in JSON format

## Example use cases

This tool can be useful for:

* QA Automation Engineers
* SDETs
* CI/CD pipeline debugging
* Jenkins or GitHub Actions log analysis
* Test infrastructure troubleshooting
* Fast triage of failed automated test runs

## Status

MVP is implemented and covered with basic tests.

