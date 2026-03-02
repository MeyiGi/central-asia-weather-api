"""
file_utils.py

Tiny helpers for working with file paths and checking if things exist.
I added these after wasting time debugging missing GRIB files with confusing errors.
"""

from pathlib import Path


def check_file_exists(path: Path, label: str = "File") -> None:
    """
    Raises a FileNotFoundError with a helpful message if the file doesn't exist.
    `label` is just so the error says something like "GRIB file" instead of generic "File".
    """
    if not path.exists():
        raise FileNotFoundError(f"{label} not found at: {path}")


def ensure_dir(path: Path) -> Path:
    """
    Makes sure a directory exists, creating it if needed.
    Returns the path so you can chain it if you want.

    Example:
        log_dir = ensure_dir(Path("logs"))
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def is_grib_file(path: Path) -> bool:
    """
    Very basic check — just looks at the extension.
    Doesn't validate the actual file contents (that's cfgrib's job).
    """
    return path.suffix.lower() in (".grib", ".grb", ".grib2", ".grb2")