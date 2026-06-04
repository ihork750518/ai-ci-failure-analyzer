from dataclasses import dataclass
from pathlib import Path


@dataclass
class FailedTest:
    test_id: str
    error_line: str
    failure_block: str = ""


def read_log_file(file_path: str | Path) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {path}")

    return path.read_text(encoding="utf-8")


def parse_failed_tests(log_text: str) -> list[FailedTest]:
    failed_tests: list[FailedTest] = []

    summary_failures = _parse_short_summary_failures(log_text)
    failure_blocks = _parse_failure_blocks(log_text)

    for test_id, error_line in summary_failures:
        failed_tests.append(
            FailedTest(
                test_id=test_id,
                error_line=error_line,
                failure_block=failure_blocks.get(_extract_test_name(test_id), ""),
            )
        )

    return failed_tests


def _parse_short_summary_failures(log_text: str) -> list[tuple[str, str]]:
    failures: list[tuple[str, str]] = []

    for line in log_text.splitlines():
        line = line.strip()

        if line.startswith("FAILED "):
            parts = line.split(" - ", maxsplit=1)

            test_id = parts[0].replace("FAILED ", "").strip()
            error_line = parts[1].strip() if len(parts) > 1 else "Unknown error"

            failures.append((test_id, error_line))

    return failures


def _parse_failure_blocks(log_text: str) -> dict[str, str]:
    blocks: dict[str, str] = {}
    lines = log_text.splitlines()

    current_test_name: str | None = None
    current_block: list[str] = []

    for line in lines:
        stripped = line.strip()

        if _is_failure_header(stripped):
            if current_test_name and current_block:
                blocks[current_test_name] = "\n".join(current_block).strip()

            current_test_name = _normalize_failure_header(stripped)
            current_block = []
            continue

        if current_test_name:
            if stripped.startswith("FAILED "):
                blocks[current_test_name] = "\n".join(current_block).strip()
                current_test_name = None
                current_block = []
                continue

            current_block.append(line)

    if current_test_name and current_block:
        blocks[current_test_name] = "\n".join(current_block).strip()

    return blocks


def _is_failure_header(line: str) -> bool:
    return (
        line.startswith("_")
        and line.endswith("_")
        and len(line.strip("_").strip()) > 0
    )


def _normalize_failure_header(line: str) -> str:
    return line.strip("_").strip()


def _extract_test_name(test_id: str) -> str:
    return test_id.split("::")[-1]