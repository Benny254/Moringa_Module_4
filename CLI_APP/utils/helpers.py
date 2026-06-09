import re
from typing import Optional

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate_date(value: str) -> Optional[str]:
    if not _DATE_RE.match(value):
        raise ValueError(f"Date must be in YYYY-MM-DD format, got: {value!r}")
    year, month, day = (int(x) for x in value.split("-"))
    if not (1 <= month <= 12):
        raise ValueError(f"Month out of range: {month}")
    if not (1 <= day <= 31):
        raise ValueError(f"Day out of range: {day}")
    return value


def truncate(text: str, width: int = 40) -> str:
    return text if len(text) <= width else text[: width - 1] + "…"