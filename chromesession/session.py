import functools
from typing import Optional, Union

import requests
import requests_cache
import responses
from selenium.webdriver.remote.webdriver import WebDriver
from url_normalize import url_normalize  # type: ignore[import]


class CachedSession(requests_cache.CachedSession):

    def __contains__(self, url: str) -> bool:
        """Determine if a URL is present in the cache.

        Args:
            url (str): The URL to check.

        Returns:
            bool: True if a cached response exists for the URL, False otherwise.
        """
        return bool(self.get_response(url))

    @staticmethod
    def normalize(url: str) -> str:
        """Normalize a URL.

        Args:
            url (str): The URL to normalize.

        Returns:
            str: The normalized URL.
        """
        return url_normalize(url)

    @functools.lru_cache
    def create_key(self, url: str) -> str:
        """Create a cache key for a given URL.

        Args:
            url (str): The URL for which to generate a cache key.

        Returns:
            str: The created cache key.
        """
        response = requests.Request("GET", self.normalize(url)).prepare()
        return self.cache.create_key(response)

    def urls(self, **kwargs) -> list[str]:
        """Retrieve a list of cached URLs.

        Args:
            **kwargs: Additional keyword arguments for filtering the URLs.

        Returns:
            List[str]: A list of URLs present in the cache.
        """
        return self.cache.urls(**kwargs)

    def get_response(self, url: str, **kwargs) -> Union[requests.Response, None]:
        """Get the cached response for the specified URL.

        Args:
            url (str): The URL to look up.
            **kwargs: Additional keyword arguments.

        Returns:
            requests.Response: The cached HTTP response or None if not found.
        """
        key = self.create_key(url)
        return self.cache.get_response(key, **kwargs)

    def save_response(self, response: requests.Response, **kwargs) -> None:
        """Save an HTTP response to the cache.

        Args:
            response (requests.Response): The HTTP response to cache.
            **kwargs: Additional keyword arguments.
        """
        self.cache.save_response(response, **kwargs)

    def save_driver(self, driver: WebDriver, **kwargs) -> None:
        """Save a response generated from a WebDriver's page source to the cache.

        Args:
            driver (WebDriver): The WebDriver instance.
            **kwargs: Additional keyword arguments.
        """
        response = self.response(driver)
        self.save_response(response, **kwargs)

    def get(self, url: str, **kwargs) -> requests_cache.AnyResponse:  # type: ignore[override]
        """Perform a GET request with a normalized URL.

        Args:
            url (str): The URL to request.
            **kwargs: Additional keyword arguments passed to the GET request.

        Returns:
            requests.Response: The HTTP response.
        """
        return super().get(self.normalize(url), **kwargs)

    @classmethod
    def response(
        cls,
        driver: WebDriver,
        *,
        encoding: Optional[str] = None,
    ) -> requests.Response:
        """Generate an HTTP response from a WebDriver's current page.

        Args:
            driver (WebDriver): The WebDriver instance.
            encoding (str, optional): The encoding for the page source. Defaults to
                "utf-8" if not specified.

        Returns:
            requests.Response: The generated HTTP response.
        """
        encoding = encoding or "utf-8"
        url = cls.normalize(driver.current_url)
        body = driver.page_source.encode(encoding)

        # Step 2: Use responses to mock an HTTP GET request with Selenium HTML content as the body
        with responses.RequestsMock() as r:
            r.add(
                responses.GET,
                url=url,  # Mocked URL
                body=body,  # Use the HTML content from Selenium as the response body
                status=200,
                content_type=f"text/html; charset={encoding}",  # Set the appropriate content type
            )

            # Step 3: Make the mocked request
            response = requests.get(url)

        return response
