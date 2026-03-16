"""
wrf_reader/helpers.py
 
Low-level helpers shared across strategy modules.
Kept here so strategies don't import from adapter.py (avoids circular deps).
"""
 
from __future__ import annotations
 
from pathlib import Path
 
import numpy as np
import xarray as xr
 
from app.domain.exceptions import VariableNotFoundError
 
 
def read_single(ds: xr.Dataset, variable: str, path: Path) -> np.ndarray:
    """Read a single raw variable from an open WRF dataset."""
    if variable not in ds:
        raise VariableNotFoundError(
            f"Variable '{variable}' not found in '{path.name}'. "
            f"Available: {list(ds.data_vars)}"
        )
    values = ds[variable].values
    return values[0] if values.ndim == 3 else values
 