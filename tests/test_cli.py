from pathlib import Path

import pytest

from expense_tracker.cli import main


def test_missing_file_exits_with_code_1(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    missing_file = tmp_path / "missing.jsonl"
    monkeypatch.setattr(
        "sys.argv",
        ["expense-tracker", str(missing_file)],
    )

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1


def test_unsupported_file_extension_exits_with_code_1(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    unsupported_file = tmp_path / "expenses.txt"
    monkeypatch.setattr(
        "sys.argv",
        ["expense-tracker", str(unsupported_file)],
    )

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1
