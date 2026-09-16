import argparse
from pathlib import Path

from .services.pipeline import count_by_city, load_expenses


def main() -> None:
    parser = argparse.ArgumentParser(prog="expense-tracker")
    parser.add_argument("path", type=Path, help="файл із даними")
    args = parser.parse_args()

    expenses = load_expenses(args.path)

    print(f"Завантажено записів: {len(expenses)}")

    for city, count in count_by_city(expenses).most_common():
        print(f" {city}: {count}")


if __name__ == "__main__":
    main()
