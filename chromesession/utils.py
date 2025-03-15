from collections.abc import Generator, Iterable
from typing import Callable, Optional

from .chromium import chrome
from .session import CachedSession, Chrome

try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError as e:

    class BeautifulSoup:  # type: ignore[no-redef]
        __error = e

        def __new__(cls, *args, **kwargs):
            raise RuntimeError(
                "\n".join(
                    (
                        f"{cls.__error}",
                        f"\tpip install {__package__}[bs4]",
                    )
                )
            ) from cls.__error


def soups(
    urls: Iterable[str],
    *,
    scraper: Optional[Callable[[Chrome], None]] = None,
    **kwargs,
) -> Generator[BeautifulSoup, None, None]:
    """
    Generate BeautifulSoup objects for the given URLs using a cached session with
    Selenium.

    This function fetches the content of each URL using a cached session to avoid
    redundant network calls. If a cached response is not found for a URL, it will load
    the URL with Selenium, optionally process it with a scraper callback, and then cache
    the response. Finally, the function yields a BeautifulSoup object parsed from the
    response content.

    Args:
        urls (Iterable[str]): An iterable of URL strings to be fetched.
        scraper (Optional[Callable[[Chrome], None]]): An optional callback that
            accepts a Chorme instance for additional page processing before caching.
        **kwargs: Additional keyword arguments that are passed to the CachedSession.

    Returns:
        Generator[BeautifulSoup, None, None]: A generator yielding BeautifulSoup objects
            created from the HTML content of each fetched URL.
    """

    # extract kwargs for chrome()
    options = {
        k: kwargs.pop(k)
        for k in (
            "mobile",
            "verbose",
            "driver",
        )
        if k in kwargs.keys()
    }

    with CachedSession(**kwargs) as session:
        with chrome(**options) as driver:

            for url in urls:
                response = session.get_response(url)

                if response is None:
                    driver.get(url)

                    if scraper is not None:
                        scraper(driver)

                    response = session.save_driver(driver)

                yield BeautifulSoup(response.content, "html.parser")
