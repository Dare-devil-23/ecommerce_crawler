import aiohttp
import asyncio
from src.config.settings import PROXIES

async def test_proxy(proxy):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://httpbin.org/ip", proxy=proxy) as response:
                if response.status == 200:
                    print(f"Working Proxy: {proxy}")
    except Exception:
        print(f"Failed Proxy: {proxy}")

async def main():
    tasks = [test_proxy(proxy) for proxy in PROXIES]
    await asyncio.gather(*tasks)

asyncio.run(main())
