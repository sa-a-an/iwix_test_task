import asyncio
import time

from crawlers.yelp.crawler import Crawler
async def main():
    start_time = time.time()
    crawler = Crawler('restaurants', 'New York, NY')
    await crawler.parse()
    time_diff = time.time() - start_time
    print(f"Full time: {time_diff}")

if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())