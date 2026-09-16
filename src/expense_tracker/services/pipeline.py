from collections import Counter
from collections.abc import Iterable, Iterator
from pathlib import Path

from ..domain.models import Expense
from ..domain.parsing import to_expense
from ..sources.json_file import read_rows


def deduplicate(items: Iterable[Expense]) -> Iterator[Expense]:
    seen: set[tuple[str, str]] = set()

    for expense in items:
        if expense.key not in seen:
            seen.add(expense.key)
            yield expense


def count_by_city(items: Iterable[Expense]) -> Counter[str]:
    return Counter(expense.city for expense in items)


def load_expenses(path: Path) -> list[Expense]:
    rows = read_rows(path)
    parsed = (to_expense(row) for row in rows)
    valid = (expense for expense in parsed if expense is not None)

    return list(deduplicate(valid))
