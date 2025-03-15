"""
.. include:: ../README.md
"""

from .chromium import Chrome, chrome  # noqa: F401
from .session import CachedSession
from .utils import soups

__all__ = [
    "CachedSession",
    "chrome",
    "soups",
]
