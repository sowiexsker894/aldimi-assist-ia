class ExternalServiceUnavailable(Exception):
    """Microservicio externo no configurado o no disponible."""

    def __init__(self, message: str, *, service: str = "unknown") -> None:
        self.service = service
        super().__init__(message)
