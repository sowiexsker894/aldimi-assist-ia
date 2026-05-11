from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    project_name: str = "ALDIMI service-vision"
    cors_origins: str = "http://localhost:4200"
    service_core_base_url: str = ""

    @property
    def cors_origins_list(self) -> list[str]:
        raw = self.cors_origins.strip()
        if raw == "*":
            return ["*"]
        return [o.strip() for o in raw.split(",") if o.strip()]

    @field_validator("service_core_base_url", mode="before")
    @classmethod
    def strip_base_url(cls, v: str | None) -> str:
        if v is None:
            return ""
        return str(v).strip().rstrip("/")


@lru_cache
def get_settings() -> Settings:
    return Settings()
