import re
from datetime import date, datetime


_DATE_PATTERN = re.compile(r"^(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})$")
_DNI_PATTERN = re.compile(r"^\d{8}$")
_RUC_PATTERN = re.compile(r"^\d{11}$")


def parse_date_dd_mm_yyyy(value: str | None) -> date | None:
    if not value or not str(value).strip():
        return None
    match = _DATE_PATTERN.match(str(value).strip())
    if not match:
        return None
    day, month, year = int(match.group(1)), int(match.group(2)), int(match.group(3))
    try:
        return date(year, month, day)
    except ValueError:
        return None


def is_valid_dni_number(value: str | None) -> bool:
    if not value:
        return False
    cleaned = str(value).strip()
    if not _DNI_PATTERN.match(cleaned):
        return False
    return len(set(cleaned)) > 1


def is_valid_ruc(value: str | None) -> bool:
    if not value:
        return False
    return bool(_RUC_PATTERN.match(str(value).strip()))


def is_plausible_birth_date(value: str | None) -> bool:
    parsed = parse_date_dd_mm_yyyy(value)
    if parsed is None:
        return False
    return 1900 <= parsed.year <= datetime.now().year


def normalize_whitespace(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = " ".join(str(value).split())
    return cleaned or None
