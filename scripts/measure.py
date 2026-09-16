import time
import tracemalloc
from pathlib import Path

from expense_tracker.sources.json_file import read_rows_jsonl

PATH = Path("data/large.jsonl")


def measure_lazy() -> tuple[int, float, float]:
    tracemalloc.start()
    start = time.perf_counter()

    count = 0
    for _ in read_rows_jsonl(PATH):
        count += 1

    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return count, elapsed, peak / 1024 / 1024


def measure_list() -> tuple[int, float, float]:
    tracemalloc.start()
    start = time.perf_counter()

    rows = list(read_rows_jsonl(PATH))
    count = len(rows)

    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return count, elapsed, peak / 1024 / 1024


def main() -> None:
    lazy_count, lazy_time, lazy_memory = measure_lazy()
    list_count, list_time, list_memory = measure_list()

    print(f"Lazy: {lazy_count} records, {lazy_time:.2f}s, peak {lazy_memory:.2f} MB")
    print(f"List: {list_count} records, {list_time:.2f}s, peak {list_memory:.2f} MB")


if __name__ == "__main__":
    main()
