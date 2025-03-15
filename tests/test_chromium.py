import pytest

from chromesession import Chrome, chrome
from chromesession.chromium import chromedriver, find_chromedriver


def test_chrome():
    """check return value from contextmanager."""

    with chrome(driver="chromedriver", verbose=False, mobile=True) as driver:
        assert isinstance(driver, Chrome)


def test_find_chromedriver(mocker):
    """returns path of driver if found in PATH."""

    mocker.patch("shutil.which", side_effect=lambda x: x)

    result = find_chromedriver()

    assert isinstance(result, str)
    assert result.startswith("chromedriver")


def test_chromedriver_missing(mocker):
    """raise RuntimeError if chromedriver is not found."""

    mocker.patch("chromesession.chromium.__chromedriver", None)
    mocker.patch("chromesession.chromium.find_chromedriver", return_value=None)

    with pytest.raises(RuntimeError):
        chromedriver()


def test_chromedriver(mocker):
    """returns path to chromedriver."""

    mocker.patch("chromesession.chromium.__chromedriver", "chromedriver")
    mocker.patch("chromesession.chromium.Path.resolve", return_value="chromedriver")

    assert chromedriver() == "chromedriver"
