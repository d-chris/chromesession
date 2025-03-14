"""
.. include:: ../README.md
"""

from .chromium import WebDriver, chrome  # noqa: F401
from .session import CachedSession
from .utils import soups

__all__ = [
    "CachedSession",
    "chrome",
    "soups",
]
