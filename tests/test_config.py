import os
from pathlib import Path

from _pytest.monkeypatch import MonkeyPatch

from expense_tracker.config import Settings


def test_default_settings(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv("DATA_PATH", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("BATCH_SIZE", raising=False)
    monkeypatch.delenv("API_TOKEN", raising=False)
    monkeypatch.chdir(os.getcwd())

    config = Settings(_env_file=None)  # type: ignore[call-arg]

    assert config.data_path == Path("data/large.jsonl")
    assert config.log_level == "INFO"
    assert config.batch_size == 500
    assert config.api_token == ""


def test_environment_variables_override_defaults(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setenv("DATA_PATH", "data/custom.jsonl")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("BATCH_SIZE", "100")
    monkeypatch.setenv("API_TOKEN", "test-secret")

    config = Settings()

    assert config.data_path == Path("data/custom.jsonl")
    assert config.log_level == "DEBUG"
    assert config.batch_size == 100
    assert config.api_token == "test-secret"


def test_environment_overrides_dotenv(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "LOG_LEVEL=WARNING\nBATCH_SIZE=200\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    config = Settings(_env_file=env_file)  # type: ignore[call-arg]

    assert config.log_level == "DEBUG"
    assert config.batch_size == 200
