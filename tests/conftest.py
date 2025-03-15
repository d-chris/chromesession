from pathlib import Path
from unittest.mock import patch

import pytest

import chromesession


@pytest.fixture(scope="session", autouse=True)
def mock_chromewebdriver():
    """mock WebDriver class."""

    class MockedChromeWebDriver(chromesession.Chrome):
        def __init__(self, *args, **kwargs):
            self.__current_url = "https://example.com/"
            self.__page_source = (
                Path(__file__)
                .parent.joinpath("bin/example.html")
                .read_text(encoding="utf-8")
            )
            pass

        def quit(self) -> None:
            pass

        def get(self, url):
            self.__current_url = url

        @property
        def current_url(self) -> str:
            return self.__current_url

        @property
        def page_source(self) -> str:
            return self.__page_source

    mocker = patch("chromesession.chromium.Chrome", MockedChromeWebDriver)

    try:
        mocker.start()
        yield
    finally:
        mocker.stop()
