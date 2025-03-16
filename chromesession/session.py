import functools
from typing import Callable, Optional, Protocol, Union

import requests
import requests_cache
import responses
from url_normalize import url_normalize  # type: ignore[import]

from .chromium import Chrome


class _ProtocolCachedSession(Protocol):
    def create_key(self, url: str) -> str:
        """Create and cache key for a given URL.

        Args:
            url (str): The URL for which to generate a cache key.

        Returns:
            str: The cached cache key.
        """
        pass


class CachedSession(requests_cache.CachedSession, _ProtocolCachedSession):

    def __init__(
        self,
        *args,
        maxsize: Optional[int] = None,
        **kwargs,
    ):
        """
        Initialize the CachedSession.

        Args:
            maxsize (Optional[int]): The maximum size of the LRU cache for
                `CachedSession.create_key`. Defaults to 4096.
        """
        super().__init__(*args, **kwargs)
        self.create_key: Callable[[str], str] = functools.lru_cache(
            maxsize=maxsize or 4096
        )(
            self._create_key
        )  # type: ignore[assignment]

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

    def _create_key(self, url: str) -> str:
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

    def save_driver(self, driver: Chrome, **kwargs) -> requests.Response:
        """Save a response generated from a WebDriver's page source to the cache.

        Args:
            driver (WebDriver): The WebDriver instance.
            **kwargs: Additional keyword arguments.
        """
        response = self.response(driver)
        self.save_response(response, **kwargs)

        return response

    def save(
        self, response: Union[requests.Response, Chrome], **kwargs
    ) -> requests.Response:
        """Save an HTTP or WebDriver response to the cache.

        Args:
            response (Union[requests.Response, WebDriver]): The HTTP response or
                WebDriver instance to cache.
            **kwargs: Additional keyword arguments.

        Returns:
            requests.Response: The cached HTTP response.
        """

        if isinstance(response, Chrome):
            return self.save_driver(response, **kwargs)

        self.save_response(response, **kwargs)
        return response

    def get(self, url: str, **kwargs) -> requests_cache.AnyResponse:  # type: ignore[override] # noqa: E501
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
        driver: Chrome,
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

        # Step 1: Mock the request using the responses library
        with responses.RequestsMock() as r:
            r.add(
                responses.GET,
                url=url,
                body=body,
                status=200,
                content_type=f"text/html; charset={encoding}",
            )

            # Step 3: Make the mocked request
            response = requests.get(url)

        return response
