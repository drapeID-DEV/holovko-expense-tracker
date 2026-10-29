import logging
import sys


def setup(level: str = "INFO") -> None:
    """Configure application logging once at the entry point."""
    logging.basicConfig(
        level=level.upper(),
        format="%(asctime)s %(levelname)-8s %(name)s | %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stdout,
    )
