from collections.abc import Generator
from contextlib import contextmanager

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


@contextmanager
def chrome(
    *,
    mobile: bool = False,
    verbose: bool = True,
    driver: str = "./chromedriver-win64/chromedriver.exe",
) -> Generator[webdriver.Chrome, None, None]:
    """Create a Selenium Chrome webdriver context.

    This context manager sets up the Chrome webdriver with specified configuration options.
    It allows running in headless mode and emulating mobile devices, and ensures that the
    webdriver is properly terminated after use.

    Args:
        mobile (bool): Enable mobile emulation if True. Defaults to False.
        verbose (bool): If False, runs the browser in headless mode with a fixed window size.
            Defaults to True.
        driver (str): The path to the ChromeDriver executable. Defaults to
            "./chromedriver-win64/chromedriver.exe".

    Yields:
        webdriver.Chrome: A configured Chrome webdriver instance.
    """

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
                "AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"
            ),
        }
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    # Set up the Selenium WebDriver (ensure you have the correct WebDriver installed for your browser)
    service = Service(
        executable_path=driver,
    )  # Update with your WebDriver path
    drv = webdriver.Chrome(service=service, options=chrome_options)

    try:
        yield drv
    finally:
        drv.quit()
