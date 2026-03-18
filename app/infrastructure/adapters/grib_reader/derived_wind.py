from datetime import datetime
import numpy as np

from app.domain.entities import BoundingBox, WeatherGrid
from app.domain.interfaces import WeatherDataReader


class BaseWindReader(WeatherDataReader):
    def __init__(self, u_reader: WeatherDataReader, v_reader: WeatherDataReader) -> None:
        self._u_reader = u_reader
        self._v_reader = v_reader

    def _read_uv(self, time: datetime, bbox: BoundingBox):
        u = self._u_reader.read("wind_u", time, bbox)
        v = self._v_reader.read("wind_v", time, bbox)
        return u, v

    def available_times(self) -> list[datetime]:
        return self._u_reader.available_times()


class WindSpeedReader(BaseWindReader):
    def read(self, variable: str, time: datetime, bbox: BoundingBox) -> WeatherGrid:
        u, v = self._read_uv(time, bbox)

        values = np.hypot(u.values, v.values)  # cleaner than sqrt(u^2 + v^2)

        return WeatherGrid(
            lats=u.lats,
            lons=u.lons,
            values=values,
            variable="wind_speed",
            time=u.time,
        )


class WindDirectionReader(BaseWindReader):
    def read(self, variable: str, time: datetime, bbox: BoundingBox) -> WeatherGrid:
        u, v = self._read_uv(time, bbox)

        values = (270 - np.degrees(np.arctan2(v.values, u.values))) % 360

        return WeatherGrid(
            lats=u.lats,
            lons=u.lons,
            values=values,
            variable="wind_direction",
            time=u.time,
        )