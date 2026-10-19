import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any


def read_rows(path: Path) -> Iterator[dict[str, Any]]:
    with path.open(encoding="utf-8") as file:
        yield from json.load(file)


class JsonlSource:
    name = "jsonl"

    def __init__(self, path: Path) -> None:
        self.path = path

    def read(self) -> Iterator[dict[str, Any]]:
        with self.path.open(encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    continue

                try:
                    row: Any = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if isinstance(row, dict):
                    yield row


def read_json_array(path: Path) -> Iterator[dict[str, Any]]:
    with path.open(encoding="utf-8") as file:
        yield from json.load(file)
