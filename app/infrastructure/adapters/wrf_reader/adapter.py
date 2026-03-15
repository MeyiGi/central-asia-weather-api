"""
WrfReaderAdapter — implements WrfDataReader for WRF output files.
"""

import os
from pathlib import Path

import xarray as xr

from app.domain.entities import WeatherGrid, WrfMeta
from app.domain.exceptions import VariableNotFoundError
from app.domain.interfaces import WrfDataReader
from app.infrastructure.adapters.dataset_loader import WrfDatasetLoader
from . import coord_extractor, time_parser
from .file_locator import WrfFileLocator

_WRFOUT_PREFIX = "wrfout_d01_"


class WrfReaderAdapter(WrfDataReader):

    def __init__(self, wrf_dir: str) -> None:
        self._locator = WrfFileLocator(wrf_dir)

    def read_variable(self, wrf_variable: str, time: str | None) -> WeatherGrid:
        path = self._locator.resolve(time)
        ds = self._load(path)
        values = self._extract_values(ds, wrf_variable, path)
        lats, lons = coord_extractor.extract(ds)
        return WeatherGrid(
            lats=lats,
            lons=lons,
            values=values,
            variable=wrf_variable,
            time=time_parser.to_datetime(self._time_token(path)),
        )

    def get_meta(self) -> WrfMeta:
        files = self._locator.list_sorted()
        lats, lons = coord_extractor.extract(self._load(files[-1]))
        return WrfMeta(
            bounds=(
                (float(lats.min()), float(lons.min())),
                (float(lats.max()), float(lons.max())),
            ),
            available_times=[self._time_token(f) for f in files],
        )

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    @staticmethod
    def _load(path: str) -> xr.Dataset:
        return WrfDatasetLoader(Path(path)).get()

    @staticmethod
    def _time_token(path: str) -> str:
        """Strip the wrfout prefix from a filename to get the time string."""
        return os.path.basename(path).removeprefix(_WRFOUT_PREFIX)

    @staticmethod
    def _extract_values(ds: xr.Dataset, variable: str, path: str):
        if variable not in ds:
            raise VariableNotFoundError(
                f"Variable '{variable}' not found in '{os.path.basename(path)}'. "
                f"Available: {list(ds.data_vars)}"
            )
        values = ds[variable].values
        # WRF variables carry a leading time dimension (T, Y, X) — drop it
        return values[0] if values.ndim == 3 else values