import json
import re
import logging
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import asyncio
from aiohttp import ClientSession, TCPConnector, ClientTimeout, ClientError
import backoff
from typing import Optional, Set
from collections import deque

from src.config.settings import (
    PRODUCT_PATTERNS,
    MAX_RETRIES,
    REQUEST_TIMEOUT,
    OUTPUT_FILE,
    HEADERS
)

class WebCrawler:
    def __init__(self):
        self.visited_urls: Set[str] = set()
        self.product_urls_set: Set[str] = set()
        
        # Configure Logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        
        #empty the file
        with open(OUTPUT_FILE, "w") as f:
            f.write("")

    def is_product_url(self, url: str) -> bool:
        return any(re.search(pattern, url) for pattern in PRODUCT_PATTERNS)

    @backoff.on_exception(
        backoff.expo,
        (ClientError, asyncio.TimeoutError),
        max_tries=MAX_RETRIES
    )
    async def fetch_page(self, session: ClientSession, url: str) -> Optional[str]:
        try:
            async with session.get(url, headers=HEADERS, ssl=False) as response:
                if response.status == 200:
                    return await response.text()
                logging.warning(f"Non-200 response for {url}: {response.status}")
                return None
        except Exception as e:
            logging.error(f"Unexpected error fetching {url}: {e}")
            return None

    async def fetch_with_playwright(self, url: str) -> Optional[str]:
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False, args=["--disable-http2", "--ignore-certificate-errors"])
                page = await browser.new_page()
                await page.goto(url, timeout=60000)

                # Scroll to load all products
                previous_height = None
                while True:
                    current_height = await page.evaluate("document.body.scrollHeight")
                    if previous_height == current_height:
                        break
                    previous_height = current_height
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    await asyncio.sleep(3)  # Wait for more content to load

                content = await page.content()
                await browser.close()
                return content
        except Exception as e:
            logging.error(f"Failed to fetch dynamic content for {url}: {e}")
        return None

    def extract_urls(self, base_url: str, soup: BeautifulSoup) -> Set[str]:
        urls = set()
        for link in soup.find_all("a", href=True):
            href = urljoin(base_url, link["href"])
            parsed_href = urlparse(href)
            if parsed_href.netloc == urlparse(base_url).netloc and href not in self.visited_urls:
                urls.add(href)
        return urls

    def extract_product_urls(self, base_url: str, soup: BeautifulSoup) -> Set[str]:
        product_urls = set()
        for link in soup.find_all("a", href=True):
            href = urljoin(base_url, link["href"])
            if self.is_product_url(href):
                product_urls.add(href)
        return product_urls

    def write_product_url_to_file(self, domain: str, url: str) -> None:
        try:
            try:
                with open(OUTPUT_FILE, "r") as f:
                    content = f.read()
                    data = json.loads(content) if content.strip() else {}  # Initialize as empty object if the file is empty
            except FileNotFoundError:
                data = {}  # File doesn't exist, initialize an empty object

            # Add the new product URL to the domain's list
            if domain not in data:
                data[domain] = []
            if url not in data[domain]:
                data[domain].append(url)

            # Write the updated data back to the file
            with open(OUTPUT_FILE, "w") as f:
                json.dump(data, f, indent=4)
            logging.info(f"Product URL written to file: {url}")

        except Exception as e:
            logging.error(f"Error writing product URL to file: {e}")

    async def crawl_domain(self, domain: str) -> None:
        logging.info(f"Starting crawl for domain: {domain}")
        queue = deque([domain])
        
        conn = TCPConnector(ssl=False, limit=10)
        timeout = ClientTimeout(total=REQUEST_TIMEOUT)
        
        async with ClientSession(connector=conn, timeout=timeout) as session:
            while queue:
                current_url = queue.popleft()
                if current_url in self.visited_urls:
                    continue

                logging.info(f"Crawling URL: {current_url}")
                self.visited_urls.add(current_url)

                try:
                    content = await self.fetch_page(session, current_url)
                    if not content:
                        logging.info(f"Falling back to Playwright for {current_url}")
                        content = await self.fetch_with_playwright(current_url)
                        if not content:
                            continue

                    soup = BeautifulSoup(content, "html.parser")
                    new_urls = self.extract_urls(domain, soup)
                    queue.extend(new_urls - self.visited_urls)

                    product_urls = self.extract_product_urls(domain, soup)
                    for product_url in product_urls:
                        self.write_product_url_to_file(domain, product_url)

                except Exception as e:
                    logging.error(f"Error processing {current_url}: {e}")
                    continue

        logging.info(f"Finished crawling domain: {domain}")

    async def run(self, domains: list[str]) -> None:
        tasks = [self.crawl_domain(domain) for domain in domains]
        await asyncio.gather(*tasks)