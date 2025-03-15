from pathlib import Path

from chromesession import CachedSession, chrome


def caching(*urls: str) -> Path:
    """
    Cache the specified URLs by fetching them via Selenium and saving the responses.
    """
    cachfile = "caching.sqlite"

    with CachedSession(cache_name=cachfile) as session:
        with chrome(verbose=False) as driver:
            for url in urls:
                if url in session:
                    print(f"{url=} already cached.")
                    continue

                try:
                    driver.get(url)
                    session.save_driver(driver)
                except Exception as e:
                    print(f"{url=} failed to cache: {e}")
                else:
                    print(f"{url=} saved in cache.")

    return Path(cachfile)


if __name__ == "__main__":

    caching("https://example.com/", "https://example.com/")
