from pathlib import Path

from expense_tracker.domain.models import Expense
from expense_tracker.domain.parsing import to_expense
from expense_tracker.services.pipeline import load_expenses


def test_expense_pipeline_output():
    expenses = load_expenses(Path("data/expenses.json"))

    assert len(expenses) == 7
    assert expenses[0].title == "food"
    assert expenses[0].amount == 500

    assert expenses[1].title == "taxi"
    assert expenses[1].amount is None


def test_invalid_amount_becomes_none():
    expense = to_expense(
        {
            "title": "Taxi",
            "category": "Transport",
            "amount": "not available",
            "city": "Lviv",
        }
    )

    assert isinstance(expense, Expense)
    assert expense.amount is None
