import logging
from collections.abc import Generator
from typing import Callable, Optional

from bs4 import BeautifulSoup

from chromesession import CachedSession, WebDriver, chrome


def soups(
    *urls: str,
    scraper: Optional[Callable[[WebDriver], None]] = None,
) -> Generator[BeautifulSoup, None, None]:
    """
    Generate BeautifulSoup objects for the given URLs, using a cached session to avoid
    redundant network calls. If a response is not found in the cache, it will be fetched
    using Selenium and then cached.
    """
    with CachedSession("soups.sqlite") as session:
        with chrome() as driver:

            for url in urls:
                response = session.get_response(url)

                if response is None:
                    driver.get(url)

                    if scraper is not None:
                        scraper(driver)
                        logging.info(f"{url=} scraped.")

                    response = session.save_driver(driver)

                logging.debug(f"yields parsed content from {url=}.")
                yield BeautifulSoup(response.content, "html.parser")


if __name__ == "__main__":

    for soup in soups("https://example.com/", "https://example.com/"):
        print(soup.title)
