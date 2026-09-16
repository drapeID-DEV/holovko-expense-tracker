from expense_tracker.domain.models import Expense
from expense_tracker.domain.parsing import to_expense
from legacy.loader import process


def test_legacy_output_is_stable():
    rows = process("data/expenses.json")

    assert len(rows) == 7
    assert rows[0][0] == "food"
    assert rows[0][2] == 500

    assert rows[1][0] == "taxi"
    assert rows[1][2] == 0


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
