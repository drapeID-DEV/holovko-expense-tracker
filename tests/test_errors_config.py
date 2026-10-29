import pytest

from expense_tracker.config import mask
from expense_tracker.errors import (
    ConfigError,
    ExpenseTrackerError,
    ParseError,
    SourceError,
)


def test_exception_hierarchy() -> None:
    assert issubclass(SourceError, ExpenseTrackerError)
    assert issubclass(ParseError, SourceError)
    assert issubclass(ConfigError, ExpenseTrackerError)


@pytest.mark.parametrize(
    ("secret", "expected"),
    [
        ("my-secret-token", "***********oken"),
        ("abcd", "****"),
        ("abc", "****"),
        ("", "****"),
    ],
)
def test_mask_secret(secret: str, expected: str) -> None:
    assert mask(secret) == expected
