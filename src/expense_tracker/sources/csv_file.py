import csv
from collections.abc import Iterator
from pathlib import Path
from typing import Any


class CsvSource:
    name = "csv"

    def __init__(self, path: Path, delimiter: str = ";") -> None:
        self.path = path
        self.delimiter = delimiter

    def read(self) -> Iterator[dict[str, Any]]:
        with self.path.open(
            encoding="utf-8-sig",
            newline="",
        ) as file:
            reader = csv.DictReader(file, delimiter=self.delimiter)

            for row in reader:
                yield dict(row)
