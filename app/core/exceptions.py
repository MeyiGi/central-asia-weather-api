class GribReadError(Exception):
    """Raised when a GRIB file can't be opened, parsed, or has no usable data."""


class TimeNotFoundError(Exception):
    """Raised when the requested timestamp isn't available in the dataset."""