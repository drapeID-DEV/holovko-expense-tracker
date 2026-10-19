from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Expense:
    title: str
    category: str
    amount: int | None
    city: str

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("title must not be empty")

        if not self.category.strip():
            raise ValueError("category must not be empty")

        if self.amount is not None and self.amount <= 0:
            raise ValueError("amount must be positive")

    @property
    def key(self) -> tuple[str, str]:
        return self.title, self.category
