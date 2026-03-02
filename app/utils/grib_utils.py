from datetime import datetime
import numpy as np
import xarray as xr

from app.core.exceptions import TimeNotFoundError


TIME_KEYS = ("time", "valid_time")


def get_first_data_var(ds: xr.Dataset) -> xr.DataArray:
    if not ds.data_vars:
        raise ValueError("No data variables in dataset")
    return ds[next(iter(ds.data_vars))]


def select_nearest_time(da: xr.DataArray, t: datetime) -> xr.DataArray:
    key = next((k for k in TIME_KEYS if k in da.coords and k in da.dims), None)
    if not key:
        return da

    t64 = np.datetime64(t.replace(tzinfo=None), "ns")

    try:
        return da.sel({key: t64}, method="nearest")
    except KeyError:
        available = [
            v.astype("datetime64[ms]").astype(datetime)
            for v in np.ravel(da.coords[key].values)
        ]
        raise TimeNotFoundError(
            f"Requested time {t.isoformat()} not found. "
            f"Available: {[x.isoformat() for x in available]}"
        )


def slice_bbox(
    da: xr.DataArray,
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
) -> xr.DataArray:
    lat = da.latitude
    lon = da.longitude

    lat_slice = slice(lat_min, lat_max) if lat[0] < lat[-1] else slice(lat_max, lat_min)
    lon_slice = slice(lon_min, lon_max) if lon[0] < lon[-1] else slice(lon_max, lon_min)

    return da.sel(latitude=lat_slice, longitude=lon_slice)