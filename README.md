# E-commerce Crawler

A high-performance, asynchronous web crawler specifically designed for e-commerce websites. This crawler efficiently extracts product URLs while respecting website crawling policies.

## Features

- **Asynchronous Crawling**: Utilizes `aiohttp` and `asyncio` for fast, non-blocking web requests
- **JavaScript Support**: Uses Playwright for JavaScript-rendered content
- **Intelligent Product Detection**: Automatically identifies product URLs using configurable patterns
- **Robust Error Handling**: Implements exponential backoff for failed requests
- **Rate Limiting**: Built-in rate limiting to avoid overwhelming target servers
- **URL Deduplication**: Prevents duplicate URL processing
- **Configurable Settings**: Easy to customize crawling parameters
- **Detailed Logging**: Comprehensive logging for monitoring and debugging

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Dare-devil-23/ecommerce_crawler.git
cd ecommerce_crawler
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:

On Windows:
```bash
.\venv\Scripts\activate
```

On Unix or MacOS:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements/base.txt
```

5. Install Playwright browsers:
```bash
playwright install
```

## Configuration

Configure the crawler settings in `src/config/settings.py`:
- `DOMAINS`: List of domains to crawl
- `PRODUCT_PATTERNS`: Regular expressions to identify product URLs
- `MAX_RETRIES`: Maximum number of retry attempts for failed requests
- `REQUEST_TIMEOUT`: Timeout for HTTP requests
- `OUTPUT_FILE`: Path to save extracted product URLs

## Usage

Run the crawler:
```bash
python main.py
```

The crawler will:
1. Start crawling the configured domains
2. Extract and validate product URLs
3. Save results to the specified output file (default: `product_urls.json`)

## Output

Product URLs are saved in JSON format with the following structure:
```json
{
    "domain.com": [
        "https://domain.com/product1",
        "https://domain.com/product2"
    ]
}
```

## License

This project is licensed under the MIT License - see below for details:

MIT License
