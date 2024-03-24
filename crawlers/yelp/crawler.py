import aiohttp
import sys
import logging
import time

from bs4 import BeautifulSoup

from data_model import MainPageData, ReviewData
from utils.get_user_agent import generate_user_agent
from utils.logger_setup import get_logger

class Crawler:
    BASE_YELP_URL_TEMPLATE = 'https://www.yelp.com{biz}'
    BASE_URL_TEMPLATE = 'https://www.yelp.com/search?find_desc={category}&find_loc={location}&start={page}'
    def __init__(self, category: str, location: str, **kwargs):

        self.logger = get_logger(__name__)

        self._additional_kwargs = kwargs
        self._category = category
        self._location = location.replace(',', '%2C').replace(' ', '+')
        self._first_page = 0
        self.user_agent = generate_user_agent()

    async def __build_url(self, page: int):
        url = self.BASE_URL_TEMPLATE.format(category=self._category, location=self._location, page=page)
        for key, value in self._additional_kwargs.items():
            url += f"&{key}={value.replace(',', '%2C')}"
        return url

    async def __get_list_page_main_block(self, soup: BeautifulSoup):
        _blocks = soup.find('ul', {'class':'list__09f24__ynIEd'}).find_all('div', {'class': 'css-65wjx3'})[2:-1]
        for data in _blocks:
            yield data

    async def __gather_data(self, data: list[BeautifulSoup]):
        async for block in data:
            names: str = await self.__get_buisness_name(block)
            yelp_urls: str = await self.__get_buisness_yelp_url(block)
            number_of_rewiews: int = await self.__get_number_of_reviews(block)
            buisness_raitings: float = await self.__get_buisness_rating(block)
            data = MainPageData(
                name=names,
                yelp_url=yelp_urls,
                rating=buisness_raitings,
                number_of_reviews=number_of_rewiews,
                reviews=None)
            self.logger.info(data)

    def __build_yelp_url(self, url: str):
        return self.BASE_YELP_URL_TEMPLATE.format(biz=url)

    def __get_soup(self, html: str):
        return BeautifulSoup(html, 'html.parser')

    async def __request(self, session: aiohttp.ClientSession, url: str):
        headers={"User-Agent": self.user_agent_list[0]}
        async with session.get(url, headers=headers) as resp:
            return await resp.text()

    async def __get_buisness_name(self, soup: BeautifulSoup):
        _block = soup.find('a', {'class':'css-19v1rkv'})
        return _block.text

    async def __get_buisness_rating(self, soup: BeautifulSoup) -> float:
        _block = soup.find('span', {'class':'css-gutk1c'})
        return float(_block.text.strip())

    async def __get_number_of_reviews(self, soup: BeautifulSoup) -> int:
        _block = soup.find('div', {'class':'css-bwc5d7'})
        try:
            _raw_str = _block.find('span', {'class':'css-chan6m'}).text
            _cleaned_string = _raw_str.replace('(', '').replace(')', '').replace('reviews', '').strip()
            if 'k' in _cleaned_string:
                _cleaned_string = int(float(_cleaned_string.replace('k', '')) * 1000)
            else:
                _cleaned_string = int(_cleaned_string)
        except Exception as e:
            self.logger.error('Error while gettine number of reviews', exc_info=e)

        return _cleaned_string

    async def __get_buisness_yelp_url(self, soup: BeautifulSoup) -> str:
        _block = soup.find('a', {'class':'css-19v1rkv'})
        return self.__build_yelp_url(_block['href'])

    async def __get_buisness_url(self, soup: BeautifulSoup) -> str:
        _block = soup.find('div', {'class':'css-s81j3n'}).find['a'].text
        return 'http://www.' + _block

    async def __get_reviewer_name(self):
        ...

    async def __get_reviewer_location(self):
        ...

    async def __get_reviewer_location(self):
        ... 
    async def parse(self):
        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            while True:
                url = await self.__build_url(self._first_page)
                print(url)
                html = await self.__request(session, url) # self
                soup = self.__get_soup(html)
                list_page = self.__get_list_page_main_block(soup)
                await self.__gather_data(list_page)


                break
                self._first_page += 10

        self.logger.info('Done in {} seconds'.format(time.time() - start_time))
if __name__ == '__main__':
    import asyncio
    crawler = Crawler('restaurants', 'New York, NY')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(crawler.parse())