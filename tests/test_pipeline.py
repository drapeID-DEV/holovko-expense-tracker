from collections.abc import Iterator
from itertools import islice
from typing import Any

from expense_tracker.services.pipeline import (
    Pipeline,
    PipelineStats,
    batched,
    parse_all,
)
from tests.conftest import FakeSource


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


def test_batched_returns_nothing_for_empty_input() -> None:
    assert list(batched([], 3)) == []


def test_parse_all_is_lazy(row: dict[str, Any]) -> None:
    consumed = 0

    def endless() -> Iterator[dict[str, Any]]:
        nonlocal consumed
        while True:
            consumed += 1
            yield row

    stats = PipelineStats()
    taken = list(islice(parse_all(endless(), stats), 3))

    assert len(taken) == 3
    assert consumed == 3
    assert stats.read == 3
