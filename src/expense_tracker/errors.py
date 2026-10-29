"""Application exception hierarchy."""


class ExpenseTrackerError(Exception):
    """Base exception for application errors."""


class SourceError(ExpenseTrackerError):
    """An error occurred while accessing or reading a data source."""


class ParseError(SourceError):
    """A data record could not be parsed."""


class ConfigError(ExpenseTrackerError):
    """Application configuration is invalid."""
