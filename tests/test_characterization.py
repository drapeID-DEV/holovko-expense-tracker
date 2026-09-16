from legacy.loader import process


def test_legacy_output_is_stable():
    rows = process("data/expenses.json")

    assert len(rows) == 7
    assert rows[0][0] == "food"
    assert rows[0][2] == 500

    assert rows[1][0] == "taxi"
    assert rows[1][2] == 0
