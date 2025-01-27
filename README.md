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

## Live Demo

The API is deployed and accessible at: https://ecommerce-crawler.onrender.com

You can interact with the live API using the endpoints documented in the API Documentation section below. The following sections describe how to set up the project locally for development.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- MongoDB installed and running

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
pip install -r requirements.txt
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

### MongoDB Setup

You can use either a local MongoDB installation or MongoDB Atlas (cloud-hosted):

#### Local MongoDB
1. Install and start MongoDB on your system
2. Create a new database and collection:
```bash
mongosh
use web_crawler_db
db.createCollection("product_urls")
```

#### MongoDB Atlas
1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster and database
3. In the Atlas UI, create a collection named `product_urls` in your database
4. Get your connection string from Atlas UI (Click "Connect" > "Connect your application")

#### Configuration
Configure MongoDB connection in your `.env` file:

For local MongoDB:
```
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=web_crawler_db
MONGODB_COLLECTION=product_urls
```

For MongoDB Atlas:
```
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net
MONGODB_DB=web_crawler_db
MONGODB_COLLECTION=product_urls
```

Note: For production deployment, make sure to use appropriate MongoDB connection URI with authentication and replace the placeholder values in the Atlas URI with your actual credentials.

## Usage

You can either use the live API or run the crawler locally:

### Local Setup
Run the crawler locally with:
```bash
python main.py
```

### Live API
Use the deployed version at https://ecommerce-crawler.onrender.com with the documented API endpoints.

The crawler will:
1. Start crawling the configured domains
2. Extract and validate product URLs
3. Save results to the specified output file (default: `product_urls.json`)

## API Documentation

The application exposes the following REST API endpoints:

### Start Crawling
- **Endpoint**: `/crawl`
- **Method**: POST
- **Request Body**:
```json
{
    "domains": ["example.com", "example2.com"]
}
```
- **Response**: 200 OK
```json
{
    "message": "Crawling process started"
}
```

### Get Products
- **Endpoint**: `/get-products`
- **Method**: GET
- **Query Parameters**: 
  - `domain` (optional): Filter products by domain
- **Response**: 200 OK
```json
{
    "products": [
        {
            "domain": "example.com",
            "urls": ["https://example.com/product1", "https://example.com/product2"]
        }
    ]
}
```

### Stop Crawling
- **Endpoint**: `/stop-crawling`
- **Method**: POST
- **Response**: 200 OK
```json
{
    "message": "Stop signal sent to crawler"
}
```

## Output

The crawler saves product URLs in an array format:

### JSON Output
```json
[
    {
        "domain": "https://flipkart.com",
        "url": "https://flipkart.com/canon-pixma-mega-efficient-g3012-multi-function-wifi-color-ink-tank-printer-color-page-cost-0-21-rs-black-0-09-borderless-printing-2-additional-bottles/p/itm8b3fad9e0208a?pid=PRNF2QC6BX5M9NAJ&lid=LSTPRNF2QC6BX5M9NAJKRNVSY&marketplace=FLIPKART"
    },
    {
        "domain": "https://flipkart.com",
        "url": "https://flipkart.com/hp-smart-tank-all-one-580-multi-function-wifi-color-ink-printer-voice-activated-printing-google-assistant-print-scan-copy-1-extra-black-bottle-up-8000-6000-pages-box/p/itm57b849f65df2c?pid=PRNGKZB6CXPAQWZS&lid=LSTPRNGKZB6CXPAQWZSUYPZX3&marketplace=FLIPKART"
    }
]
```

Each product URL is stored as a document in the array. The same structure is used for both the JSON file and MongoDB collection.

### MongoDB Storage
The documents in MongoDB collection follow the same structure, with each document containing a domain and URL:
```json
[
    {
        "domain": "https://flipkart.com",
        "url": "https://flipkart.com/canon-pixma-mega-efficient-g3012-multi-function-wifi-color-ink-tank-printer-color-page-cost-0-21-rs-black-0-09-borderless-printing-2-additional-bottles/p/itm8b3fad9e0208a?pid=PRNF2QC6BX5M9NAJ&lid=LSTPRNF2QC6BX5M9NAJKRNVSY&marketplace=FLIPKART"
    },
    {
        "domain": "https://flipkart.com",
        "url": "https://flipkart.com/hp-smart-tank-all-one-580-multi-function-wifi-color-ink-printer-voice-activated-printing-google-assistant-print-scan-copy-1-extra-black-bottle-up-8000-6000-pages-box/p/itm57b849f65df2c?pid=PRNGKZB6CXPAQWZS&lid=LSTPRNGKZB6CXPAQWZSUYPZX3&marketplace=FLIPKART"
    }
]
```

Note: MongoDB automatically adds an `_id` field to each document for internal use.

## License

This project is licensed under the MIT License - see below for details:

MIT License
