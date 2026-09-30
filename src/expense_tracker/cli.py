import argparse
from collections.abc import Iterator
from itertools import islice
from pathlib import Path

from .domain.models import Expense
from .services.pipeline import (
    PipelineStats,
    collect,
    deduplicate,
    parse_all,
)
from .sources.json_file import read_rows_jsonl


def build_pipeline(path: Path, stats: PipelineStats) -> Iterator[Expense]:
    rows = read_rows_jsonl(path)
    parsed = parse_all(rows, stats)
    return deduplicate(parsed, stats)


def main() -> None:
    parser = argparse.ArgumentParser(prog="expense-tracker")
    parser.add_argument("path", type=Path, help="файл із даними")
    parser.add_argument(
        "--preview",
        type=int,
        help="показати перші N записів",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="показати статистику",
    )

    args = parser.parse_args()

    stats = PipelineStats()
    pipeline = build_pipeline(args.path, stats)

    if args.preview is not None:
        for expense in islice(pipeline, args.preview):
            print(expense)

        print(f"Прочитано рядків: {stats.read}")
        return

    collect(pipeline, stats)

    if args.stats:
        print(f"Прочитано записів: {stats.read}")
        print(f"Відхилено: {stats.invalid}")
        print(f"Дублікатів: {stats.duplicates}")
        print(f"Залишилось: {stats.kept}")

        if stats.amount_count:
            print(f"Сума: min={stats.amount_min} max={stats.amount_max} avg={stats.amount_avg:.2f}")

        for city, count in stats.by_city.most_common():
            print(f" {city}: {count}")


if __name__ == "__main__":
    main()
