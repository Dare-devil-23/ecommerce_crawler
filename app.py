import asyncio
from flask import Flask, request, jsonify
from pymongo import MongoClient
from src.crawler.core import WebCrawler
import os
from dotenv import load_dotenv
from threading import Thread

# Load environment variables from the .env file
load_dotenv()

# Access environment variables
MONGO_DB_USERNAME = os.getenv("MONGO_DB_USERNAME")
MONGO_DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")

app = Flask(__name__)

# MongoDB Atlas Configuration
MONGO_URI = f"mongodb+srv://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@cluster0.wesrr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&tlsAllowInvalidCertificates=true"
client = MongoClient(MONGO_URI)
db = client["web_crawler_db"]
collection = db["product_urls"]

# Web Crawler Instance
web_crawler = WebCrawler()
crawler_thread = None

def run_crawler(domains):
    asyncio.run(web_crawler.run(domains))

@app.route("/crawl", methods=["POST"])
def crawl_domains():
    try:
        # Parse domains from request
        data = request.json
        if "domains" not in data:
            return jsonify({"error": "Domains are required in the request"}), 400

        domains = data["domains"]
        if not isinstance(domains, list):
            return jsonify({"error": "Domains should be a list"}), 400

        global crawler_thread
        # Stop any existing crawler thread
        if crawler_thread and crawler_thread.is_alive():
            web_crawler.stop_crawling()
            crawler_thread.join()

        # Reset crawler state
        web_crawler.reset()

        # Start new crawler thread
        crawler_thread = Thread(target=run_crawler, args=(domains,))
        crawler_thread.start()

        return jsonify({"message": "Crawling process started"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get-products", methods=["GET"])
def get_products():
    try:
        #if domain is not provided, return all products
        domain = request.args.get("domain")
        if not domain:
            products = list(collection.find({}, {"_id": 0}))
            return jsonify({"products": products}), 200

        # Query MongoDB for products from the specified domain
        products = list(collection.find({"domain": domain}, {"_id": 0}))
        return jsonify({"products": products}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/stop-crawling", methods=["POST"])
def stop_crawling():
    try:
        global crawler_thread
        if crawler_thread and crawler_thread.is_alive():
            web_crawler.stop_crawling()
            return jsonify({"message": "Stop signal sent to crawler"}), 200
        return jsonify({"message": "No active crawler to stop"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
