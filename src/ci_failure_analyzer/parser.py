from dataclasses import dataclass
from pathlib import Path


@dataclass
class FailedTest:
    test_id: str
    error_line: str


def read_log_file(file_path: str | Path) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {path}")

    return path.read_text(encoding="utf-8")


def parse_failed_tests(log_text: str) -> list[FailedTest]:
    failed_tests: list[FailedTest] = []

    for line in log_text.splitlines():
        line = line.strip()

        if line.startswith("FAILED "):
            parts = line.split(" - ", maxsplit=1)

            test_id = parts[0].replace("FAILED ", "").strip()
            error_line = parts[1].strip() if len(parts) > 1 else "Unknown error"

            failed_tests.append(
                FailedTest(
                    test_id=test_id,
                    error_line=error_line,
                )
            )

    return failed_tests