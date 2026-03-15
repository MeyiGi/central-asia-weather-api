"""
Clips a GRIB DataArray to a geographic bounding box.
 
xarray's sel() requires the slice bounds to match the coordinate's
sort direction — ascending grids need slice(min, max), descending
grids need slice(max, min). We detect the direction from the first
two values and build the slice accordingly.
"""
import xarray as xr
 
from app.domain.entities import BoundingBox
 
 
def clip(da: xr.DataArray, bbox: BoundingBox) -> xr.DataArray:
    return da.sel(
        latitude=_ordered_slice(da.latitude, bbox.lat_min, bbox.lat_max),
        longitude=_ordered_slice(da.longitude, bbox.lon_min, bbox.lon_max),
    )
 
 
def _ordered_slice(coord: xr.DataArray, lo: float, hi: float) -> slice:
    return slice(lo, hi) if coord[0] < coord[-1] else slice(hi, lo)
 