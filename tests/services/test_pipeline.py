from collections.abc import Iterator
from typing import Any

from expense_tracker.services.pipeline import Pipeline

ROW = {
    "title": "Coffee",
    "category": "Food",
    "amount": "100",
    "city": "Kyiv",
}


class FakeSource:
    def __init__(
        self,
        rows: list[dict[str, Any]],
        name: str = "fake",
    ) -> None:
        self.name = name
        self._rows = rows

    def read(self) -> Iterator[dict[str, Any]]:
        yield from self._rows


def test_empty_source() -> None:
    pipeline = Pipeline([FakeSource([])])

    expenses = pipeline.run()

    assert expenses == []
    assert pipeline.stats.read == 0
    assert pipeline.stats.kept == 0


def test_invalid_row_is_skipped() -> None:
    invalid_row = {"title": "", "category": "Food"}

    pipeline = Pipeline([FakeSource([ROW, invalid_row])])

    expenses = pipeline.run()

    assert len(expenses) == 1
    assert pipeline.stats.invalid == 1
    assert pipeline.stats.kept == 1


def test_duplicates_across_sources() -> None:
    pipeline = Pipeline(
        [
            FakeSource([ROW], "first"),
            FakeSource([ROW], "second"),
        ]
    )

    expenses = pipeline.run()

    assert len(expenses) == 1
    assert pipeline.stats.duplicates == 1
    assert pipeline.stats.by_source["first"] == 1
    assert pipeline.stats.by_source["second"] == 1


def test_multiple_cities_are_counted() -> None:
    second_row = {
        "title": "Taxi",
        "category": "Transport",
        "amount": "250",
        "city": "Lviv",
    }

    pipeline = Pipeline([FakeSource([ROW, second_row])])

    pipeline.run()

    assert pipeline.stats.by_city["Kyiv"] == 1
    assert pipeline.stats.by_city["Lviv"] == 1


def test_unknown_amount_is_not_invalid() -> None:
    row = {**ROW, "amount": "unknown"}

    pipeline = Pipeline([FakeSource([row])])

    expenses = pipeline.run()

    assert len(expenses) == 1
    assert pipeline.stats.invalid == 0
    assert pipeline.stats.kept == 1
