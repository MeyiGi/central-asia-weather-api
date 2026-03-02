from pathlib import Path

from pydantic_settings import BaseSettings

from app.utils.file_utils import ensure_dir


class Settings(BaseSettings):
    PROJECT_NAME: str = "Weather API"

    DATA_DIR: Path = Path(__file__).resolve().parents[2] / "data"
    TEMPERATURE_GRIB: Path = DATA_DIR / "temperature.grib"
    PRESSURE_GRIB: Path = DATA_DIR / "pressure.grib"

    SQLITE_FILENAME: str = "weather.db"

    @property
    def DATABASE_URL(self) -> str:
        db_path = self.DATA_DIR / self.SQLITE_FILENAME
        ensure_dir(db_path.parent)
        return f"sqlite:///{db_path}"

    # Central Asia bounding box
    REGION_LAT_MIN: float = 35.0
    REGION_LAT_MAX: float = 55.0
    REGION_LON_MIN: float = 50.0
    REGION_LON_MAX: float = 90.0


settings = Settings()
