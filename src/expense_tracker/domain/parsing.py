from .models import Expense


def normalize_title(raw: str) -> str:
    return " ".join(raw.split()).lower()


def parse_amount(raw: object) -> int | None:
    if isinstance(raw, (str, int)):
        try:
            return int(raw)
        except ValueError:
            return None
    return None


def to_expense(row: dict[str, object]) -> Expense | None:
    title = row.get("title")
    category = row.get("category")
    amount = row.get("amount")
    city = row.get("city", "")

    if not isinstance(title, str):
        return None

    if not isinstance(category, str):
        return None

    if not isinstance(city, str):
        return None

    parsed_amount = parse_amount(amount)

    if not title.strip() or not category.strip():
        return None

    return Expense(
        title=normalize_title(title),
        category=category,
        amount=parsed_amount,
        city=city,
    )
