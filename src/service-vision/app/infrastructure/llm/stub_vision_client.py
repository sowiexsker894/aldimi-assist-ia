import json

from app.infrastructure.llm.protocols import VisionCompletionClient


class StubVisionClient:
    """Respuesta JSON mínima válida sin llamar a Azure."""

    def complete_dni_extraction(
        self, *, system_prompt: str, image_data_urls: list[str]
    ) -> str:
        _ = system_prompt, image_data_urls
        payload = {
            "nombre": None,
            "apellido_paterno": None,
            "apellido_materno": None,
            "dni_number": None,
            "sexo": None,
            "nacionalidad": None,
            "fecha_nacimiento": None,
            "fecha_expiracion": None,
            "lugar_nacimiento": None,
            "direccion": None,
        }
        return json.dumps(payload, ensure_ascii=False)
