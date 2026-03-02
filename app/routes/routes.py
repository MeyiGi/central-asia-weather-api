from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.exceptions import GribReadError, TimeNotFoundError
from app.repository.log_repository import RequestLogRepository
from app.schemas.weather import RequestLogSchema
from app.services.grib_reader import GribReader
from app.services.visualization import VisualizationService
from app.services.weather_service import WeatherService
from app.utils.response_utils import raise_not_found, raise_server_error, raise_unprocessable
from app.utils.time_utils import parse_iso_datetime

router = APIRouter()


def _make_service(grib_path) -> WeatherService:
    return WeatherService(reader=GribReader(grib_path), visualizer=VisualizationService())


def _parse_time(time: str):
    parsed = parse_iso_datetime(time)
    if parsed is None:
        raise_unprocessable("time", time, "Expected ISO 8601, e.g. 2025-01-29T00:00")
    return parsed


def _get_png(variable: str, grib_path, endpoint: str, time: str, db: Session) -> bytes:
    repo = RequestLogRepository(db)
    parsed_time = _parse_time(time)

    try:
        png_bytes = _make_service(grib_path).get_png(variable=variable, time=parsed_time)
    except TimeNotFoundError as exc:
        repo.create(endpoint, time, "error", str(exc))
        raise_not_found(str(exc))
    except GribReadError as exc:
        repo.create(endpoint, time, "error", str(exc))
        raise_server_error(str(exc))

    repo.create(endpoint, time, "success")
    return png_bytes


@router.get("/temperature", response_class=Response)
def get_temperature(
    time: str = Query(..., description="ISO 8601 datetime, e.g. 2025-01-29T00:00"),
    db: Session = Depends(get_db),
):
    """Return a PNG visualisation of temperature over Central Asia at the given time."""
    png = _get_png("temperature", settings.TEMPERATURE_GRIB, "/temperature", time, db)
    return Response(content=png, media_type="image/png")


@router.get("/pressure", response_class=Response)
def get_pressure(
    time: str = Query(..., description="ISO 8601 datetime, e.g. 2025-01-29T00:00"),
    db: Session = Depends(get_db),
):
    """Return a PNG visualisation of pressure over Central Asia at the given time."""
    png = _get_png("pressure", settings.PRESSURE_GRIB, "/pressure", time, db)
    return Response(content=png, media_type="image/png")


@router.get("/logs", response_model=list[RequestLogSchema])
def get_logs(limit: int = 50, db: Session = Depends(get_db)):
    """Return recent API request logs (useful for debugging and monitoring)."""
    return RequestLogRepository(db).get_all(limit=limit)
