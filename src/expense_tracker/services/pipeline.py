from collections import Counter
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from itertools import islice
from pathlib import Path
from typing import TypeVar

from pydantic import ValidationError

from ..domain.models import Expense
from ..sources.json_file import read_rows, read_rows_jsonl
from ..sources.schemas import ExpenseIn


@dataclass(slots=True)
class PipelineStats:
    read: int = 0
    invalid: int = 0
    duplicates: int = 0
    kept: int = 0
    by_city: Counter[str] = field(default_factory=Counter)
    amount_count: int = 0
    amount_sum: int = 0
    amount_min: int | None = None
    amount_max: int | None = None

    @property
    def amount_avg(self) -> float | None:
        if not self.amount_count:
            return None
        return self.amount_sum / self.amount_count


def parse_all(
    rows: Iterable[dict[str, object]],
    stats: PipelineStats,
) -> Iterator[Expense]:
    for row in rows:
        stats.read += 1

        try:
            expense = ExpenseIn.model_validate(row).to_domain()
        except ValidationError:
            stats.invalid += 1
            continue

        yield expense


def deduplicate(
    items: Iterable[Expense],
    stats: PipelineStats,
) -> Iterator[Expense]:
    seen: set[tuple[str, str]] = set()

    for expense in items:
        if expense.key in seen:
            stats.duplicates += 1
            continue

        seen.add(expense.key)
        yield expense


T = TypeVar("T")


def batched(  # noqa: UP047
    items: Iterable[T],
    size: int,
) -> Iterator[tuple[T, ...]]:
    iterator = iter(items)
    while batch := tuple(islice(iterator, size)):
        yield batch


def collect(
    items: Iterable[Expense],
    stats: PipelineStats,
) -> None:
    for expense in items:
        stats.kept += 1
        stats.by_city[expense.city] += 1

        amount = expense.amount

        if amount is None:
            continue

        stats.amount_count += 1
        stats.amount_sum += amount

        if stats.amount_min is None or amount < stats.amount_min:
            stats.amount_min = amount

        if stats.amount_max is None or amount > stats.amount_max:
            stats.amount_max = amount


def load_expenses(path: Path) -> list[Expense]:
    rows = read_rows(path)
    stats = PipelineStats()
    parsed = parse_all(rows, stats)
    unique = deduplicate(parsed, stats)

    result = list(unique)
    stats.kept = len(result)

    return result


def load_jsonl_stats(path: Path) -> PipelineStats:
    stats = PipelineStats()

    rows = read_rows_jsonl(path)
    parsed = parse_all(rows, stats)
    unique = deduplicate(parsed, stats)

    collect(unique, stats)

    return stats


def count_by_city(items: Iterable[Expense]) -> Counter[str]:
    return Counter(expense.city for expense in items)
