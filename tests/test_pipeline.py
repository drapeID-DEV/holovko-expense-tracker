from expense_tracker.services.pipeline import (
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
