import importlib.util
from collections.abc import Generator

import pytest

from chromesession import soups


@pytest.fixture
def options(tmp_path):
    yield {
        "urls": ["https://example.com"],
        "scraper": lambda x: None,
        "verbose": False,
        "cache_name": tmp_path / "cache.sqlite",
        "driver": "chromedriver",
    }


def bs4_installed():
    """check if bs4 is available."""

    return bool(importlib.util.find_spec("bs4"))


def test_soups(options):
    """check return value from generator."""

    bs4 = pytest.importorskip("bs4", reason="bs4 is not installed")

    result = soups(**options)

    assert isinstance(next(result), bs4.BeautifulSoup)


def test_soups_generator(options):
    """check if soups is a generator."""

    assert isinstance(soups(**options), Generator)


@pytest.mark.skipif(
    bs4_installed(), reason="check if dummy class raises error if bs4 is not installed."
)
def test_soup_raises(options):
    """raise RuntimeError if bs4 is not installed."""

    with pytest.raises(RuntimeError):
        next(soups(**options))
