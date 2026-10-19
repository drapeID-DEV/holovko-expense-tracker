import pytest
from pydantic import ValidationError

from expense_tracker.sources.schemas import ExpenseIn


def test_expense_in_normalizes_data() -> None:
    expense = ExpenseIn.model_validate(
        {
            "title": "  Coffee  ",
            "category": "Food",
            "amount": "1500",
            "city": "Kyiv",
        }
    )

    assert expense.title == "coffee"
    assert expense.category == "Food"
    assert expense.amount == 1500
    assert expense.city == "Kyiv"


def test_unknown_amount_becomes_none() -> None:
    expense = ExpenseIn.model_validate(
        {
            "title": "Coffee",
            "category": "Food",
            "amount": "not specified",
            "city": "Kyiv",
        }
    )

    assert expense.amount is None


@pytest.mark.parametrize(
    "data",
    [
        {"title": "", "category": "Food", "amount": 100},
        {"title": "Coffee", "category": "", "amount": 100},
        {"title": "Coffee", "category": "Food", "amount": 0},
        {"title": "Coffee", "category": "Food", "amount": -100},
    ],
)
def test_invalid_input_is_rejected(data: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        ExpenseIn.model_validate(data)


def test_to_domain_returns_expense() -> None:
    expense = ExpenseIn.model_validate(
        {
            "title": "Coffee",
            "category": "Food",
            "amount": "100",
            "city": "Kyiv",
        }
    )

    domain_expense = expense.to_domain()

    assert domain_expense.title == "coffee"
    assert domain_expense.category == "Food"
    assert domain_expense.amount == 100
    assert domain_expense.city == "Kyiv"
