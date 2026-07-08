from functools import lru_cache
from typing import Literal, Self

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    project_name: str = "ALDIMI service-nlp"
    cors_origins: str = "http://localhost:4200"
    service_core_base_url: str = ""

    llm_provider: Literal["stub", "azure"] = "azure"

    openai_base_url: str = ""
    openai_api_key: str = ""
    openai_chat_model: str = ""
    chat_system_prompt: str = ""

    # Modelo BERT emocional
    emotion_model_dir: str = "/app/models/emotion_bert"
    emotion_model_prefix: str = "bert_"
    emotion_tokenizer_name: str = "bert-base-multilingual-cased"
    emotion_threshold: float = 0.50
    emotion_max_length: int = 256

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

    @field_validator("openai_base_url", mode="before")
    @classmethod
    def normalize_openai_base_url(cls, v: str | None) -> str:
        if v is None:
            return ""
        return str(v).strip().rstrip("/")

    @model_validator(mode="after")
    def azure_requires_openai_config(self) -> Self:
        if self.llm_provider == "azure":
            missing: list[str] = []
            if not self.openai_base_url:
                missing.append("OPENAI_BASE_URL")
            if not self.openai_api_key:
                missing.append("OPENAI_API_KEY")
            if not self.openai_chat_model:
                missing.append("OPENAI_CHAT_MODEL")
            if missing:
                raise ValueError(
                    f"LLM_PROVIDER=azure requiere variables: {', '.join(missing)}"
                )
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
