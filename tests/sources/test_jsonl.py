import logging
from pathlib import Path

import pytest

from expense_tracker.errors import SourceError
from expense_tracker.sources.jsonl import JsonlSource


def test_missing_file_raises_source_error(tmp_path: Path) -> None:
    path = tmp_path / "missing.jsonl"
    source = JsonlSource(path)

    with pytest.raises(SourceError) as exc_info:
        list(source.read())

    assert isinstance(exc_info.value.__cause__, FileNotFoundError)


def test_malformed_line_is_skipped_and_logged(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    path = tmp_path / "expenses.jsonl"
    path.write_text(
        '{"amount": 10}\n{invalid json}\n{"amount": 20}\n',
        encoding="utf-8",
    )
    source = JsonlSource(path)

    with caplog.at_level(
        logging.DEBUG,
        logger="expense_tracker.sources.jsonl",
    ):
        rows = list(source.read())

    assert rows == [{"amount": 10}, {"amount": 20}]
    assert "skip malformed line 2" in caplog.text
