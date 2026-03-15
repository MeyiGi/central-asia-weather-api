"""
Parse WRF timestamps embedded in filenames.

Example:
    wrfout_d01_2024-01-15_120000
                       ^^^^^^^ timestamp
"""
from contextlib import suppress
from datetime import datetime
from typing_extensions import Final
from app.domain.exceptions import DataSourceError


_WRF_TIME_FORMATS: Final = (
    "%Y-%m-%d_%H%M%S",    # canonical WRF
    "%Y-%m-%d_%H:%M:%S",  # colon variant
    "%Y-%m-%dT%H:%M:%S",  # ISO 8601
)

_ERROR_MESSAGE: Final = (
    "Invalid WRF time format: '{value}'." \
    "Expected: YYYY-MM-DD_HHMMSS, YYYY-MM-DD_HH:MM:SS, or YYYY-MM-DDTHH:MM:SS"
)

def to_filename_token(time_str: str) -> str:
    """Normalize any accepted format to canonical YYYY-MM-DD_HHMMSS."""
    dt = _parse_or_raise(time_str)
    return dt.strftime("%Y-%m-%d_%H%M%S")

def to_datetime(time_str: str) -> datetime:
    """Parse WRF time string into datetime."""
    return _parse_or_raise(time_str)

def _try_parse(time_str: str) -> datetime | None:
    for fmt in _WRF_TIME_FORMATS:
        with suppress(ValueError):
            return datetime.strptime(time_str, fmt)
    return None

def _parse_or_raise(time_str: str) -> datetime:
    dt = _try_parse(time_str)
    if dt is None:
        raise DataSourceError(_ERROR_MESSAGE.format(value=time_str))
    return dt