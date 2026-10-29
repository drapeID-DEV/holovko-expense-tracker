from collections.abc import Iterator
from typing import Any

from expense_tracker.services.pipeline import (
    Pipeline,
    PipelineStats,
    batched,
    parse_all,
)


def test_invalid_rows_are_counted() -> None:
    rows: list[dict[str, object]] = [
        {
            "title": "Coffee",
            "category": "Food",
            "amount": "100",
            "city": "Kyiv",
        },
        {
            "title": "",
            "category": "Transport",
            "amount": "200",
            "city": "Lviv",
        },
    ]

    stats = PipelineStats()
    result = list(parse_all(rows, stats))

    assert len(result) == 1
    assert stats.read == 2
    assert stats.invalid == 1


def test_batched_splits_tail() -> None:
    assert [len(batch) for batch in batched(range(7), 3)] == [3, 3, 1]


class FakeSource:
    def __init__(self, name: str, rows: list[dict[str, Any]]) -> None:
        self.name = name
        self.rows = rows

    def read(self) -> Iterator[dict[str, Any]]:
        yield from self.rows


def test_pipeline_accepts_multiple_sources() -> None:
    first = FakeSource(
        "first",
        [{"title": "Coffee", "category": "Food", "amount": "100", "city": "Kyiv"}],
    )
    second = FakeSource(
        "second",
        [{"title": "Taxi", "category": "Transport", "amount": "200", "city": "Lviv"}],
    )

    pipeline = Pipeline([first, second])
    expenses = pipeline.run()

    assert len(expenses) == 2
    assert pipeline.stats.read == 2
    assert pipeline.stats.kept == 2
    assert pipeline.stats.by_source == {"first": 1, "second": 1}


def test_pipeline_deduplicates_across_sources() -> None:
    row = {"title": "Coffee", "category": "Food", "amount": "100", "city": "Kyiv"}
    pipeline = Pipeline(
        [
            FakeSource("first", [row]),
            FakeSource("second", [row]),
        ]
    )

    expenses = pipeline.run()

    assert len(expenses) == 1
    assert pipeline.stats.duplicates == 1
    assert pipeline.stats.kept == 1
