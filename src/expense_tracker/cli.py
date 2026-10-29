import argparse
import logging
from collections.abc import Callable
from pathlib import Path

from .config import settings
from .errors import ExpenseTrackerError, SourceError
from .logging_setup import setup
from .services.pipeline import Pipeline, PipelineStats
from .services.ports import Source
from .sources.csv_file import CsvSource
from .sources.jsonl import JsonlSource

logger = logging.getLogger(__name__)

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
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Override the configured logging level",
    )

    args = parser.parse_args()
    setup(args.log_level or settings.log_level)
    factory = FACTORIES.get(args.path.suffix.lower())

    try:
        if factory is None:
            raise SourceError(f"unsupported file type: {args.path.suffix}")

        pipeline = Pipeline([factory(args.path)])
        expenses = pipeline.run()
        stats: PipelineStats = pipeline.stats
    except ExpenseTrackerError as exc:
        logger.error("%s", exc)
        raise SystemExit(1) from exc

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
                f"Amount: min={stats.amount_min} max={stats.amount_max} avg={stats.amount_avg:.2f}"
            )

        for city, count in stats.by_city.most_common():
            print(f" {city}: {count}")


if __name__ == "__main__":
    main()
