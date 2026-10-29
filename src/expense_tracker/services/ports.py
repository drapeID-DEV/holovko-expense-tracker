from collections.abc import Iterator
from typing import Any, Protocol


class Source(Protocol):
    name: str

    def read(self) -> Iterator[dict[str, Any]]: ...
