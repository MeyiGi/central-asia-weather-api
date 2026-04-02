"""
Finds wrfout files in a directory and resolves a time string to a path.
 
Files are sorted lexicographically — this works because the WRF filename
format is zero-padded and date-first, so alphabetical == chronological.
"""

from pathlib import Path
from typing_extensions import Final
from app.domain.exceptions import DataSourceError
from app.infrastructure.adapters.wrf_reader import time_parser

_WRFOUT_GLOB: Final = "wrfout_d01_*"
_WRFOUT_PREFIX: Final = "wrfout_d01_"


class WrfFileLocator:
    def __init__(self, wrf_dir: Path) -> None:
        self._wrf_dir = wrf_dir

    def list_sorted(self) -> list[Path]:
        files = sorted(self._wrf_dir.glob(_WRFOUT_GLOB))
        if not files:
            raise DataSourceError(f"No wrfout files found in '{self._wrf_dir}'")
        return files
    
    def resolve(self, time: str | None) -> Path:
        """Return the path for *time*, or the latest file when *time* is None."""
        if time is None:
            return self.list_sorted()[-1]
        
        normalized = time_parser.to_filename_token(time)
        path = self._wrf_dir / f"{_WRFOUT_PREFIX}{normalized}"

        if not path.exists():
            raise DataSourceError(f"WRF output file not found: '{path}'")

        return path