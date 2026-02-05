from scraper.crawler import *


def test_valid_abb_page():
    assert is_allowed_url("https://abb-bank.az/az/ferdi/kreditler")
    assert is_allowed_url("https://abb-bank.az/en/ferdi/kartlar")
    assert is_allowed_url("https://abb-bank.az/ru/xeberler/abb-tam-visa-kartini-teqdim-etdi")
    print("valid abb page test passed")


def test_external_website():
    assert not is_allowed_url("https://google.com")
    print("external website test passed")


def test_disallowed_path():
    assert not is_allowed_url("https://abb-bank.az/cdn-cgi/l/email-protection")
    print("disallowed path test passed")

