
# Patterns to identify product URLs
PRODUCT_PATTERNS = [r"/product/", r"/item/", r"/p/", r"/dp/"]

# List of domains to crawl
DOMAINS = [
    "https://www.amazon.in/",
    "https://www.flipkart.com/"
]

# Request settings
MAX_RETRIES = 3
REQUEST_TIMEOUT = 30
OUTPUT_FILE = "product_urls.json"

# Browser headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}