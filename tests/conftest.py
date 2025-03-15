from pathlib import Path

import pytest

from chromesession import WebDriver


@pytest.fixture
def mock_chromewebdriver(mocker):
    """mock WebDriver class."""

    class MockedChromeWebDriver(WebDriver):
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

    mocker.patch("selenium.webdriver.chrome.webdriver.WebDriver", MockedChromeWebDriver)

    yield
