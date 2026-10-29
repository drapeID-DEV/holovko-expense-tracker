import argparse
from collections.abc import Callable
from pathlib import Path

from .services.pipeline import Pipeline, PipelineStats
from .services.ports import Source
from .sources.csv_file import CsvSource
from .sources.jsonl import JsonlSource

FACTORIES: dict[str, Callable[[Path], Source]] = {
    ".jsonl": JsonlSource,
    ".csv": CsvSource,
}


def main() -> None:
    parser = argparse.ArgumentParser(prog="expense-tracker")
    parser.add_argument("path", type=Path, help="Path to the input file")
    parser.add_argument(
        "--preview",
        type=int,
        help="Show the first N records",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show statistics",
    )

    args = parser.parse_args()
    factory = FACTORIES.get(args.path.suffix.lower())

    if factory is None:
        raise SystemExit(f"Unsupported file type: {args.path.suffix}")

    pipeline = Pipeline([factory(args.path)])
    expenses = pipeline.run()
    stats: PipelineStats = pipeline.stats

    if args.preview is not None:
        for expense in expenses[: args.preview]:
            print(expense)
        print(f"Rows read: {stats.read}")
        return

    if args.stats:
        print(f"Rows read: {stats.read}")
        print(f"Invalid rows: {stats.invalid}")
        print(f"Duplicates: {stats.duplicates}")
        print(f"Rows kept: {stats.kept}")

        if stats.amount_count:
            print(
                f"Amount: min={stats.amount_min} "
                f"max={stats.amount_max} avg={stats.amount_avg:.2f}"
            )

        for city, count in stats.by_city.most_common():
            print(f" {city}: {count}")


if __name__ == "__main__":
    main()
