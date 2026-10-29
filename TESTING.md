# Testing Guide

## Running Tests

Run the complete test suite:
python -m pytest

Run tests for a specific module:
python -m pytest -q tests/test_cli.py

## Test Coverage

Measure test coverage and display lines that are not covered:
python -m pytest --cov=expense_tracker --cov-report=term-missing

The project requires at least 70% code coverage. The configured pytest options enforce this threshold automatically.

## Types of Tests

The test suite covers:

- **Domain tests** — expense model validation and business rules.
- **Service tests** — pipeline processing, duplicate detection, statistics, and batch handling.
- **Schema tests** — input validation and normalization.
- **Source tests** — JSONL parsing, malformed input, error handling, and logging.
- **Configuration tests** — settings and environment variables.
- **CLI tests** — command-line arguments, unsupported file formats, missing files, and exit codes.

## Quality Checks

Run Ruff to check code style:
python -m ruff check .

Run mypy to check types:
python -m mypy src tests

Run all tests and quality checks before committing changes.

## Test Isolation

Tests use temporary directories and files where appropriate. Pytest fixtures provide reusable test data, while `monkeypatch` allows command-line arguments and configuration values to be changed without permanently modifying the environment.
