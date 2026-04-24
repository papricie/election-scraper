import pytest

from scraper.utils import validate_url


def test_validate_url_accepts_volby_url():
    assert validate_url("https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ")


def test_validate_url_rejects_other_url():
    assert not validate_url("https://example.com")
