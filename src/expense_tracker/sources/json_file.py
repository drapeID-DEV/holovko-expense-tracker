import json
from collections.abc import Iterator
from pathlib import Path


def read_rows(path: Path) -> Iterator[dict]:
    with path.open(encoding="utf-8") as file:
        yield from json.load(file)


def read_rows_jsonl(path: Path) -> Iterator[dict]:
    with path.open(encoding="utf-8") as file:
        for line in file:
            yield json.loads(line)
