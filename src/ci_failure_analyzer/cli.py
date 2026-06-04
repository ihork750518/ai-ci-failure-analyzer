import argparse
from pathlib import Path

from ci_failure_analyzer.json_report import generate_json_report
from ci_failure_analyzer.parser import read_log_file, parse_failed_tests
from ci_failure_analyzer.report import generate_markdown_report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze CI/test failure logs and generate reports."
    )

    parser.add_argument(
        "log_file",
        help="Path to pytest/Jenkins log file.",
    )

    parser.add_argument(
        "--output",
        default="reports/report.md",
        help="Path to output Markdown report.",
    )

    parser.add_argument(
        "--json-output",
        help="Optional path to output JSON report.",
    )

    args = parser.parse_args()

    log_text = read_log_file(args.log_file)
    failed_tests = parse_failed_tests(log_text)

    markdown_report = generate_markdown_report(failed_tests)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown_report, encoding="utf-8")

    print(f"Markdown report generated: {output_path}")

    if args.json_output:
        json_report = generate_json_report(failed_tests)

        json_output_path = Path(args.json_output)
        json_output_path.parent.mkdir(parents=True, exist_ok=True)
        json_output_path.write_text(json_report, encoding="utf-8")

        print(f"JSON report generated: {json_output_path}")


if __name__ == "__main__":
    main()