import pytest

from expense_tracker.domain.models import Expense


@pytest.mark.parametrize(
    "title, category, amount",
    [
        ("", "Food", 100),
        ("   ", "Food", 100),
        ("Coffee", "", 100),
        ("Coffee", "   ", 100),
        ("Coffee", "Food", 0),
        ("Coffee", "Food", -100),
    ],
)
def test_invalid_expense_rejected(
    title: str,
    category: str,
    amount: int,
) -> None:
    with pytest.raises(ValueError):
        Expense(title, category, amount, "Kyiv")


def test_frozen_model_is_hashable() -> None:
    first = Expense("coffee", "Food", 100, "Kyiv")
    second = Expense("coffee", "Food", 100, "Kyiv")

    assert len({first, second}) == 1


def test_unknown_amount_is_allowed() -> None:
    expense = Expense("coffee", "Food", None, "Kyiv")

    assert expense.amount is None
