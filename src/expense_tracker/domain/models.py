from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Expense:
    title: str
    category: str
    amount: int | None
    city: str

    @property
    def key(self) -> tuple[str, str]:
        return self.title, self.category
