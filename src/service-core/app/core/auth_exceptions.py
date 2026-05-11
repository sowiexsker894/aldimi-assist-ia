class InvalidCredentialsError(Exception):
    """Email o contraseña incorrectos."""

class UserInactiveError(Exception):
    """Cuenta desactivada (ej. voluntario inactivo)."""

class ForbiddenActionError(Exception):
    """Sin permisos para la acción."""
