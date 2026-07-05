class VisionRequestError(Exception):
    """Error de petición de visión; el API traduce a HTTP (400 / 413)."""

    def __init__(self, detail: str, *, status_code: int = 400) -> None:
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code


class VisionRejectedError(Exception):
    """Gatekeeper rechazó la imagen; el API traduce a HTTP 422."""

    def __init__(self, *, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = 422
