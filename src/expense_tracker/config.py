from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings loaded from defaults, .env, and environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    data_path: Path = Path("data/large.jsonl")
    log_level: str = "INFO"
    batch_size: int = 500
    api_token: str = ""


def mask(secret: str) -> str:
    """Mask a secret, keeping only its last four characters visible."""
    if len(secret) <= 4:
        return "****"
    return "*" * (len(secret) - 4) + secret[-4:]


settings = Settings()
