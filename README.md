# AI CI Failure Analyzer

A small Python CLI tool for analyzing CI/test failure logs and generating readable Markdown and JSON reports.

The current version is rule-based and focuses on pytest-style failure logs. It extracts failed tests, classifies common failure types, detects potential flaky candidates, assigns severity levels, and generates CI failure summaries for faster investigation.

Future versions may include AI-assisted summaries, root cause suggestions, JUnit XML support, and Jira bug report drafts.

## Why this project exists

CI failures are often noisy and time-consuming to investigate.

This tool helps quickly extract failed tests from logs, classify common failure types, identify potential flaky failures, assign severity levels, and generate short human-readable reports with suggested next steps.

The goal is to make CI failure triage faster, more structured, and easier to understand.

## Features

* Parse pytest-style failure logs
* Detect failed tests from short summary output
* Extract failure details from pytest logs
* Classify common failure types
* Generate Markdown reports
* Generate JSON reports
* Suggest basic next steps for investigation
* Aggregate failed tests by category to highlight the most common CI failure reasons
* Detect potential flaky failures based on error category and failure patterns
* Assign severity levels to failures to help prioritize CI investigation
* Covered with pytest tests
* Can be used as a CLI tool

## Supported failure categories

* Assertion failure
* Timeout / wait issue
* UI locator issue
* API / environment connectivity issue
* Dependency / environment setup issue
* Unknown failure

## Severity levels

The tool assigns severity levels to help prioritize investigation:

* `high` - failures that may block CI execution or indicate environment, dependency, or service availability problems
* `medium` - product, test, or unclear failures that require investigation
* `low` - likely flaky or stability-related failures that still need monitoring

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
      flaky.py
      severity.py
      report.py
      json_report.py
      cli.py
  tests/
    test_parser.py
    test_classifier.py
    test_flaky.py
    test_severity.py
    test_report.py
    test_json_report.py
  samples/
    pytest_failure.log
  reports/
    report.md
    report.json
  .github/
    workflows/
      tests.yml
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

Analyze a sample pytest failure log and generate both Markdown and JSON reports:

```bash
./.venv/bin/python -m ci_failure_analyzer.cli samples/pytest_failure.log --output reports/report.md --json-output reports/report.json
```

Example result:

```text
Markdown report generated: reports/report.md
JSON report generated: reports/report.json
```

Open generated Markdown report:

```bash
cat reports/report.md
```

Open generated JSON report:

```bash
cat reports/report.json
```

Pretty-print JSON report with `jq`:

```bash
cat reports/report.json | jq
```

## Example output

After analyzing a pytest failure log, the tool generates a Markdown report with summary, failure categories, severity counts, flaky candidate detection, and detailed failure information.

Example Markdown report:

```text
# CI Failure Report

## Summary

Total failed tests: 2

## Failure Categories

| Category | Count |
|---|---:|
| Assertion failure | 1 |
| API / environment connectivity issue | 1 |

## Severity Counts

| Severity | Count |
|---|---:|
| medium | 1 |
| high | 1 |

## Failed Tests

### tests/test_export.py::test_export_image

- Error: AssertionError: assert False
- Category: Assertion failure
- Severity: medium
- Flaky candidate: No

### tests/test_api.py::test_get_user

- Error: requests.exceptions.ConnectionError
- Category: API / environment connectivity issue
- Severity: high
- Flaky candidate: Yes
```

Example JSON summary:

```json
{
  "total_failed_tests": 2,
  "failure_categories": {
    "Assertion failure": 1,
    "API / environment connectivity issue": 1
  },
  "severity_counts": {
    "medium": 1,
    "high": 1
  },
  "flaky_candidates_count": 1
}
```

Example JSON failure item:

```json
{
  "test_id": "tests/test_api.py::test_get_user",
  "error_line": "requests.exceptions.ConnectionError",
  "category": "API / environment connectivity issue",
  "severity": "high",
  "severity_reason": "High severity failure may block CI execution or indicate environment, dependency, or service availability problems.",
  "suggested_next_step": "Check service availability, network, environment config, and credentials.",
  "is_flaky_candidate": true,
  "flaky_reason": "Connectivity failure may be caused by network instability, unavailable service, or environment configuration issue."
}
```

## Running tests

Run all tests:

```bash
./.venv/bin/python -m pytest -v
```

Expected result:

```text
29 passed
```

## Current implementation

The current version contains the following main parts:

### Parser

Reads log text and extracts failed tests from pytest short summary lines.

Example line:

```text
FAILED tests/test_api.py::test_get_user - requests.exceptions.ConnectionError
```

The parser also extracts failure details from the pytest failure section when available.

### Classifier

Classifies failures using simple rule-based matching.

For example:

```text
AssertionError -> Assertion failure
ConnectionError -> API / environment connectivity issue
TimeoutError -> Timeout / wait issue
NoSuchElementException -> UI locator issue
ModuleNotFoundError -> Dependency / environment setup issue
```

### Flaky candidate detection

Detects potential flaky failures based on category and error patterns.

Examples of flaky-like signals:

```text
TimeoutError
ConnectionError
NoSuchElementException
stale element
element click intercepted
failed to establish a new connection
```

### Severity classification

Assigns severity levels based on failure category and flaky candidate status.

Examples:

```text
API / environment connectivity issue -> high
Dependency / environment setup issue -> high
Assertion failure -> medium
Timeout / wait issue + flaky candidate -> low
UI locator issue + flaky candidate -> low
Unknown failure -> medium
```

### Markdown report generator

Creates a Markdown report with:

* total number of failed tests
* failure category summary
* severity summary
* failed test names
* detected error lines
* failure categories
* severity levels
* flaky candidate status
* suggested next steps
* detailed failure blocks

### JSON report generator

Creates a machine-readable JSON report with:

* total failed tests
* failure category counts
* severity counts
* flaky candidate count
* detailed failure data for each test

## Roadmap

Planned improvements:

* Support JUnit XML reports
* Add AI-generated summaries
* Add AI-assisted root cause suggestions
* Generate Jira bug report drafts
* Add GitHub Actions summary output
* Add historical trend comparison between CI runs
* Add configuration file for custom classification rules

## Example use cases

This tool can be useful for:

* QA Automation Engineers
* SDETs
* CI/CD pipeline debugging
* Jenkins or GitHub Actions log analysis
* Test infrastructure troubleshooting
* Fast triage of failed automated test runs
* Flaky test investigation
* Quality intelligence reporting

## Status

MVP is implemented and covered with pytest tests.

Current capabilities include pytest log parsing, failure classification, Markdown and JSON reports, failure category aggregation, flaky candidate detection, severity classification, and automated test coverage.

