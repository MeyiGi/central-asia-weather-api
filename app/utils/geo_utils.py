"""
geo_utils.py

Small helpers for geographic stuff — bounding boxes, coordinate validation, that kind of thing.
Nothing too fancy, just avoiding copy-paste across the codebase.
"""

from dataclasses import dataclass


@dataclass
class BoundingBox:
    """
    Simple container for a lat/lon bounding box.
    I got tired of passing 4 separate floats everywhere.
    """
    lat_min: float
    lat_max: float
    lon_min: float
    lon_max: float

    def is_valid(self) -> bool:
        """Quick sanity check — lat must be -90..90, lon -180..180, and min < max."""
        lat_ok = -90 <= self.lat_min < self.lat_max <= 90
        lon_ok = -180 <= self.lon_min < self.lon_max <= 180
        return lat_ok and lon_ok

    def contains(self, lat: float, lon: float) -> bool:
        """Check if a single point falls inside this box."""
        return (
            self.lat_min <= lat <= self.lat_max
            and self.lon_min <= lon <= self.lon_max
        )

    def __str__(self) -> str:
        return (
            f"lat [{self.lat_min}, {self.lat_max}] "
            f"lon [{self.lon_min}, {self.lon_max}]"
        )


def is_valid_lat(lat: float) -> bool:
    """Latitude has to be between -90 and 90. That's just geography."""
    return -90.0 <= lat <= 90.0


def is_valid_lon(lon: float) -> bool:
    """Longitude has to be between -180 and 180."""
    return -180.0 <= lon <= 180.0


def is_valid_coordinate(lat: float, lon: float) -> bool:
    """Check both lat and lon at once."""
    return is_valid_lat(lat) and is_valid_lon(lon)


def get_central_asia_bbox() -> BoundingBox:
    """
    Returns the hardcoded Central Asia bounding box we use everywhere.
    Pulled from config but wrapped here so you don't have to import settings just for a box.
    """
    # these values come from app/core/config.py — keeping them in sync manually for now
    return BoundingBox(lat_min=35.0, lat_max=55.0, lon_min=50.0, lon_max=90.0)