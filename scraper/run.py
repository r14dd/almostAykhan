import json
import asyncio

from scraper.crawler import crawl
from scraper.chunker import chunk_page
from scraper.config import *


async def main():
    pages = await crawl()

    all_chunks: list[dict] = []

    for page in pages:
        chunks = chunk_page(page)
        all_chunks.extend(chunks)

    with open(CHUNKS_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"Crawled pages: {len(pages)}")
    print(f"Generated chunks: {len(all_chunks)}")
    print(f"Saved output to: {CHUNKS_OUTPUT}")


if __name__ == "__main__":
    asyncio.run(main())
