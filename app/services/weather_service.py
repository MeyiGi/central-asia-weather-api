from datetime import datetime

from app.core.config import settings
from app.core.exceptions import GribReadError, TimeNotFoundError
from app.services.base_reader import WeatherDataReader
from app.services.visualization import VisualizationService


class WeatherService:
    """Glue code: read the data, clip it, hand it to the visualizer"""

    def __init__(self, reader: WeatherDataReader, visualizer: VisualizationService):
        self._reader = reader
        self._visualizer = visualizer

    def get_png(self, variable: str, time: datetime) -> bytes:
        """
        Fetch data for variable at time, clip to Central Asia in the end return PNG

        Raises:
            TimeNotFoundError: will triggered from reader.
            GribReadError: will trigger from reader.
        """
        lats, lons, values = self._reader.read(
            time=time,
            lat_min=settings.REGION_LAT_MIN,
            lat_max=settings.REGION_LAT_MAX,
            lon_min=settings.REGION_LON_MIN,
            lon_max=settings.REGION_LON_MAX,
        )
        return self._visualizer.render_png(lats, lons, values, variable=variable, time=time)
