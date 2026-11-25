from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки из переменных окружения (см. .env.example в корне репозитория)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://legal:legal@localhost:5432/legal"
    anthropic_api_key: str | None = None
    llm_model: str = "claude-opus-5-5"
    # Откуда разрешены запросы из браузера (адрес фронтенда), через запятую.
    cors_origins: str = "http://localhost:3000"
    # Сколько статей НПА подставлять в промпт.
    retrieval_top_k: int = 8

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
