import json
import logging
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from ..errors import SourceError

logger = logging.getLogger(__name__)


def read_rows(path: Path) -> Iterator[dict[str, Any]]:
    with path.open(encoding="utf-8") as file:
        yield from json.load(file)


class JsonlSource:
    name = "jsonl"

    def __init__(self, path: Path) -> None:
        self.path = path

    def read(self) -> Iterator[dict[str, Any]]:
        try:
            handle = self.path.open(encoding="utf-8")
        except OSError as exc:
            raise SourceError(f"cannot open {self.path}") from exc

        with handle as file:
            for number, line in enumerate(file, start=1):
                if not line.strip():
                    continue

                try:
                    row: Any = json.loads(line)
                except json.JSONDecodeError:
                    logger.debug(
                        "skip malformed line %d in %s",
                        number,
                        self.path,
                    )
                    continue

                if isinstance(row, dict):
                    yield row


def read_json_array(path: Path) -> Iterator[dict[str, Any]]:
    with path.open(encoding="utf-8") as file:
        yield from json.load(file)
