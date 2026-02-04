import asyncio, pytest
from scraper.fetcher import fetch

@pytest.mark.asyncio
async def test_valid_html():
    url = "https://abb-bank.az/az"
    html = await fetch(url)

    assert html is not None
    assert isinstance(html, str)
    assert "<html" in html.lower()
    print("html test passed")

@pytest.mark.asyncio
async def test_non_html():
    url = "https://abb-bank.az/favicon/browserconfig.xml"
    html = await fetch(url)
    
    assert html is None
    print("non html test passed")

@pytest.mark.asyncio
async def test_invalid_url():
    url = "https://abb-bank.az/menmovcuddeilem"
    html = await fetch(url)

    assert html is None
    print("invalid url test passed")