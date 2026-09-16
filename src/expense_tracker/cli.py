from expense_tracker.domain.text import normalize_title


def main() -> None:
    title = "  Expense   Tracker  "
    print(normalize_title(title))


if __name__ == "__main__":
    main()
