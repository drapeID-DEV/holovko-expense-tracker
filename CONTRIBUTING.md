# Contributing

## Branch naming

Use descriptive branch names with the following format:

- `feature/<name>` — for new functionality
- `fix/<name>` — for bug fixes
- `docs/<name>` — for documentation changes

Example:

`feature/title-normalizer`

## Commit messages

Use short and meaningful commit messages.

Recommended format:

`type: short description`

Examples:

- `feat: add title normalizer`
- `fix: handle empty title`
- `docs: update README`

## Pull Requests

Before creating a pull request:

- Run `ruff check .`
- Run `ruff format .`
- Make sure the working tree is clean
- Keep commits atomic and meaningful
- Do not include secrets, databases, virtual environments or cache files

Pull requests should contain:

- a short description of the changes;
- an explanation of why the changes are needed;
- instructions for testing the changes.
