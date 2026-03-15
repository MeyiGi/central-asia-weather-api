from abc import ABC, abstractmethod
from pathlib import Path
import xarray as xr # pyright: ignore[reportMissingImports]
from app.domain.exceptions import DataSourceError

GRID_EXTENSIONS = {".grib", ".grb", ".grib2", ".grb2"}

class DatasetLoader(ABC):
    """
    Opens a file as an xr.Dataset and caches the result.
 
    Subclasses implement _validate() to reject wrong file types early,
    and _open() to pick the right xarray engine and wrap I/O errors.
    """

    def __init__(self, path: Path) -> None:
        self._path = self._validate(path)
        self._ds: xr.Dataset | None = None

    def get(self) -> xr.Dataset:
        """Return the dataset, opening the file on the first call."""
        if self._ds is None:
            self._ds = self._open(self._path)
        return self._ds


    @abstractmethod
    def _validate(self, path: Path) -> Path:
        """Check the path is acceptable before any I/O. Return the path if valid."""
        ...

    @abstractmethod
    def _open(self, path: Path) -> xr.Dataset:
        """Open the file and return a dataset. Wrap exceptions as DataSourceError."""
        ...

    @staticmethod
    def _assert_exists(path: Path) -> None:
        if not path.exists():
            raise DataSourceError(f"File not found: {path}")
        

class GridDatasetLoader(DatasetLoader):
    """
    Opens a GRIB file using the cfgrib engine.
 
    decode_timedelta=False keeps time offsets as raw integers rather than
    converting them to timedeltas, which avoids ambiguity when the file
    mixes forecast steps and valid times.
    """
    def _validate(self, path: Path) -> Path:
        self._assert_exists(path)
        if path.suffix.lower() not in GRID_EXTENSIONS:
            raise DataSourceError(f"Not a recognized GRIB extension {path}")
        return path
    
    def _open(self, path: Path) -> xr.Dataset:
        try:
            return xr.open_dataset(path, engine="cfgrib", decode_timedelta=False)
        except Exception as exc:
            raise DataSourceError(f"Failed to open GRIB file '{path}': {exc}") from exc

class WrfDatasetLoader(DatasetLoader):
    """
    Opens a WRF NetCDF output file using the default xarray engine.
 
    WRF files have no special extension — validation only checks existence.
    The caller (WrfFileLocator) is responsible for ensuring the path
    points to an actual wrfout file.
    """
    def _validate(self, path: Path) -> Path:
        self._assert_exists(path)
        return path
    
    def _open(self, path: Path) -> xr.Dataset:
        try:
            return xr.open_dataset(path)
        except Exception as exc:
            raise DataSourceError(f"Cannot open WRF file '{path}': {exc}") from exc