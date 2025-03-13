import os
import shutil
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver

try:
    from chromedriver_py import binary_path as __chromedriver
except ModuleNotFoundError:
    __chromedriver = None


def chromedriver() -> Path:
    """Get the path to the ChromeDriver executable.

    Either from package `chromedriver-py` or check System PATH.

    Returns:
        Path: The path to the ChromeDriver executable.
    """

    driver = "chromedriver.exe"

    path = __chromedriver or shutil.which(driver)

    if path is None:
        raise RuntimeError(
            "\n".join(
                (
                    f"{driver=} could not be found in PATH.",
                    f"\tpip install {__package__}[driver]",
                )
            )
        )
    return Path(path).resolve(strict=True)


@contextmanager
def chrome(
    *,
    mobile: bool = False,
    verbose: bool = True,
    driver: Optional[os.PathLike] = None,
) -> Generator[WebDriver, None, None]:
    """Create a Selenium Chrome webdriver context.

    This context manager sets up the Chrome webdriver with specified configuration
    options. It allows running in headless mode and emulating mobile devices, and
    ensures that the webdriver is properly terminated after use.

    Args:
        mobile (bool): Enable mobile emulation if True. Defaults to False.
        verbose (bool): If False, runs the browser in headless mode with a fixed window
            size. Defaults to True.
        driver (str): The path to the ChromeDriver executable.

    Yields:
        webdriver.Chrome: A configured Chrome webdriver instance.
    """

    driver = driver or chromedriver()

    browser_args = [
        "--disable-search-engine-choice-screen",
        "--no-default-browser-check",
        "--no-first-run",
        "--disable-default-apps",
        "--disable-popup-blocking",
        "--disable-extensions",
        "--disable-notifications",
    ]

    if verbose is False:
        browser_args += [
            "--headless",
            "--window-size=1920,1080",
        ]

    chrome_options = Options()
    for arg in browser_args:
        chrome_options.add_argument(arg)

    if mobile is True:
        # Set up device emulation for iPhone SE
        mobile_emulation = {
            "deviceMetrics": {"width": 375, "height": 667, "pixelRatio": 2.0},
            "userAgent": (
                "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) "
                "AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14E304 "
                "Safari/602.1"
            ),
        }
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    service = Service(
        executable_path=driver,
    )
    drv = webdriver.Chrome(service=service, options=chrome_options)

    try:
        yield drv
    finally:
        drv.quit()
