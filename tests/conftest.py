import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest


class FakeSource:
    def __init__(
        self,
        name: str,
        rows: list[dict[str, Any]],
    ) -> None:
        self.name = name
        self.rows = rows

    def read(self) -> Iterator[dict[str, Any]]:
        yield from self.rows


@pytest.fixture
def row() -> dict[str, Any]:
    """Return one valid raw expense record."""
    return {
        "title": "Groceries",
        "category": "Food",
        "amount": 1500,
        "city": "Kyiv",
    }


@pytest.fixture
def rows(row: dict[str, Any]) -> list[dict[str, Any]]:
    """Return valid, duplicate, invalid, and optional-amount records."""
    return [
        row,
        {
            "title": "Groceries",
            "category": "Food",
            "amount": 1500,
            "city": "Kyiv",
        },
        {
            "title": "",
            "category": "Transport",
            "amount": 200,
            "city": "Lviv",
        },
        {
            "title": "Taxi",
            "category": "Transport",
            "amount": None,
            "city": "Lviv",
        },
    ]


@pytest.fixture
def jsonl_file(tmp_path: Path, rows: list[dict[str, Any]]) -> Path:
    """Create a temporary JSONL file containing test records."""
    path = tmp_path / "expenses.jsonl"
    body = "\n".join(json.dumps(item, ensure_ascii=False) for item in rows)
    path.write_text(body + "\n", encoding="utf-8")
    return path
