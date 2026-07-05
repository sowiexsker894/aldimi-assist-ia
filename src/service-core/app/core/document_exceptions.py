class DocumentAnalysisRejectedError(Exception):
    """Vision gatekeeper rechazó la imagen."""

    def __init__(self, *, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)


class DocumentSessionError(Exception):
    """Sesión de análisis inválida, expirada o ya consumida."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class DocumentValidationError(Exception):
    """Campos confirmados inválidos."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
