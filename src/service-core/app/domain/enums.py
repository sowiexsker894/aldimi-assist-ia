from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "ADMIN"
    VOLUNTEER = "VOLUNTEER"
    FAMILY = "FAMILY"
    PATIENT = "PATIENT"
