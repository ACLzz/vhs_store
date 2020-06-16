from scrapy import Spider, Request
from scrapy.utils.log import configure_logging

from film_constructor import film_construct

import logging

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='INFO.log',
    format='%(levelname)s: %(message)s',
    level=logging.INFO
)
logging.basicConfig(
    filename='ERROR.log',
    format='%(levelname)s: %(message)s',
    level=logging.ERROR
)
logging.basicConfig(
    filename='WARNING.log',
    format='%(levelname)s: %(message)s',
    level=logging.WARNING
)


class RezkaSpider(Spider):
    def __init__(self, categories=None, *args, **kwargs):
        super().__init__(self.name)
        if categories is None:
            categories = ['horror', 'thriller']

        self.categories = categories

    name = 'RezkaSpider'

    def start_requests(self):
        base_url = 'https://rezka.ag/films/best'
        urls = []
        years = list(range(1970, 1996))

        for category in self.categories:
            for year in years:
                urls.append(f"{base_url}/{category}/{year}/")

        for page in urls:
            yield Request(page, callback=self.film_selector)

    def film_selector(self, response):
        films = response.xpath('//div[@class="b-content__inline_item-link"]//a/@href').getall()

        for film in films:
            if film is not None:
                yield response.follow(film, callback=self.parse_film)

            try:
                next_page = response.xpath('//div[@class="b-navigation"]//a/@href').getall()[-1]
                Request(next_page, callback=self.film_selector)
            except IndexError:
                pass

    def parse_film(self, response):
        title = response.xpath('//h1[@itemprop="name"]/text()').get()
        image = response.xpath("//img[@itemprop='image']/@src").get()
        rate = response.xpath('//span[@class="b-post__info_rates imdb"]//span[@class="bold"]/text()').get()
        description = response.xpath('//div[@class="b-post__description_text"]/text()').get()

        genres = response.xpath('//span[@itemprop="genre"]/text()').getall()
        actors = response.xpath('//div[@class="persons-list-holder"]//span[@itemprop="actor"]//a//text()').getall()

        film_construct.add_film(title, image, rate, description, genres, actors)
