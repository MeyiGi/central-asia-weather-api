from datetime import datetime

from pydantic import BaseModel, field_validator


class WeatherRequest(BaseModel):
    """Query params for /temperature and /pressure"""

    time: datetime

    @field_validator("time", mode="before")
    @classmethod
    def parse_iso_time(cls, v: str | datetime) -> datetime:
        if isinstance(v, datetime):
            return v
        try:
            return datetime.fromisoformat(str(v))
        except ValueError:
            raise ValueError(
                f"Invalid time format: '{v}'. Expected ISO 8601, e.g. 2025-01-29T00:00"
            )


class RequestLogSchema(BaseModel):
    id: int
    endpoint: str
    requested_time: str
    status: str
    error_message: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
