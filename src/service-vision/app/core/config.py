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

    project_name: str = "ALDIMI service-vision"
    cors_origins: str = "http://localhost:4200"
    service_core_base_url: str = ""

    llm_provider: Literal["stub", "azure"] = "azure"

    gatekeeper_provider: Literal["stub"] = "stub"

    openai_base_url: str = ""
    openai_api_key: str = ""
    openai_vision_model: str = ""

    max_vision_input_images: int = 8
    max_image_base64_chars_per_image: int = 4_000_000
    max_total_jpeg_bytes_after_preprocess: int = 20 * 1024 * 1024

    preprocess_jpeg_quality: int = 90
    preprocess_max_width: int = 2000

    # Vacío = usa `dni_extractor_system_prompt.DNI_EXTRACTOR_SYSTEM_PROMPT`
    dni_system_prompt: str = ""
    receta_system_prompt: str = ""
    recibo_system_prompt: str = ""

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

    @field_validator("preprocess_jpeg_quality")
    @classmethod
    def jpeg_quality_range(cls, v: int) -> int:
        return max(1, min(100, v))

    @model_validator(mode="after")
    def azure_requires_openai_config(self) -> Self:
        if self.llm_provider == "azure":
            missing: list[str] = []
            if not self.openai_base_url:
                missing.append("OPENAI_BASE_URL")
            if not self.openai_api_key:
                missing.append("OPENAI_API_KEY")
            if not self.openai_vision_model:
                missing.append("OPENAI_VISION_MODEL")
            if missing:
                raise ValueError(
                    f"LLM_PROVIDER=azure requiere variables: {', '.join(missing)}"
                )
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
