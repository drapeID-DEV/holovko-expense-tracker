import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any


def read_rows(path: Path) -> Iterator[dict[str, Any]]:
    with path.open(encoding="utf-8") as file:
        yield from json.load(file)


def read_rows_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    # Any виправданий: структура JSON-рядка стане відомою після валідації.
    with path.open(encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


class JsonArraySource:
    name = "json"

    def __init__(self, path: Path) -> None:
        self.path = path

    def read(self) -> Iterator[dict[str, Any]]:
        yield from read_rows(self.path)
