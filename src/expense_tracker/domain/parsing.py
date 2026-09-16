from .models import Expense


def normalize_title(raw: str) -> str:
    return " ".join(raw.split()).lower()


def parse_amount(raw: object) -> int | None:
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


def to_expense(row: dict) -> Expense | None:
    title = row.get("title") or ""

    if not title.strip():
        return None

    return Expense(
        title=normalize_title(title),
        category=row.get("category", ""),
        amount=parse_amount(row.get("amount")),
        city=row.get("city", ""),
    )
