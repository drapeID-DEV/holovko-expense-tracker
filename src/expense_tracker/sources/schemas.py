from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..domain.models import Expense


class ExpenseIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=200)
    category: str = Field(min_length=1)
    amount: int | None = Field(default=None, gt=0)
    city: str = Field(default="")

    @field_validator("amount", mode="before")
    @classmethod
    def unknown_amount(cls, value: object) -> object:
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                return None
        return value

    @field_validator("title", "category")
    @classmethod
    def strip_spaces(cls, value: str) -> str:
        return " ".join(value.split())

    @field_validator("title")
    @classmethod
    def lowercase(cls, value: str) -> str:
        return value.lower()

    def to_domain(self) -> Expense:
        return Expense(
            title=self.title,
            category=self.category,
            amount=self.amount,
            city=self.city,
        )
