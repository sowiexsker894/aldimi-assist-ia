class VisionService:
    """Lógica de visión: por ahora stub sin inferencia."""

    def analyze_stub(self, *, hint: str | None, has_image: bool) -> str:
        parts = ["[stub] Análisis no implementado."]
        if hint:
            parts.append(f"hint={hint.strip()[:200]!r}")
        if has_image:
            parts.append("imagen_recibida=true")
        return " ".join(parts)
