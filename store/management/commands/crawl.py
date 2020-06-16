from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from film_parser.spiders.rezka_spider import RezkaSpider


class Command(BaseCommand):
    help = 'Starting crawler'

    def handle(self, *args, **kwargs):
        proc = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
        proc.crawl(RezkaSpider)
        proc.start()
