import asyncio
import hashlib
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from collections import deque

from scraper.config import *
from scraper.fetcher import fetch
from scraper.parser import parse

def normalize_url(_url: str) -> str:
    """
    Input: A url.
    Output: Normalized url for later extraction
    """
    if not _url:
        return ""

    parsed = urlparse(_url)
    if not parsed.scheme:
        return ""

    host: str = parsed.netloc.lower()
    path: str = parsed.path or "/"

    if host in ALLOWED_DOMAINS and path in {"", "/"}:
        path = "/az"

    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")

    return parsed._replace(netloc=host, path=path, query="", fragment="").geturl()


def is_allowed_url(_url: str) -> bool:
    """
    Input: normalized URL string
    Output: True if we can crawl the url given, false if not
    """

    parsed = urlparse(_url)
    host: str = parsed.netloc.split(":")[0].lower()

    if host not in ALLOWED_DOMAINS:
        return False

    path = parsed.path or "/"

    for bad in DISALLOWED_PATH_KEYWORDS:
        if bad in path:
            return False

    if path.startswith(ALLOWED_PATH_PREFIXES):
        return True

    first_segment = path.lstrip("/").split("/", 1)[0]

    # Soo we looking at the first piece of the path 
    # If its something like “/az/...” we know its a language 
    # but if its like “/haqqimizda or “/kartlar, thats not a language
    # and we still want to crawl those too lol so if the first part 
    # aint “az”, “en”, or “ru”—like “/haqqimizda” we allow it.

    if first_segment and first_segment not in SUPPORTED_LANGUAGES:
        return True

    if path.count("/") <= 1:
        return True

    return False

async def load_sitemap() -> list:
    """
    Input: ()
    Output: list of urls from sitemap
    """

    if not SITEMAP_URL:
        return []

    xml_text = await fetch(SITEMAP_URL)
    if not xml_text:
        return []

    soup = BeautifulSoup(xml_text, "xml")
    urls = []

    for loc in soup.find_all("loc"):
        raw = loc.text.strip()
        if not raw:
            continue
        norm = normalize_url(raw)
        if not norm:
            continue
        if not is_allowed_url(norm):
            continue
        urls.append(norm)

    return urls

def extract_links(_base_url: str, _html: str) -> list[str]:
    """
    Input: base url of the page currently being crawled, raw html str of the page
    Output: A list of normalized urls found on the page
    """

    soup = BeautifulSoup(_html, "html.parser")
    links: list[str] = []

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href:
            continue

        if href.startswith(("mailto:", "tel:", "javascript:")):
            continue

        abs_url = urljoin(_base_url, href)
        abs_url = normalize_url(abs_url)
        if abs_url:
            links.append(abs_url)

    return links


async def crawl() -> list[dict]:
    """
    Input: ()
    Outut: List of page dictionaries with values url, title, clean lines, clean text
    """


    visited: set[str] = set()
    seen_hashes: set[str] = set()
    results: list[dict] = []
    queue = deque()

    sitemap_urls = await load_sitemap()
    for url in sitemap_urls:
        queue.append((url, 0))
        
    for url in SEED_URLS:
        queue.append((url, 0)) #tuple for the depthh


    while queue:
        url, depth = queue.popleft()

        url = normalize_url(url)
        if not url:
            continue

        if url in visited:
            continue

        if depth > MAX_CRAWL_DEPTH:
            continue

        if len(results) >= MAX_PAGES:
            break

        if not is_allowed_url(url):
            continue

        visited.add(url)

        html = await fetch(url)
        if html is None:
            continue

        page_data = parse(html)
        page_data["url"] = url

        clean_text = page_data.get("clean_text", "")
        if len(clean_text) < MIN_CLEAN_TEXT_LEN:
            continue

        content_hash = hashlib.sha256(clean_text.encode("utf-8")).hexdigest()
        if content_hash in seen_hashes:
            continue
        seen_hashes.add(content_hash)

        results.append(page_data)

        for link in extract_links(url, html):
            if link not in visited:
                queue.append((link, depth + 1))

        await asyncio.sleep(CRAWL_DELAY_SECONDS)

    return results
