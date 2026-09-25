import time
import tracemalloc
from pathlib import Path

from expense_tracker.domain.parsing import to_expense
from expense_tracker.services.pipeline import (
    PipelineStats,
    deduplicate,
    load_jsonl_stats,
)
from expense_tracker.sources.json_file import read_rows_jsonl

PATH = Path("data/large.jsonl")


def lazy() -> int:
    stats = load_jsonl_stats(PATH)
    return stats.kept


def greedy() -> int:
    rows = list(read_rows_jsonl(PATH))
    parsed = [to_expense(row) for row in rows]
    valid = [expense for expense in parsed if expense is not None]

    stats = PipelineStats()
    unique = list(deduplicate(valid, stats))

    return len(unique)


def main() -> None:
    for name, fn in (
        ("генераторний конвеєр", lazy),
        ("проміжні списки", greedy),
    ):
        tracemalloc.start()
        t0 = time.perf_counter()

        n = fn()

        elapsed = time.perf_counter() - t0
        peak = tracemalloc.get_traced_memory()[1] / 1024 / 1024

        tracemalloc.stop()

        print(f"{name:22} {n} записів {elapsed:.2f} с пік {peak:.1f} МБ")


if __name__ == "__main__":
    main()
