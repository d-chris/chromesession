# chromesession

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chromesession)](https://pypi.org/project/chromesession/)
[![PyPI - Version](https://img.shields.io/pypi/v/chromesession)](https://pypi.org/project/chromesession/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/chromesession)](https://pypi.org/project/chromesession/)
[![PyPI - License](https://img.shields.io/pypi/l/chromesession)](https://raw.githubusercontent.com/d-chris/chromesession/main/LICENSE)
[![GitHub - Pytest](https://img.shields.io/github/actions/workflow/status/d-chris/chromesession/pytest.yml?logo=github&label=pytest)](https://github.com/d-chris/chromesession/actions/workflows/pytest.yml)
[![GitHub - Page](https://img.shields.io/website?url=https%3A%2F%2Fd-chris.github.io%2Fchromesession&up_message=pdoc&logo=github&label=documentation)](https://d-chris.github.io/chromesession)
[![GitHub - Release](https://img.shields.io/github/v/tag/d-chris/chromesession?logo=github&label=github)](https://github.com/d-chris/chromesession)
[![codecov](https://codecov.io/gh/d-chris/chromesession/graph/badge.svg?token=OFD1IARN1U)](https://codecov.io/gh/d-chris/chromesession)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://raw.githubusercontent.com/d-chris/chromesession/main/.pre-commit-config.yaml)

---

`chromesession` is a Python package that provides a convenient contextmanager for managing `selenium` chrome sessions.

In addition, a `CachedSession` is provided to directly cache the driver responses.

## Installation

```cmd
pip install chromesession
```

To use the `chromesession.chrome` context manager with `selenium`, the [chromedriver](https://googlechromelabs.github.io/chrome-for-testing/) must be installed on the system.

Alternatively, you can install the latest `chromedriver` as an [extra](#extras).

```cmd
pip install chromesession[driver]
```

## Examples

Cache the specified URLs by fetching them via Selenium and saving the responses.

```python
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
                    print(f"{url=} failed to cache: {e}", exc_info=True)
                else:
                    print(f"{url=} saved in cache.")

    return Path(cachfile)


if __name__ == "__main__":

    caching("https://example.com/", "https://example.com/")
```

## Dependencies

[![PyPI - requests-cache](https://img.shields.io/pypi/v/requests-cache?logo=pypi&logoColor=white&label=requests-cache)](https://pypi.org/project/requests-cache/)
[![PyPI - responses](https://img.shields.io/pypi/v/responses?logo=pypi&logoColor=white&label=responses)](https://pypi.org/project/responses/)
[![PyPI - selenium](https://img.shields.io/pypi/v/selenium?logo=pypi&logoColor=white&label=selenium)](https://pypi.org/project/selenium/)

## Extras

Install optional dependencies using extras.

| extra  | installation                        | dependency                                                                                                                                                           |
| ------ | ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| all    | `pip install chromesession[all]`    | Install all extras.                                                                                                                                                  |
| driver | `pip install chromesession[driver]` | [![PyPI - chromedrive-py](https://img.shields.io/pypi/v/chromedriver-py?logo=pypi&logoColor=white&label=chromedriver-py)](https://pypi.org/project/chromedriver-py/) |
| bs4    | `pip install chromesession[bs4]`    | [![PyPI - beautifulsoup4](https://img.shields.io/pypi/v/beautifulsoup4?logo=pypi&logoColor=white&label=beautifulsoup4)](https://pypi.org/project/beautifulsoup4/)    |

---
