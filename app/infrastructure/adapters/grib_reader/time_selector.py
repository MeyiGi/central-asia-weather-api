"""
Selects time slices from a GRIB DataArray.
 
GRIB files from different producers use different names for the time axis.
We check both known candidates before giving up.
"""
import numpy as np
import xarray as xr
from typing import Final
from datetime import datetime

from app.domain.exceptions import TimeNotFoundError

_TIME_COORDS: Final = ("time", "valid_time")

def _find_time_dim(da: xr.Dataset) -> str | None:
    return next((k for k in _TIME_COORDS if k in da.dims), None)

def _find_time_coords(da: xr.Dataset) -> str | None:
    return next((k for k in _TIME_COORDS if k in da.coords), None)

def _to_datetimes(values: np.ndarray) -> list[datetime]:
    raw = np.ravel(values).astype("datetime64[ms]")
    return [v.astype(datetime) for v in raw]

def select(da: xr.Dataset, target: datetime) -> xr.DataArray:
    dim = _find_time_dim(da)
    if dim is None:
        return da
    
    t64 = np.datetime64(target.replace(tzinfo=None), "ns")
    try:
        return da.sel({dim: t64}, method="nearest")
    except:
        available_times = _to_datetimes(da.coords[dim].values)
        shown = available_times[:10]
        raise TimeNotFoundError(
            f"Time {target.isoformat()} not found. "
            f"Available examples: {[t.isoformat() for t in shown]}"
        )

def available(ds: xr.Dataset) -> list[datetime]:
    coord = _find_time_coords(ds)
    if coord is None:
        return []
    
    return _to_datetimes(ds.coords[coord].values)