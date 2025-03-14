import pytest

from chromesession import WebDriver, chrome
from chromesession.chromium import chromedriver, find_chromedriver


def test_chrome():
    """check return value from contextmanager."""

    pytest.importorskip("chromedriver_py", reason="chromedriver_py is not installed")

    with chrome(verbose=False, mobile=True) as driver:
        assert isinstance(driver, WebDriver)


def test_find_chromedriver(mocker):
    """returns path of driver if found in PATH."""

    mocker.patch("shutil.which", side_effect=lambda x: x)

    result = find_chromedriver()

    assert isinstance(result, str)
    assert result.startswith("chromedriver")


def test_chromedriver(mocker):
    """raise RuntimeError if chromedriver is not found."""

    mocker.patch("chromesession.chromium.__chromedriver", None)
    mocker.patch("chromesession.chromium.find_chromedriver", return_value=None)

    with pytest.raises(RuntimeError):
        chromedriver()
