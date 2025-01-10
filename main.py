"""Main entry point for the crawler application"""
import asyncio
from src.crawler.core import WebCrawler
from src.config.settings import DOMAINS

async def main():
    crawler = WebCrawler()
    await crawler.run(DOMAINS)

if __name__ == "__main__":
    asyncio.run(main())