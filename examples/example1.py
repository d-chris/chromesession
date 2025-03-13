import logging

from chromesession import CachedSession, chrome


def caching(*urls: str) -> None:
    """
    Cache the specified URLs by fetching them via Selenium and saving the responses.
    """
    with CachedSession("caching.sqlite") as session:
        with chrome() as driver:
            for url in urls:
                if url in session:
                    logging.info(f"{url=} already cached.")
                    continue

                try:
                    driver.get(url)
                    session.save_driver(driver)
                except Exception as e:
                    logging.error(f"{url=} failed to cache: {e}", exc_info=True)
                else:
                    logging.info(f"{url=} from cache.")


if __name__ == "__main__":

    caching("https://example.com/", "https://example.com/")
