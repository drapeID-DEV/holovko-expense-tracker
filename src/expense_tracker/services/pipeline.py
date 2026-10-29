import logging
from collections import Counter
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from itertools import islice
from typing import TypeVar

from pydantic import ValidationError

from ..domain.models import Expense
from .ports import Source
from .schemas import ExpenseIn

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class PipelineStats:
    read: int = 0
    invalid: int = 0
    duplicates: int = 0
    kept: int = 0
    by_source: Counter[str] = field(default_factory=Counter)
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


class Pipeline:
    def __init__(self, sources: list[Source]) -> None:
        self.sources = sources
        self.stats = PipelineStats()

    def run(self) -> list[Expense]:
        seen: set[tuple[str, str]] = set()
        expenses: list[Expense] = []
        logger.info("start processing %d source(s)", len(self.sources))

        for source in self.sources:
            for row in source.read():
                self.stats.read += 1
                self.stats.by_source[source.name] += 1

                try:
                    expense = ExpenseIn.model_validate(row).to_domain()
                except ValidationError as exc:
                    self.stats.invalid += 1
                    logger.debug("skip row: %d validation errors", exc.error_count())
                    continue

                if expense.key in seen:
                    self.stats.duplicates += 1
                    continue

                seen.add(expense.key)
                expenses.append(expense)
                self._collect(expense)

        logger.info(
            "done: kept %d, invalid %d, duplicates %d",
            self.stats.kept,
            self.stats.invalid,
            self.stats.duplicates,
        )
        if self.stats.invalid:
            logger.warning("skipped %d invalid rows", self.stats.invalid)

        return expenses

    def _collect(self, expense: Expense) -> None:
        self.stats.kept += 1
        self.stats.by_city[expense.city] += 1

        amount = expense.amount
        if amount is None:
            return

        self.stats.amount_count += 1
        self.stats.amount_sum += amount

        if self.stats.amount_min is None or amount < self.stats.amount_min:
            self.stats.amount_min = amount

        if self.stats.amount_max is None or amount > self.stats.amount_max:
            self.stats.amount_max = amount


T = TypeVar("T")


def batched(  # noqa: UP047
    items: Iterable[T],
    size: int,
) -> Iterator[tuple[T, ...]]:
    iterator = iter(items)
    while batch := tuple(islice(iterator, size)):
        yield batch


def load_expenses(source: Source) -> list[Expense]:
    pipeline = Pipeline([source])
    return pipeline.run()
