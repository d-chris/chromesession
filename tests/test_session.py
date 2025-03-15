import requests

from chromesession import CachedSession
from chromesession.chromium import chrome


def test_contains():
    with CachedSession() as session:
        assert "https://example.com/" in session


def test_urls():

    with CachedSession() as session:
        assert isinstance(session.urls(), list)


def test_get():
    with CachedSession() as session:
        result = session.get("https://example.com/")

        assert isinstance(result, requests.Response)


def test_save_driver():
    with CachedSession() as session:
        with chrome() as driver:
            driver.get("https://example.com/")
            result = session.save(driver)

            assert isinstance(result, requests.Response)


def test_save_response():
    with CachedSession() as session:
        response = session.get("https://example.com/")
        result = session.save(response)

        assert isinstance(result, requests.Response)
