from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración cargada desde variables de entorno / `.env`."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    project_name: str = "ALDIMI service-core"
    database_url: str = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/aldimi_core"
    )
    nlp_service_url: str = ""
    vision_service_url: str = ""
    cors_origins: str = "http://localhost:4200"

    @property
    def cors_origins_list(self) -> list[str]:
        raw = self.cors_origins.strip()
        if raw == "*":
            return ["*"]
        return [o.strip() for o in raw.split(",") if o.strip()]

    @field_validator("nlp_service_url", "vision_service_url", mode="before")
    @classmethod
    def strip_urls(cls, v: str | None) -> str:
        if v is None:
            return ""
        return str(v).strip()


@lru_cache
def get_settings() -> Settings:
    return Settings()
