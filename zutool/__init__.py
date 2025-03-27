""".. include:: ../README.md"""

from __future__ import annotations

import importlib.metadata

from .api import get_otenki_asp, get_pain_status, get_weather_point, get_weather_status

try:
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = (
    "get_otenki_asp",
    "get_pain_status",
    "get_weather_point",
    "get_weather_status",
    "set_weather_point",
)
