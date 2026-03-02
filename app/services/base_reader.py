from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

import numpy as np


class WeatherDataReader(ABC):
    """Contract for reading weather data."""

    @abstractmethod
    def get_available_times(self) -> list[datetime]:
        """Return all available timestamps"""

    @abstractmethod
    def read(
        self,
        time: datetime,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Return (lats, lons, values) arrays to the given bounding box
        for the requested timestamp.

        Raises:
            TimeNotFoundError: if the requested time is not in the data.
            GribReadError: if the file cannot be parsed.
        """
