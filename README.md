# chromesession

`chromesession` is a Python package that provides a convenient contextmanager for managing `selenium` chrome sessions.

In addition, a `CachedSession` is provided to directly cache the driver responses.

## Installation

```cmd
pip install chromesession
```

To use the `chromesession.chrome` contextmanager to use `selenium`, the chromedriver must be installed the system.

Alternatively, you can install the latest `chromedriver` as extra.

[![PyPI - eth-hash](https://img.shields.io/pypi/v/chromedriver-py?logo=pypi&logoColor=white&label=chromedriver-py)](https://pypi.org/project/chromedriver-py/)


```cmd
pip install chromesession[driver]
```

## Examples

Cache the specified URLs by fetching them via Selenium and saving the responses.

```python
import logging

from chromesession import CachedSession, chrome


def caching(*urls: str) -> None:

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
```

## Dependencies

[![PyPI - requests-cache](https://img.shields.io/pypi/v/requests-cache?logo=pypi&logoColor=white&label=requests-cache)](https://pypi.org/project/requests-cache/)
[![PyPI - responses](https://img.shields.io/pypi/v/responses?logo=pypi&logoColor=white&label=responses)](https://pypi.org/project/responses/)
[![PyPI - selenium](https://img.shields.io/pypi/v/selenium?logo=pypi&logoColor=white&label=selenium)](https://pypi.org/project/selenium/)

---
