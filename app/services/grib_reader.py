from datetime import datetime
from pathlib import Path

import numpy as np
import xarray as xr

from app.core.exceptions import GribReadError
from app.services.base_reader import WeatherDataReader
from app.utils.file_utils import check_file_exists, is_grib_file
from app.utils.grib_utils import get_first_data_var, select_nearest_time, slice_bbox


class GribReader(WeatherDataReader):
    """Reads meteorological data from a GRIB file and caches it."""

    def __init__(self, grib_path: Path):
        check_file_exists(grib_path, label="GRIB file")
        if not is_grib_file(grib_path):
            raise GribReadError(f"Not a valid GRIB file: {grib_path}")

        self._path = grib_path
        self._ds: xr.Dataset | None = None

    def _load(self) -> xr.Dataset:
        if self._ds is None:
            try:
                self._ds = xr.open_dataset(self._path, engine="cfgrib", decode_timedelta=False)
            except Exception as exc:
                raise GribReadError(f"Failed to open GRIB file {self._path}: {exc}") from exc
        return self._ds

    def get_available_times(self) -> list[datetime]:
        ds = self._load()
        for key in ("time", "valid_time"):
            if key in ds.coords:
                vals = np.ravel(ds.coords[key].values).astype("datetime64[ms]")
                return [v.astype(datetime) for v in vals]
        return []

    def read(
        self,
        time: datetime,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        ds = self._load()

        try:
            da = get_first_data_var(ds)
        except ValueError as exc:
            raise GribReadError(f"No data variables found in {self._path}") from exc

        da = select_nearest_time(da, time)
        da = slice_bbox(da, lat_min, lat_max, lon_min, lon_max)

        return da.latitude.values, da.longitude.values, da.values