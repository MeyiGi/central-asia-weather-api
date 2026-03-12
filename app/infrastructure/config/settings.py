"""
infrastructure/config/settings.py

All environment-driven configuration lives here.
The rest of the codebase imports `get_settings()` rather than a bare module-level
singleton so it can be overridden in tests via dependency injection.
"""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ------------------------------------------------------------------
    # General
    # ------------------------------------------------------------------
    PROJECT_NAME: str = "Weather API"
    LOG_LEVEL: str = "INFO"

    # ------------------------------------------------------------------
    # Data paths
    # ------------------------------------------------------------------
    DATA_DIR: Path = Path(__file__).resolve().parents[4] / "data"

    @property
    def TEMPERATURE_GRIB(self) -> Path:
        return self.DATA_DIR / "temperature.grib"

    @property
    def PRESSURE_GRIB(self) -> Path:
        return self.DATA_DIR / "pressure.grib"

    # WRF output directory (override via env var WRF_DIR)
    WRF_DIR: str = "/wrf"

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------
    SQLITE_FILENAME: str = "weather.db"

    @property
    def DATABASE_URL(self) -> str:
        db_path = self.DATA_DIR / self.SQLITE_FILENAME
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{db_path}"

    # ------------------------------------------------------------------
    # Region bounding box (Central Asia)
    # ------------------------------------------------------------------
    REGION_LAT_MIN: float = 35.0
    REGION_LAT_MAX: float = 55.0
    REGION_LON_MIN: float = 50.0
    REGION_LON_MAX: float = 90.0

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
