import json
import random
from pathlib import Path


random.seed(7)

titles = [
    "Coffee",
    "Groceries",
    "Taxi",
    "Internet",
    "Rent",
    "Books",
    "Restaurant",
    "Fuel",
    "Clothes",
    "Medicine",
    "Cinema",
    "Gym",
]

categories = [
    "Food",
    "Transport",
    "Bills",
    "Housing",
    "Education",
    "Entertainment",
    "Health",
    "Shopping",
]

cities = [
    "Kyiv",
    "Lviv",
    "Odesa",
    "Kharkiv",
    "Dnipro",
]


def main() -> None:
    path = Path("data/large.jsonl")
    previous = None

    with path.open("w", encoding="utf-8") as file:
        for i in range(200_000):
            if i % 10 == 3 and previous is not None:
                row = dict(previous)
            else:
                row = {
                    "title": f"{random.choice(titles)} {i}",
                    "category": random.choice(categories),
                    "amount": (str(random.randint(100, 15_000)) if i % 7 else "not specified"),
                    "city": random.choice(cities),
                }

            if i % 1_000 == 0:
                row = dict(row, title="")

            file.write(json.dumps(row, ensure_ascii=False) + "\n")
            previous = row

    print(f"Created {path} with 200000 records")


if __name__ == "__main__":
    main()
