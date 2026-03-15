"""
Extracts 2-D lat/lon arrays from a WRF dataset.
 
WRF stores coordinates as XLAT/XLONG (not the CF-convention
latitude/longitude used by GRIB). Both have a leading time dimension
(shape: 1, Y, X) that we drop — the grid doesn't move between timesteps.
"""
import numpy as np
import xarray as xr
from typing import Final
from app.domain.exceptions import DataSourceError

_REQUIRED_COORDS: Final = ("XLONG", "XLAT")

def extract(ds: xr.Dataset) -> tuple[np.ndarray, np.ndarray]:
    if any(coord not in ds for coord in _REQUIRED_COORDS):
        raise DataSourceError("XLAT/XLONG not found in wrfout file")
    
    lats, lons = ds["XLAT"].values, ds["XLONG"].values

    lats = lats[0] if lats.ndim == 3 else lats
    lons = lons[0] if lons.ndim == 3 else lons

    return lats, lons