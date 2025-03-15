import importlib.util
from collections.abc import Generator

import pytest

from chromesession import WebDriver, soups


@pytest.fixture
def mock_driver(mocker):
    """mock WebDriver class."""

    class DummyDriver(WebDriver):
        def __init__(self, *args, **kwargs):
            pass

        def quit(self):
            pass

        def get(self, arg):
            pass

    mocker.patch("selenium.webdriver.chrome.webdriver.WebDriver", DummyDriver)

    yield


@pytest.fixture
def options(tmp_path):
    yield {
        "urls": ["https://example.com"],
        "scraper": lambda x: None,
        "verbose": False,
        "cache_name": tmp_path / "cache.sqlite",
    }


def bs4_missing():
    """check if bs4 is available."""

    return bool(importlib.util.find_spec("bs4"))


def test_soups(options):
    """check return value from generator."""

    bs4 = pytest.importorskip("bs4", reason="bs4 is not installed")

    result = soups(**options)

    assert isinstance(result, Generator)
    assert isinstance(next(result), bs4.BeautifulSoup)


@pytest.mark.skipif(bs4_missing(), reason="check dummy class if bs4 is not installed.")
def test_soup_raises(options, mock_driver):
    """raise RuntimeError if bs4 is not installed."""

    with pytest.raises(RuntimeError):
        next(soups(**options))
